#!/usr/bin/env python3
"""Audit multilingual verbosity/erosion or compare saved reports. See --help."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import re
import subprocess
import sys

from language_profiles import EXTENSIONS, POLYGLOT_PROFILE, RULES, language_for


SCHEMA = "code-slop-report/2"
PROFILE = "multilingual-two-term/2"
DEFAULT_SKIP = {".git", ".hg", ".svn", ".venv", "venv", "env", "node_modules", "vendor",
                "__pycache__", ".tox", ".nox", "dist", "build", ".next", ".cache", "target", "bin", "obj", ".gradle", ".build", "Pods", ".bundle"}
SOURCE_SUFFIXES = {".py", ".pyw", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".rs", ".go", ".java",
                   ".c", ".h", ".cc", ".cpp", ".hpp", ".cs", ".rb", ".php", ".swift", ".kt", ".zig", ".hs", ".vue", ".svelte", ".razor", ".cshtml", ".fs", ".fsx", ".vb", ".erb", ".scala", ".ex", ".exs", ".dart", ".m", ".mm"}


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def matches(path, patterns):
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def test_path(path, extra):
    p = Path(path)
    return (any(part.lower() in {"test", "tests", "testing", "spec", "specs", "__tests__", "androidtest"} or part.lower().endswith(".tests") for part in p.parts[:-1])
            or bool(re.search(r"(^test[_-]|[._-](test|spec)$|(?:Test|Tests|Spec|Specs)$|^Test[A-Z])", p.stem))
            or matches(path, extra))


def discover(target, includes, excludes, test_globs, languages=()):
    """Use Git's tracked/untracked inventory when available; never follow symlinks."""
    target = target.absolute()
    if target.is_symlink() or not target.exists():
        raise ValueError("Target must be an existing, non-symlink file or directory")
    target = target.resolve()
    root = target if target.is_dir() else target.parent
    mode = "filesystem"
    if target.is_file():
        candidates = [target]
        mode = "single-file"
    else:
        try:
            probe = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"], capture_output=True, timeout=30)
        except FileNotFoundError:
            probe = None
        if probe is not None and probe.returncode == 0:
            inventory = subprocess.run(["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", "."], capture_output=True, timeout=30)
            if inventory.returncode:
                raise ValueError("Git file inventory failed")
            candidates = [root/os.fsdecode(p) for p in inventory.stdout.split(b"\0") if p]
            mode = "git-tracked-and-untracked"
        else:
            candidates = []
            for directory, dirs, files in os.walk(root, onerror=lambda error: (_ for _ in ()).throw(error)):
                dirs[:] = sorted(d for d in dirs if d not in DEFAULT_SKIP and not (Path(directory)/d).is_symlink())
                candidates.extend(Path(directory)/f for f in sorted(files))
    groups = {"production": [], "tests": []}
    skipped, unsupported = [], []
    for path in sorted(set(candidates)):
        relative = path.relative_to(root).as_posix()
        if (any(part in DEFAULT_SKIP for part in path.relative_to(root).parts[:-1])
                or matches(relative, excludes) or (includes and not matches(relative, includes))):
            skipped.append({"path": relative, "reason": "scope exclusion"})
            continue
        if not path.exists():  # Tracked deletion in the working tree.
            continue
        if path.is_symlink() or any((root/Path(*Path(relative).parts[:n])).is_symlink() for n in range(1, len(Path(relative).parts))):
            skipped.append({"path": relative, "reason": "symlink"})
            continue
        if not path.is_file():
            skipped.append({"path": relative, "reason": "not a regular file (possibly submodule)"})
            continue
        language = language_for(path)
        if language and languages and language not in languages:
            skipped.append({"path": relative, "reason": "scope exclusion"})
        elif language:
            groups["tests" if test_path(relative, test_globs) else "production"].append(relative)
        elif path.suffix.lower() in SOURCE_SUFFIXES:
            unsupported.append(relative)
    return root, mode, groups, skipped, unsupported


def summarize(rows):
    """Aggregate counts and masses; do not average ratios."""
    loc = flagged = ast_count = clone_count = 0
    masses, high_masses, functions = [], [], []
    for row in rows:
        sloc = set(row["sloc_lines"])
        ast_lines = set(row["ast_lines"]) & sloc
        clone_lines = set(row["clone_lines"]) & sloc
        loc += len(sloc)
        flagged += len(ast_lines | clone_lines)
        ast_count += len(ast_lines)
        clone_count += len(clone_lines)
        for function in row["functions"]:
            mass = function["cc"] * math.sqrt(function["sloc"])
            masses.append(mass)
            if function["cc"] > 10:
                high_masses.append(mass)
            functions.append(function)
    total_mass, high_mass = math.fsum(masses), math.fsum(high_masses)
    return {"files": len(rows), "sloc": loc, "flagged_lines": flagged, "ast_lines": ast_count,
            "clone_lines": clone_count, "overlap_lines": ast_count + clone_count - flagged,
            "verbosity": flagged/loc if loc else None,
            "total_mass": total_mass, "high_cc_mass": high_mass,
            "erosion": high_mass/total_mass if total_mass else None,
            "functions": len(functions), "high_cc_functions": len(high_masses),
            "max_cc": max((f["cc"] for f in functions), default=None)}


def build_group(rows):
    directories = {"."}
    for row in rows:
        directories.update(p.as_posix() for p in Path(row["path"]).parents if p.as_posix() != ".")
    return {"summary": summarize(rows), "files": rows, "languages": language_summaries(rows),
            "directories": {p: summarize([r for r in rows if p == "." or r["path"].startswith(p + "/")]) for p in sorted(directories)}}


def language_summaries(rows):
    names = sorted({r.get("language", "python") for r in rows})
    return {name: summarize([r for r in rows if r.get("language", "python") == name]) for name in names}


def metric_changes(before, after):
    dilution = []
    for metric, numerator in (("verbosity", "flagged_lines"), ("erosion", "high_cc_mass")):
        if delta(before[metric], after[metric]) is not None and after[metric] < before[metric] and after[numerator] >= before[numerator]:
            dilution.append(f"{metric} fell while {numerator} did not; denominator growth explains the lower ratio")
    return {"before": before, "after": after, "delta": {k: delta(before[k], after[k]) for k in before},
            "percentage_point_delta": {k: None if delta(before[k], after[k]) is None else 100 * (after[k] - before[k]) for k in ("verbosity", "erosion")},
            "dilution_warnings": dilution}


def scan(args):
    from scb_adapter import analyze_group, load_backend
    from polyglot_adapter import analyze_group as analyze_polyglot, load_parsers
    if sys.version_info[:2] != (3, 12):
        raise ValueError("Scan requires Python 3.12 to keep parsing stable; compare needs only Python 3.10+.")
    root, mode, groups, skipped, unsupported = discover(args.path, args.include, args.exclude, args.test_glob, args.language)
    if not any(groups.values()):
        raise ValueError(f"No supported source files selected; {len(unsupported)} unsupported source files. No metrics measured.")
    backend = load_backend()
    parsers, grammar_hashes = load_parsers()
    profiles = {name: {"profile": "python-scb-0.2.0-two-term/1" if name == "python" else POLYGLOT_PROFILE,
                       "rule_count": backend["identity"]["rule_count"] if name == "python" else len(RULES)} for name in EXTENSIONS}
    scripts = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(__file__).parent.glob("*.py"))}
    contract = {"profile": PROFILE, "python": platform.python_version(), "backend": backend["identity"],
                "grammars": grammar_hashes, "language_profiles": profiles, "languages": sorted(set(args.language)),
                "adapter": scripts, "discovery": mode,
                "include": sorted(set(args.include)), "exclude": sorted(set(args.exclude)),
                "test_glob": sorted(set(args.test_glob)), "default_skip": sorted(DEFAULT_SKIP),
                "single_file": args.path.name if mode == "single-file" else None,
                "cc_cutoff": 10, "suppression": "raw-all-bundled-rules", "clone_context": "separate-language-and-production-tests"}
    results = {}
    for name, paths in groups.items():
        rows = []
        for language in sorted(EXTENSIONS):
            selected = [p for p in paths if language_for(p) == language]
            if not selected:
                continue
            measured = analyze_group(root, selected, backend, args.timeout) if language == "python" else analyze_polyglot(root, selected, language, parsers)
            for row in measured:
                row["language"] = language
            rows.extend(measured)
        results[name] = build_group(sorted(rows, key=lambda r: r["path"]))
    # Catch additions/deletions and edits between groups as well as inside each detector run.
    _, _, final_groups, final_skipped, final_unsupported = discover(args.path, args.include, args.exclude, args.test_glob, args.language)
    if (groups, skipped, unsupported) != (final_groups, final_skipped, final_unsupported):
        raise ValueError("File selection changed during analysis; rerun on a stable snapshot")
    for group in results.values():
        for row in group["files"]:
            if hashlib.sha256((root/row["path"]).read_bytes()).hexdigest() != row["sha256"]:
                raise ValueError(f"Source changed during analysis: {row['path']}")
    revision = None
    if mode == "git-tracked-and-untracked":
        result = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=30)
        revision = result.stdout.strip() if result.returncode == 0 else None
    manifest = {row["path"]: row["sha256"] for g in results.values() for row in g["files"]}
    return {"schema": SCHEMA, "contract": contract, "contract_sha256": fingerprint(contract),
            "snapshot": {"label": args.label, "root": str(root), "git_head": revision,
                         "source_sha256": fingerprint(manifest)},
            "coverage": {"status": "partial" if unsupported or any(s["reason"] != "scope exclusion" for s in skipped) else "complete-for-selected-supported-source",
                         "unsupported_source_files": unsupported, "skipped": skipped,
                         "note": "Language profiles differ in rule breadth and counting conventions. Unrecognized extensions are not classified; generated source needs explicit exclusions."},
            "calibration": "uncalibrated language profiles: use per-language trends; aggregate scores are composition-sensitive and do not reproduce the paper's baseline",
            "groups": results}


def validate_report(report):
    """Reject malformed, inconsistent, or non-finite saved measurements."""
    if report.get("schema") not in {SCHEMA, "code-slop-report/1"} or fingerprint(report["contract"]) != report["contract_sha256"]:
        raise ValueError("Unsupported report schema or invalid contract fingerprint")
    seen = set()
    for group in report["groups"].values():
        for row in group["files"]:
            path = row["path"]
            if path in seen or Path(path).is_absolute() or ".." in Path(path).parts:
                raise ValueError("Duplicate or invalid report path")
            seen.add(path)
            if report["schema"] == SCHEMA and row.get("language") not in EXTENSIONS:
                raise ValueError("Missing or unsupported language in report evidence")
            for field in ("sloc_lines", "ast_lines", "clone_lines"):
                values = row[field]
                if not isinstance(values, list) or any(type(v) is not int or v < 1 for v in values) or len(values) != len(set(values)):
                    raise ValueError("Invalid source line set")
            if not (set(row["ast_lines"]) | set(row["clone_lines"])) <= set(row["sloc_lines"]):
                raise ValueError("Flagged lines outside measured source")
            for f in row["functions"]:
                if any(type(f[k]) is not int or f[k] < 1 for k in ("cc", "sloc", "start", "end")) or f["start"] > f["end"]:
                    raise ValueError("Invalid function measurement")
        if summarize(group["files"]) != group["summary"]:
            raise ValueError("Stored totals do not match measurement evidence")
        if report["schema"] == SCHEMA and group.get("languages") != language_summaries(group["files"]):
            raise ValueError("Stored language totals do not match measurement evidence")
    manifest = {r["path"]: r["sha256"] for g in report["groups"].values() for r in g["files"]}
    if fingerprint(manifest) != report["snapshot"]["source_sha256"]:
        raise ValueError("Invalid source manifest fingerprint")


def delta(before, after):
    return None if before is None or after is None else after - before


def compare(before, after):
    validate_report(before)
    validate_report(after)
    if before["contract"] != after["contract"]:
        raise ValueError("Incompatible measurement contracts. Remeasure both snapshots using identical tools and scope settings.")
    if set(before["groups"]) != set(after["groups"]):
        raise ValueError("Incompatible report groups")
    result = {"schema": "code-slop-comparison/1", "before": before["snapshot"], "after": after["snapshot"],
              "coverage_changed": before["coverage"] != after["coverage"], "groups": {}}
    for name in before["groups"]:
        old, new = before["groups"][name], after["groups"][name]
        old_rows, new_rows = ({r["path"]: r for r in g["files"]} for g in (old, new))
        changes = []
        for path in sorted(old_rows.keys() | new_rows.keys()):
            a, b = old_rows.get(path), new_rows.get(path)
            # Compare findings too: an untouched file can acquire/lose a clone peer.
            if a != b:
                changes.append({"path": path, "status": "added" if a is None else "removed" if b is None else "changed",
                                "source_changed": a is None or b is None or a["sha256"] != b["sha256"],
                                "before": summarize([a] if a else []), "after": summarize([b] if b else [])})
        new_high, resolved_high, cc_changes = [], [], []
        def index(rows):
            indexed = {}
            for row in rows.values():
                occurrences = {}
                for f in sorted(row["functions"], key=lambda f: (f["start"], f["end"], f["name"])):
                    occurrence = occurrences.get(f["name"], 0) + 1
                    occurrences[f["name"]] = occurrence
                    indexed[row["path"], f["name"], occurrence] = f
            return indexed
        a_functions, b_functions = index(old_rows), index(new_rows)
        for key in sorted(a_functions.keys() | b_functions.keys()):
            a, b = a_functions.get(key), b_functions.get(key)
            record = {"path": key[0], "name": key[1], "occurrence": key[2], "before": a, "after": b}
            if b and b["cc"] > 10 and (not a or a["cc"] <= 10):
                new_high.append(record)
            if a and a["cc"] > 10 and (not b or b["cc"] <= 10):
                resolved_high.append(record)
            if a and b and a["cc"] != b["cc"]:
                cc_changes.append(record)
        a, b = old["summary"], new["summary"]
        old_languages, new_languages = (language_summaries(g["files"]) for g in (old, new))
        languages = {language: metric_changes(old_languages.get(language, summarize([])), new_languages.get(language, summarize([]))) for language in sorted(old_languages.keys() | new_languages.keys())}
        def mix(summaries):
            total = sum(s["sloc"] for s in summaries.values())
            return {key: s["sloc"]/total for key, s in summaries.items()} if total else {}
        result["groups"][name] = {**metric_changes(a, b), "languages": languages,
            "language_mix_changed": mix(old_languages) != mix(new_languages), "files": changes, "new_high_cc": new_high,
            "resolved_high_cc": resolved_high, "cc_changes": cc_changes}
    return result


def percentage(value):
    return "not measured" if value is None else f"{100 * value:.2f}%"


def label(text):
    return str(text).replace("\n", " ").replace("\r", " ").replace("|", "\\|").replace("`", "'")


def render(report):
    if report["schema"] == "code-slop-comparison/1":
        lines = ["Code slop comparison", "", "Behavior verification: not assessed by this script."]
        if report["coverage_changed"]:
            lines += ["", "Coverage changed. Inspect exclusions/unsupported files before interpreting improvement."]
        for name, group in report["groups"].items():
            lines += ["", name.title(), "", "| Measurement | Before | After | Change |", "|---|---:|---:|---:|"]
            for key in ("verbosity", "erosion"):
                change = group["percentage_point_delta"][key]
                lines.append(f"| {key} | {percentage(group['before'][key])} | {percentage(group['after'][key])} | {'not comparable' if change is None else f'{change:+.2f} pp'} |")
            for key in ("sloc", "flagged_lines", "clone_lines", "high_cc_mass", "total_mass", "high_cc_functions", "max_cc"):
                lines.append(f"| {key} | {group['before'][key]} | {group['after'][key]} | {group['delta'][key]} |")
            if group["language_mix_changed"]:
                lines += ["", "Language proportions changed; interpret aggregate scores alongside the language results."]
            lines += ["", "| Language | Verbosity before | After | Erosion before | After |", "|---|---:|---:|---:|---:|"]
            for language, change in group["languages"].items():
                lines.append(f"| {language} | {percentage(change['before']['verbosity'])} | {percentage(change['after']['verbosity'])} | {percentage(change['before']['erosion'])} | {percentage(change['after']['erosion'])} |")
            language_warnings = [f"- {language}: {warning}" for language, change in group["languages"].items() for warning in change["dilution_warnings"]]
            if language_warnings:
                lines += ["", *language_warnings]
            lines += ["", *group["dilution_warnings"], "", "Changed files:"]
            lines += [f"- {label(f['path'])}: {f['status']}; verbosity {percentage(f['before']['verbosity'])} to {percentage(f['after']['verbosity'])}; erosion {percentage(f['before']['erosion'])} to {percentage(f['after']['erosion'])}" for f in group["files"]]
            for title, key in (("New high-complexity functions", "new_high_cc"), ("Removed/below-cutoff functions", "resolved_high_cc")):
                lines += ["", title + ":"]
                lines += [f"- {label(f['path'])}: {label(f['name'])}" for f in group[key]] or ["- None"]
            lines += ["", "Changed function complexity:"]
            lines += [f"- {label(f['path'])}: {label(f['name'])} (occurrence {f['occurrence']}): CC {f['before']['cc']} to {f['after']['cc']}" for f in group["cc_changes"]] or ["- None"]
        return "\n".join(lines) + "\n"
    lines = ["Code slop audit", "", f"Scope: {label(report['snapshot']['root'])}",
             f"Coverage: {report['coverage']['status']}", f"Calibration: {report['calibration']}",
             "Behavior verification: not assessed by this script."]
    for name, group in report["groups"].items():
        s = group["summary"]
        lines += ["", name.title() + " by language", "", "| Language | SLOC | Flagged | Verbosity | Erosion | Rules |", "|---|---:|---:|---:|---:|---:|"]
        for language, summary in language_summaries(group["files"]).items():
            rule_count = report["contract"].get("language_profiles", {}).get(language, {}).get("rule_count", "legacy")
            lines.append(f"| {language} | {summary['sloc']} | {summary['flagged_lines']} | {percentage(summary['verbosity'])} | {percentage(summary['erosion'])} | {rule_count} |")
        lines += ["", f"{name.title()}: verbosity {percentage(s['verbosity'])}; erosion {percentage(s['erosion'])}.",
                  f"{s['flagged_lines']} flagged/{s['sloc']} source lines; {s['high_cc_functions']}/{s['functions']} functions exceed CC 10.",
                  f"High-CC mass {s['high_cc_mass']:.3f}; total mass {s['total_mass']:.3f}.",
                  "", "| File | SLOC | Flagged | Verbosity | Erosion |", "|---|---:|---:|---:|---:|"]
        ranked = sorted(group["files"], key=lambda r: (-summarize([r])["flagged_lines"], r["path"]))
        for row in ranked:
            f = summarize([row])
            lines.append(f"| {label(row['path'])} | {f['sloc']} | {f['flagged_lines']} | {percentage(f['verbosity'])} | {percentage(f['erosion'])} |")
        hotspots = [(r["path"], f) for r in group["files"] for f in r["functions"] if f["cc"] > 10]
        lines += ["", "Largest high-complexity contributors (up to 10):"]
        for path, f in sorted(hotspots, key=lambda x: (-x[1]["cc"] * math.sqrt(x[1]["sloc"]), x[0], x[1]["start"]))[:10]:
            lines.append(f"- {label(path)}:{f['start']} {label(f['name'])}: CC {f['cc']}, SLOC {f['sloc']}, mass {f['cc'] * math.sqrt(f['sloc']):.3f}")
        lines += ["", "Rule/clone locations (up to 20 of each per group; JSON includes every finding):"]
        findings = [(r["path"], f) for r in ranked for f in r["rules"]]
        for path, f in findings[:20]:
            lines.append(f"- {label(path)}:{f['start']}: {label(f['rule'])}, {label(f['message'])}")
        clones = [(r["path"], c) for r in ranked for c in r["clones"]]
        for path, c in clones[:20]:
            peers = ", ".join(f"{label(p['path'])}:{p['start']}" for p in c["peers"])
            lines.append(f"- Clone {label(path)}:{c['start']}-{c['end']}; peers: {peers}")
    if report["coverage"]["unsupported_source_files"]:
        lines += ["", "Unsupported source files (unscored):", *[f"- {label(p)}" for p in report["coverage"]["unsupported_source_files"]]]
    lines += ["", f"Skipped entries: {len(report['coverage']['skipped'])}; inspect JSON for reasons."]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    scan_parser = commands.add_parser("scan", help="Measure selected Python source without modifying it")
    scan_parser.add_argument("path", type=Path)
    scan_parser.add_argument("--language", choices=sorted(EXTENSIONS), action="append", default=[], help="Limit to a supported language (repeatable; default all)")
    scan_parser.add_argument("--include", action="append", default=[], help="Case-sensitive root-relative fnmatch pattern (repeatable)")
    scan_parser.add_argument("--exclude", action="append", default=[], help="Additional root-relative exclusions (repeatable)")
    scan_parser.add_argument("--test-glob", action="append", default=[], help="Additional test classification pattern (repeatable)")
    scan_parser.add_argument("--label", default="working tree")
    scan_parser.add_argument("--timeout", type=int, default=120, help="Seconds per ast-grep batch")
    compare_parser = commands.add_parser("compare", help="Compare compatible saved JSON reports; no checker dependencies")
    compare_parser.add_argument("before", type=Path)
    compare_parser.add_argument("after", type=Path)
    report_parser = commands.add_parser("render", help="Render a saved audit JSON report without rescanning")
    report_parser.add_argument("report", type=Path)
    for child in (scan_parser, compare_parser, report_parser):
        child.add_argument("--format", choices=("json", "markdown"), default="markdown")
        child.add_argument("--output", type=Path, help="Create a NEW report file; refuses to overwrite")
    args = parser.parse_args(argv)
    try:
        if args.command == "scan":
            if args.timeout < 1:
                raise ValueError("timeout must be positive")
            report = scan(args)
        elif args.command == "compare":
            report = compare(json.loads(args.before.read_text()), json.loads(args.after.read_text()))
        else:
            report = json.loads(args.report.read_text())
            validate_report(report)
        output = json.dumps(report, sort_keys=True, indent=2, allow_nan=False) + "\n" if args.format == "json" else render(report)
        if args.output:
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(output)
        else:
            print(output, end="")
        return 0
    except (OSError, ValueError, KeyError, TypeError, ImportError, subprocess.SubprocessError) as exc:
        print(f"Measurement unavailable: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
