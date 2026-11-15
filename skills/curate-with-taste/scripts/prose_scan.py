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
MIDDLE_DOT = "\u00b7"
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
MARKDOWN_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(?P<title>.+?)\s*$")
COMMA_TAIL = re.compile(
    r"^(?P<lead>[^,]{2,100}),\s+(?P<tail>[A-Za-z][A-Za-z'-]*(?:\s+[A-Za-z][A-Za-z'-]*){0,3})$"
)
COMMA_TAIL_WORDS = {
    "ahead",
    "alive",
    "assembled",
    "better",
    "connected",
    "different",
    "elevated",
    "forward",
    "human",
    "refined",
    "reimagined",
    "simplified",
    "together",
    "transformed",
    "unlocked",
}


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


def _comma_tail_offset(title: str) -> int | None:
    primary = title.split(MIDDLE_DOT, 1)[0].strip().strip("*_`")
    match = COMMA_TAIL.fullmatch(primary)
    if not match:
        return None

    tail = match.group("tail")
    last_word = tail.rsplit(maxsplit=1)[-1].lower()
    looks_stylized = (
        tail[:1].islower()
        or last_word.endswith(("ed", "ing"))
        or last_word in COMMA_TAIL_WORDS
    )
    return title.find(",") if looks_stylized else None


def _comma_tail_heading_signals(text: str) -> list[Signal]:
    lines_with_endings = text.splitlines(keepends=True)
    lines = [line.rstrip("\r\n") for line in lines_with_endings]
    signals: list[Signal] = []
    absolute_offset = 0

    for index, line in enumerate(lines):
        title: str | None = None
        title_start = 0
        heading = MARKDOWN_HEADING.fullmatch(line)
        if heading:
            title = heading.group("title")
            title_start = heading.start("title")
        else:
            stripped = line.strip()
            previous_blank = index == 0 or not lines[index - 1].strip()
            next_blank = index == len(lines) - 1 or not lines[index + 1].strip()
            excluded_prefix = stripped.startswith(("- ", "* ", ">", "```", "|"))
            title_like = (
                bool(stripped)
                and len(stripped) <= 100
                and previous_blank
                and next_blank
                and not excluded_prefix
                and not stripped.endswith((".", "?", "!", ";"))
            )
            if title_like:
                title = stripped
                title_start = line.find(stripped)

        if title is not None:
            comma_offset = _comma_tail_offset(title)
            if comma_offset is not None:
                start = absolute_offset + title_start + comma_offset
                line_number, column = _location(text, start)
                signals.append(
                    Signal(
                        kind="comma_tail_heading",
                        status="candidate",
                        line=line_number,
                        column=column,
                        excerpt=_excerpt(text, start, start + 1),
                    )
                )

        absolute_offset += len(lines_with_endings[index])

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

    for match in re.finditer(MIDDLE_DOT, text):
        line, column = _location(text, match.start())
        signals.append(
            Signal(
                kind="middle_dot",
                status="exact",
                line=line,
                column=column,
                excerpt=_excerpt(text, match.start(), match.end()),
            )
        )

    signals.extend(_pattern_signals(text, NEGATIVE_PARALLELISM, "negative_parallelism"))
    signals.extend(_pattern_signals(text, TRIAD, "triad"))
    signals.extend(_pattern_signals(text, ORDERLY_SEQUENCE, "orderly_sequence"))
    signals.extend(_comma_tail_heading_signals(text))
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
            "Em-dash and middle-dot matches are exact. Other signals are candidates that "
            "require contextual review and do not establish AI authorship."
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
