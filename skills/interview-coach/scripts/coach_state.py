#!/usr/bin/env python3
"""Initialize, validate, and summarize a private interview-coaching workspace."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


FILES = {
    "coaching_state.md": (
        "## Current Truth",
        "## Profile",
        "## Active Coaching Strategy",
        "## Coaching Preferences",
        "## State Files",
    ),
    "coaching_state.storybank.md": ("## Story Index", "## Story Details"),
    "coaching_state.loops.md": ("## Active Loops", "## Past Loops", "## Materials Index"),
    "coaching_state.history.md": (
        "## Score History",
        "## Outcome Log",
        "## Interview Intelligence",
        "## Feedback Log",
        "## Session Log",
        "## Meta-Check Log",
    ),
}

CORE_LIMIT_BYTES = 48 * 1024
STORY_ID_PATTERN = re.compile(r"^###\s+(S\d{3,})\b", re.MULTILINE)
LEVEL_TWO_PATTERN = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

CORE_SECTIONS = {
    "Current Truth",
    "Profile",
    "Active Coaching Strategy",
    "Coaching Notes",
    "Coaching Preferences",
    "State Files",
}
STORYBANK_SECTIONS = {"Storybank"}
LOOP_SECTION_PREFIXES = (
    "Interview Loops",
    "JD Analysis",
    "LinkedIn Analysis",
    "Resume Optimization",
    "Positioning Statement",
    "Outreach Strategy",
    "Presentation Prep",
    "Comp Strategy",
)
HISTORY_SECTIONS = {
    "Resume Analysis",
    "Score History",
    "Outcome Log",
    "Interview Intelligence",
    "Drill Progression",
    "Calibration State",
    "Meta-Check Log",
    "Session Log",
}


@dataclass(frozen=True)
class Finding:
    level: str
    path: str
    message: str

    def render(self) -> str:
        return f"{self.level} {self.path}: {self.message}"


def one_line(value: str) -> str:
    return " ".join(value.replace("\x00", "").split()).strip()


def workspace_path(raw: str) -> Path:
    candidate = Path(raw).expanduser()
    if candidate.is_symlink():
        raise ValueError("workspace path must not be a symbolic link")
    resolved = candidate.resolve()
    if resolved == Path(resolved.anchor) or resolved == Path.home().resolve():
        raise ValueError("choose a dedicated coaching workspace, not a filesystem or home root")
    return resolved


def templates(name: str, target_role: str, timeline: str, directness: int) -> dict[str, str]:
    name = one_line(name) or "Candidate"
    target_role = one_line(target_role) or "Unknown"
    timeline = one_line(timeline) or "Unknown"
    return {
        "coaching_state.md": f"""# Interview Coaching State — {name}

Last updated: Not yet updated

## Current Truth
- Profile: {name}; target role: {target_role}
- Positioning spine: Unknown
- Conversion thesis: Insufficient evidence
- Primary bottleneck: Unknown
- Secondary bottleneck: None confirmed
- Calibration tendency: Unknown
- Target filters: {target_role}
- Live pipeline: None recorded
- Open corrections — do not relapse: None recorded

## Profile
- Target roles and level: {target_role}
- Location and work authorization, if volunteered and relevant: Unknown
- Timeline: {timeline}
- Background and strengths: Unknown
- Constraints: Unknown
- Career-transition context: Unknown

## Active Coaching Strategy
- Directness: {directness}
- Current focus: Establish evidence
- Next drill stage: Unknown
- Immediate recommendation: Start with the candidate's most time-sensitive need

## Coaching Preferences
- Helpful formats: Unknown
- Friction or anxiety patterns volunteered by candidate: None recorded
- Accessibility or pacing needs volunteered by candidate: None recorded

## State Files
- Storybank: coaching_state.storybank.md
- Loops and materials: coaching_state.loops.md
- Scores, outcomes, intelligence, and sessions: coaching_state.history.md
""",
        "coaching_state.storybank.md": """# Interview Coaching Storybank

## Story Index
| ID | Title | Competencies | Strength | Last used | Evidence status |
| --- | --- | --- | --- | --- | --- |

## Story Details

""",
        "coaching_state.loops.md": """# Interview Coaching Loops

## Active Loops

## Past Loops
| Company | Role | Outcome | Closed | Durable lesson |
| --- | --- | --- | --- | --- |

## Materials Index
| Company | Artifact | Path | Updated |
| --- | --- | --- | --- |
""",
        "coaching_state.history.md": """# Interview Coaching History

## Score History
| Date | Company/role | Format | Evidence | Substance | Structure | Relevance | Credibility | Differentiation | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Outcome Log
| Date | Company/role | Stage | Outcome | Evidence | Notes |
| --- | --- | --- | --- | --- | --- |

## Interview Intelligence
### Effective Patterns

### Ineffective Patterns

### Question Bank

### Company-Specific Evidence

## Feedback Log
| Date | Source | Provenance | Feedback | Interpretation | State changes |
| --- | --- | --- | --- | --- | --- |

## Session Log
| Date | Operations | Durable changes | Recommended next |
| --- | --- | --- | --- |

## Meta-Check Log
| Date | Candidate feedback | Coaching adjustment |
| --- | --- | --- |
""",
    }


def atomic_create(path: Path, content: str) -> bool:
    if path.exists():
        return False
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError:
            return False
        return True
    finally:
        temporary.unlink(missing_ok=True)


def init_workspace(args: argparse.Namespace) -> int:
    root = workspace_path(args.workspace)
    root.mkdir(parents=True, exist_ok=True)
    if root.is_symlink():
        raise ValueError("workspace path must not be a symbolic link")
    materials_path = root / "materials"
    if materials_path.is_symlink():
        raise ValueError(f"refusing to use symbolic-link materials directory: {materials_path}")
    materials_existed = materials_path.exists()
    materials_path.mkdir(exist_ok=True)

    created: list[str] = []
    preserved: list[str] = []
    for name, content in templates(args.name, args.target_role, args.timeline, args.directness).items():
        path = root / name
        if path.is_symlink():
            raise ValueError(f"refusing to write through symbolic link: {path}")
        if atomic_create(path, content):
            created.append(name)
        else:
            preserved.append(name)

    result = {
        "workspace": str(root),
        "created": created,
        "preserved": preserved,
        "materials": "present" if materials_existed else "created",
    }
    print(json.dumps(result, indent=2))
    return validate_workspace(root, quiet=True)


def validate_workspace(root: Path, quiet: bool = False) -> int:
    findings: list[Finding] = []
    contents: dict[str, str] = {}

    for name, headings in FILES.items():
        path = root / name
        if not path.is_file():
            findings.append(Finding("ERROR", name, "missing required state file"))
            continue
        if path.is_symlink():
            findings.append(Finding("ERROR", name, "state file must not be a symbolic link"))
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(Finding("ERROR", name, "file is not valid UTF-8"))
            continue
        contents[name] = text

        positions: list[int] = []
        for heading in headings:
            position = text.find(heading)
            if position < 0:
                findings.append(Finding("ERROR", name, f"missing heading {heading!r}"))
            positions.append(position)
        present_positions = [position for position in positions if position >= 0]
        if present_positions != sorted(present_positions):
            findings.append(Finding("ERROR", name, "required headings are out of order"))

        seen: set[str] = set()
        for heading in LEVEL_TWO_PATTERN.findall(text):
            normalized = heading.strip().lower()
            if normalized in seen:
                findings.append(Finding("ERROR", name, f"duplicate level-two heading {heading!r}"))
            seen.add(normalized)

    core = root / "coaching_state.md"
    if core.is_file() and core.stat().st_size > CORE_LIMIT_BYTES:
        findings.append(
            Finding(
                "ERROR",
                core.name,
                f"always-load core exceeds {CORE_LIMIT_BYTES} bytes; move detail to sibling files",
            )
        )

    story_text = contents.get("coaching_state.storybank.md", "")
    story_ids = STORY_ID_PATTERN.findall(story_text)
    duplicate_ids = sorted({story_id for story_id in story_ids if story_ids.count(story_id) > 1})
    for story_id in duplicate_ids:
        findings.append(Finding("ERROR", "coaching_state.storybank.md", f"duplicate story ID {story_id}"))

    materials = root / "materials"
    if not materials.is_dir():
        findings.append(Finding("ERROR", "materials", "missing materials directory"))
    elif materials.is_symlink():
        findings.append(Finding("ERROR", "materials", "materials directory must not be a symbolic link"))

    if findings:
        for finding in findings:
            print(finding.render())
        return 1
    if not quiet:
        print(f"OK {root}: coaching workspace is structurally valid")
    return 0


def count_table_rows(text: str, heading: str) -> int:
    start = text.find(heading)
    if start < 0:
        return 0
    remainder = text[start + len(heading) :]
    next_heading = remainder.find("\n## ")
    section = remainder if next_heading < 0 else remainder[:next_heading]
    rows = [line for line in section.splitlines() if line.startswith("|")]
    return max(0, len(rows) - 2)


def status_workspace(root: Path) -> int:
    if validate_workspace(root, quiet=True):
        return 1
    story = (root / "coaching_state.storybank.md").read_text(encoding="utf-8")
    loops = (root / "coaching_state.loops.md").read_text(encoding="utf-8")
    history = (root / "coaching_state.history.md").read_text(encoding="utf-8")
    active_section = loops.split("## Active Loops", 1)[1].split("\n## ", 1)[0]
    result = {
        "workspace": str(root),
        "stories": len(STORY_ID_PATTERN.findall(story)),
        "active_loops": len(re.findall(r"^###\s+.+", active_section, re.MULTILINE)),
        "score_rows": count_table_rows(history, "## Score History"),
        "outcome_rows": count_table_rows(history, "## Outcome Log"),
        "session_rows": count_table_rows(history, "## Session Log"),
    }
    print(json.dumps(result, indent=2))
    return 0


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def migration_destination(heading: str) -> str:
    if heading in CORE_SECTIONS:
        return "coaching_state.md"
    if heading in STORYBANK_SECTIONS:
        return "coaching_state.storybank.md"
    if heading in HISTORY_SECTIONS:
        return "coaching_state.history.md"
    if any(heading == prefix or heading.startswith(f"{prefix}:") for prefix in LOOP_SECTION_PREFIXES):
        return "coaching_state.loops.md"
    return "manual-review"


def migration_sections(text: str) -> tuple[str, list[tuple[str, str, int, int]]]:
    matches = list(LEVEL_TWO_PATTERN.finditer(text))
    preamble = text[: matches[0].start()] if matches else text
    sections: list[tuple[str, str, int, int]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append(
            (
                match.group(1).strip(),
                text[match.start() : end],
                len(text[: match.start()].encode("utf-8")),
                len(text[:end].encode("utf-8")),
            )
        )
    return preamble, sections


def build_migration_manifest(root: Path, source: Path) -> dict[str, object]:
    if not source.is_file():
        raise ValueError(f"missing legacy state file: {source}")
    if source.is_symlink():
        raise ValueError("legacy state file must not be a symbolic link")
    text = source.read_text(encoding="utf-8")
    preamble, parsed_sections = migration_sections(text)
    sections: list[dict[str, object]] = []
    headings: list[str] = []

    for heading, block, start_byte, end_byte in parsed_sections:
        headings.append(heading)
        sections.append(
            {
                "heading": heading,
                "destination": migration_destination(heading),
                "start_byte": start_byte,
                "end_byte": end_byte,
                "sha256": sha256_text(block),
                "story_ids": STORY_ID_PATTERN.findall(block),
            }
        )

    normalized = [heading.lower() for heading in headings]
    duplicates = sorted(
        {heading for heading in headings if normalized.count(heading.lower()) > 1},
        key=str.lower,
    )
    manual_review = [
        section["heading"] for section in sections if section["destination"] == "manual-review"
    ]
    siblings = [name for name in FILES if name != "coaching_state.md" and (root / name).exists()]
    return {
        "workspace": str(root),
        "source": source.name,
        "source_bytes": len(text.encode("utf-8")),
        "source_sha256": sha256_text(text),
        "preamble_sha256": sha256_text(preamble),
        "section_count": len(sections),
        "has_current_truth": "Current Truth" in headings,
        "duplicate_headings": duplicates,
        "manual_review": manual_review,
        "existing_sibling_files": siblings,
        "ready_for_lossless_split": bool(parsed_sections)
        and not duplicates
        and not manual_review
        and not siblings,
        "sections": sections,
    }


def migration_plan(root: Path) -> int:
    result = build_migration_manifest(root, root / "coaching_state.md")
    print(json.dumps(result, indent=2))
    return 0


def verify_migration(root: Path, backup_raw: str, expected_sha256: str) -> int:
    if not re.fullmatch(r"[0-9a-fA-F]{64}", expected_sha256):
        raise ValueError("expected source SHA-256 must contain exactly 64 hexadecimal characters")
    backup = Path(backup_raw).expanduser()
    if not backup.is_absolute():
        backup = root / backup
    backup = backup.resolve()
    try:
        backup.relative_to(root)
    except ValueError as exc:
        raise ValueError("backup must be inside the coaching workspace") from exc

    manifest = build_migration_manifest(root, backup)
    source_matches = manifest["source_sha256"] == expected_sha256.lower()
    backup_text = backup.read_text(encoding="utf-8")
    preamble, original_sections = migration_sections(backup_text)
    output_text: dict[str, str] = {}
    for name in FILES:
        path = root / name
        output_text[name] = path.read_text(encoding="utf-8") if path.is_file() else ""

    missing_sections: list[dict[str, str]] = []
    for heading, block, _start, _end in original_sections:
        destination = migration_destination(heading)
        if destination == "manual-review":
            candidates = output_text.values()
        elif heading == "Current Truth":
            candidates = (
                output_text["coaching_state.md"],
                output_text["coaching_state.history.md"],
            )
        else:
            candidates = (output_text.get(destination, ""),)
        if not any(block in candidate for candidate in candidates):
            missing_sections.append(
                {"heading": heading, "destination": destination, "sha256": sha256_text(block)}
            )

    original_story_ids = sorted(set(STORY_ID_PATTERN.findall(backup_text)))
    migrated_story_ids = set(STORY_ID_PATTERN.findall(output_text["coaching_state.storybank.md"]))
    missing_story_ids = [story_id for story_id in original_story_ids if story_id not in migrated_story_ids]
    preamble_preserved = preamble in output_text["coaching_state.md"]
    structurally_valid = validate_workspace(root, quiet=True) == 0
    verified = (
        source_matches
        and preamble_preserved
        and not missing_sections
        and not missing_story_ids
        and structurally_valid
    )
    result = {
        "workspace": str(root),
        "backup": str(backup),
        "expected_source_sha256": expected_sha256.lower(),
        "actual_backup_sha256": manifest["source_sha256"],
        "source_hash_matches": source_matches,
        "preamble_preserved": preamble_preserved,
        "original_section_count": manifest["section_count"],
        "missing_sections": missing_sections,
        "missing_story_ids": missing_story_ids,
        "structurally_valid": structurally_valid,
        "verified": verified,
    }
    print(json.dumps(result, indent=2))
    return 0 if verified else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="create missing workspace files without overwriting")
    init.add_argument("workspace")
    init.add_argument("--name", default="Candidate")
    init.add_argument("--target-role", default="Unknown")
    init.add_argument("--timeline", default="Unknown")
    init.add_argument("--directness", type=int, choices=range(1, 6), default=3)

    validate = subparsers.add_parser("validate", help="validate workspace structure")
    validate.add_argument("workspace")

    status = subparsers.add_parser("status", help="summarize workspace counts")
    status.add_argument("workspace")

    migration = subparsers.add_parser(
        "migration-plan", help="inventory and hash a legacy monolithic state file"
    )
    migration.add_argument("workspace")

    verification = subparsers.add_parser(
        "verify-migration", help="verify a split against its approved legacy backup"
    )
    verification.add_argument("workspace")
    verification.add_argument("--backup", required=True)
    verification.add_argument("--expected-source-sha256", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "init":
            return init_workspace(args)
        root = workspace_path(args.workspace)
        if args.command == "validate":
            return validate_workspace(root)
        if args.command == "status":
            return status_workspace(root)
        if args.command == "migration-plan":
            return migration_plan(root)
        if args.command == "verify-migration":
            return verify_migration(root, args.backup, args.expected_source_sha256)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
