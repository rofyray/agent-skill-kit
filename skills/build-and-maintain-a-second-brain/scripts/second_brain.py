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
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any
from urllib.parse import parse_qsl, urlsplit


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR.parent / "assets" / "vault-template"
MANIFEST_VERSION = 1
REQUIRED_ROOT_FILES = (
    "SECOND_BRAIN.md",
    "AGENTS.md",
    "CLAUDE.md",
    "index.md",
    "log.md",
    "automation/lint-wiki.md",
    "automation/recurring-ingest.md",
    "automation/second_brain.py",
    "automation/weekly-review.md",
    ".second-brain/config.json",
    ".second-brain/ingest-schedules.json",
    ".second-brain/raw-manifest.json",
    ".cursor/rules/second-brain.mdc",
)
REQUIRED_PAGE_FIELDS = ("title", "summary", "type", "created", "updated", "status", "sources")
DEFAULT_PAGE_TYPES = ("concept", "entity", "source-summary", "comparison", "analysis", "question")
ALLOWED_STATUSES = ("current", "provisional", "contested", "superseded")
INGEST_SOURCE_KINDS = ("conversation", "url", "file", "connected-document", "directory")
INGEST_SOURCE_FIELDS = {
    "id",
    "kind",
    "locator",
    "cadence",
    "timezone",
    "enabled",
    "max_items_per_run",
    "max_bytes_per_run",
    "normalization",
    "checkpoint",
}
SENSITIVE_FIELD_RE = re.compile(
    r"(?:^|[_-])(?:access[_-]?token|api[_-]?key|authorization|cookie|credential|password|secret|signature|token)(?:$|[_-])",
    re.IGNORECASE,
)
SENSITIVE_QUERY_FIELDS = {
    "access_token",
    "api_key",
    "apikey",
    "auth",
    "authorization",
    "client_secret",
    "code",
    "id_token",
    "key",
    "password",
    "refresh_token",
    "secret",
    "sig",
    "signature",
    "token",
    "x-amz-credential",
    "x-amz-security-token",
    "x-amz-signature",
}
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
FENCED_CODE_RE = re.compile(r"(?:```|~~~).*?(?:```|~~~)", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


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


def normalize_domains(domains: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for raw in domains:
        value = " ".join(raw.split()).strip()
        key = value.casefold()
        if value and key not in seen:
            seen.add(key)
            normalized.append(value)
    return normalized


def index_sections(domains: list[str]) -> str:
    normalized = normalize_domains(domains)
    if normalized:
        headings = [*(f"## {domain}" for domain in normalized), "## Cross-domain syntheses", "## Open questions"]
    else:
        headings = [
            "## Concepts",
            "## Entities",
            "## Source summaries",
            "## Comparisons and analyses",
            "## Open questions",
        ]
    return "\n\n".join(headings)


def knowledge_text(text: str) -> str:
    return INLINE_CODE_RE.sub("", FENCED_CODE_RE.sub("", text))


def init_vault(args: argparse.Namespace) -> int:
    root = vault_path(args.vault)
    if root.exists() and not root.is_dir():
        raise VaultError(f"vault path is not a directory: {root}")
    root.mkdir(parents=True, exist_ok=True)

    directories = (
        "raw/assets",
        "raw/scheduled",
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
    existing_domains = existing_config.get("domains")
    selected_domains = normalize_domains(
        args.domain
        or ([str(value) for value in existing_domains if str(value).strip()] if isinstance(existing_domains, list) else [])
    )
    created_date = str(existing_config.get("created") or date.today().isoformat())
    replacements = {
        "VAULT_NAME": selected_name,
        "KNOWLEDGE_SCOPE": selected_scope,
        "WRITING_VOICE": selected_voice,
        "REVIEW_MODE": selected_review_mode,
        "CREATED_DATE": created_date,
        "INDEX_SECTIONS": index_sections(selected_domains),
        "DOMAINS": ", ".join(selected_domains) if selected_domains else "General catalog",
    }
    template_map = {
        "SECOND_BRAIN.md": "SECOND_BRAIN.md",
        "AGENTS.md": "AGENTS.md",
        "CLAUDE.md": "CLAUDE.md",
        "CURSOR_RULE.mdc": ".cursor/rules/second-brain.mdc",
        "index.md": "index.md",
        "log.md": "log.md",
        "automation/lint-wiki.md": "automation/lint-wiki.md",
        "automation/recurring-ingest.md": "automation/recurring-ingest.md",
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
        "domains": selected_domains,
        "allowed_types": list(DEFAULT_PAGE_TYPES),
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
    empty_ingest_schedules = {"version": 1, "sources": []}
    outcomes[".second-brain/ingest-schedules.json"] = create_or_preserve(
        root / ".second-brain/ingest-schedules.json",
        json.dumps(empty_ingest_schedules, indent=2, sort_keys=True) + "\n",
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


def parse_frontmatter(text: str) -> tuple[dict[str, Any], list[str]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, ["missing opening --- delimiter"]
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return {}, ["missing closing --- delimiter"]
    fields: dict[str, Any] = {}
    issues: list[str] = []
    current_list: str | None = None
    for line_number, raw in enumerate(lines[1:end], start=2):
        stripped = raw.strip()
        if not stripped:
            continue
        if "\t" in raw:
            issues.append(f"line {line_number}: tabs are not allowed")
            continue
        if raw[:1].isspace():
            if not raw.startswith("  - ") or raw.startswith("   ") or not current_list:
                issues.append(f"line {line_number}: expected a two-space-indented list item")
                continue
            item = raw[4:].strip()
            if not item:
                issues.append(f"line {line_number}: list item cannot be empty")
                continue
            if item[0] in {"'", '"'}:
                if len(item) < 2 or item[-1] != item[0]:
                    issues.append(f"line {line_number}: unbalanced quoted list item")
                    continue
                item = item[1:-1]
            elif item[-1:] in {"'", '"'}:
                issues.append(f"line {line_number}: unbalanced quoted list item")
                continue
            fields[current_list].append(item)
            continue
        if ":" not in raw:
            issues.append(f"line {line_number}: expected key: value")
            current_list = None
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        if not re.fullmatch(r"[a-z][a-z0-9_-]*", key):
            issues.append(f"line {line_number}: invalid key {key!r}")
            current_list = None
            continue
        if key in fields:
            issues.append(f"line {line_number}: duplicate key {key!r}")
            current_list = None
            continue
        value = value.strip()
        if not value:
            fields[key] = []
            current_list = key
        else:
            if value.startswith("[") or value.startswith("{"):
                issues.append(f"line {line_number}: inline collections are not supported")
                current_list = None
                continue
            if value[0] in {"'", '"'}:
                if len(value) < 2 or value[-1] != value[0]:
                    issues.append(f"line {line_number}: unbalanced quoted scalar")
                    current_list = None
                    continue
                value = value[1:-1]
            elif value[-1:] in {"'", '"'}:
                issues.append(f"line {line_number}: unbalanced quoted scalar")
                current_list = None
                continue
            fields[key] = value
            current_list = None
    return fields, issues


def valid_iso_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return False
    return parsed.isoformat() == value


def allowed_page_types(root: Path) -> set[str]:
    allowed = set(DEFAULT_PAGE_TYPES)
    config_path = root / ".second-brain/config.json"
    if not config_path.is_file():
        return allowed
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return allowed
    extensions = config.get("allowed_types") if isinstance(config, dict) else None
    if isinstance(extensions, list):
        allowed.update(str(value).strip() for value in extensions if str(value).strip())
    return allowed


def source_locator_issues(root: Path, sources: Any, manifest: dict[str, Any]) -> list[str]:
    if not isinstance(sources, list) or not sources:
        return ["sources must be a non-empty list of raw/ locators"]
    findings: list[str] = []
    raw_root = (root / "raw").resolve()
    recorded = manifest.get("files", {})
    for value in sources:
        if not isinstance(value, str):
            findings.append("source locators must be strings")
            continue
        path_text = value.split("#", 1)[0]
        pure = PurePosixPath(path_text)
        if pure.is_absolute() or not pure.parts or pure.parts[0] != "raw" or ".." in pure.parts:
            findings.append(f"source locator must stay under raw/: {value}")
            continue
        candidate = root.joinpath(*pure.parts)
        cursor = root
        if any((cursor := cursor / part).is_symlink() for part in pure.parts):
            findings.append(f"source locator traverses a symlink: {value}")
            continue
        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(raw_root)
        except (FileNotFoundError, OSError, ValueError):
            findings.append(f"source locator is missing or escapes raw/: {value}")
            continue
        if not resolved.is_file() or candidate.is_symlink():
            findings.append(f"source locator must identify a regular non-symlink file: {value}")
            continue
        relative = resolved.relative_to(root).as_posix()
        if relative not in recorded:
            findings.append(f"source locator is not recorded in the raw manifest: {value}")
    return findings


def invalid_page_values(
    fields: dict[str, Any], allowed_types: set[str], root: Path, manifest: dict[str, Any]
) -> list[str]:
    findings: list[str] = []
    for field in ("title", "summary"):
        if field in fields and (not isinstance(fields[field], str) or not fields[field].strip()):
            findings.append(f"{field} must be a non-empty scalar")
    if "type" in fields and fields["type"] not in allowed_types:
        findings.append("type must be allowed by the vault config")
    if "status" in fields and fields["status"] not in ALLOWED_STATUSES:
        findings.append("status must be current, provisional, contested, or superseded")
    for field in ("created", "updated"):
        if field in fields and not valid_iso_date(fields[field]):
            findings.append(f"{field} must be an ISO YYYY-MM-DD date")
    if "sources" in fields:
        findings.extend(source_locator_issues(root, fields.get("sources"), manifest))
    return findings


def sensitive_field_paths(value: Any, prefix: str = "") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            rendered = f"{prefix}.{key}" if prefix else str(key)
            if SENSITIVE_FIELD_RE.search(str(key)):
                findings.append(rendered)
            findings.extend(sensitive_field_paths(nested, rendered))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            findings.extend(sensitive_field_paths(nested, f"{prefix}[{index}]"))
    return findings


def locator_issues(kind: Any, locator: Any) -> list[str]:
    if not isinstance(locator, str) or not locator.strip():
        return ["locator must be a non-empty string"]
    findings: list[str] = []
    parsed = urlsplit(locator)
    if parsed.username or parsed.password:
        findings.append("locator URL must not contain userinfo credentials")
    sensitive_query = sorted(
        key for key, _ in parse_qsl(parsed.query, keep_blank_values=True) if key.casefold() in SENSITIVE_QUERY_FIELDS
    )
    if sensitive_query:
        findings.append("locator URL has secret-bearing query fields: " + ", ".join(sensitive_query))
    if kind == "url" and (parsed.scheme not in {"http", "https"} or not parsed.netloc):
        findings.append("URL locator must be an absolute http or https URL")
    if kind in {"file", "directory"}:
        posix_absolute = PurePosixPath(locator).is_absolute()
        windows_absolute = PureWindowsPath(locator).is_absolute()
        if not posix_absolute and not windows_absolute:
            findings.append("file and directory locators must be absolute paths")
        if locator.startswith("~"):
            findings.append("file and directory locators must not rely on home-directory expansion")
    return findings


def validate_ingest_schedule_data(data: Any) -> list[str]:
    if not isinstance(data, dict) or data.get("version") != 1 or not isinstance(data.get("sources"), list):
        return ["root must contain version 1 and a sources list"]

    issues: list[str] = []
    unknown_root = sorted(set(data) - {"version", "sources"})
    if unknown_root:
        issues.append("root has unknown fields: " + ", ".join(unknown_root))
    root_secrets = sensitive_field_paths(data)
    if root_secrets:
        issues.append("configuration has credential-like fields: " + ", ".join(root_secrets))
    seen: set[str] = set()
    for index, source in enumerate(data["sources"], start=1):
        prefix = f"source {index}"
        if not isinstance(source, dict):
            issues.append(f"{prefix} must be an object")
            continue
        missing = sorted(INGEST_SOURCE_FIELDS - set(source))
        if missing:
            issues.append(f"{prefix} missing: {', '.join(missing)}")
        unknown = sorted(set(source) - INGEST_SOURCE_FIELDS)
        if unknown:
            issues.append(f"{prefix} has unknown fields: {', '.join(unknown)}")
        secret_paths = sensitive_field_paths(source)
        if secret_paths:
            issues.append(f"{prefix} has credential-like fields: {', '.join(secret_paths)}")
        source_id = source.get("id")
        if not isinstance(source_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", source_id):
            issues.append(f"{prefix} id must be unique lowercase kebab-case")
        elif source_id in seen:
            issues.append(f"{prefix} id is duplicated: {source_id}")
        else:
            seen.add(source_id)
        if source.get("kind") not in INGEST_SOURCE_KINDS:
            issues.append(f"{prefix} kind must be one of: {', '.join(INGEST_SOURCE_KINDS)}")
        for field in ("cadence", "timezone"):
            if not isinstance(source.get(field), str) or not source[field].strip():
                issues.append(f"{prefix} {field} must be a non-empty string")
        issues.extend(f"{prefix} {finding}" for finding in locator_issues(source.get("kind"), source.get("locator")))
        if not isinstance(source.get("enabled"), bool):
            issues.append(f"{prefix} enabled must be true or false")
        for field in ("max_items_per_run", "max_bytes_per_run"):
            if not isinstance(source.get(field), int) or isinstance(source.get(field), bool) or source[field] <= 0:
                issues.append(f"{prefix} {field} must be a positive integer")
        if source.get("checkpoint") is not None and not isinstance(source.get("checkpoint"), dict):
            issues.append(f"{prefix} checkpoint must be an object or null")
        normalization = source.get("normalization")
        if source.get("kind") == "url":
            if not isinstance(normalization, dict) or not all(
                isinstance(normalization.get(field), str) and normalization[field].strip()
                for field in ("strategy", "version")
            ):
                issues.append(f"{prefix} URL normalization needs non-empty strategy and version strings")
        elif normalization is not None:
            issues.append(f"{prefix} normalization must be null unless kind is url")
    return issues


def ingest_schedule_issues(root: Path) -> list[str]:
    path = root / ".second-brain/ingest-schedules.json"
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid JSON: {exc}"]
    return validate_ingest_schedule_data(data)


def canonical_json_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_ingest_schedule_data(root: Path) -> dict[str, Any]:
    path = root / ".second-brain/ingest-schedules.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise VaultError("ingest schedule configuration is missing") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise VaultError(f"invalid ingest schedule configuration: {exc}") from exc
    issues = validate_ingest_schedule_data(data)
    if issues:
        raise VaultError("invalid ingest schedule configuration: " + "; ".join(issues))
    return data


def find_ingest_source(data: dict[str, Any], source_id: str) -> dict[str, Any]:
    for source in data["sources"]:
        if source.get("id") == source_id:
            return source
    raise VaultError(f"recurring ingest source not found: {source_id}")


def ingest_checkpoint(args: argparse.Namespace) -> int:
    root = vault_path(args.vault)
    require_vault(root)
    if args.action == "show":
        data = load_ingest_schedule_data(root)
        source = find_ingest_source(data, args.source_id)
        checkpoint = source["checkpoint"]
        print_report(
            {
                "vault": str(root),
                "source_id": args.source_id,
                "checkpoint_sha256": canonical_json_digest(checkpoint),
                "checkpoint": checkpoint,
            },
            args.json,
        )
        return 0

    try:
        replacement = json.loads(args.checkpoint_json)
    except json.JSONDecodeError as exc:
        raise VaultError(f"checkpoint must be valid JSON: {exc}") from exc
    if not isinstance(replacement, dict):
        raise VaultError("checkpoint must be a JSON object")
    secret_paths = sensitive_field_paths(replacement)
    if secret_paths:
        raise VaultError("checkpoint contains credential-like fields: " + ", ".join(secret_paths))

    lock_path = root / ".second-brain/ingest-schedules.lock"
    try:
        lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise VaultError(
            "checkpoint lock already exists; confirm no ingest run is active before removing the stale lock"
        ) from exc
    try:
        os.write(lock_fd, f"pid={os.getpid()}\nsource={args.source_id}\n".encode("utf-8"))
        os.close(lock_fd)
        data = load_ingest_schedule_data(root)
        source = find_ingest_source(data, args.source_id)
        current = source["checkpoint"]
        current_digest = canonical_json_digest(current)
        if current_digest != args.expected_sha256:
            print_report(
                {
                    "vault": str(root),
                    "source_id": args.source_id,
                    "updated": False,
                    "expected_checkpoint_sha256": args.expected_sha256,
                    "current_checkpoint_sha256": current_digest,
                },
                args.json,
            )
            return 3
        source["checkpoint"] = replacement
        issues = validate_ingest_schedule_data(data)
        if issues:
            raise VaultError("checkpoint update would invalidate configuration: " + "; ".join(issues))
        atomic_write(
            root / ".second-brain/ingest-schedules.json",
            json.dumps(data, indent=2, sort_keys=True) + "\n",
        )
        print_report(
            {
                "vault": str(root),
                "source_id": args.source_id,
                "updated": True,
                "checkpoint_sha256": canonical_json_digest(replacement),
            },
            args.json,
        )
        return 0
    finally:
        try:
            os.close(lock_fd)
        except OSError:
            pass
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


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
    schedule_issues = ingest_schedule_issues(root)
    pages = sorted(path for path in wiki.rglob("*.md") if path.is_file() and not path.is_symlink()) if wiki.is_dir() else []
    by_relative, by_name = build_page_maps(pages, wiki) if wiki.is_dir() else ({}, {})
    page_labels = {page: page.relative_to(root).as_posix() for page in pages}

    missing_fields: dict[str, list[str]] = {}
    weak_provenance: list[str] = []
    invalid_fields: dict[str, list[str]] = {}
    frontmatter_syntax: dict[str, list[str]] = {}
    broken_links: list[str] = []
    ambiguous_links: list[str] = []
    inbound: Counter[Path] = Counter()
    identities: dict[str, list[str]] = defaultdict(list)
    allowed_types = allowed_page_types(root)

    for page in pages:
        text = page.read_text(encoding="utf-8", errors="replace")
        checked_text = knowledge_text(text)
        fields, syntax_issues = parse_frontmatter(text)
        if syntax_issues:
            frontmatter_syntax[page_labels[page]] = syntax_issues
        absent = [field for field in REQUIRED_PAGE_FIELDS if field not in fields]
        if absent:
            missing_fields[page_labels[page]] = absent
        invalid = invalid_page_values(fields, allowed_types, root, manifest)
        if invalid:
            invalid_fields[page_labels[page]] = invalid
        if source_locator_issues(root, fields.get("sources"), manifest):
            weak_provenance.append(page_labels[page])
        title = fields.get("title")
        identity = (title if isinstance(title, str) and title.strip() else page.stem).strip().casefold()
        identities[identity].append(page_labels[page])
        for raw_target in WIKILINK_RE.findall(checked_text):
            matches = resolve_link(raw_target, by_relative, by_name)
            if not matches:
                broken_links.append(f"{page_labels[page]} -> [[{raw_target}]]")
            elif len(matches) > 1:
                ambiguous_links.append(f"{page_labels[page]} -> [[{raw_target}]]")
            else:
                inbound[matches[0]] += 1

    duplicates = {identity: paths for identity, paths in identities.items() if len(paths) > 1}
    orphans = sorted(page_labels[page] for page in pages if inbound[page] == 0) if len(pages) > 1 else []

    indexed_pages: set[Path] = set()
    bad_index_links: list[str] = []
    index_path = root / "index.md"
    if index_path.is_file():
        index_text = knowledge_text(index_path.read_text(encoding="utf-8", errors="replace"))
        for raw_target in WIKILINK_RE.findall(index_text):
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
        "pages_frontmatter_syntax": frontmatter_syntax,
        "pages_invalid_fields": invalid_fields,
        "ingest_schedule_issues": schedule_issues,
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
            frontmatter_syntax,
            invalid_fields,
            schedule_issues,
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
    init.add_argument("--domain", action="append", default=[], help="repeat for each top-level index domain")
    init.add_argument("--review-mode", choices=("review-after", "proposal-first"))
    init.add_argument("--json", action="store_true")
    init.set_defaults(handler=init_vault)

    record = subparsers.add_parser("record-raw", help="record hashes for new immutable raw sources")
    record.add_argument("vault")
    record.add_argument("sources", nargs="*", help="specific source paths under the vault's raw directory")
    record.add_argument("--all-new", action="store_true", help="record every new raw source in an approved batch")
    record.add_argument("--json", action="store_true")
    record.set_defaults(handler=record_raw)

    checkpoint = subparsers.add_parser(
        "ingest-checkpoint", help="show or atomically compare-and-set a recurring-ingest checkpoint"
    )
    checkpoint.add_argument("action", choices=("show", "update"))
    checkpoint.add_argument("vault")
    checkpoint.add_argument("source_id")
    checkpoint.add_argument("--expected-sha256")
    checkpoint.add_argument("--checkpoint-json")
    checkpoint.add_argument("--json", action="store_true")
    checkpoint.set_defaults(handler=ingest_checkpoint)

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
        if args.command == "ingest-checkpoint" and args.action == "update":
            if not args.expected_sha256 or args.checkpoint_json is None:
                raise VaultError("checkpoint update requires --expected-sha256 and --checkpoint-json")
        if args.command == "ingest-checkpoint" and args.action == "show":
            if args.expected_sha256 or args.checkpoint_json is not None:
                raise VaultError("checkpoint show does not accept update arguments")
        return args.handler(args)
    except (OSError, VaultError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
