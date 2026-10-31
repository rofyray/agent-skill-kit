"""Export a read-only knowledge snapshot and serve only generated viewer files."""

from __future__ import annotations

import functools
import hashlib
import json
import os
import re
import webbrowser
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote, urlsplit

import second_brain as vault


VIEWER_FILES = ("index.html", "viewer.js", "viewer.css", "THIRD_PARTY_NOTICES.txt")
OWNER = "second-brain-viewer-v1"
MD_LINK = re.compile(r"(?<!!)\[[^\]\n]*\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)")


def checked_path(root: Path, relative: str) -> Path:
    """Never follow vault symlinks, even when their destination is inside the vault."""
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or "\\" in relative:
        raise vault.VaultError(f"unsafe vault path: {relative}")
    cursor = root
    for part in pure.parts:
        cursor = cursor/part
        if cursor.is_symlink():
            raise vault.VaultError(f"symlink is not supported: {relative}")
    return cursor


def read_json(root: Path, relative: str) -> dict:
    try:
        value = json.loads(checked_path(root, relative).read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise vault.VaultError(f"cannot read {relative}: {exc}") from exc
    if not isinstance(value, dict):
        raise vault.VaultError(f"expected an object in {relative}")
    return value


def inventory(root: Path, directory: str, diagnostics: list) -> list[Path]:
    base = checked_path(root, directory)
    result = []
    for parent, directories, files in os.walk(base, followlinks=False):
        for name in list(directories):
            path = Path(parent)/name
            if path.is_symlink():
                directories.remove(name)
                diagnostics.append({"kind": "symlink", "page": path.relative_to(root).as_posix()})
        for name in files:
            path = Path(parent)/name
            if path.is_symlink():
                diagnostics.append({"kind": "symlink", "page": path.relative_to(root).as_posix()})
            elif path.is_file():
                result.append(path)
    return sorted(result)


def scalar(fields: dict, name: str, default: str = "") -> str:
    value = fields.get(name)
    return value if isinstance(value, str) else default


def graph_snapshot(root: Path) -> dict:
    root = root.resolve()
    vault.require_vault(root)
    config = read_json(root, ".second-brain/config.json")
    manifest = read_json(root, ".second-brain/raw-manifest.json")
    if not isinstance(manifest.get("files"), dict):
        raise vault.VaultError("raw manifest must contain a files object")
    diagnostics: list[dict] = []
    pages = [p for p in inventory(root, "wiki", diagnostics) if p.suffix == ".md"]
    raw = inventory(root, "raw", diagnostics)
    by_path: dict[str, list[Path]] = {}
    by_name: dict[str, list[Path]] = {}
    for page in pages:
        relative = page.relative_to(root/"wiki").with_suffix("").as_posix().casefold()
        by_path.setdefault(relative, []).append(page)
        by_name.setdefault(page.stem.casefold(), []).append(page)

    def resolve(target: str) -> list[Path]:
        key = vault.wikilink_target(target)
        if ".." in PurePosixPath(key).parts:
            return []
        return by_path.get(key, []) if "/" in key else by_name.get(key, [])

    def linked(target: str, origin: str) -> Path | None:
        matches = resolve(target)
        if len(matches) != 1:
            diagnostics.append({"kind": "ambiguous-link" if matches else "broken-link",
                                "page": origin, "target": target})
            return None
        return matches[0]

    # Index membership organizes pages, but never creates knowledge edges.
    groups: dict[Path, str] = {}
    section = "Unfiled"
    index = checked_path(root, "index.md").read_text(encoding="utf-8")
    for line in vault.knowledge_text(index).splitlines():
        if line.startswith("## "):
            section = line[3:].strip() or "Unfiled"
        for target in vault.WIKILINK_RE.findall(line):
            page = linked(target, "index.md")
            if page:
                groups.setdefault(page, section)

    nodes = []
    edges: dict[tuple[str, str, str], dict] = {}
    raw_ids = {p.relative_to(root).as_posix() for p in raw}
    name = str(config.get("name") or root.name)

    def edge(source: str, target: str, kind: str, locator: str = "") -> None:
        key = (source, target, kind)
        item = edges.setdefault(key, {"source": source, "target": target, "kind": kind, "locators": []})
        if locator and locator not in item["locators"]:
            item["locators"].append(locator)

    for page in pages:
        relative = page.relative_to(root).as_posix()
        text = page.read_text(encoding="utf-8")
        fields, errors = vault.parse_frontmatter(text)
        for issue in errors:
            diagnostics.append({"kind": "frontmatter", "page": relative, "detail": issue})
        for field in vault.REQUIRED_PAGE_FIELDS:
            if field not in fields:
                diagnostics.append({"kind": "missing-field", "page": relative, "detail": field})
        tags = fields.get("tags", [])
        tags = [t for t in tags if isinstance(t, str)] if isinstance(tags, list) else []
        sources = fields.get("sources", [])
        sources = [s for s in sources if isinstance(s, str)] if isinstance(sources, list) else []
        nodes.append({
            "id": relative, "title": scalar(fields, "title", page.stem),
            "summary": scalar(fields, "summary"), "type": scalar(fields, "type", "unknown"),
            "status": scalar(fields, "status", "unknown"), "created": scalar(fields, "created"),
            "updated": scalar(fields, "updated"), "tags": tags, "sources": sources,
            "group": groups.get(page, tags[0] if tags else "Unfiled"), "indexed": page in groups,
            "kind": "page",
            "obsidianUri": f"obsidian://open?vault={quote(name, safe='')}&file={quote(relative, safe='')}",
        })
        # Strip frontmatter and code before reading knowledge links.
        body = text
        if text.startswith("---\n"):
            parts = text.split("\n---", 1)
            if len(parts) == 2:
                body = parts[1]
        body = vault.knowledge_text(body)
        for target in vault.WIKILINK_RE.findall(body):
            if not target.split("|", 1)[0].split("#", 1)[0].strip():
                continue  # Same-page heading reference.
            destination = linked(target, relative)
            if destination:
                edge(relative, destination.relative_to(root).as_posix(), "reference", target)
        for target in MD_LINK.findall(body):
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme or parsed.netloc or not parsed.path.endswith(".md"):
                continue
            target_path = Path(os.path.normpath(page.parent/unquote(parsed.path)))
            try:
                target_key = target_path.relative_to(root/"wiki").with_suffix("").as_posix()
            except ValueError:
                continue
            matches = by_path.get(target_key.casefold(), [])
            if len(matches) == 1:
                edge(relative, matches[0].relative_to(root).as_posix(), "reference", target)
            else:
                diagnostics.append({"kind": "ambiguous-link" if matches else "broken-link",
                                    "page": relative, "target": target})
        for locator in sources:
            source_id = locator.split("#", 1)[0]
            if source_id in raw_ids:
                edge(relative, source_id, "evidence", locator)
            else:
                diagnostics.append({"kind": "missing-source", "page": relative, "target": locator})
            if source_id not in manifest["files"]:
                diagnostics.append({"kind": "unrecorded-source", "page": relative, "target": locator})

    for path in raw:
        relative = path.relative_to(root).as_posix()
        nodes.append({"id": relative, "title": path.name, "summary": "Source file. Contents are not included in this snapshot.",
                      "kind": "source", "type": "source", "status": "recorded" if relative in manifest["files"] else "unrecorded",
                      "group": "Sources", "tags": [], "sources": [], "created": "", "updated": "", "indexed": False,
                      "obsidianUri": f"obsidian://open?vault={quote(name, safe='')}&file={quote(relative, safe='')}"})
    degree = {n["id"]: set() for n in nodes}
    for source, target, kind in edges:
        if kind == "reference" and source != target:
            degree[source].add(target)
            degree[target].add(source)
    for node in nodes:
        node["degree"] = len(degree[node["id"]])
    links = sorted(edges.values(), key=lambda e: (e["source"], e["target"], e["kind"]))
    # Absolute paths and raw contents never enter the browser snapshot.
    payload = {"version": 1, "name": name, "nodes": nodes, "links": links, "diagnostics": diagnostics}
    payload["digest"] = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    payload["generatedAt"] = datetime.now(timezone.utc).isoformat()
    return payload


def viewer_assets() -> Path:
    candidates = (Path(__file__).resolve().parent.parent/"assets"/"brain-viewer",
                  Path(__file__).resolve().parent/"brain-viewer")
    for directory in candidates:
        if all((directory/name).is_file() for name in VIEWER_FILES):
            return directory
    raise vault.VaultError("bundled brain-viewer assets are missing; use a complete skill installation")


def export_viewer(root: Path, output: Path | None = None) -> tuple[Path, dict]:
    root = root.resolve()
    assets = viewer_assets()
    requested = output or root/".second-brain"/"visualization"
    # Check the lexical path first so resolve() cannot hide a symlink.
    requested = requested.expanduser().absolute()
    if any(p.is_symlink() for p in (requested, *requested.parents)):
        raise vault.VaultError("visualization output must not traverse symlinks")
    output = requested.resolve()
    default = root/".second-brain"/"visualization"
    if output != default and (output == root or root in output.parents or output in root.parents):
        raise vault.VaultError("custom output must be outside the vault and cannot contain the vault")
    marker = output/".viewer-owner"
    if output.exists() and (not output.is_dir() or not marker.is_file() or marker.is_symlink()
                            or marker.read_text() != OWNER):
        raise vault.VaultError("output exists and is not an owned visualization; choose an empty new path")
    if output.exists() and any(p.is_symlink() for p in output.iterdir()):
        raise vault.VaultError("visualization output contains a symlink")
    snapshot = graph_snapshot(root)
    output.mkdir(parents=True, exist_ok=True)
    lock = output/".export-lock"
    try:
        lock.mkdir()
    except FileExistsError as exc:
        raise vault.VaultError("another export may be active; inspect .export-lock before retrying") from exc
    try:
        vault.atomic_write(marker, OWNER)
        for name in VIEWER_FILES:
            vault.atomic_write(output/name, (assets/name).read_text(encoding="utf-8"))
        vault.atomic_write(output/"graph.json", json.dumps(snapshot, ensure_ascii=False, separators=(",", ":")) + "\n")
    finally:
        lock.rmdir()
    return output, snapshot


class ViewerHandler(SimpleHTTPRequestHandler):
    """An allowlist prevents directory listings, vault reads, and symlink escapes."""

    def send_head(self):
        allowed_hosts = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
        if self.headers.get("Host") not in allowed_hosts:
            self.send_error(403)
            return None
        relative = unquote(urlsplit(self.path).path).lstrip("/") or "index.html"
        if relative not in (*VIEWER_FILES, "graph.json") or (Path(self.directory)/relative).is_symlink():
            self.send_error(404)
            return None
        return super().send_head()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
        super().end_headers()

    def log_message(self, format, *args):
        pass


def make_server(output: Path, port: int = 0) -> ThreadingHTTPServer:
    return ThreadingHTTPServer(("127.0.0.1", port), functools.partial(ViewerHandler, directory=str(output)))


def visualize(args) -> int:
    if args.open and not args.serve:
        raise vault.VaultError("--open requires --serve")
    if not 0 <= args.port <= 65535:
        raise vault.VaultError("port must be between 0 and 65535")
    output, snapshot = export_viewer(vault.vault_path(args.vault), Path(args.output) if args.output else None)
    report = {"vault": str(vault.vault_path(args.vault)), "output": str(output), "pages": sum(n["kind"] == "page" for n in snapshot["nodes"]),
              "sources": sum(n["kind"] == "source" for n in snapshot["nodes"]),
              "links": len(snapshot["links"]), "diagnostics": len(snapshot["diagnostics"]), "digest": snapshot["digest"]}
    if not args.serve:
        vault.print_report(report, args.json)
        return 0
    with make_server(output, args.port) as server:
        report["url"] = f"http://127.0.0.1:{server.server_port}"
        vault.print_report(report, args.json)
        print("Viewer ready. Keep this process running; Ctrl+C stops it.", flush=True)
        if args.open:
            webbrowser.open(report["url"])
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
    return 0
