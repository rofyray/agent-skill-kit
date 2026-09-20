#!/usr/bin/env python3
"""Compare local prompt text mechanically; never execute or grade its meaning."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import difflib
import json
from pathlib import Path
import re
import sys


NAME = r"[A-Za-z_][A-Za-z0-9_.-]*"
PATTERNS = {
    "double-braces": rf"(?<!\{{)\{{\{{\s*{NAME}\s*\}}\}}(?!\}})",
    "dollar-braces": rf"\$\{{{NAME}\}}",
    "braces": rf"(?<![\{{$])\{{{NAME}\}}(?!\}})",
}


def placeholder_counts(text: str, styles: list[str]) -> Counter:
    """Discover candidates only; this is deliberately not a template parser."""
    counts: Counter = Counter()
    for style in styles:
        counts.update(re.findall(PATTERNS[style], text))
    return counts


def duplicate_paragraphs(text: str) -> list[dict]:
    """Locate exactly repeated paragraphs without including their contents."""
    locations: dict[str, list[int]] = defaultdict(list)
    current: list[str] = []
    start = 1
    for number, line in enumerate(text.splitlines() + [""], start=1):
        if line.strip():
            if not current:
                start = number
            current.append(line)
        elif current:
            locations["\n".join(current)].append(start)
            current = []
    return [
        {"start_lines": starts, "occurrences": len(starts)}
        for starts in locations.values()
        if len(starts) > 1
    ]


def stats(text: str) -> dict:
    return {
        "characters": len(text),
        "whitespace_delimited_words": len(text.split()),
        "lines": len(text.splitlines()),
    }


def read_requirements(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != {"required_literals"}:
        raise ValueError("manifest must be an object containing only required_literals")
    literals = data["required_literals"]
    if not isinstance(literals, list) or any(
        not isinstance(item, str) or not item.strip() for item in literals
    ):
        raise ValueError("required_literals must be a list of nonempty strings")
    return list(dict.fromkeys(literals))


def compare(
    original: str,
    revised: str,
    required_literals: list[str],
    styles: list[str],
    include_diff: bool = False,
) -> dict:
    before = placeholder_counts(original, styles)
    after = placeholder_counts(revised, styles)
    changes = [
        {"candidate": name, "original_occurrences": before[name], "revised_occurrences": after[name]}
        for name in sorted(before.keys() | after.keys())
        if before[name] != after[name]
    ]
    missing_original = [item for item in required_literals if item not in original]
    missing_revised = [item for item in required_literals if item not in revised]
    review = bool(changes or missing_original or missing_revised)
    report = {
        "schema_version": 1,
        "mechanical_status": "review-required" if review else "no-flags",
        "semantic_validation": "not-performed",
        "runtime_validation": "not-performed",
        "original": stats(original),
        "revised": stats(revised),
        "placeholder_styles": styles,
        "placeholder_changes": changes,
        "required_literals_missing_from_original": missing_original,
        "required_literals_missing_from_revised": missing_revised,
        "duplicate_paragraphs": {
            "original": duplicate_paragraphs(original),
            "revised": duplicate_paragraphs(revised),
        },
        "limitations": [
            "No semantic preservation, contradiction detection, or quality score is computed.",
            "Placeholder discovery is heuristic; expressions, escaping, and template logic need manual review.",
            "Word counts are whitespace-delimited, not model token counts.",
            "Repeated paragraphs are informational; tested reinforcement may be intentional.",
        ],
    }
    if include_diff:
        report["diff"] = "\n".join(difflib.unified_diff(
            original.splitlines(), revised.splitlines(),
            fromfile="original", tofile="revised", lineterm="",
        ))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path, help="original UTF-8 plain-text prompt")
    parser.add_argument("revised", type=Path, help="revised UTF-8 plain-text prompt")
    parser.add_argument("--requirements", type=Path, help="JSON manifest of exact required_literals")
    parser.add_argument("--diff", action="store_true", help="include changed prompt text in the report")
    parser.add_argument(
        "--placeholder-style", action="append", choices=[*PATTERNS, "none"],
        help="repeat to select syntax; defaults to all; none disables discovery",
    )
    args = parser.parse_args()
    styles = list(dict.fromkeys(args.placeholder_style or list(PATTERNS)))
    if "none" in styles:
        if len(styles) > 1:
            parser.error("none cannot be combined with another placeholder style")
        styles = []
    try:
        required = read_requirements(args.requirements) if args.requirements else []
        report = compare(
            args.original.read_text(encoding="utf-8"),
            args.revised.read_text(encoding="utf-8"),
            required, styles, args.diff,
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["mechanical_status"] == "review-required" else 0


if __name__ == "__main__":
    raise SystemExit(main())
