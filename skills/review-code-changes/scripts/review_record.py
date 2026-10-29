#!/usr/bin/env python3
"""Validate a review record without executing or inspecting the reviewed project.

Python 3.10+; standard library only. Checks declared record consistency, not
whether the evidence is true, reviewers ran, or a change is safe to merge.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA_PATH = Path(__file__).resolve().parents[1]/"assets"/"review-record.schema.json"
SCHEMA_KEYS = {
    "$schema", "$id", "$defs", "$ref", "title", "description", "type",
    "properties", "required", "additionalProperties", "items", "minItems",
    "uniqueItems", "minLength", "minimum", "maximum", "enum", "const",
}


def shape_errors(value: Any, schema: dict, root: dict, path: str = "record") -> list[str]:
    """Interpret only the JSON Schema keywords used by the bundled contract.

    Fail on unsupported keywords so a future schema change cannot silently
    weaken this validator. This is not a general JSON Schema implementation.
    """
    unknown = set(schema) - SCHEMA_KEYS
    if unknown:
        raise ValueError(f"Unsupported schema keywords: {', '.join(sorted(unknown))}")
    if "$ref" in schema:
        if set(schema) - {"$ref", "title", "description"}:
            raise ValueError("Schema references cannot have sibling constraints in this validator")
        prefix = "#/$defs/"
        ref = schema["$ref"]
        if not ref.startswith(prefix) or ref[len(prefix):] not in root.get("$defs", {}):
            raise ValueError(f"Unsupported schema reference: {ref}")
        return shape_errors(value, root["$defs"][ref[len(prefix):]], root, path)

    expected = schema.get("type")
    choices = expected if isinstance(expected, list) else [expected]
    matches = {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": type(value) is int,
        "boolean": type(value) is bool,
        "null": value is None,
    }
    if expected is not None and not any(matches.get(choice, False) for choice in choices):
        return [f"{path}: expected {expected}"]
    errors = []
    if "const" in schema and (type(value) is not type(schema["const"]) or value != schema["const"]):
        errors.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value is not in {schema['enum']!r}")
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}.{key}: required")
        for key, item in value.items():
            if key in properties:
                errors.extend(shape_errors(item, properties[key], root, f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}.{key}: unknown field")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: too few items")
        if schema.get("uniqueItems") and len({json.dumps(item, sort_keys=True) for item in value}) != len(value):
            errors.append(f"{path}: duplicate items")
        if "items" in schema:
            for index, item in enumerate(value):
                errors.extend(shape_errors(item, schema["items"], root, f"{path}[{index}]"))
    if isinstance(value, str) and len(value.strip()) < schema.get("minLength", 0):
        errors.append(f"{path}: must contain non-whitespace text")
    if type(value) is int:
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: above maximum {schema['maximum']}")
    return errors


def validate(record: Any) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = shape_errors(record, schema, schema)
    if errors:
        return errors

    current = record["target"]["reviewed"]
    previous = record["target"]["previous_reviewed"]
    if record["round"] == 1 and previous is not None:
        errors.append("target.previous_reviewed: first round must use null")
    if record["round"] > 1 and previous is None:
        errors.append("target.previous_reviewed: re-review requires the previous snapshot")
    limitations = record["limitations"]
    committee = {member["id"]: member for member in record["committee"]}
    if len(committee) != len(record["committee"]):
        errors.append("committee: duplicate member IDs")
    for member in record["committee"]:
        if member["status"] == "superseded":
            replacement_id = member.get("replacement_id")
            replacement = committee.get(replacement_id)
            if (
                replacement is None
                or replacement_id == member["id"]
                or replacement["status"] != "complete"
                or replacement["role"] != member["role"]
            ):
                errors.append(f"committee.{member['id']}: superseded member needs a different completed same-role replacement")
        elif "replacement_id" in member:
            errors.append(f"committee.{member['id']}: replacement_id is only allowed for superseded members")
    if record["status"] == "complete" and not any(
        member["role"] in {"verification", "adjudication"} and member["status"] == "complete"
        for member in committee.values()
    ):
        errors.append("committee: a complete review requires a completed verifier or adjudicator")
    finding_ids = [finding["id"] for finding in record["findings"]]
    if len(set(finding_ids)) != len(finding_ids):
        errors.append("findings: duplicate finding IDs")

    blocked = any(item["status"] == "blocked" for item in record["coverage"] + record["committee"])
    stale = any(check["state"] == "passed" and check["revision"] != current for check in record["checks"])
    check_failure = any(check["state"] in {"failed", "blocked"} for check in record["checks"])
    unrun = not record["checks"] or any(check["state"] == "not-run" for check in record["checks"])
    fallback = any(not member["independent"] for member in committee.values())
    if (blocked or stale or check_failure or unrun or fallback) and not limitations:
        errors.append("limitations: explain blocked, stale, failed, unrun, or non-independent work")
    if (blocked or stale) and record["status"] == "complete":
        errors.append("status: incomplete coverage, committee work, or stale passes cannot be complete")
    if record["status"] == "complete" and record["outcome"] == "inconclusive":
        errors.append("status: an inconclusive outcome requires incomplete or needs-human status")
    for index, check in enumerate(record["checks"]):
        if check["state"] in {"passed", "failed"} and check["revision"] is None:
            errors.append(f"checks[{index}].revision: executed checks need a tested state")

    open_findings = [finding for finding in record["findings"] if finding["status"] == "open"]
    if record["outcome"] == "no-findings":
        if open_findings or blocked or stale or check_failure or record["status"] != "complete":
            errors.append("outcome: no-findings requires complete review with no open findings or unresolved evidence failures")
    if record["outcome"] == "findings" and not open_findings:
        errors.append("outcome: findings requires at least one open finding")
    if record["round"] >= record["round_limit"] and (open_findings or blocked or stale or check_failure or record["status"] == "incomplete"):
        if record["status"] != "needs-human":
            errors.append("status: unresolved work at or beyond round_limit requires needs-human")

    for index, finding in enumerate(record["findings"]):
        label = f"findings[{index}]"
        if finding["status"] != "dismissed" and finding["validation"]["method"] == "executed" and not any(
            check["state"] in {"passed", "failed"} and check["revision"] == current
            for check in record["checks"]
        ):
            errors.append(f"{label}.validation.method: executed validation needs a current executed check")
        for reviewer_id in finding["validation"]["reviewers"]:
            reviewer = committee.get(reviewer_id)
            if reviewer is None or reviewer["role"] not in {"verification", "adjudication"} or reviewer["status"] != "complete":
                errors.append(f"{label}.validation.reviewers: {reviewer_id!r} is not a completed verifier or adjudicator")
        disposition = finding["disposition"]
        if finding["status"] == "open" and disposition is not None:
            errors.append(f"{label}.disposition: open finding must have null disposition")
        if finding["status"] in {"fixed", "dismissed"} and disposition is None:
            errors.append(f"{label}.disposition: resolved finding needs reason, evidence, and revision")
        if finding["status"] == "fixed" and disposition is not None and disposition["revision"] != current:
            errors.append(f"{label}.disposition.revision: a fix must be verified at the reviewed state")
    return errors


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path, help="JSON review record to validate")
    args = parser.parse_args()
    try:
        record = json.loads(args.record.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)
        errors = validate(record)
    except (OSError, ValueError, RecursionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Review record is consistent. This does not verify evidence or authorize merging.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
