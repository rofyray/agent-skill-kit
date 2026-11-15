from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1]/"skills"/"curate-with-taste"/"scripts"/"prose_scan.py"
SPEC = importlib.util.spec_from_file_location("prose_scan", SCRIPT)
assert SPEC and SPEC.loader
prose_scan = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = prose_scan
SPEC.loader.exec_module(prose_scan)


class ProseScanTests(unittest.TestCase):
    def test_reports_exact_em_dash_location(self) -> None:
        text = "Opening line.\nOne issue" + chr(0x2014) + "the deadline.\n"
        report = prose_scan.scan_text(text)
        matches = [item for item in report["signals"] if item["kind"] == "em_dash"]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["status"], "exact")
        self.assertEqual(matches[0]["line"], 2)
        self.assertEqual(matches[0]["column"], 10)

    def test_reports_middle_dot_and_comma_tail_heading(self) -> None:
        text = "# Simulated humans, assembled " + chr(0x00B7) + " 2 agents\n"
        report = prose_scan.scan_text(text)
        middle_dots = [item for item in report["signals"] if item["kind"] == "middle_dot"]
        comma_tails = [
            item for item in report["signals"] if item["kind"] == "comma_tail_heading"
        ]
        self.assertEqual(len(middle_dots), 1)
        self.assertEqual(middle_dots[0]["status"], "exact")
        self.assertEqual(middle_dots[0]["line"], 1)
        self.assertEqual(len(comma_tails), 1)
        self.assertEqual(comma_tails[0]["status"], "candidate")
        self.assertEqual(comma_tails[0]["line"], 1)

    def test_reports_standalone_comma_tail_title(self) -> None:
        text = "Systems, reimagined\n\nThe new architecture reduces queue latency.\n"
        report = prose_scan.scan_text(text)
        matches = [
            item for item in report["signals"] if item["kind"] == "comma_tail_heading"
        ]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["line"], 1)

    def test_ignores_legitimate_heading_commas(self) -> None:
        text = (
            "# Portland, Oregon\n\n"
            "# Research, Design, and Engineering\n\n"
            "The team met in Portland, Oregon, before the launch.\n"
        )
        report = prose_scan.scan_text(text)
        matches = [
            item for item in report["signals"] if item["kind"] == "comma_tail_heading"
        ]
        self.assertEqual(matches, [])

    def test_surfaces_semantic_candidates_without_authorship_claim(self) -> None:
        text = (
            "This is not just a tool but a new habit.\n"
            "It is not merely convenient; it is dependable.\n"
            "First, frame the problem. Second, inspect the options. Third, choose.\n"
            "The draft promises speed, clarity, and confidence.\n"
        )
        report = prose_scan.scan_text(text)
        kinds = {item["kind"] for item in report["signals"]}
        self.assertIn("negative_parallelism", kinds)
        self.assertEqual(report["signal_counts"]["negative_parallelism"], 2)
        self.assertIn("orderly_sequence", kinds)
        self.assertIn("triad", kinds)
        self.assertIn("do not establish AI authorship", report["notice"])

    def test_clean_prose_has_no_signals(self) -> None:
        report = prose_scan.scan_text(
            "We shipped the billing fix yesterday. Two customers confirmed that invoices now load."
        )
        self.assertEqual(report["signals"], [])
        self.assertEqual(report["signal_counts"], {})

    def test_cli_reads_stdin_and_returns_json(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--format", "json"],
            input="The plan is fast, clear, and credible.\n",
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["source"], "stdin")
        self.assertEqual(report["lines"], 1)
        self.assertEqual(report["signal_counts"], {"triad": 1})


if __name__ == "__main__":
    unittest.main()
