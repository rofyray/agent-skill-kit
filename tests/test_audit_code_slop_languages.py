"""Executable language conformance fixtures for the pinned multilingual profile."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1]/"skills"/"audit-code-slop"/"scripts"
sys.path.insert(0, str(SCRIPTS))
from language_profiles import EXTENSIONS, language_for
import audit


# Independently authored, syntactically complete source fixtures. No target builds run.
SHAPES = {
    "javascript": ("function work(x) {\n", "  if (x === INDEX) { return INDEX; }\n", "  return -1;\n}\n"),
    "typescript": ("function work(x: number): number {\n", "  if (x === INDEX) { return INDEX; }\n", "  return -1;\n}\n"),
    "go": ("package example\nfunc work(x int) int {\n", "  if x == INDEX { return INDEX }\n", "  return -1\n}\n"),
    "rust": ("fn work(x: i32) -> i32 {\n", "  if x == INDEX { return INDEX; }\n", "  return -1;\n}\n"),
    "csharp": ("class Example {\nint Work(int x) {\n", "  if (x == INDEX) { return INDEX; }\n", "  return -1;\n}\n}\n"),
    "cpp": ("int work(int x) {\n", "  if (x == INDEX) { return INDEX; }\n", "  return -1;\n}\n"),
    "php": ("<?php\nfunction work($x) {\n", "  if ($x == INDEX) { return INDEX; }\n", "  return -1;\n}\n"),
    "ruby": ("def work(x)\n", "  if x == INDEX\n    return INDEX\n  end\n", "  return -1\nend\n"),
    "kotlin": ("fun work(x: Int): Int {\n", "  if (x == INDEX) { return INDEX }\n", "  return -1\n}\n"),
    "swift": ("func work(_ x: Int) -> Int {\n", "  if x == INDEX { return INDEX }\n", "  return -1\n}\n"),
    "java": ("class Example {\nint work(int x) {\n", "  if (x == INDEX) { return INDEX; }\n", "  return -1;\n}\n}\n"),
}
BOOLEAN_SOURCES = {
    "javascript": "function work(x) { if (x) { return true; } else { return false; } }",
    "typescript": "function work(x: boolean): boolean { if (x) { return true; } else { return false; } }",
    "go": "package example\nfunc work(x bool) bool { if x { return true } else { return false } }",
    "rust": "fn work(x: bool) -> bool { if x { return true; } else { return false; } }",
    "csharp": "class Example { bool Work(bool x) { if (x) { return true; } else { return false; } } }",
    "cpp": "bool work(bool x) { if (x) { return true; } else { return false; } }",
    "php": "<?php function work($x) { if ($x) { return true; } else { return false; } }",
    "ruby": "def work(x)\n if x\n  return true\n else\n  return false\n end\nend",
    "kotlin": "fun work(x: Boolean): Boolean { if (x) { return true } else { return false } }",
    "swift": "func work(_ x: Bool) -> Bool { if x { return true } else { return false } }",
    "java": "class Example { boolean work(boolean x) { if (x) { return true; } else { return false; } } }",
}
ASSIGNMENTS = {
    "javascript": "function work(x) { x = x; }", "typescript": "function work(x: number) { x = x; }",
    "go": "package example\nfunc work(x int) { x = x }", "rust": "fn work(mut x: i32) { x = x; }",
    "csharp": "class Example { void Work(int x) { x = x; } }", "cpp": "void work(int x) { x = x; }",
    "php": "<?php function work($x) { $x = $x; }", "ruby": "def work(x)\n x = x\nend",
    "kotlin": "fun work() { var x = 1; x = x }", "swift": "func work() { var x = 1; x = x }",
    "java": "class Example { void work(int x) { x = x; } }",
}


def complex_source(language, branches=10):
    header, branch, tail = SHAPES[language]
    return header + "".join(branch.replace("INDEX", str(i)) for i in range(branches)) + tail


class InventoryTests(unittest.TestCase):
    def test_all_requested_languages_and_variants_are_discovered(self):
        expected = {"x.tsx": "typescript", "x.mts": "typescript", "x.cts": "typescript", "x.jsx": "javascript",
                    "x.rs": "rust", "x.go": "go", "x.cs": "csharp", "x.csx": "csharp", "x.hpp": "cpp",
                    "x.php": "php", "Gemfile": "ruby", "x.kt": "kotlin", "x.kts": "kotlin", "x.swift": "swift", "x.java": "java"}
        for path, language in expected.items():
            with self.subTest(path=path):
                self.assertEqual(language_for(path), language)
        for path in ("x.razor", "x.fs", "x.vb", "x.vue", "x.svelte"):
            self.assertIsNone(language_for(path))

    def test_test_conventions(self):
        for path in ("__tests__/x.tsx", "x.test.ts", "x.spec.js", "x_test.go", "Example.Tests/Thing.cs", "ThingTests.cs", "spec/x_spec.rb", "src/test/java/ExampleTest.java", "src/androidTest/kotlin/Thing.kt", "ThingTests.swift"):
            with self.subTest(path=path):
                self.assertTrue(audit.test_path(path, []))
        self.assertFalse(audit.test_path("src/latest.ts", []))

    def test_language_filter_and_unsupported_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for path in ("a.ts", "a.py", "a.razor", "a.vb"):
                (root/path).touch()
            _, _, groups, skipped, unsupported = audit.discover(root, [], [], [], ["typescript"])
            self.assertEqual(groups["production"], ["a.ts"])
            self.assertEqual(unsupported, ["a.razor", "a.vb"])
            self.assertIn({"path": "a.py", "reason": "scope exclusion"}, skipped)


WORKER = '''
import json, sys, tempfile
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from polyglot_adapter import load_parsers, analyze_group
from audit import summarize
parsers, hashes = load_parsers()
results = {}
for key, case in json.load(sys.stdin).items():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for path, source in case['files'].items():
            (root/path).write_text(source)
        try:
            rows = analyze_group(root, sorted(case['files']), case['language'], parsers)
            results[key] = {'files': rows, 'summary': summarize(rows)}
        except Exception as exc:
            results[key] = {'error': str(exc)}
print(json.dumps(results))
'''


@unittest.skipUnless(os.environ.get("CODE_SLOP_TEST_PYTHON"), "Set CODE_SLOP_TEST_PYTHON for pinned multilingual integration")
class LanguageConformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cases = {}
        for language in SHAPES:
            extension = EXTENSIONS[language][0]
            for kind, source in (("high", complex_source(language)), ("cutoff", complex_source(language, 9)),
                                 ("boolean", BOOLEAN_SOURCES[language]), ("identical", BOOLEAN_SOURCES[language].replace("false", "true")),
                                 ("assignment", ASSIGNMENTS[language])):
                cases[language + ":" + kind] = {"language": language, "files": {"a" + extension: source}}
            cases[language + ":clones"] = {"language": language, "files": {"a" + extension: complex_source(language), "b" + extension: complex_source(language).replace("work", "other").replace("Work", "Other")}}
        extras = {
            "tsx": ("typescript", "component.tsx", "export const View = ({x}: {x: boolean}) => x ? <div>Hello</div> : <span>No</span>;"),
            "jsx": ("javascript", "component.jsx", "export const View = ({x}) => x ? <div>Hello</div> : <span>No</span>;"),
            "declarations": ("typescript", "api.d.ts", "export interface API { run(x: number): boolean; }\nexport declare function run(x: number): boolean;"),
            "nested": ("typescript", "a.ts", "function outer() { return (x: boolean) => { if (x) { return 1; } return 0; }; }"),
            "cpp-reference": ("cpp", "a.cpp", "void work(int&& x) { use(x); }"),
            "cpp-lambda": ("cpp", "a.cpp", "auto work = [](int x) { if (x) { return 1; } return 0; };"),
            "csharp-expression": ("csharp", "a.cs", "class A { bool P => x && y; int Work(int x) => x > 1 ? x : 0; }"),
            "kotlin-expression": ("kotlin", "a.kt", "fun work(x: Boolean) = if (x) 1 else 0"),
            "swift-getter": ("swift", "a.swift", "struct A { var value: Int { if ready { return 1 }; return 0 } }"),
            "comment-string": ("javascript", "a.js", "//if (x) return true; else return false;\nfunction work() {\n//&& ||\n return 'if (x) { x = x; } else { x = x; }';\n}\n"),
            "malformed": ("typescript", "a.ts", "function broken( {"),
            "short-circuit": ("typescript", "a.ts", "function work(a: boolean,b: boolean,c: boolean) { return a && b || c; }"),
            "branches-differ": ("javascript", "a.js", "function work(x) { if (x) { return 'a'; } else { return 'b'; } }"),
            "member-assignment": ("javascript", "a.js", "function work(x) { x.value = x.value; }"),
            "javascript-flow": ("javascript", "a.js", "function work(a) { try { for (const x of a) { while (x) { break; } } } catch(e) { log(e); } switch(a) { case 1: return 1; default: return 0; } }"),
            "go-case": ("go", "a.go", "package example\nfunc work(x int) int { switch x { case 1,2: return 1; default: return 0 } }"),
            "rust-case": ("rust", "a.rs", "fn work(x: i32) -> i32 { match x { 0 | 1 => 1, _ => 0 } }"),
            "csharp-case": ("csharp", "a.cs", "class A { int Work(int x) { switch(x) { case 1: case 2: return 1; default: return 0; } } }"),
            "cpp-case": ("cpp", "a.cpp", "int work(int x) { switch(x) { case 1: return 1; default: return 0; } }"),
            "php-case": ("php", "a.php", "<?php function work($x) { return match($x) { 1,2 => 1, default => 0 }; }"),
            "ruby-case": ("ruby", "a.rb", "def work(x)\n case x\n when 1,2\n  1\n else\n  0\n end\nend"),
            "kotlin-case": ("kotlin", "a.kt", "fun work(x: Int): Int { return when(x) { 1,2 -> 1; else -> 0 } }"),
            "swift-case": ("swift", "a.swift", "func work(_ x: Int) -> Int { switch x { case 1,2: return 1; default: return 0 } }"),
            "java-case": ("java", "a.java", "class A { int work(int x) { return switch(x) { case 1,2 -> 1; default -> 0; }; } }"),
            "kotlin-accessor": ("kotlin", "a.kt", "class A {\n init {\n if (ready) {\n check()\n }\n }\n val result: Int\n get() {\n if (ready) { return 1 }\n return 0\n }\n}\n"),
            "swift-initializer": ("swift", "a.swift", "struct A { init(_ x: Int) { if x > 0 { check() } } }"),
            "java-record": ("java", "a.java", "record A(int x) { A { if (x < 0) { throw new IllegalArgumentException(); } } }"),
            "csharp-interface": ("csharp", "a.cs", "interface I { bool Work(int x); int P { get; set; } } class A { public int P { get; set; } }"),
        }
        for name, (language, path, source) in extras.items():
            cases[name] = {"language": language, "files": {path: source}}
        result = subprocess.run([os.environ["CODE_SLOP_TEST_PYTHON"], "-c", WORKER, str(SCRIPTS)], input=json.dumps(cases), capture_output=True, text=True, timeout=60)
        if result.returncode:
            raise AssertionError(result.stderr)
        cls.results = json.loads(result.stdout)

    def case(self, name):
        result = self.results[name]
        self.assertNotIn("error", result, name + ": " + str(result))
        return result

    def test_all_languages_count_complexity_and_strict_cutoff(self):
        for language in SHAPES:
            with self.subTest(language=language):
                high = self.case(language + ":high")
                self.assertEqual(len(high["files"][0]["functions"]), 1)
                self.assertEqual(high["summary"]["max_cc"], 11)
                self.assertEqual(high["summary"]["erosion"], 1)
                low = self.case(language + ":cutoff")
                self.assertEqual(low["summary"]["max_cc"], 10)
                self.assertEqual(low["summary"]["erosion"], 0)

    def test_three_rules_have_positive_fixtures_in_every_language(self):
        for language in SHAPES:
            for kind, rule in (("boolean", "redundant-boolean-branch"), ("identical", "identical-branch-bodies"), ("assignment", "self-assignment")):
                with self.subTest(language=language, rule=rule):
                    result = self.case(language + ":" + kind)
                    self.assertIn(rule, [r["rule"] for r in result["files"][0]["rules"]])
                    self.assertGreater(result["summary"]["flagged_lines"], 0)

    def test_all_languages_find_cross_file_renamed_clones(self):
        for language in SHAPES:
            with self.subTest(language=language):
                result = self.case(language + ":clones")
                for row in result["files"]:
                    self.assertGreater(len(row["clone_lines"]), 0)
                    self.assertTrue(any(peer["path"] != row["path"] for c in row["clones"] for peer in c["peers"]))

    def test_jsx_tsx_expression_bodies_closures_and_getters(self):
        for name in ("tsx", "jsx", "cpp-lambda", "kotlin-expression", "swift-getter"):
            with self.subTest(case=name):
                result = self.case(name)
                self.assertEqual(result["summary"]["functions"], 1)
                self.assertEqual(result["summary"]["max_cc"], 2)
        self.assertEqual(self.case("csharp-expression")["summary"]["functions"], 2)
        self.assertEqual(self.case("csharp-expression")["summary"]["max_cc"], 2)

    def test_nested_functions_have_exclusive_complexity(self):
        result = self.case("nested")
        self.assertEqual([f["cc"] for f in result["files"][0]["functions"]], [1, 2])

    def test_case_defaults_handlers_loops_and_initializer_bodies(self):
        self.assertEqual(self.case("javascript-flow")["summary"]["max_cc"], 5)
        for language in ("go", "rust", "csharp", "cpp", "php", "ruby", "kotlin", "swift", "java"):
            with self.subTest(language=language):
                self.assertEqual(self.case(language + "-case")["summary"]["max_cc"], 3 if language == "csharp" else 2)
        for name in ("kotlin-accessor", "swift-initializer", "java-record"):
            with self.subTest(case=name):
                self.assertEqual(self.case(name)["summary"]["max_cc"], 2)
        self.assertEqual(self.case("kotlin-accessor")["summary"]["functions"], 2)
        self.assertIsNone(self.case("csharp-interface")["summary"]["erosion"])

    def test_declarations_and_parse_errors_are_not_zero_erosion(self):
        self.assertIsNone(self.case("declarations")["summary"]["erosion"])
        self.assertIn("Cannot parse", self.results["malformed"]["error"])

    def test_tokens_in_comments_strings_types_and_properties_do_not_trigger(self):
        comments = self.case("comment-string")
        self.assertEqual(comments["summary"]["sloc"], 3)
        self.assertEqual(comments["summary"]["max_cc"], 1)
        self.assertEqual(comments["summary"]["flagged_lines"], 0)
        self.assertEqual(self.case("cpp-reference")["summary"]["max_cc"], 1)
        self.assertEqual(self.case("short-circuit")["summary"]["max_cc"], 3)
        self.assertEqual(self.case("branches-differ")["summary"]["flagged_lines"], 0)
        self.assertEqual(self.case("member-assignment")["summary"]["flagged_lines"], 0)


@unittest.skipUnless(os.environ.get("CODE_SLOP_TEST_PYTHON"), "Set CODE_SLOP_TEST_PYTHON for multilingual CLI integration")
class MixedRepositoryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root/"source"
        self.source.mkdir()

    def cli(self, *args, code=0, python=None):
        result = subprocess.run([python or os.environ["CODE_SLOP_TEST_PYTHON"], str(SCRIPTS/"audit.py"), *map(str, args)], capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, code, result.stderr)
        return result

    def test_twelve_language_repo_grouping_repeatability_and_partial_coverage(self):
        for language in SHAPES:
            (self.source/(language + EXTENSIONS[language][0])).write_text(complex_source(language))
        (self.source/"python.py").write_text("def work(x):\n    return x\n")
        (self.source/"view.test.tsx").write_text("const testView = () => <div>Hello</div>;\n")
        (self.source/"unsupported.fs").write_text("let work x = x\n")
        first = json.loads(self.cli("scan", self.source, "--format", "json").stdout)
        second = json.loads(self.cli("scan", self.source, "--format", "json").stdout)
        self.assertEqual(first, second)
        self.assertEqual(set(first["groups"]["production"]["languages"]), set(EXTENSIONS))
        self.assertEqual(first["groups"]["production"]["summary"]["clone_lines"], 0)
        self.assertEqual(first["groups"]["tests"]["summary"]["files"], 1)
        self.assertEqual(first["coverage"]["status"], "partial")
        self.assertEqual(first["coverage"]["unsupported_source_files"], ["unsupported.fs"])
        audit.validate_report(first)
        self.assertEqual(first["contract"]["language_profiles"]["typescript"]["rule_count"], 3)
        self.assertEqual(first["contract"]["language_profiles"]["python"]["rule_count"], 197)

    def test_typescript_refactor_compares_without_detector_runtime(self):
        (self.source/"a.ts").write_text(complex_source("typescript"))
        (self.source/"a.js").write_text("function clean() { return 1; }\n")
        before, after = self.root/"before.json", self.root/"after.json"
        self.cli("scan", self.source, "--format", "json", "--output", before)
        (self.source/"a.ts").write_text(complex_source("typescript", 9))
        self.cli("scan", self.source, "--format", "json", "--output", after)
        compared = json.loads(self.cli("compare", before, after, "--format", "json", python=sys.executable).stdout)
        group = compared["groups"]["production"]
        self.assertTrue(group["language_mix_changed"])
        self.assertEqual(group["languages"]["typescript"]["percentage_point_delta"]["erosion"], -100)
        self.assertEqual(len(group["resolved_high_cc"]), 1)
        readable = self.cli("compare", before, after, python=sys.executable).stdout
        self.assertIn("Language proportions changed", readable)
        self.assertIn("typescript", readable)
        self.assertIn("by language", self.cli("render", before, python=sys.executable).stdout)

    def test_zero_python_repo_and_language_selection(self):
        (self.source/"a.ts").write_text(BOOLEAN_SOURCES["typescript"])
        (self.source/"a.go").write_text(BOOLEAN_SOURCES["go"])
        measured = json.loads(self.cli("scan", self.source, "--language", "typescript", "--format", "json").stdout)
        self.assertEqual(set(measured["groups"]["production"]["languages"]), {"typescript"})
        self.assertGreater(measured["groups"]["production"]["summary"]["verbosity"], 0)
        self.assertFalse(measured["coverage"]["unsupported_source_files"])

    def test_corrupt_language_totals_rejected(self):
        (self.source/"a.ts").write_text(BOOLEAN_SOURCES["typescript"])
        report = json.loads(self.cli("scan", self.source, "--format", "json").stdout)
        report["groups"]["production"]["languages"]["typescript"]["sloc"] = 999
        with self.assertRaisesRegex(ValueError, "language totals"):
            audit.validate_report(report)


if __name__ == "__main__":
    unittest.main()
