"""Formula, failure-path, and optional pinned-detector integration tests.

Set CODE_SLOP_TEST_PYTHON to the isolated Python 3.12 executable for integration.
"""

import copy
import importlib.util
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


SKILL = Path(__file__).resolve().parents[1]/"skills"/"audit-code-slop"
sys.path.insert(0, str(SKILL/"scripts"))


def load(name):
    spec = importlib.util.spec_from_file_location(name, SKILL/"scripts"/(name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


audit = load("audit")
adapter = load("scb_adapter")


def function(cc, sloc, name="work", start=1):
    return {"name": name, "cc": cc, "sloc": sloc, "start": start, "end": start + sloc - 1}


def row(path="a.py", sloc=10, ast_lines=(), clones=(), functions=()):
    return {"path": path, "language": "python", "sha256": "source-content", "sloc_lines": list(range(1, sloc + 1)),
            "ast_lines": list(ast_lines), "clone_lines": list(clones),
            "functions": list(functions), "rules": [], "clones": []}


def report(rows):
    contract = {"profile": audit.PROFILE}
    return {"schema": audit.SCHEMA, "contract": contract, "contract_sha256": audit.fingerprint(contract),
            "snapshot": {"label": "fixture", "root": "fixture", "source_sha256": audit.fingerprint({r["path"]: r["sha256"] for r in rows})},
            "coverage": {}, "groups": {"production": audit.build_group(rows), "tests": audit.build_group([])}}


class FormulaTests(unittest.TestCase):
    def test_union_uses_file_identity_and_aggregation_uses_counts(self):
        result = audit.summarize([row(sloc=4, ast_lines=(1, 2), clones=(2, 3)), row("b.py", sloc=96, ast_lines=(1,))])
        self.assertEqual(result["flagged_lines"], 4)
        self.assertEqual(result["overlap_lines"], 1)
        self.assertEqual(result["verbosity"], 0.04)

    def test_erosion_uses_sqrt_mass_and_strict_cutoff(self):
        result = audit.summarize([row(functions=[function(10, 4), function(11, 9)])])
        self.assertEqual(result["total_mass"], 53)
        self.assertEqual(result["high_cc_mass"], 33)
        self.assertAlmostEqual(result["erosion"], 33/53)
        self.assertEqual(result["high_cc_functions"], 1)

    def test_empty_and_functionless_are_not_clean_scores(self):
        self.assertIsNone(audit.summarize([])["verbosity"])
        self.assertIsNone(audit.summarize([row()])["erosion"])
        self.assertEqual(audit.summarize([row()])["verbosity"], 0)

    def test_directory_rollup_retains_clone_context(self):
        group = audit.build_group([row("one/a.py", clones=(1, 2)), row("two/b.py", clones=(1, 2))])
        self.assertEqual(group["directories"]["."]["clone_lines"], 4)
        self.assertEqual(group["directories"]["one"]["clone_lines"], 2)

    def test_dilution_detected_for_both_metrics(self):
        old = report([row(functions=[function(11, 9)], ast_lines=(1, 2))])
        new = report(old["groups"]["production"]["files"] + [row("new.py", 100, functions=[function(1, 100)])])
        result = audit.compare(old, new)["groups"]["production"]
        self.assertEqual(len(result["dilution_warnings"]), 2)
        self.assertLess(result["percentage_point_delta"]["verbosity"], 0)

    def test_unchanged_file_can_gain_clone_findings(self):
        old, new = report([row()]), report([row(clones=(1,))])
        change = audit.compare(old, new)["groups"]["production"]["files"][0]
        self.assertFalse(change["source_changed"])
        self.assertEqual(change["after"]["clone_lines"], 1)

    def test_repeated_function_names_not_lost(self):
        old = report([row(sloc=20, functions=[function(10, 5), function(12, 6, start=9)])])
        new = report([row(sloc=20, functions=[function(11, 5), function(10, 6, start=9)])])
        result = audit.compare(old, new)["groups"]["production"]
        self.assertEqual(len(result["new_high_cc"]), 1)
        self.assertEqual(len(result["resolved_high_cc"]), 1)
        self.assertEqual(len(result["cc_changes"]), 2)

    def test_incompatible_contract_rejected(self):
        old, new = report([row()]), report([row()])
        new["contract"]["profile"] = "another-profile"
        new["contract_sha256"] = audit.fingerprint(new["contract"])
        with self.assertRaisesRegex(ValueError, "Incompatible"):
            audit.compare(old, new)

    def test_compatible_legacy_reports_still_compare(self):
        old = report([row()])
        old["schema"] = "code-slop-report/1"
        old["contract"]["profile"] = "python-scb-0.2.0-two-term/1"
        old["contract_sha256"] = audit.fingerprint(old["contract"])
        for group in old["groups"].values():
            group.pop("languages")
            for file in group["files"]:
                file.pop("language")
        compared = audit.compare(old, copy.deepcopy(old))
        self.assertEqual(compared["groups"]["production"]["delta"]["verbosity"], 0)
        with self.assertRaisesRegex(ValueError, "Incompatible"):
            audit.compare(old, report([row()]))

    def test_corrupt_evidence_and_totals_rejected(self):
        original = report([row()])
        for corrupt in ("totals", "outside", "duplicate", "invalid_cc", "nan"):
            damaged = copy.deepcopy(original)
            group = damaged["groups"]["production"]
            if corrupt == "totals":
                group["summary"]["sloc"] = 999
            elif corrupt == "outside":
                group["files"][0]["clone_lines"] = [999]
            elif corrupt == "duplicate":
                group["files"].append(group["files"][0])
            elif corrupt == "nan":
                group["summary"]["erosion"] = math.nan
            else:
                group["files"][0]["functions"] = [function(-1, 1)]
            with self.subTest(corrupt=corrupt), self.assertRaises(ValueError):
                audit.validate_report(damaged)


class DiscoveryTests(unittest.TestCase):
    def test_filesystem_scope_groups_and_partial_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for path in ("a.py", "tests/a.py", "sample_test.py", "generated/client.py", "module.vue", "vendor/dep.py"):
                (root/path).parent.mkdir(parents=True, exist_ok=True)
                (root/path).write_text("pass\n")
            (root/"linked.py").symlink_to(root/"a.py")
            _, mode, groups, skipped, unsupported = audit.discover(root, [], ["generated/*"], [])
            self.assertEqual(mode, "filesystem")
            self.assertEqual(groups["production"], ["a.py"])
            self.assertEqual(groups["tests"], ["sample_test.py", "tests/a.py"])
            self.assertEqual(unsupported, ["module.vue"])
            self.assertIn({"path": "linked.py", "reason": "symlink"}, skipped)

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_git_subdirectory_untracked_ignored_and_deleted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root/"src").mkdir()
            for path in ("src/tracked.py", "src/deleted.py", "src/new.py", "src/ignored.py"):
                (root/path).write_text("pass\n")
            (root/".gitignore").write_text("ignored.py\n")
            subprocess.run(["git", "-C", str(root), "add", "src/tracked.py", "src/deleted.py"], check=True)
            (root/"src/deleted.py").unlink()
            _, mode, groups, _, _ = audit.discover(root/"src", [], [], [])
            self.assertEqual(mode, "git-tracked-and-untracked")
            self.assertEqual(groups["production"], ["new.py", "tracked.py"])


class DetectorFailureTests(unittest.TestCase):
    def test_missing_and_mismatched_dependencies_fail_before_import(self):
        with patch.object(adapter.metadata, "version", side_effect=adapter.metadata.PackageNotFoundError):
            with self.assertRaisesRegex(adapter.AnalysisError, "Missing"):
                adapter.load_backend()
        with patch.object(adapter.metadata, "version", return_value="0.0.0"):
            with self.assertRaisesRegex(adapter.AnalysisError, "Expected"):
                adapter.load_backend()

    def test_staging_changes_only_ignore_comment_text(self):
        source = 'value = "ast-grep-ignore"  # ast-grep-ignore\n'
        with tempfile.TemporaryDirectory() as tmp:
            staged = adapter.stage_sources({Path("example.py"): source}, Path(tmp))
            text = next(iter(staged)).read_text()
            self.assertEqual(text, 'value = "ast-grep-ignore"  # ast_grep_ignore\n')

    def test_failed_or_malformed_detector_never_becomes_zero(self):
        backend = {"binary": "unused", "rule_text": "", "rules": {"test": {}}}
        for result in (SimpleNamespace(returncode=1, stdout="", stderr="failure"),
                       SimpleNamespace(returncode=0, stdout="", stderr="warning"),
                       SimpleNamespace(returncode=0, stdout="invalid-json", stderr="")):
            with self.subTest(result=result), patch.object(adapter.subprocess, "run", return_value=result):
                with self.assertRaises(adapter.AnalysisError):
                    adapter.scan_rules((Path("a.py").absolute(),), backend, 1)

    def test_exclusive_end_and_minimum_rule_count(self):
        path = Path("a.py").absolute()
        finding = {"file": str(path), "range": {"start": {"line": 0, "column": 0}, "end": {"line": 2, "column": 0}}, "ruleId": "test", "message": "candidate"}
        backend = {"binary": "unused", "rule_text": "", "rules": {"test": {"metadata": {"min_file_count": 2}}}}
        result = SimpleNamespace(returncode=0, stdout=json.dumps(finding), stderr="")
        with patch.object(adapter.subprocess, "run", return_value=result):
            self.assertEqual(adapter.scan_rules((path,), backend, 1), [])
            result.stdout += "\n" + json.dumps(finding)
            self.assertEqual(adapter.scan_rules((path,), backend, 1)[0]["end"], 2)


@unittest.skipUnless(os.environ.get("CODE_SLOP_TEST_PYTHON"), "Set CODE_SLOP_TEST_PYTHON for pinned-detector integration")
class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root/"source"
        self.source.mkdir()

    def cli(self, *args, code=0):
        result = subprocess.run([os.environ["CODE_SLOP_TEST_PYTHON"], str(SKILL/"scripts"/"audit.py"), *map(str, args)], capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, code, result.stderr)
        return result

    def scan(self):
        return json.loads(self.cli("scan", self.source, "--format", "json").stdout)

    def test_cross_file_clones_separate_tests_and_repeatability(self):
        code = "def collect(items):\n    result = []\n    for item in items:\n        if item:\n            result.append(item + 1)\n    return result\n"
        (self.source/"a.py").write_text(code)
        (self.source/"b.py").write_text(code.replace("collect", "gather"))
        (self.source/"test_a.py").write_text(code)
        before = self.scan()
        self.assertEqual(before, self.scan())
        production = before["groups"]["production"]
        self.assertEqual(production["summary"]["clone_lines"], 12)
        self.assertEqual(production["summary"]["sloc"], 12)
        self.assertGreater(production["summary"]["overlap_lines"], 0)
        self.assertEqual(before["groups"]["tests"]["summary"]["clone_lines"], 0)
        peer = production["files"][0]["clones"][0]["peers"][0]
        self.assertEqual(peer["path"], "b.py")
        audit.validate_report(before)

    def test_no_execution_and_comment_only_no_scores(self):
        marker = self.root/"must-not-exist"
        (self.source/"a.py").write_text(f"from pathlib import Path\nPath({str(marker)!r}).touch()\n")
        self.scan()
        self.assertFalse(marker.exists())
        (self.source/"a.py").write_text('# comment\n\n"""module documentation"""\n')
        summary = self.scan()["groups"]["production"]["summary"]
        self.assertEqual(summary["sloc"], 0)
        self.assertIsNone(summary["verbosity"])
        self.assertIsNone(summary["erosion"])

    def test_syntax_failure_and_unsupported_only_fail(self):
        (self.source/"a.py").write_text("def broken(\n")
        result = self.cli("scan", self.source, "--format", "json", code=2)
        self.assertIn("Cannot parse", result.stderr)
        self.assertEqual(result.stdout, "")
        (self.source/"a.py").unlink()
        (self.source/"a.vue").write_text("<template>Hello</template>\n")
        result = self.cli("scan", self.source, code=2)
        self.assertIn("No metrics measured", result.stderr)

    def test_cutoff_and_inclusive_nested_function_semantics(self):
        code = "def outer(x):\n    def inner(y):\n"
        code += "".join(f"        if y == {i}:\n            return {i}\n" for i in range(10))
        code += "        return -1\n    return inner(x)\n"
        (self.source/"a.py").write_text(code)
        functions = self.scan()["groups"]["production"]["files"][0]["functions"]
        self.assertEqual(len(functions), 2)
        self.assertEqual([f["cc"] for f in functions], [11, 11])
        self.assertGreater(functions[0]["sloc"], functions[1]["sloc"])

    def test_extensions_encoding_and_ignore_comments_cannot_hide_rules(self):
        code = "# coding: latin-1\n# caf\u00e9\ndef answer(x):\n    # ast-grep-ignore\n    if x:\n        return True\n    else:\n        return False\n"
        for extension in ("py", "pyw", "PY"):
            path = self.source/("source." + extension)
            raw = code.encode("latin-1")
            path.write_bytes(raw)
            result = json.loads(self.cli("scan", path, "--format", "json").stdout)
            self.assertEqual(result["groups"]["production"]["summary"]["flagged_lines"], 4)
            self.assertEqual(path.read_bytes(), raw)

    def test_saved_report_comparison_and_overwrite_refusal(self):
        target = self.source/"a.py"
        target.write_text("def answer(x):\n    if x:\n        return True\n    else:\n        return False\n")
        baseline = self.root/"before.json"
        self.cli("scan", self.source, "--format", "json", "--output", baseline)
        before_bytes = baseline.read_bytes()
        self.cli("scan", self.source, "--format", "json", "--output", baseline, code=2)
        self.assertEqual(baseline.read_bytes(), before_bytes)
        target.write_text("def answer(x):\n    return bool(x)\n")
        after = self.root/"after.json"
        self.cli("scan", self.source, "--format", "json", "--output", after)
        result = json.loads(self.cli("compare", baseline, after, "--format", "json").stdout)
        self.assertLess(result["groups"]["production"]["delta"]["flagged_lines"], 0)
        self.assertFalse(result["groups"]["production"]["dilution_warnings"])
        self.assertIn("Behavior verification: not assessed", self.cli("render", baseline).stdout)


if __name__ == "__main__":
    unittest.main()
