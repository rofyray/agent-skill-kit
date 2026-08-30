#!/usr/bin/env python3
"""Surface candidate formulaic prose patterns without modifying the source."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


EM_DASH = "\u2014"
NEGATIVE_PARALLELISM = re.compile(
    r"\bnot\b[^\n.!?]{1,140}\bbut\b"
    r"|\bnot\b[^\n.!?;]{1,140};\s*(?:it|this|that)\s+(?:is|was|means)\b"
    r"|\brather\s+than\b",
    re.IGNORECASE,
)
TRIAD = re.compile(
    r"\b[^,\n.!?]{1,60},\s+[^,\n.!?]{1,60},\s+(?:and|or)\s+[^,\n.!?]{1,60}",
    re.IGNORECASE,
)
ORDERLY_SEQUENCE = re.compile(
    r"\bfirst(?:ly)?\b[\s\S]{1,900}\bsecond(?:ly)?\b[\s\S]{1,900}\bthird(?:ly)?\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Signal:
    kind: str
    status: str
    line: int
    column: int
    excerpt: str


def _location(text: str, index: int) -> tuple[int, int]:
    line = text.count("\n", 0, index) + 1
    last_newline = text.rfind("\n", 0, index)
    column = index + 1 if last_newline < 0 else index - last_newline
    return line, column


def _excerpt(text: str, start: int, end: int, limit: int = 180) -> str:
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    if line_end < 0:
        line_end = len(text)
    value = " ".join(text[line_start:line_end].strip().split())
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def _pattern_signals(text: str, pattern: re.Pattern[str], kind: str) -> list[Signal]:
    signals: list[Signal] = []
    for match in pattern.finditer(text):
        line, column = _location(text, match.start())
        signals.append(
            Signal(
                kind=kind,
                status="candidate",
                line=line,
                column=column,
                excerpt=_excerpt(text, match.start(), match.end()),
            )
        )
    return signals


def scan_text(text: str) -> dict[str, object]:
    signals: list[Signal] = []

    for match in re.finditer(EM_DASH, text):
        line, column = _location(text, match.start())
        signals.append(
            Signal(
                kind="em_dash",
                status="exact",
                line=line,
                column=column,
                excerpt=_excerpt(text, match.start(), match.end()),
            )
        )

    signals.extend(_pattern_signals(text, NEGATIVE_PARALLELISM, "negative_parallelism"))
    signals.extend(_pattern_signals(text, TRIAD, "triad"))
    signals.extend(_pattern_signals(text, ORDERLY_SEQUENCE, "orderly_sequence"))
    signals.sort(key=lambda item: (item.line, item.column, item.kind))

    counts: dict[str, int] = {}
    for signal in signals:
        counts[signal.kind] = counts.get(signal.kind, 0) + 1

    return {
        "characters": len(text),
        "lines": len(text.splitlines()),
        "signal_counts": counts,
        "signals": [asdict(signal) for signal in signals],
        "notice": (
            "Em-dash matches are exact. Other signals are candidates that require contextual "
            "review and do not establish AI authorship."
        ),
    }


def _read_source(source: str) -> tuple[str, str]:
    if source == "-":
        return sys.stdin.read(), "stdin"
    path = Path(source).expanduser()
    return path.read_text(encoding="utf-8"), str(path)


def _render_text(report: dict[str, object], source: str) -> str:
    lines = [f"Source: {source}", str(report["notice"])]
    signals = report["signals"]
    assert isinstance(signals, list)
    if not signals:
        lines.append("No scanner signals found.")
        return "\n".join(lines)

    for signal in signals:
        assert isinstance(signal, dict)
        lines.append(
            f"{signal['line']}:{signal['column']} "
            f"{signal['kind']} ({signal['status']}): {signal['excerpt']}"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", default="-", help="UTF-8 text file or - for stdin")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    try:
        text, source = _read_source(args.source)
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    report = scan_text(text)
    if args.format == "json":
        print(json.dumps({"source": source, **report}, indent=2, ensure_ascii=False))
    else:
        print(_render_text(report, source))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
