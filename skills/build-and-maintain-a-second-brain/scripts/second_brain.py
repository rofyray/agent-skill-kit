#!/usr/bin/env python3
"""Initialize and structurally inspect a source-grounded second-brain vault."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR.parent / "assets" / "vault-template"
MANIFEST_VERSION = 1
REQUIRED_ROOT_FILES = (
    "SECOND_BRAIN.md",
    "AGENTS.md",
    "CLAUDE.md",
    "index.md",
    "log.md",
    ".second-brain/config.json",
    ".second-brain/raw-manifest.json",
    ".cursor/rules/second-brain.mdc",
)
REQUIRED_PAGE_FIELDS = ("title", "summary", "type", "created", "updated", "status", "sources")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


class VaultError(RuntimeError):
    """Raised for a user-actionable vault error."""


def vault_path(value: str) -> Path:
    return Path(value).expanduser().resolve()


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = path.stat().st_mode if path.exists() else 0o644
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def render_template(path: Path, replacements: dict[str, str]) -> str:
    content = path.read_text(encoding="utf-8")
    for marker, value in replacements.items():
        content = content.replace("{{" + marker + "}}", value)
    unresolved = sorted(set(re.findall(r"\{\{([A-Z_]+)\}\}", content)))
    if unresolved:
        raise VaultError(f"unresolved template markers in {path.name}: {', '.join(unresolved)}")
    return content


def create_or_preserve(path: Path, content: str, appendable: bool = False) -> str:
    if not path.exists():
        atomic_write(path, content)
        return "created"
    if not path.is_file():
        return "conflict"
    if appendable or path.read_text(encoding="utf-8") == content:
        return "preserved"
    return "conflict"


def init_vault(args: argparse.Namespace) -> int:
    root = vault_path(args.vault)
    if root.exists() and not root.is_dir():
        raise VaultError(f"vault path is not a directory: {root}")
    root.mkdir(parents=True, exist_ok=True)

    directories = (
        "raw/assets",
        "wiki",
        "reports/lint",
        "reports/reviews",
        "automation",
        ".second-brain",
        ".cursor/rules",
    )
    for relative in directories:
        destination = root / relative
        if destination.exists() and not destination.is_dir():
            raise VaultError(f"required directory path is occupied by a file: {destination}")
        destination.mkdir(parents=True, exist_ok=True)

    existing_config: dict[str, Any] = {}
    config_path = root / ".second-brain/config.json"
    if config_path.is_file():
        try:
            loaded = json.loads(config_path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                existing_config = loaded
        except (OSError, json.JSONDecodeError):
            pass

    selected_name = args.name or str(existing_config.get("name") or root.name)
    selected_scope = args.scope or str(existing_config.get("knowledge_scope") or "General personal knowledge")
    selected_voice = args.voice or str(
        existing_config.get("writing_voice") or "Clear, concise, and faithful to the user's terminology"
    )
    selected_review_mode = args.review_mode or str(existing_config.get("review_mode") or "review-after")
    created_date = str(existing_config.get("created") or date.today().isoformat())
    replacements = {
        "VAULT_NAME": selected_name,
        "KNOWLEDGE_SCOPE": selected_scope,
        "WRITING_VOICE": selected_voice,
        "REVIEW_MODE": selected_review_mode,
        "CREATED_DATE": created_date,
    }
    template_map = {
        "SECOND_BRAIN.md": "SECOND_BRAIN.md",
        "AGENTS.md": "AGENTS.md",
        "CLAUDE.md": "CLAUDE.md",
        "CURSOR_RULE.mdc": ".cursor/rules/second-brain.mdc",
        "index.md": "index.md",
        "log.md": "log.md",
        "automation/lint-wiki.md": "automation/lint-wiki.md",
        "automation/weekly-review.md": "automation/weekly-review.md",
    }

    outcomes: dict[str, str] = {}
    for source_name, destination_name in template_map.items():
        source = TEMPLATE_DIR / source_name
        destination = root / destination_name
        outcomes[destination_name] = create_or_preserve(
            destination,
            render_template(source, replacements),
            appendable=destination_name in {"index.md", "log.md"},
        )

    helper_destination = root / "automation/second_brain.py"
    outcomes["automation/second_brain.py"] = create_or_preserve(
        helper_destination,
        Path(__file__).read_text(encoding="utf-8"),
    )
    if outcomes["automation/second_brain.py"] == "created":
        helper_destination.chmod(0o755)

    config = {
        "version": 1,
        "name": replacements["VAULT_NAME"],
        "knowledge_scope": selected_scope,
        "writing_voice": selected_voice,
        "review_mode": selected_review_mode,
        "created": replacements["CREATED_DATE"],
    }
    outcomes[".second-brain/config.json"] = create_or_preserve(
        root / ".second-brain/config.json",
        json.dumps(config, indent=2, sort_keys=True) + "\n",
    )
    empty_manifest = {"version": MANIFEST_VERSION, "algorithm": "sha256", "files": {}}
    outcomes[".second-brain/raw-manifest.json"] = create_or_preserve(
        root / ".second-brain/raw-manifest.json",
        json.dumps(empty_manifest, indent=2, sort_keys=True) + "\n",
        appendable=True,
    )

    if outcomes.get("log.md") == "created":
        log_path = root / "log.md"
        with log_path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(
                f"\n## [{date.today().isoformat()}] setup | {replacements['VAULT_NAME']}\n\n"
                "- Created the second-brain vault contract and host adapters.\n"
                f"- Review mode: `{selected_review_mode}`\n"
            )

    report = {
        "vault": str(root),
        "created": sorted(path for path, result in outcomes.items() if result == "created"),
        "preserved": sorted(path for path, result in outcomes.items() if result == "preserved"),
        "conflicts": sorted(path for path, result in outcomes.items() if result == "conflict"),
    }
    print_report(report, args.json)
    return 2 if report["conflicts"] else 0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def raw_files(root: Path) -> tuple[list[Path], list[str]]:
    raw = root / "raw"
    if not raw.is_dir():
        return [], []
    files: list[Path] = []
    symlinks: list[str] = []
    for path in sorted(raw.rglob("*")):
        if any(part.startswith(".") for part in path.relative_to(raw).parts):
            continue
        if path.is_symlink():
            symlinks.append(path.relative_to(root).as_posix())
        elif path.is_file():
            files.append(path)
    return files, symlinks


def load_manifest(root: Path) -> dict[str, Any]:
    path = root / ".second-brain/raw-manifest.json"
    if not path.is_file():
        return {"version": MANIFEST_VERSION, "algorithm": "sha256", "files": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise VaultError(f"invalid raw manifest: {exc}") from exc
    if data.get("version") != MANIFEST_VERSION or data.get("algorithm") != "sha256":
        raise VaultError("unsupported raw manifest version or algorithm")
    if not isinstance(data.get("files"), dict):
        raise VaultError("raw manifest files must be an object")
    return data


def raw_integrity(root: Path, manifest: dict[str, Any]) -> dict[str, list[str]]:
    files, symlinks = raw_files(root)
    current = {path.relative_to(root).as_posix(): sha256(path) for path in files}
    recorded = manifest["files"]
    return {
        "modified": sorted(path for path, digest in current.items() if path in recorded and recorded[path] != digest),
        "unrecorded": sorted(path for path in current if path not in recorded),
        "missing": sorted(path for path in recorded if path not in current),
        "symlinks": symlinks,
    }


def record_raw(args: argparse.Namespace) -> int:
    root = vault_path(args.vault)
    require_vault(root)
    manifest = load_manifest(root)
    integrity = raw_integrity(root, manifest)
    if integrity["modified"] or integrity["missing"] or integrity["symlinks"]:
        print_report({"vault": str(root), **integrity, "recorded": []}, args.json)
        return 2

    files, _ = raw_files(root)
    current = {path.relative_to(root).as_posix(): sha256(path) for path in files}
    if args.all_new:
        selected_paths = set(current)
    else:
        selected_paths: set[str] = set()
        raw_root = (root / "raw").resolve()
        for supplied in args.sources:
            candidate = Path(supplied).expanduser()
            if not candidate.is_absolute():
                candidate = root / candidate
            if candidate.is_symlink():
                raise VaultError(f"raw source symlinks are not supported: {candidate}")
            resolved = candidate.resolve(strict=True)
            try:
                resolved.relative_to(raw_root)
            except ValueError as exc:
                raise VaultError(f"raw source is outside the vault's raw directory: {candidate}") from exc
            if not resolved.is_file():
                raise VaultError(f"raw source is not a file: {candidate}")
            selected_paths.add(resolved.relative_to(root).as_posix())
    new_paths = sorted(path for path in selected_paths if path in current and path not in manifest["files"])
    for path in new_paths:
        manifest["files"][path] = current[path]
    if new_paths:
        atomic_write(
            root / ".second-brain/raw-manifest.json",
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        )
        integrity = raw_integrity(root, manifest)
    print_report({"vault": str(root), **integrity, "recorded": new_paths}, args.json)
    return 0


def require_vault(root: Path) -> None:
    if not root.is_dir():
        raise VaultError(f"vault directory does not exist: {root}")


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return {}
    fields: dict[str, str] = {}
    for raw in lines[1:end]:
        if not raw or raw[:1].isspace() or ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        fields[key.strip()] = value.strip().strip("'\"")
    return fields


def wikilink_target(value: str) -> str:
    target = value.split("|", 1)[0].split("#", 1)[0].strip().replace("\\", "/")
    if target.lower().endswith(".md"):
        target = target[:-3]
    if target.startswith("wiki/"):
        target = target[5:]
    return target.strip("/").casefold()


def build_page_maps(pages: list[Path], wiki: Path) -> tuple[dict[str, Path], dict[str, list[Path]]]:
    by_relative: dict[str, Path] = {}
    by_name: dict[str, list[Path]] = defaultdict(list)
    for page in pages:
        relative = page.relative_to(wiki).with_suffix("").as_posix().casefold()
        by_relative[relative] = page
        by_name[page.stem.casefold()].append(page)
    return by_relative, by_name


def resolve_link(target: str, by_relative: dict[str, Path], by_name: dict[str, list[Path]]) -> list[Path]:
    normalized = wikilink_target(target)
    if not normalized:
        return []
    if normalized in by_relative:
        return [by_relative[normalized]]
    return by_name.get(Path(normalized).name, [])


def scan_vault(args: argparse.Namespace) -> int:
    root = vault_path(args.vault)
    require_vault(root)
    missing_root = [relative for relative in REQUIRED_ROOT_FILES if not (root / relative).is_file()]

    try:
        manifest = load_manifest(root)
        integrity = raw_integrity(root, manifest)
    except VaultError as exc:
        manifest = {"files": {}}
        integrity = {"modified": [], "unrecorded": [], "missing": [], "symlinks": []}
        missing_root.append(f"invalid manifest: {exc}")

    wiki = root / "wiki"
    pages = sorted(path for path in wiki.rglob("*.md") if path.is_file() and not path.is_symlink()) if wiki.is_dir() else []
    by_relative, by_name = build_page_maps(pages, wiki) if wiki.is_dir() else ({}, {})
    page_labels = {page: page.relative_to(root).as_posix() for page in pages}

    missing_fields: dict[str, list[str]] = {}
    weak_provenance: list[str] = []
    broken_links: list[str] = []
    ambiguous_links: list[str] = []
    inbound: Counter[Path] = Counter()
    identities: dict[str, list[str]] = defaultdict(list)

    for page in pages:
        text = page.read_text(encoding="utf-8", errors="replace")
        fields = parse_frontmatter(text)
        absent = [field for field in REQUIRED_PAGE_FIELDS if field not in fields]
        if absent:
            missing_fields[page_labels[page]] = absent
        if "raw/" not in text:
            weak_provenance.append(page_labels[page])
        identity = fields.get("title", page.stem).strip().casefold()
        identities[identity].append(page_labels[page])
        for raw_target in WIKILINK_RE.findall(text):
            matches = resolve_link(raw_target, by_relative, by_name)
            if not matches:
                broken_links.append(f"{page_labels[page]} -> [[{raw_target}]]")
            elif len(matches) > 1:
                ambiguous_links.append(f"{page_labels[page]} -> [[{raw_target}]]")
            else:
                inbound[matches[0]] += 1

    duplicates = {identity: paths for identity, paths in identities.items() if len(paths) > 1}
    orphans = sorted(page_labels[page] for page in pages if inbound[page] == 0)

    indexed_pages: set[Path] = set()
    bad_index_links: list[str] = []
    index_path = root / "index.md"
    if index_path.is_file():
        for raw_target in WIKILINK_RE.findall(index_path.read_text(encoding="utf-8", errors="replace")):
            matches = resolve_link(raw_target, by_relative, by_name)
            if len(matches) == 1:
                indexed_pages.add(matches[0])
            else:
                bad_index_links.append(f"[[{raw_target}]]")
    unindexed = sorted(page_labels[page] for page in pages if page not in indexed_pages)

    report: dict[str, Any] = {
        "vault": str(root),
        "counts": {
            "raw_recorded": len(manifest.get("files", {})),
            "wiki_pages": len(pages),
            "wikilinks": sum(inbound.values()),
        },
        "missing_required_files": sorted(set(missing_root)),
        "raw_integrity": integrity,
        "pages_missing_fields": missing_fields,
        "pages_without_raw_provenance": sorted(weak_provenance),
        "broken_wikilinks": sorted(set(broken_links)),
        "ambiguous_wikilinks": sorted(set(ambiguous_links)),
        "orphan_pages": orphans,
        "unindexed_pages": unindexed,
        "invalid_index_links": sorted(set(bad_index_links)),
        "duplicate_page_identities": duplicates,
    }
    print_report(report, args.json)

    has_findings = any(
        (
            report["missing_required_files"],
            *integrity.values(),
            missing_fields,
            weak_provenance,
            broken_links,
            ambiguous_links,
            orphans,
            unindexed,
            bad_index_links,
            duplicates,
        )
    )
    return 1 if args.strict and has_findings else 0


def print_report(report: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return
    print(f"Vault: {report.get('vault', '')}")
    for key, value in report.items():
        if key == "vault":
            continue
        label = key.replace("_", " ").capitalize()
        if isinstance(value, dict):
            print(f"{label}:")
            if not value:
                print("  none")
            for nested_key, nested_value in value.items():
                if isinstance(nested_value, list):
                    rendered = ", ".join(nested_value) if nested_value else "none"
                else:
                    rendered = str(nested_value)
                print(f"  {nested_key}: {rendered}")
        elif isinstance(value, list):
            print(f"{label}: {', '.join(value) if value else 'none'}")
        else:
            print(f"{label}: {value}")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    subparsers = root.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="create an idempotent vault skeleton")
    init.add_argument("vault")
    init.add_argument("--name")
    init.add_argument("--scope")
    init.add_argument("--voice")
    init.add_argument("--review-mode", choices=("review-after", "proposal-first"))
    init.add_argument("--json", action="store_true")
    init.set_defaults(handler=init_vault)

    record = subparsers.add_parser("record-raw", help="record hashes for new immutable raw sources")
    record.add_argument("vault")
    record.add_argument("sources", nargs="*", help="specific source paths under the vault's raw directory")
    record.add_argument("--all-new", action="store_true", help="record every new raw source in an approved batch")
    record.add_argument("--json", action="store_true")
    record.set_defaults(handler=record_raw)

    scan = subparsers.add_parser("scan", help="scan vault structure, links, provenance, and raw integrity")
    scan.add_argument("vault")
    scan.add_argument("--json", action="store_true")
    scan.add_argument("--strict", action="store_true", help="exit 1 when any finding is present")
    scan.set_defaults(handler=scan_vault)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "record-raw" and not args.sources and not args.all_new:
            raise VaultError("record-raw requires at least one source path or --all-new")
        if args.command == "record-raw" and args.sources and args.all_new:
            raise VaultError("choose specific source paths or --all-new, not both")
        return args.handler(args)
    except (OSError, VaultError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
