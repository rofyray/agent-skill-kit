#!/usr/bin/env python3
"""Validate the catalog's Codex, Claude, Cursor, ChatGPT, and Cowork contract."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PORTABLE_FIELDS = {"name", "description"}
KNOWN_ENTRIES = {"SKILL.md", "agents", "scripts", "references", "assets"}
MAX_DESCRIPTION_LENGTH = 200
REQUIRED_OPENAI_INTERFACE_FIELDS = {
    "display_name",
    "short_description",
    "default_prompt",
}
MENTION_PATTERN = re.compile(r"(?:\$|@)[a-z0-9][a-z0-9-]*", re.IGNORECASE)
HELP_REFERENCE = "references/help.md"
REQUIRED_HELP_HEADINGS = (
    "## What this skill does",
    "## Modes",
    "## Start here",
    "## Examples",
)


@dataclass(frozen=True)
class Issue:
    path: Path
    message: str

    def render(self, root: Path) -> str:
        try:
            location = self.path.relative_to(root)
        except ValueError:
            location = self.path
        return f"{location}: {self.message}"


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[Issue], str]:
    issues: list[Issue] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, [Issue(path, "SKILL.md must start with YAML frontmatter")], text

    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return {}, [Issue(path, "frontmatter is missing its closing --- delimiter")], text

    fields: dict[str, str] = {}
    for line_number, raw_line in enumerate(lines[1:end], start=2):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            issues.append(Issue(path, f"frontmatter line {line_number} is not a key-value pair"))
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if not key or raw_line[:1].isspace():
            issues.append(Issue(path, f"frontmatter line {line_number} must be a top-level scalar field"))
            continue
        if key in fields:
            issues.append(Issue(path, f"frontmatter field {key!r} is duplicated"))
            continue
        fields[key] = _unquote(value)

    body = "\n".join(lines[end + 1 :]).strip()
    return fields, issues, body


def parse_openai_interface(path: Path) -> tuple[dict[str, str], list[Issue]]:
    issues: list[Issue] = []
    fields: dict[str, str] = {}
    in_interface = False

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if raw_line == "interface:":
            in_interface = True
            continue
        if in_interface and raw_line and not raw_line.startswith(" "):
            break
        if not in_interface or not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        match = re.fullmatch(r'  ([a-z_]+):\s*"(.*)"', raw_line)
        if not match:
            issues.append(
                Issue(path, f"interface line {line_number} must be a two-space-indented quoted scalar")
            )
            continue
        key, value = match.groups()
        fields[key] = value

    return fields, issues


def validate_openai_metadata(skill_dir: Path) -> list[Issue]:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.is_file():
        return [Issue(path, "missing agents/openai.yaml required for ChatGPT and Codex presentation")]

    fields, issues = parse_openai_interface(path)
    missing = sorted(REQUIRED_OPENAI_INTERFACE_FIELDS - set(fields))
    if missing:
        issues.append(Issue(path, "missing interface field(s): " + ", ".join(missing)))

    short_description = fields.get("short_description", "")
    if short_description and not 25 <= len(short_description) <= 64:
        issues.append(Issue(path, "short_description must contain 25–64 characters"))

    default_prompt = fields.get("default_prompt", "")
    if default_prompt and MENTION_PATTERN.search(default_prompt):
        issues.append(
            Issue(
                path,
                "default_prompt must be invocation-neutral; README documents @, $, and client pickers",
            )
        )

    return issues


def validate_eval(root: Path, skill_dir: Path) -> list[Issue]:
    path = root / "evals" / skill_dir.name / "cases.json"
    if not path.is_file():
        return [Issue(path, "missing evaluation cases for this skill")]

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [Issue(path, f"invalid evaluation JSON: {exc}")]

    issues: list[Issue] = []
    if data.get("skill") != skill_dir.name:
        issues.append(Issue(path, "evaluation skill must match the skill directory name"))

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        issues.append(Issue(path, "evaluation cases must be a non-empty list"))
        return issues

    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict) or not isinstance(case.get("request"), str):
            issues.append(Issue(path, f"case {index} must contain a string request"))
        if not isinstance(case, dict) or not isinstance(case.get("expect"), list) or not case["expect"]:
            issues.append(Issue(path, f"case {index} must contain non-empty expectations"))

    help_cases = [case for case in cases if isinstance(case, dict) and case.get("mode") == "help"]
    if not help_cases:
        issues.append(Issue(path, "evaluation cases must include one case with mode 'help'"))
    elif not any(case.get("request", "").strip().lower() == "help" for case in help_cases):
        issues.append(Issue(path, "help-mode evaluation must include the bare request 'help'"))

    return issues


def validate_help_mode(skill_dir: Path, body: str) -> list[Issue]:
    path = skill_dir / HELP_REFERENCE
    issues: list[Issue] = []
    if not path.is_file():
        return [Issue(path, "missing references/help.md required for portable help mode")]

    text = path.read_text(encoding="utf-8")
    positions: list[int] = []
    for heading in REQUIRED_HELP_HEADINGS:
        position = text.find(heading)
        if position < 0:
            issues.append(Issue(path, f"missing required help heading {heading!r}"))
        positions.append(position)
    present_positions = [position for position in positions if position >= 0]
    if present_positions != sorted(present_positions):
        issues.append(Issue(path, "required help headings are out of order"))

    if HELP_REFERENCE not in body:
        issues.append(Issue(skill_dir / "SKILL.md", "SKILL.md must route help mode to references/help.md"))
    return issues


def validate_skill(skill_dir: Path) -> list[Issue]:
    issues: list[Issue] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [Issue(skill_dir, "each direct child of skills/ must contain SKILL.md")]

    fields, parse_issues, body = parse_frontmatter(skill_file)
    issues.extend(parse_issues)

    unknown_fields = sorted(set(fields) - PORTABLE_FIELDS)
    if unknown_fields:
        issues.append(
            Issue(
                skill_file,
                "portable frontmatter may contain only name and description; found "
                + ", ".join(unknown_fields),
            )
        )

    missing_fields = sorted(PORTABLE_FIELDS - set(fields))
    if missing_fields:
        issues.append(Issue(skill_file, "missing required field(s): " + ", ".join(missing_fields)))

    name = fields.get("name", "")
    if name:
        if len(name) > 64:
            issues.append(Issue(skill_file, "name must be at most 64 characters"))
        if not NAME_PATTERN.fullmatch(name):
            issues.append(Issue(skill_file, "name must use lowercase letters, digits, and single hyphens"))
        if name != skill_dir.name:
            issues.append(Issue(skill_file, f"name {name!r} must match directory {skill_dir.name!r}"))

    description = fields.get("description", "")
    if description:
        if len(description) > MAX_DESCRIPTION_LENGTH:
            issues.append(
                Issue(
                    skill_file,
                    f"description must be at most {MAX_DESCRIPTION_LENGTH} characters for Claude Desktop",
                )
            )
        lowered = description.lower()
        if "use when" not in lowered:
            issues.append(Issue(skill_file, "description must state its trigger boundary with 'Use when'"))

    if not body:
        issues.append(Issue(skill_file, "instruction body must not be empty"))

    line_count = len(skill_file.read_text(encoding="utf-8").splitlines())
    if line_count > 500:
        issues.append(Issue(skill_file, f"SKILL.md has {line_count} lines; maximum is 500"))

    for entry in skill_dir.iterdir():
        if entry.name.startswith("."):
            continue
        if entry.name not in KNOWN_ENTRIES:
            issues.append(Issue(entry, "unexpected installable-skill entry; keep development artifacts at repo root"))
        if entry.is_dir() and not any(entry.iterdir()):
            issues.append(Issue(entry, "remove empty optional directories"))

    issues.extend(validate_openai_metadata(skill_dir))
    issues.extend(validate_help_mode(skill_dir, body))

    return issues


def validate_root(root: Path) -> list[Issue]:
    root = root.resolve()
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return [Issue(skills_dir, "missing skills directory")]

    issues: list[Issue] = []
    direct_skill_dirs = sorted(
        path for path in skills_dir.iterdir() if path.is_dir() and not path.name.startswith(".")
    )
    readme_path = root / "README.md"
    readme = readme_path.read_text(encoding="utf-8") if readme_path.is_file() else ""
    for skill_dir in direct_skill_dirs:
        issues.extend(validate_skill(skill_dir))
        issues.extend(validate_eval(root, skill_dir))
        if f"(skills/{skill_dir.name}/)" not in readme:
            issues.append(Issue(readme_path, f"missing skill directory entry for {skill_dir.name}"))

    direct_files = [
        path for path in skills_dir.iterdir() if path.is_file() and not path.name.startswith(".")
    ]
    for path in direct_files:
        issues.append(Issue(path, "skills/ may contain only skill directories"))

    nested_skill_files = {
        path.resolve()
        for path in skills_dir.rglob("SKILL.md")
        if path.parent.parent.resolve() != skills_dir.resolve()
    }
    for path in sorted(nested_skill_files):
        issues.append(Issue(path, "skills must be direct children of skills/; do not add category nesting"))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the parent of scripts/)",
    )
    args = parser.parse_args()

    issues = validate_root(args.root)
    if issues:
        for issue in issues:
            print(f"ERROR {issue.render(args.root.resolve())}", file=sys.stderr)
        print(f"Validation failed with {len(issues)} issue(s).", file=sys.stderr)
        return 1

    skill_count = sum(
        1
        for path in (args.root / "skills").iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )
    print(f"Validated {skill_count} skill(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
