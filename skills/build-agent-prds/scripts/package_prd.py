#!/usr/bin/env python3
"""Package a reviewed PRD delivery folder and verify its archived bytes."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path


IGNORED = {".DS_Store", "Thumbs.db", "Desktop.ini"}
FORBIDDEN = {"__pycache__", "node_modules", ".git", ".svn"}
TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def digest(stream) -> str:
    value = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        value.update(chunk)
    return value.hexdigest()


def delivery_files(source: Path) -> list[Path]:
    if source.is_symlink() or not source.is_dir():
        raise ValueError("Input must be an ordinary delivery directory, not a symlink")
    if not (source/"PRD.md").is_file():
        raise ValueError("Delivery directory must contain PRD.md")
    files = []

    def visit(directory: Path) -> None:
        for path in sorted(directory.iterdir()):
            if path.is_symlink():
                raise ValueError(f"Stage a reviewed ordinary file instead of symlink: {path}")
            if path.name in IGNORED and path.is_file():
                continue
            if (path.name.startswith(".") or path.name in FORBIDDEN
                    or path.suffix in {".pyc", ".pyo"}):
                raise ValueError(f"Remove non-delivery material from staging: {path}")
            if "\\" in path.name or any(ord(char) < 32 for char in path.name):
                raise ValueError(f"Use portable filenames: {path}")
            if path.is_dir():
                visit(path)
            elif path.is_file():
                files.append(path)
            else:
                raise ValueError(f"Only ordinary files can be packaged: {path}")

    visit(source)
    return files


def package(source: Path, output: Path) -> dict:
    # Inspect the supplied path before resolution so a symlink root is rejected.
    files = delivery_files(source)
    source = source.resolve()
    files = [path.resolve() for path in files]
    output = output.absolute()
    if output.resolve().is_relative_to(source):
        raise ValueError("Output ZIP must be outside the input directory")
    if output.suffix.lower() != ".zip":
        raise ValueError("Output must have a .zip suffix")
    if output.exists() or output.is_symlink():
        raise ValueError("Output already exists; choose a new versioned filename")
    if (source.name.startswith(".") or "\\" in source.name
            or any(ord(char) < 32 for char in source.name)):
        raise ValueError("Use a portable, non-hidden delivery directory name")

    inventory = {}
    output.parent.mkdir(parents=True, exist_ok=True)
    # Build and verify privately before creating the final downloadable path.
    with tempfile.TemporaryDirectory(prefix="prd-package-") as staging:
        candidate = Path(staging)/"delivery.zip"
        with zipfile.ZipFile(candidate, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                name = f"{source.name}/{path.relative_to(source).as_posix()}"
                info = zipfile.ZipInfo(name, TIMESTAMP)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                with path.open("rb") as original, archive.open(info, "w", force_zip64=True) as target:
                    shutil.copyfileobj(original, target)
                with path.open("rb") as original:
                    inventory[name] = digest(original)
        with zipfile.ZipFile(candidate) as archive:
            if archive.testzip() is not None or set(archive.namelist()) != set(inventory):
                raise ValueError("Archive integrity or inventory check failed")
            for name, expected in inventory.items():
                with archive.open(name) as archived:
                    if digest(archived) != expected:
                        raise ValueError(f"Source changed during packaging: {name}")
        # Exclusive creation protects an existing destination even after checks.
        final = output.open("xb")
        try:
            with final, candidate.open("rb") as archived:
                shutil.copyfileobj(archived, final)
        except BaseException:
            output.unlink(missing_ok=True)
            raise
    with output.open("rb") as archived:
        archive_hash = digest(archived)
    return {"archive": str(output), "entry_point": f"{source.name}/PRD.md",
            "files": len(inventory), "sha256": archive_hash}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(package(args.source, args.output), indent=2))
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        parser.exit(1, f"ERROR: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
