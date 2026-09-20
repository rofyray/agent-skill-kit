"""Pinned Python detectors. No target imports, execution, or automatic rewrites."""

from __future__ import annotations

import ast
import hashlib
import importlib.metadata as metadata
import importlib.resources as resources
import io
import json
from pathlib import Path
import subprocess
import tempfile
import tokenize
from collections import Counter


class AnalysisError(ValueError):
    """Measurement could not complete; no clean score may be inferred."""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_backend():
    """Check every installed version before importing the private pinned API."""
    lock = Path(__file__).resolve().parents[1]/"assets"/"requirements.txt"
    versions = {}
    for line in lock.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        name, expected = line.split("==")
        try:
            installed = metadata.version(name)
        except metadata.PackageNotFoundError as exc:
            raise AnalysisError(f"Missing {name}=={expected}; install assets/requirements.txt in an isolated Python 3.12 environment.") from exc
        if installed != expected:
            raise AnalysisError(f"Expected {name}=={expected}, found {installed}; use the skill's isolated environment.")
        versions[name] = installed
    from scb_check.analysis.clones import detect_clones
    from scb_check.tree_walking.dispatch import parse_source_file

    rule_dir = resources.files("scb_check.resources").joinpath("slop_rules")
    # Read only bundled resources: environment-provided and repository rules are not used.
    rule_text = "\n".join(p.read_text(encoding="utf-8") for p in sorted(rule_dir.iterdir(), key=lambda p: p.name) if p.name.endswith(".yaml"))
    import yaml
    documents = [d for d in yaml.safe_load_all(rule_text) if d]
    rules = {d["id"]: d for d in documents}
    if not rules or len(rules) != len(documents):
        raise AnalysisError("Missing or duplicated bundled rule IDs")
    dist = metadata.distribution("ast-grep-cli")
    binaries = [Path(dist.locate_file(p)).resolve() for p in dist.files or () if Path(p).name in {"ast-grep", "ast-grep.exe"}]
    if len(binaries) != 1:
        raise AnalysisError("Cannot locate the package-owned ast-grep executable")
    binary = binaries[0]
    probe = subprocess.run([str(binary), "--version"], capture_output=True, text=True, timeout=30)
    if probe.returncode or probe.stdout.strip() != "ast-grep 0.42.1":
        raise AnalysisError("The pinned ast-grep executable did not report version 0.42.1")
    # Include installed Python detector code, not just the declared package version.
    engine = hashlib.sha256()
    for p in sorted(resources.files("scb_check").rglob("*.py")):
        engine.update(p.relative_to(resources.files("scb_check")).as_posix().encode())
        engine.update(p.read_bytes())
    return {
        "parse": parse_source_file, "clones": detect_clones, "binary": binary,
        "rule_text": rule_text, "rules": rules,
        "identity": {"packages": versions, "rules_sha256": digest(rule_text.encode()),
                     "rule_count": len(rules), "detector_sha256": engine.hexdigest(),
                     "ast_grep_sha256": digest(binary.read_bytes())},
    }


def scan_rules(files, backend, timeout):
    """Run fixed rules in a neutral directory; fail on subprocess or data errors."""
    matches = []
    allowed = {str(p.resolve()) for p in files}
    with tempfile.TemporaryDirectory(prefix="code-slop-rules-") as directory:
        rule_path = Path(directory)/"rules.yaml"
        rule_path.write_text(backend["rule_text"], encoding="utf-8")
        # Bound command length; retain project-wide per-file occurrence filtering below.
        for offset in range(0, len(files), 100):
            command = [str(backend["binary"]), "scan", "--json=stream", "--include-metadata", "--rule", str(rule_path)]
            for kind in ("hidden", "dot", "exclude", "global", "parent", "vcs"):
                command.extend(["--no-ignore", kind])
            command.extend(str(p) for p in files[offset:offset + 100])
            result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=timeout)
            if result.returncode or result.stderr.strip():
                raise AnalysisError(f"ast-grep failed or reported diagnostics (exit {result.returncode}): {result.stderr[:1000]}")
            for line in result.stdout.splitlines():
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                    path = str(Path(item["file"]).resolve())
                    start, end = item["range"]["start"], item["range"]["end"]
                    first = int(start["line"]) + 1
                    # ast-grep end coordinates are exclusive.
                    last = int(end["line"]) + (int(end["column"]) != 0)
                    if path not in allowed or item["ruleId"] not in backend["rules"] or first < 1 or last < first:
                        raise ValueError("invalid location or rule")
                    matches.append({"file": path, "start": first, "end": last,
                                    "rule": item["ruleId"], "message": item["message"]})
                except (KeyError, TypeError, ValueError) as exc:
                    raise AnalysisError("Malformed ast-grep output; measurement is unavailable") from exc
    counts = Counter((m["file"], m["rule"]) for m in matches)
    return [m for m in matches if counts[m["file"], m["rule"]] >= backend["rules"][m["rule"]].get("metadata", {}).get("min_file_count", 1)]


def stage_sources(sources, directory):
    """Make UTF-8 .py copies and neutralize native ignore comments, preserving lines."""
    staged_to_original = {}
    for index, (original, source) in enumerate(sources.items()):
        lines = source.splitlines(keepends=True)
        for token in tokenize.generate_tokens(io.StringIO(source).readline):
            if token.type == tokenize.COMMENT and "ast-grep-ignore" in token.string:
                line, column = token.start
                lines[line - 1] = lines[line - 1][:column] + lines[line - 1][column:].replace("ast-grep-ignore", "ast_grep_ignore")
        # Each file has its own directory to avoid extension-normalization collisions.
        staged = directory/str(index)/(original.name + ".py")
        staged.parent.mkdir()
        staged.write_bytes("".join(lines).encode("utf-8"))
        staged_to_original[staged] = original
    return staged_to_original


def analyze_group(root, paths, backend, timeout):
    """Clone context is the whole group, not one file at a time."""
    parsed, rows, sources = [], {}, {}
    for relative in paths:
        path = root/relative
        raw = path.read_bytes()
        try:
            encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
            source = raw.decode(encoding)
            ast.parse(source, filename=relative)  # Reject partial/error-recovery parses.
            item = backend["parse"](path, source)
        except Exception as exc:
            raise AnalysisError(f"Cannot parse {relative}: {type(exc).__name__}: {exc}") from exc
        parsed.append(item)
        sources[path] = source
        functions = []
        for symbol in item.module.symbols:
            if symbol.kind.value not in {"function", "method"}:
                continue
            functions.append({"name": symbol.qualified_name, "start": symbol.start_line,
                              "end": symbol.end_line, "cc": symbol.cyc_complexity, "sloc": symbol.sloc})
        rows[relative] = {"path": relative, "sha256": digest(raw),
                          "sloc_lines": sorted(item.module.sloc_lines), "ast_lines": [], "clone_lines": [],
                          "functions": functions, "rules": [], "clones": []}
    if not paths:
        return []
    clones = backend["clones"](tuple(parsed))
    for clone in clones:
        relative = clone.file.relative_to(root).as_posix()
        rows[relative]["clone_lines"].extend(range(clone.start_line, clone.end_line + 1))
        rows[relative]["clones"].append({"start": clone.start_line, "end": clone.end_line,
            "group": clone.group_hash,
            "peers": [{"path": p.relative_to(root).as_posix(), "start": n} for p, n in clone.other_instances]})
    with tempfile.TemporaryDirectory(prefix="code-slop-source-") as directory:
        staged = stage_sources(sources, Path(directory).resolve())
        matches = scan_rules(tuple(staged), backend, timeout)
        for match in matches:
            match["file"] = str(staged[Path(match["file"])])
    for match in matches:
        relative = Path(match.pop("file")).relative_to(root).as_posix()
        rows[relative]["ast_lines"].extend(range(match["start"], match["end"] + 1))
        rows[relative]["rules"].append(match)
    for relative, row in rows.items():
        if digest((root/relative).read_bytes()) != row["sha256"]:
            raise AnalysisError(f"Source changed during analysis: {relative}; rerun on a stable snapshot")
        sloc = set(row["sloc_lines"])
        for field in ("ast_lines", "clone_lines"):
            row[field] = sorted(set(row[field]) & sloc)
        row["rules"].sort(key=lambda x: (x["start"], x["end"], x["rule"]))
        row["clones"].sort(key=lambda x: (x["start"], x["end"], x["group"]))
    return [rows[p] for p in sorted(rows)]
