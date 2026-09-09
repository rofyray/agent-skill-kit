#!/usr/bin/env python3
"""Check declared motion timelines, copy, references, holds, and percentage geometry."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


TOLERANCE = 0.000001
SCOPE = "Checks declared plan structure only, not rendered media, factual truth, or artistic quality."


def validate_plan(plan: Any) -> dict[str, Any]:
    errors: list[dict[str, str]] = []

    def error(path: str, message: str) -> None:
        errors.append({"path": path, "message": message})

    def fields(value: Any, path: str, required: set[str], optional: set[str]) -> bool:
        if not isinstance(value, dict):
            error(path, "Expected an object.")
            return False
        for key in sorted(required - value.keys()):
            error(f"{path}.{key}", "Required field is missing.")
        for key in value:
            if key not in required | optional | {"metadata"}:
                error(f"{path}.{key}", "Unknown field; put additional notes in metadata.")
        if "metadata" in value and not isinstance(value["metadata"], dict):
            error(f"{path}.metadata", "Expected an object.")
        return True

    def number(value: Any, path: str) -> float | None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            error(path, "Expected a finite number, not a boolean or string.")
            return None
        try:
            result = float(value)
        except (OverflowError, ValueError):
            result = math.inf
        if not math.isfinite(result):
            error(path, "Expected a finite number.")
            return None
        return result

    def nonempty(value: Any, path: str) -> bool:
        if not isinstance(value, str) or not value.strip():
            error(path, "Expected a nonempty string.")
            return False
        return True

    def array(value: Any, path: str) -> list[Any]:
        if not isinstance(value, list):
            error(path, "Expected an array.")
            return []
        return value

    def unique_id(item: dict[str, Any], path: str, seen: set[str]) -> str | None:
        identity = item.get("id")
        if not nonempty(identity, f"{path}.id"):
            return None
        if identity in seen:
            error(f"{path}.id", f"Duplicate ID {identity!r}.")
            return None
        seen.add(identity)
        return identity

    def catalog(key: str, property_name: str) -> dict[str, str]:
        result: dict[str, str] = {}
        seen: set[str] = set()
        for index, item in enumerate(array(plan.get(key), key)):
            path = f"{key}[{index}]"
            if not fields(item, path, {"id", property_name}, set()):
                continue
            identity = unique_id(item, path, seen)
            value = item.get(property_name)
            good = nonempty(value, f"{path}.{property_name}")
            if identity is not None and good:
                result[identity] = value
        return result

    def bindings(value: Any, path: str, declared: dict[str, str]) -> set[str]:
        seen: set[str] = set()
        for index, identity in enumerate(array(value, path)):
            item_path = f"{path}[{index}]"
            if not nonempty(identity, item_path):
                continue
            if identity in seen:
                error(item_path, f"Duplicate active ID {identity!r}.")
            if identity not in declared:
                error(item_path, f"Undeclared ID {identity!r}.")
            seen.add(identity)
        return seen

    required = {"schema_version", "duration_seconds", "references", "copy", "beats"}
    optional = {"fps", "final_hold_seconds", "percent_bars"}
    if not fields(plan, "$", required, optional):
        return {"valid": False, "errors": errors, "scope": SCOPE}
    if type(plan.get("schema_version")) is not int or plan["schema_version"] != 1:
        error("schema_version", "Expected integer schema version 1.")
    duration = number(plan.get("duration_seconds"), "duration_seconds")
    if duration is not None and duration <= 0:
        error("duration_seconds", "Must be greater than zero.")
    if "fps" in plan:
        fps = number(plan["fps"], "fps")
        if fps is not None and fps <= 0:
            error("fps", "Must be greater than zero.")

    references = catalog("references", "role")
    copy = catalog("copy", "text")
    beats = array(plan.get("beats"), "beats")
    if not beats:
        error("beats", "At least one beat is required.")
    seen_beats: set[str] = set()
    previous_end: float | None = 0.0
    tail_hold = 0.0
    timeline_valid = True
    for index, beat in enumerate(beats):
        path = f"beats[{index}]"
        if not fields(beat, path, {"id", "start", "end", "action", "copy_ids", "reference_ids"}, {"hold", "copy_text"}):
            previous_end = None
            timeline_valid = False
            continue
        unique_id(beat, path, seen_beats)
        nonempty(beat.get("action"), f"{path}.action")
        active_copy = bindings(beat.get("copy_ids"), f"{path}.copy_ids", copy)
        bindings(beat.get("reference_ids"), f"{path}.reference_ids", references)
        if "copy_text" in beat:
            text_map = beat["copy_text"]
            if not isinstance(text_map, dict):
                error(f"{path}.copy_text", "Expected an object mapping active copy IDs to exact strings.")
            else:
                for identity, text in text_map.items():
                    if identity not in active_copy or identity not in copy:
                        error(f"{path}.copy_text.{identity}", "Copy ID must be declared and active in this beat.")
                    elif text != copy[identity]:
                        error(f"{path}.copy_text.{identity}", "Compiled copy differs from the declared exact string.")
        hold = beat.get("hold", False)
        if not isinstance(hold, bool):
            error(f"{path}.hold", "Expected a boolean.")
        start = number(beat.get("start"), f"{path}.start")
        end = number(beat.get("end"), f"{path}.end")
        if start is None or end is None:
            previous_end = None
            timeline_valid = False
            tail_hold = 0.0
            continue
        valid_interval = True
        if start < 0 or end <= start:
            error(path, "Beat must start at or after zero and have positive duration.")
            valid_interval = False
        if duration is not None and end > duration + TOLERANCE:
            error(f"{path}.end", "Beat extends past the declared duration.")
            valid_interval = False
        if previous_end is not None and abs(start - previous_end) > TOLERANCE:
            relation = "Gap" if start > previous_end else "Overlap or out-of-order beat"
            error(f"{path}.start", f"{relation}; expected start {previous_end:g}.")
            valid_interval = False
        timeline_valid = timeline_valid and valid_interval
        tail_hold = tail_hold + end - start if hold is True and valid_interval else 0.0
        previous_end = end
    if beats and duration is not None and previous_end is not None:
        if abs(previous_end - duration) > TOLERANCE:
            error("beats", "The final beat must end at the declared duration.")
            timeline_valid = False

    if "final_hold_seconds" in plan:
        hold_seconds = number(plan["final_hold_seconds"], "final_hold_seconds")
        if hold_seconds is not None:
            if hold_seconds < 0:
                error("final_hold_seconds", "Must be nonnegative.")
            elif duration is not None and hold_seconds > duration + TOLERANCE:
                error("final_hold_seconds", "Cannot exceed the film duration.")
            elif timeline_valid and tail_hold + TOLERANCE < hold_seconds:
                error("final_hold_seconds", f"Declared ending hold is only {tail_hold:g} seconds.")

    seen_bars: set[str] = set()
    for index, bar in enumerate(array(plan.get("percent_bars", []), "percent_bars")):
        path = f"percent_bars[{index}]"
        if not fields(bar, path, {"id", "percent", "track_length", "filled_length"}, set()):
            continue
        unique_id(bar, path, seen_bars)
        percent = number(bar.get("percent"), f"{path}.percent")
        track = number(bar.get("track_length"), f"{path}.track_length")
        fill = number(bar.get("filled_length"), f"{path}.filled_length")
        if percent is None or track is None or fill is None:
            continue
        if not 0 <= percent <= 100:
            error(f"{path}.percent", "Must be between zero and 100.")
        if track <= 0:
            error(f"{path}.track_length", "Must be greater than zero.")
        elif not 0 <= fill <= track:
            error(f"{path}.filled_length", "Must be between zero and track_length.")
        elif abs(100 * (fill/track) - percent) > TOLERANCE:
            error(f"{path}.filled_length", "Fill geometry does not match the declared percentage.")

    return {"valid": not errors, "errors": errors, "scope": SCOPE}


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"Non-finite JSON number: {value}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", help="JSON file path, or - to read standard input")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    try:
        source = sys.stdin.read() if args.plan == "-" else Path(args.plan).read_text(encoding="utf-8-sig")
        plan = json.loads(source, object_pairs_hook=reject_duplicate_keys, parse_constant=reject_constant)
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        report = {"valid": False, "errors": [{"path": "$", "message": str(exc)}], "scope": SCOPE}
        exit_code = 2
    else:
        report = validate_plan(plan)
        exit_code = 0 if report["valid"] else 1
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("PASS" if report["valid"] else "FAIL")
        for item in report["errors"]:
            print(f"{item['path']}: {item['message']}")
        print(SCOPE)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
