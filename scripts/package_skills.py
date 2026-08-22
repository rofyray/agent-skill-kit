#!/usr/bin/env python3
"""Create deterministic, upload-ready ZIP archives for desktop skill clients."""

from __future__ import annotations

import argparse
import stat
import sys
import zipfile
from pathlib import Path


PACKAGE_ENTRIES = {"SKILL.md", "agents", "scripts", "references", "assets"}
IGNORED_DIRECTORY_NAMES = {"__pycache__"}
IGNORED_FILE_SUFFIXES = {".pyc", ".pyo"}
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def package_files(skill_dir: Path) -> list[Path]:
    files: list[Path] = []
    for entry in sorted(skill_dir.iterdir(), key=lambda path: path.name):
        if entry.name.startswith(".") or entry.name not in PACKAGE_ENTRIES:
            continue
        if entry.is_file():
            files.append(entry)
            continue
        files.extend(
            path
            for path in sorted(entry.rglob("*"))
            if path.is_file()
            and not any(
                part.startswith(".") or part in IGNORED_DIRECTORY_NAMES
                for part in path.relative_to(skill_dir).parts
            )
            and path.suffix not in IGNORED_FILE_SUFFIXES
        )
    return files


def package_skill(skill_dir: Path, output_dir: Path) -> Path:
    if not (skill_dir/"SKILL.md").is_file():
        raise ValueError(f"{skill_dir} does not contain SKILL.md")

    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir/f"{skill_dir.name}.zip"

    with zipfile.ZipFile(archive_path, "w") as archive:
        for path in package_files(skill_dir):
            relative = path.relative_to(skill_dir)
            info = zipfile.ZipInfo(f"{skill_dir.name}/{relative.as_posix()}", ZIP_TIMESTAMP)
            mode = stat.S_IMODE(path.stat().st_mode)
            info.external_attr = (mode or 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())

    return archive_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--skill", action="append", dest="skills", metavar="NAME")
    args = parser.parse_args()

    root = args.root.resolve()
    skills_dir = root/"skills"
    output_dir = (args.output_dir or root/"dist"/"skills").resolve()
    selected = args.skills or sorted(
        path.name for path in skills_dir.iterdir() if path.is_dir() and not path.name.startswith(".")
    )

    try:
        for name in selected:
            skill_dir = skills_dir/name
            if not skill_dir.is_dir():
                raise ValueError(f"unknown skill: {name}")
            archive_path = package_skill(skill_dir, output_dir)
            print(archive_path.relative_to(root) if archive_path.is_relative_to(root) else archive_path)
    except (OSError, ValueError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
