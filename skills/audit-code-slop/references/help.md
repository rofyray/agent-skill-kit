# Audit Code Slop Help

## What this skill does

Measure two repeatable structural signals: verbosity, the share of source lines flagged by rules or clone detection, and erosion, the share of complexity mass in functions exceeding cyclomatic complexity 10. Save evidence, locate contributors, and track refactoring results. Report each language within production and test code separately.

Supports Python, JavaScript/TypeScript including JSX/TSX, Go, Rust, C#/.NET source, C++, PHP, Ruby, Kotlin, Swift, and Java. Python is the analyzer's runtime, not a restriction on the repository's language. Scanning needs source access, code execution, Python 3.12, and isolated pinned dependencies. No target compiler is needed. Reading or comparing saved reports needs Python 3.10+ without the detector packages. When execution is unavailable, receive a handoff instead of guessed metrics.

These signals do not prove AI authorship, bugs, security, or overall quality. Python has 197 upstream rules; each added language has three conservative core rules plus clone detection. Compare trends within each language. The profiles have no validated universal pass/fail thresholds or equivalent sensitivity across languages. C# support does not include F#, VB.NET, or Razor; embedded Vue/Svelte extraction is also outside scope.

## Modes

| Mode | Use it to | Result |
|---|---|---|
| audit | Measure a repository, directory, or file | JSON baseline, readable scores, coverage, and actionable hotspots |
| compare | Compare compatible baselines or source snapshots | Score changes in percentage points, raw burden changes, changed files/functions, and dilution warnings |
| improve | Simplify relevant measured hotspots | Scoped edits, behavior checks, and a comparable before/after report |
| help | Learn how to use the skill | This complete catalog and all examples |

## Start here

Name or select audit-code-slop and describe the desired mode. Provide a repository or files when they are not already accessible. Mention generated/vendor paths, relevant test commands, and any restricted change scope. For compare, provide two saved JSON reports or two available source snapshots. For improve, state the functionality that must be preserved and the area to change; existing instructions remain sufficient authorization for their scope.

Default to audit when asking for measurement. All supported languages are selected unless the requested scope narrows them. A repository-wide scan detects clones across files within the same language and production/test group. A standalone file scan has narrower context. Prefer repeated measurements of the same project with unchanged tools and exclusions; historical article thresholds are context, not calibrated verdicts for this version. Remeasure both snapshots when upgrading an older Python-only baseline.

## Examples

**audit**

- "Audit this TypeScript/React repository, including TSX files. Exclude generated clients and save a baseline."
- "Measure this C#, Go, and Python monorepo and show separate language results and hotspots."

**compare**

- "Compare before.json and after.json. Did the raw burden fall, or only the percentages?"
- "Compare these Rust and Java snapshots with identical exclusions. Show which functions crossed CC 10 and whether language proportions changed."

**improve**

- "Audit the Kotlin/Swift client modules, simplify useful hotspots, run their tests, and remeasure."
- "Reduce duplication in these PHP/Ruby files while preserving their public API. Show before/after counts and scores."

**help**

- "Use audit-code-slop and show help."
- "What modes and examples does audit-code-slop provide?"
