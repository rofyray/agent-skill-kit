# Execution and improvement workflow

## Runtime and capability check

Resolve the installed skill directory from its actual location. Do not assume it is in the target repository. Read the entry point's `--help` when command options are unclear.

Scanning any supported target language requires an executable Python 3.12 environment and the pinned packages in `assets/requirements.txt`. The repository being scanned can be TypeScript, Go, C#, or any other supported language without containing Python code. Use an existing compatible isolated environment or create a dedicated one outside the target project. For example, with resolved absolute paths substituted for the placeholders:

```text
python3.12 -m venv <environment-directory>
<environment-python> -m pip install -r <skill-directory>/assets/requirements.txt
```

Use the host's available equivalent environment manager if Python lacks pip/venv support. Check host permissions and network availability before setup. Do not alter the target project's dependencies, copy its secrets, or execute its setup hooks. The adapter verifies package versions and resolves the package-owned ast-grep binary; no separate ast-grep installation is needed. The pinned multilingual grammar package bundles its parsers, and scanning needs no grammar downloads or target-language toolchains. Native dependency availability can vary by platform.

If execution, source, or dependencies are unavailable, identify the specific gap and give the ready-to-run command or request the missing source context. A qualitative source review may supplement the handoff if useful, but label it unmeasured. Do not substitute an LLM estimate, download source to an external service, or claim a successful audit from partial detector output. An unsupported-only source selection returns an error and no numerical report.

## Audit

1. Resolve scope, generated/vendor exclusions, and test classification. Reuse recorded project policy where available. Keep these choices consistent across repeated runs.
2. Choose new output filenames outside the source tree, or exclude a dedicated reports directory consistently. Prefer JSON as the authoritative baseline, then render it without rescanning:

```text
<environment-python> <skill-directory>/scripts/audit.py scan <source-directory> --exclude 'generated/*' --label before --format json --output <reports-directory>/before.json
<python> <skill-directory>/scripts/audit.py render <reports-directory>/before.json --output <reports-directory>/before.md
```

3. Inspect coverage and evidence before describing results. Default to all supported languages; use repeatable `--language typescript --language javascript` options when the user wants a subset. Report each language within production/tests, including rule breadth. Do not infer low sloppiness from null scores or rank a three-rule language against the 197-rule Python profile. For a selected file, disclose that clone context excludes other files.
4. Inspect the largest absolute flagged-line contributors and high-CC mass contributors in source. Explain which detector findings are actionable and which are intentional. Use JSON for full directory and evidence details; Markdown limits detailed rule/clone listings.

The analyzer is read-only toward target source. Exit 0 means measurement/comparison completed, regardless of score. Exit 2 means measurement unavailable or invalid input; the message goes to stderr. Existing output paths are refused. Tests/builds have not run merely because an audit completed.

## Compare

Use two JSON audit reports made with exactly the same measurement contract:

```text
<python> <skill-directory>/scripts/audit.py compare <reports-directory>/before.json <reports-directory>/after.json --format json --output <reports-directory>/comparison.json
<python> <skill-directory>/scripts/audit.py compare <reports-directory>/before.json <reports-directory>/after.json --output <reports-directory>/comparison.md
```

Comparison and rendering use standard-library Python 3.10+ and do not need detector dependencies. Compare accepts audit reports, not prose summaries or comparison reports. Rendering accepts audit JSON; use compare with Markdown output for readable comparisons.

When only Git revisions are available, inspect them in isolated checkouts or temporary source snapshots and measure both with the same inventory mode and exclusions. Preserve uncommitted user work. The CLI does not switch branches or create worktrees automatically. Do not compare a filesystem-export profile with a Git-inventory profile; remeasure both in the same mode.

Report changes in percentage points, raw flagged lines, source lines, high-CC mass, total mass, high-CC function count, and maximum CC. Inspect per-language changes before interpreting mixed totals. Show changed files and functions, including findings that change in untouched source because a same-language clone peer changed. Review additions, removals, production/test movement, unsupported files, language-proportion changes, and dilution warnings before claiming improvement. The comparison rejects incompatible settings; there is no override that pretends different profiles are comparable. Remeasure both snapshots after upgrading from the Python-only profile. Compatible legacy reports remain readable/comparable to each other.

## Improve

1. Save the baseline before editing. Identify the relevant existing behavior checks and run a focused baseline check when feasible. Record existing failures; do not attribute them to later edits.
2. Choose concrete hotspots within the authorized scope. Prefer removing redundant logic, consolidating actual shared behavior, clarifying branching, and replacing unnecessarily elaborate constructs with readable equivalents. Inspect callers and contracts before extraction. Similar syntax alone does not justify a shared abstraction.
3. Make a coherent, reviewable change. Preserve necessary validation, error behavior, public interfaces, comments explaining intent, and test assertions. Avoid trivial function splitting or broad unrelated cleanup to improve the score.
4. Run the appropriate tests, type checks, or build checks. Add targeted behavior coverage where a meaningful refactor exposes a gap. If checks cannot run, explain exactly what remains unverified; score improvement is not behavior verification.
5. Remeasure with the identical runtime and options, then compare. Inspect absolute burden, changed scope, new high-CC functions, and the other metric as well as the target metric. A tradeoff can be worthwhile, but explain it rather than calling every reduction a win.
6. Stop when the requested useful changes are complete and verified, or when remaining findings are intentional, outside scope, or cannot be changed confidently with available evidence. Do not chase zero or a historical threshold. If a proposed change has no clear maintenance benefit, leave it out. Revert only your unsuccessful change, preserving user edits.

Deliver the practical outcome, before/after measurements, behavior checks and their results, remaining material limitations, and links to the saved evidence. If the user supplied a threshold, state whether the measured scope meets that policy without presenting it as a validated scientific classification.
