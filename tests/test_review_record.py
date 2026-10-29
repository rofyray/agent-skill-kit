from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT/"skills"/"review-code-changes"/"scripts"/"review_record.py"
SPEC = importlib.util.spec_from_file_location("review_record", SCRIPT)
assert SPEC and SPEC.loader
review_record = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review_record)


def clean_record() -> dict:
    return {
        "schema_version": 1,
        "target": {"baseline": "base:a1", "reviewed": "tree:b2", "previous_reviewed": None},
        "round": 1,
        "round_limit": 3,
        "status": "complete",
        "outcome": "no-findings",
        "coverage": [{"area": "request path and caller", "status": "complete", "evidence": "service.py:5 and route.py:8 inspected"}],
        "checks": [{"name": "route probe", "state": "passed", "revision": "tree:b2", "evidence": "Expected denied response observed."}],
        "committee": [
            {"id": "d1", "role": "discovery", "independent": True, "status": "complete", "scope": "request path"},
            {"id": "v1", "role": "verification", "independent": True, "status": "complete", "scope": "candidate validation"},
        ],
        "findings": [],
        "limitations": [],
    }


def finding() -> dict:
    return {
        "id": "F1", "title": "Cross-tenant read", "severity": "high",
        "provenance": "introduced", "status": "open",
        "location": {"path": "service.py", "line": 5},
        "trigger": "Read another tenant's identifier.", "impact": "Exposes that tenant's data.",
        "evidence": "The query is missing tenant scope at service.py:5.",
        "validation": {"method": "static", "reviewers": ["v1"], "rationale": "No upstream tenant guard in route.py:8."},
        "disposition": None,
    }


class ReviewRecordTests(unittest.TestCase):
    def assert_invalid(self, record: dict, expected: str) -> None:
        self.assertTrue(any(expected in error for error in review_record.validate(record)), review_record.validate(record))

    def test_complete_no_findings(self) -> None:
        self.assertEqual(review_record.validate(clean_record()), [])

    def test_static_fallback_preserves_limitations(self) -> None:
        record = clean_record()
        record["checks"] = []
        record["committee"][1]["independent"] = False
        self.assert_invalid(record, "limitations")
        record["limitations"] = ["No runtime or independent verifier; separate static challenge only."]
        self.assertEqual(review_record.validate(record), [])

    def test_not_run_is_never_passed_evidence(self) -> None:
        record = clean_record()
        record["checks"][0].update(state="not-run", revision=None)
        self.assert_invalid(record, "limitations")
        record["limitations"] = ["Runtime probe unavailable; conclusion covers static inspection."]
        self.assertEqual(review_record.validate(record), [])

    def test_no_findings_cannot_hide_open_issue(self) -> None:
        record = clean_record()
        record["findings"] = [finding()]
        self.assert_invalid(record, "no-findings")
        record["outcome"] = "findings"
        self.assertEqual(review_record.validate(record), [])

    def test_stale_pass_requires_incomplete_verdict(self) -> None:
        record = clean_record()
        record["checks"][0]["revision"] = "old:9"
        record["limitations"] = ["Only an older log is available."]
        self.assert_invalid(record, "stale passes")
        record.update(status="incomplete", outcome="inconclusive")
        self.assertEqual(review_record.validate(record), [])

    def test_blocked_coverage_or_committee_cannot_be_complete(self) -> None:
        for collection in ("coverage", "committee"):
            with self.subTest(collection=collection):
                record = clean_record()
                record[collection][0]["status"] = "blocked"
                record["limitations"] = ["A required review area could not be inspected."]
                self.assert_invalid(record, "cannot be complete")

    def test_completed_replacement_retains_attempt_without_blocking_review(self) -> None:
        record = clean_record()
        attempt = copy.deepcopy(record["committee"][1])
        attempt.update(id="v0", status="superseded", replacement_id="v1")
        record["committee"].append(attempt)
        self.assertEqual(review_record.validate(record), [])
        self.assertEqual(len(record["committee"]), 3)
        self.assertEqual(record["committee"][2]["id"], "v0")

    def test_superseded_requires_real_completed_same_role_replacement(self) -> None:
        for replacement_id in (None, "missing", "v0", "d1", "blocked", "superseded"):
            with self.subTest(replacement_id=replacement_id):
                record = clean_record()
                attempt = copy.deepcopy(record["committee"][1])
                attempt.update(id="v0", status="superseded")
                if replacement_id is not None:
                    attempt["replacement_id"] = replacement_id
                record["committee"].append(attempt)
                if replacement_id in {"blocked", "superseded"}:
                    replacement = copy.deepcopy(record["committee"][1])
                    replacement.update(id=replacement_id, status=replacement_id)
                    if replacement_id == "superseded":
                        replacement["replacement_id"] = "v1"
                    record["committee"].append(replacement)
                self.assert_invalid(record, "different completed same-role replacement")

    def test_replacement_field_cannot_mask_active_blocked_work(self) -> None:
        for status in ("blocked", "complete"):
            record = clean_record()
            record["committee"][0].update(status=status, replacement_id="v1")
            self.assert_invalid(record, "only allowed for superseded")
            if status == "blocked":
                self.assert_invalid(record, "cannot be complete")

    def test_superseded_worker_cannot_validate_findings(self) -> None:
        record = clean_record()
        attempt = copy.deepcopy(record["committee"][1])
        attempt.update(id="v0", status="superseded", replacement_id="v1")
        record["committee"].append(attempt)
        item = finding()
        item["validation"]["reviewers"] = ["v0"]
        record.update(findings=[item], outcome="findings")
        self.assert_invalid(record, "not a completed verifier")

    def test_failed_or_blocked_check_cannot_be_clean(self) -> None:
        for state in ("failed", "blocked"):
            record = clean_record()
            record["checks"][0]["state"] = state
            record["limitations"] = ["Behavior check has not established the requirement."]
            self.assert_invalid(record, "no-findings")

    def test_ids_are_unique(self) -> None:
        record = clean_record()
        record["committee"].append(copy.deepcopy(record["committee"][0]))
        self.assert_invalid(record, "duplicate member IDs")
        record = clean_record()
        record.update(findings=[finding(), finding()], outcome="findings")
        self.assert_invalid(record, "duplicate finding IDs")

    def test_verifiers_must_exist_and_complete_verification_role(self) -> None:
        for reviewer in ("missing", "d1", "v1"):
            with self.subTest(reviewer=reviewer):
                record = clean_record()
                item = finding()
                item["validation"]["reviewers"] = [reviewer]
                record.update(findings=[item], outcome="findings")
                if reviewer == "v1":
                    record["committee"][1]["status"] = "blocked"
                self.assert_invalid(record, "not a completed verifier")

    def test_adjudicator_can_validate(self) -> None:
        record = clean_record()
        record["committee"][1]["role"] = "adjudication"
        record.update(findings=[finding()], outcome="findings")
        self.assertEqual(review_record.validate(record), [])

    def test_round_three_unresolved_requires_human(self) -> None:
        record = clean_record()
        record.update(round=3, findings=[finding()], outcome="findings")
        record["target"]["previous_reviewed"] = "tree:b1"
        self.assert_invalid(record, "round_limit requires needs-human")
        record["status"] = "needs-human"
        self.assertEqual(review_record.validate(record), [])

    def test_round_three_resolved_is_complete(self) -> None:
        record = clean_record()
        record.update(round=3)
        record["target"]["previous_reviewed"] = "tree:b1"
        self.assertEqual(review_record.validate(record), [])

    def test_custom_round_limit_allows_authorized_further_review(self) -> None:
        record = clean_record()
        record.update(round=4, round_limit=5, findings=[finding()], outcome="findings")
        record["target"]["previous_reviewed"] = "tree:b1"
        self.assertEqual(review_record.validate(record), [])
        for round_number in (5, 6):
            record["round"] = round_number
            self.assert_invalid(record, "round_limit requires needs-human")
        record["status"] = "needs-human"
        self.assertEqual(review_record.validate(record), [])

    def test_discovery_alone_cannot_complete_even_clean_review(self) -> None:
        record = clean_record()
        record["committee"] = [record["committee"][0]]
        self.assert_invalid(record, "requires a completed verifier")
        record.update(status="incomplete", outcome="inconclusive", limitations=["Verification unavailable."])
        self.assertEqual(review_record.validate(record), [])

    def test_short_round_limit_is_respected(self) -> None:
        record = clean_record()
        record.update(round_limit=1, findings=[finding()], outcome="findings")
        self.assert_invalid(record, "round_limit requires needs-human")

    def test_round_history_cannot_be_omitted_or_invented(self) -> None:
        record = clean_record()
        record["round"] = 2
        self.assert_invalid(record, "previous snapshot")
        record["round"] = 1
        record["target"]["previous_reviewed"] = "tree:b1"
        self.assert_invalid(record, "first round")

    def test_fixed_requires_current_confirmation(self) -> None:
        record = clean_record()
        item = finding()
        item["status"] = "fixed"
        record["findings"] = [item]
        self.assert_invalid(record, "resolved finding needs")
        item["disposition"] = {"reason": "Tenant guard restored.", "evidence": "Denial observed.", "revision": "old:9"}
        self.assert_invalid(record, "fix must be verified")
        item["disposition"]["revision"] = "tree:b2"
        self.assertEqual(review_record.validate(record), [])

    def test_dismissal_can_retain_previous_reasoned_decision(self) -> None:
        record = clean_record()
        item = finding()
        item.update(status="dismissed", disposition={"reason": "Scope guaranteed by caller.", "evidence": "route.py:8", "revision": "previous:1"})
        record["findings"] = [item]
        self.assertEqual(review_record.validate(record), [])

    def test_executed_claim_needs_current_executed_check(self) -> None:
        record = clean_record()
        item = finding()
        item["validation"]["method"] = "executed"
        record.update(findings=[item], outcome="findings", checks=[], limitations=["No execution."])
        self.assert_invalid(record, "current executed check")

    def test_strict_shapes_reject_partial_or_ambiguous_records(self) -> None:
        variants = [
            ("round", True), ("round", 0), ("round_limit", 0), ("round_limit", True), ("schema_version", 2),
            ("outcome", "approved"), ("coverage", []), ("committee", []),
            ("limitations", [""]), ("status", None),
        ]
        for field, value in variants:
            with self.subTest(field=field, value=value):
                record = clean_record()
                record[field] = value
                self.assertTrue(review_record.validate(record))
        record = clean_record()
        del record["checks"]
        self.assert_invalid(record, "required")
        record = clean_record()
        record["approval"] = True
        self.assert_invalid(record, "unknown field")

    def test_unsupported_schema_keywords_fail_explicitly(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported schema keywords"):
            review_record.shape_errors("x", {"type": "string", "pattern": "x"}, {})
        with self.assertRaisesRegex(ValueError, "sibling constraints"):
            review_record.shape_errors("x", {"$ref": "#/$defs/text", "minLength": 4}, {"$defs": {"text": {"type": "string"}}})

    def test_inconclusive_does_not_claim_completion(self) -> None:
        record = clean_record()
        record["outcome"] = "inconclusive"
        self.assert_invalid(record, "requires incomplete")

    def test_cli_handles_bad_json_and_does_not_modify_input(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"record.json"
            for content, expected_code in ((json.dumps(clean_record()), 0), ('{"outcome":"findings","outcome":"no-findings"}', 1), ("{", 1), ('{"schema_version":1}', 1)):
                path.write_text(content, encoding="utf-8")
                result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, expected_code, result.stderr)
                self.assertEqual(path.read_text(encoding="utf-8"), content)
            result = subprocess.run([sys.executable, str(SCRIPT), str(Path(directory)/"absent.json")], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
