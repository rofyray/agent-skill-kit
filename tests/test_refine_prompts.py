"""Exercise preservation checks and their limits, without running prompt content."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT/"skills"/"refine-prompts"/"scripts"/"compare_prompts.py"
FIXTURES = ROOT/"evals"/"refine-prompts"/"fixtures"
spec = importlib.util.spec_from_file_location("compare_prompts", SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class PromptComparisonTests(unittest.TestCase):
    def compare(self, before, after, required=(), styles=None, diff=False):
        return helper.compare(before, after, list(required), list(helper.PATTERNS) if styles is None else styles, diff)

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)

    def test_intact_restructure_passes_without_modifying_inputs(self):
        before = (FIXTURES/"original.txt").read_bytes()
        after = (FIXTURES/"preserved.txt").read_bytes()
        result = self.run_cli(FIXTURES/"original.txt", FIXTURES/"preserved.txt", "--requirements", FIXTURES/"requirements.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["mechanical_status"], "no-flags")
        self.assertEqual(report["runtime_validation"], "not-performed")
        self.assertEqual((FIXTURES/"original.txt").read_bytes(), before)
        self.assertEqual((FIXTURES/"preserved.txt").read_bytes(), after)

    def test_cli_reports_broken_interfaces_and_constraints(self):
        result = self.run_cli(FIXTURES/"original.txt", FIXTURES/"broken.txt", "--requirements", FIXTURES/"requirements.json", "--diff")
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertIn("Ask for confirmation before calling send_email.", report["required_literals_missing_from_revised"])
        self.assertEqual({c["candidate"] for c in report["placeholder_changes"]}, {"{{customer}}", "{{client}}"})
        self.assertIn("-Ask for confirmation", report["diff"])

    def test_semantic_regression_is_not_mislabeled_as_verified(self):
        result = self.run_cli(FIXTURES/"original.txt", FIXTURES/"semantic-loss.txt")
        self.assertEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["semantic_validation"], "not-performed")
        self.assertEqual(report["runtime_validation"], "not-performed")
        self.assertNotIn("quality_score", report)

    def test_required_literal_missing_in_original_is_visible(self):
        report = self.compare("plain", "added rule", ["rule"])
        self.assertEqual(report["required_literals_missing_from_original"], ["rule"])
        self.assertEqual(report["required_literals_missing_from_revised"], [])
        self.assertEqual(report["mechanical_status"], "review-required")

    def test_placeholder_syntax_does_not_double_count(self):
        counts = helper.placeholder_counts('{{name}} ${name} {name} {{ profile.name }} {"name": 1}', list(helper.PATTERNS))
        self.assertEqual(dict(counts), {"{{name}}": 1, "${name}": 1, "{name}": 1, "{{ profile.name }}": 1})

    def test_occurrence_loss_is_reported_even_if_variable_remains(self):
        report = self.compare("{{x}} {{x}}", "{{x}}")
        self.assertEqual(report["placeholder_changes"], [{"candidate":"{{x}}", "original_occurrences":2, "revised_occurrences":1}])

    def test_disabled_discovery_still_checks_literals(self):
        report = self.compare("{name} required", "{other}", ["required"], styles=[])
        self.assertEqual(report["placeholder_changes"], [])
        self.assertEqual(report["required_literals_missing_from_revised"], ["required"])

    def test_duplicates_inform_without_failing_or_exposing_text(self):
        text = "Secret policy\nKeep it\n\nOther\n\nSecret policy\nKeep it\n"
        report = self.compare(text, text)
        self.assertEqual(report["mechanical_status"], "no-flags")
        self.assertEqual(report["duplicate_paragraphs"]["original"], [{"start_lines":[1,6], "occurrences":2}])
        self.assertNotIn("Secret policy", json.dumps(report))
        self.assertNotIn("diff", report)

    def test_empty_and_unicode_text(self):
        empty = self.compare("", "")
        self.assertEqual(empty["original"], {"characters":0,"whitespace_delimited_words":0,"lines":0})
        report = self.compare("Résumé español\n你好", "Résumé español\n你好")
        self.assertEqual(report["original"]["whitespace_delimited_words"], 3)
        self.assertEqual(report["original"]["lines"], 2)

    def test_manifest_rejects_malformed_or_unsupported_content(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"requirements.json"
            for data in ('{', '[]', '{"required_literals":"x"}', '{"required_literals":[1]}', '{"required_literals":[""]}', '{"required_literals":[],"unknown":true}'):
                with self.subTest(data=data):
                    path.write_text(data)
                    result = self.run_cli(FIXTURES/"original.txt", FIXTURES/"preserved.txt", "--requirements", path)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, "")
                    self.assertNotIn("Traceback", result.stderr)

    def test_missing_input_is_actionable_error(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_cli(Path(directory)/"missing", FIXTURES/"original.txt")
            self.assertEqual(result.returncode, 2)
            self.assertIn("ERROR", result.stderr)
            self.assertEqual(result.stdout, "")

    def test_invalid_utf8_is_reported_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"binary"
            path.write_bytes(b'\xff')
            result = self.run_cli(path, FIXTURES/"original.txt")
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)

    def test_style_options_are_deduplicated_and_none_is_exclusive(self):
        result = self.run_cli(FIXTURES/"original.txt", FIXTURES/"broken.txt", "--placeholder-style", "double-braces", "--placeholder-style", "double-braces")
        self.assertEqual(json.loads(result.stdout)["placeholder_changes"][0]["revised_occurrences"], 1)
        result = self.run_cli(FIXTURES/"original.txt", FIXTURES/"broken.txt", "--placeholder-style", "none", "--placeholder-style", "braces")
        self.assertEqual(result.returncode, 2)

    def test_manifest_literal_content_is_never_executed(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory)/"should-not-exist"
            literal = f"$(touch {marker})"
            manifest = Path(directory)/"requirements.json"
            manifest.write_text(json.dumps({"required_literals":[literal,literal]}))
            self.assertEqual(helper.read_requirements(manifest), [literal])
            report = self.compare(literal, literal, helper.read_requirements(manifest))
            self.assertEqual(report["mechanical_status"], "no-flags")
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
