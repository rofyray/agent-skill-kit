from __future__ import annotations

import copy
import importlib.util
import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT/"skills"/"ai-motion-graphics-direction"/"scripts"/"validate_motion_plan.py"
FIXTURE = ROOT/"evals"/"ai-motion-graphics-direction"/"fixtures"/"valid-motion-plan.json"
SPEC = importlib.util.spec_from_file_location("validate_motion_plan", SCRIPT)
assert SPEC and SPEC.loader
motion_plan = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(motion_plan)


class MotionPlanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def assert_invalid(self, plan: object, path: str) -> None:
        report = motion_plan.validate_plan(plan)
        self.assertFalse(report["valid"], report)
        self.assertTrue(any(item["path"] == path for item in report["errors"]), report)

    def test_valid_plan_and_text_free_plan(self) -> None:
        self.assertTrue(motion_plan.validate_plan(self.plan)["valid"])
        self.plan["copy"] = []
        self.plan["references"] = []
        self.plan.pop("percent_bars")
        for beat in self.plan["beats"]:
            beat["copy_ids"] = []
            beat["reference_ids"] = []
            beat.pop("copy_text", None)
        self.assertTrue(motion_plan.validate_plan(self.plan)["valid"])

    def test_gap_overlap_and_out_of_order(self) -> None:
        for start in (6.2, 5.8, 1):
            with self.subTest(start=start):
                self.plan["beats"][1]["start"] = start
                self.assert_invalid(self.plan, "beats[1].start")
        self.plan["beats"].reverse()
        self.assert_invalid(self.plan, "beats[0].start")

    def test_timeline_must_cover_declared_duration(self) -> None:
        for start in (0.1, -0.1):
            with self.subTest(start=start):
                altered = copy.deepcopy(self.plan)
                altered["beats"][0]["start"] = start
                self.assertFalse(motion_plan.validate_plan(altered)["valid"])
        for end in (7, 9):
            with self.subTest(end=end):
                altered = copy.deepcopy(self.plan)
                altered["beats"][-1]["end"] = end
                self.assert_invalid(altered, "beats")
        self.plan["beats"][1]["end"] = 6
        self.assert_invalid(self.plan, "beats[1]")

    def test_float_tolerance_does_not_hide_real_gaps(self) -> None:
        self.plan["beats"][1]["start"] = 6 + 0.0000001
        self.assertTrue(motion_plan.validate_plan(self.plan)["valid"])
        self.plan["beats"][1]["start"] = 6 + 0.00001
        self.assert_invalid(self.plan, "beats[1].start")

    def test_numeric_fields_reject_booleans_strings_and_nonfinite_values(self) -> None:
        for value in (True, "8", None, math.nan, math.inf, -math.inf, 10**400):
            with self.subTest(value=repr(value)[:30]):
                self.plan["duration_seconds"] = value
                self.assert_invalid(self.plan, "duration_seconds")
        self.plan["duration_seconds"] = 8
        self.plan["fps"] = 0
        self.assert_invalid(self.plan, "fps")
        self.plan["fps"] = 29.97
        self.assertTrue(motion_plan.validate_plan(self.plan)["valid"])

    def test_unknown_missing_and_malformed_fields_fail_without_crashing(self) -> None:
        for value in (None, [], 8, "a plan"):
            with self.subTest(root=value):
                self.assert_invalid(value, "$")
        self.plan["final_hod_seconds"] = 2
        self.assert_invalid(self.plan, "$.final_hod_seconds")
        self.plan.pop("final_hod_seconds")
        self.plan["beats"][0].pop("action")
        self.assert_invalid(self.plan, "beats[0].action")
        for field in ("references", "copy", "beats", "percent_bars"):
            for value in (None, {}, "items", [None], [[]]):
                with self.subTest(field=field, value=value):
                    altered = copy.deepcopy(self.plan)
                    altered[field] = value
                    self.assertFalse(motion_plan.validate_plan(altered)["valid"])

    def test_schema_version_is_an_integer_and_metadata_is_an_object(self) -> None:
        for version in (True, 1.0, 2, "1"):
            with self.subTest(version=version):
                self.plan["schema_version"] = version
                self.assert_invalid(self.plan, "schema_version")
        self.plan["schema_version"] = 1
        self.plan["metadata"] = "notes"
        self.assert_invalid(self.plan, "$.metadata")

    def test_references_and_copy_must_be_declared_and_unique(self) -> None:
        for key in ("references", "copy", "beats", "percent_bars"):
            with self.subTest(catalog=key):
                altered = copy.deepcopy(self.plan)
                altered[key].append(copy.deepcopy(altered[key][0]))
                self.assert_invalid(altered, f"{key}[{len(altered[key]) - 1}].id")
        self.plan["beats"][0]["reference_ids"] = ["missing"]
        self.assert_invalid(self.plan, "beats[0].reference_ids[0]")
        self.plan["beats"][0]["copy_ids"] = ["result", "result", "missing"]
        self.assert_invalid(self.plan, "beats[0].copy_ids[1]")
        self.assert_invalid(self.plan, "beats[0].copy_ids[2]")

    def test_compiled_copy_must_match_active_exact_string(self) -> None:
        self.plan["beats"][1]["copy_text"]["result"] = "40% chose refil"
        self.assert_invalid(self.plan, "beats[1].copy_text.result")
        self.plan["beats"][1]["copy_text"]["result"] = self.plan["copy"][0]["text"]
        self.plan["beats"][1]["copy_ids"] = []
        self.assert_invalid(self.plan, "beats[1].copy_text.result")

    def test_multilingual_copy_is_preserved(self) -> None:
        text = "Réemploi: 40% · إعادة الاستخدام · 再利用"
        self.plan["copy"][0]["text"] = text
        self.plan["beats"][1]["copy_text"]["result"] = text
        self.assertTrue(motion_plan.validate_plan(self.plan)["valid"])

    def test_final_hold_is_contiguous_at_the_end(self) -> None:
        self.plan["final_hold_seconds"] = 3
        self.assert_invalid(self.plan, "final_hold_seconds")
        self.plan["beats"][0]["hold"] = True
        self.assertTrue(motion_plan.validate_plan(self.plan)["valid"])
        self.plan["beats"][1]["hold"] = False
        self.assert_invalid(self.plan, "final_hold_seconds")
        self.plan["beats"][1]["hold"] = "true"
        self.assert_invalid(self.plan, "beats[1].hold")
        self.plan["final_hold_seconds"] = -1
        self.assert_invalid(self.plan, "final_hold_seconds")
        self.plan["final_hold_seconds"] = 9
        self.assert_invalid(self.plan, "final_hold_seconds")

    def test_percent_geometry_handles_zero_full_and_fractional_values(self) -> None:
        for percent in (0, 25.5, 40, 50, 100):
            with self.subTest(percent=percent):
                bar = self.plan["percent_bars"][0]
                bar["percent"] = percent
                bar["filled_length"] = bar["track_length"] * percent/100
                self.assertTrue(motion_plan.validate_plan(self.plan)["valid"])
                bar["filled_length"] += 1
                self.assert_invalid(self.plan, "percent_bars[0].filled_length")

    def test_invalid_bar_bounds_and_types(self) -> None:
        for field, value in (("track_length", 0), ("track_length", -2), ("filled_length", -1), ("filled_length", 201), ("percent", 101), ("percent", -1), ("percent", True)):
            with self.subTest(field=field, value=value):
                altered = copy.deepcopy(self.plan)
                altered["percent_bars"][0][field] = value
                self.assert_invalid(altered, f"percent_bars[0].{field}")

    def test_metadata_does_not_claim_to_validate_fact_sources(self) -> None:
        self.plan["metadata"]["source"] = "This source has not been independently verified."
        report = motion_plan.validate_plan(self.plan)
        self.assertTrue(report["valid"])
        self.assertIn("not rendered media, factual truth", report["scope"])

    def run_cli(self, text: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPT), "-", "--format", "json"], input=text, capture_output=True, text=True, check=False)

    def test_cli_valid_file_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/"plan.json"
            original = json.dumps(self.plan, ensure_ascii=False)
            path.write_text(original, encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--format", "json"], capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)["valid"])
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_cli_plan_errors_return_one(self) -> None:
        self.plan["beats"][1]["start"] = 7
        result = self.run_cli(json.dumps(self.plan))
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(json.loads(result.stdout)["valid"])

    def test_cli_rejects_invalid_json_duplicate_keys_and_nonfinite_values(self) -> None:
        for text in ("{", '{"duration_seconds":8,"duration_seconds":9}', '{"duration_seconds":NaN}'):
            with self.subTest(text=text):
                result = self.run_cli(text)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertFalse(json.loads(result.stdout)["valid"])
        result = subprocess.run([sys.executable, str(SCRIPT), str(FIXTURE.parent/"missing.json"), "--format", "json"], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertFalse(json.loads(result.stdout)["valid"])


if __name__ == "__main__":
    unittest.main()
