# Measurement and interpretation

## Exact metrics

For one measured group, let S be the set of measured `(relative path, line number)` source locations, A the rule-covered locations, and C the clone-covered locations:

```text
verbosity = count((A union C) intersect S)/count(S)
mass(function) = cyclomatic_complexity(function) * sqrt(source_lines(function))
erosion = sum(mass(f) for f with CC > 10)/sum(mass(f) for all measured f)
```

Overlapping findings count once. Identical line numbers in different files remain distinct. The cutoff is strictly greater than 10, so CC 10 is below it and CC 11 exceeds it. Empty source yields null verbosity. No measured functions yields null erosion. Null means not measured, never zero.

Sum counts and masses when aggregating files and directories; do not average their percentages. Directory rollups reuse whole-group clone evidence. Report each language's results alongside descriptive mixed totals, and do not rank languages by their scores. Report raw source lines, rule lines, clone lines, overlap lines, high-CC mass, total mass, number of high-CC functions, and maximum CC alongside the two ratios. A single function's erosion is binary; its CC and mass are more useful for prioritization.

## Versioned multilingual contract

The active contract is `multilingual-two-term/2`, with report schema `code-slop-report/2`. It combines the preserved Python detector with explicit grammar-based profiles for eleven additional languages. It pins all dependencies, parser binaries, rule counts, code hashes, the exact Python runtime, and scope settings. Different contracts require remeasuring both snapshots. The adapter records per-language counts and a language-proportion-change warning so mixed totals cannot silently hide a shift in composition.

## Versioned Python profile

The Python subprofile `python-scb-0.2.0-two-term/1` uses scb-check 0.2.0 and ast-grep 0.42.1 with its original counting conventions. The exact Python patch version, binary hash, bundled-rule hash, detector code hash, adapter code hashes, and scope configuration enter the comparison contract. Upgrading tools is a new baseline exercise.

The adapter uses the upstream parser, complexity, source-line, and clone implementations. It runs all 197 bundled slop rules directly, respects their per-file minimum occurrence metadata, and captures subprocess errors rather than interpreting errors as no matches. It ignores repository/environment rule additions and suppressions for this raw profile. Structural rules and cognitive complexity from newer upstream scoring are not part of these two metrics.

For rule scanning, temporary UTF-8 copies use a `.py` suffix, ensuring `.pyw` and uppercase Python extensions receive the same analysis. Only `ast-grep-ignore` text inside comments is neutralized; line numbers and executable source remain intact. Findings map back to original paths. Source files are never rewritten. Temporary copies are deleted after scanning. The bundled rules have no path-dependent selectors; adding such rules would require revisiting this staging convention.

Specific semantics matter:

- Source lines are upstream token-bearing physical line locations, excluding blank lines, comments, and standalone string/docstring statements. Multiline token continuation lines need not each count. This is a detector convention, not a universal SLOC definition.
- Function records include functions, async functions, and methods recognized by the Python walker. Class/module summaries are excluded. Lambdas are not separate function records. Top-level code contributes to verbosity but not function mass.
- Nested functions retain upstream **inclusive** accounting: an enclosing function's CC and SLOC include nested bodies, and the nested function also has its own record. Thus total function mass is not a partition of file source lines. Do not silently switch to exclusive accounting.
- CC is the pinned walker's syntax-based counter: one plus recognized branching nodes, including assertions, comprehensions, and Boolean operators. In this release, `match`/`case` branches do not increment that counter. Inspect pattern-matching-heavy functions manually; a low measured CC does not establish low control-flow complexity. Other tools can use different conventions.
- Clones are AST-normalized structural matches, including renamed identifiers and changed literals. Upstream candidates require at least two executable body statements. They may represent deliberate parallel cases rather than removable duplication.
- Clone detection runs across selected Python files within each group, separately for production and tests. A clone shared only between production and tests is not counted. Moving code between groups changes the comparison context and must be reviewed.
- Rule locations cover matched spans intersected with measured source lines, not a count of warnings. A broad match can cover several lines. JSON retains rule IDs, locations, clone peers, and every function measurement without source snippets.

## Scope and evidence

Default to a whole repository with separate production and test summaries. Git discovery selects tracked plus nonignored untracked files beneath the requested directory; deleted tracked files are absent. Outside Git, walk the selected directory. Skip standard environment/build/vendor directories and symlinks. Submodules are not recursively analyzed. Git-ignored and pruned directories are outside discovery and are not individually inventoried in the skipped list.

Additional includes/excludes are case-sensitive `fnmatch` patterns against root-relative POSIX paths. Repeat an option for multiple patterns; includes combine with OR, exclusions win. `*` can match path separators. There is no special recursive glob expansion. Quote patterns in a shell. Generated source outside the default exclusions needs explicit, stable exclusions.

Test classification recognizes common language-specific file/directory conventions plus extra `--test-glob` patterns. Report classification and any changes. `--language` can restrict the selected languages and is repeatable. Known unsupported source formats are listed as unscored; unrecognized extensions are not automatically classified. The coverage label describes the selected supported subset, not every possible source artifact in the repository.

JSON contains production/test summaries, per-language summaries, directory summaries, file evidence, function measurements, source hashes, coverage, and the measurement contract. Snapshot identity uses content hashes; Git HEAD is contextual and can describe a dirty checkout. Fingerprints detect inconsistency, not malicious forgery. Baseline files are never overwritten by the script.

## Threshold policy

The [reference article](https://earendil.com/posts/measuring-code-sloppiness/) reports human cohort verbosity around 0.15 with standard deviation 0.06 and erosion around 0.31 with standard deviation 0.17. Its agent cohort is around 0.33 ± 0.10 and 0.68 ± 0.20 respectively. These are cohort observations, not universal boundaries.

The following were proposed as **historical advisory reference bands**, using one and two human standard deviations above the means:

| Metric | Below first reference | Elevated reference | High reference |
|---|---:|---:|---:|
| Verbosity | <0.21 | 0.21 to <0.27 | >=0.27 |
| Erosion | <0.48 | 0.48 to <0.65 | >=0.65 |

These labels do not establish healthy or unhealthy code. The paper's Python analysis used 137 rules; the shipped Python dependency contains 197, and each added language has three core rules plus clone detection with different counting conventions. **Do not apply these bands as calibrated classifications to any shipped profile.** They are especially unsuitable for comparisons between languages. Reports deliberately label calibration unavailable and do not automatically gate CI. Erosion at CC >10 is a defined numerator criterion, not a repository failure threshold.

For a useful project policy, measure a reviewed representative baseline with this exact profile, separately by language and code role. Examine hotspots and false positives before choosing thresholds. Prefer a documented regression policy combining ratio changes, raw burden increases, and newly high-CC functions. Apply small absolute-count safeguards to tiny files, and keep policy breaches separate from behavior failures. A historical baseline is useful for change detection even when it is not a quality gold standard.

## Limits and comparison

A lower ratio can come from a larger denominator. The comparison explicitly warns when a ratio drops without a reduction in its numerator, both overall and per language. It also flags changed language proportions. Inspect new code, removals, changed coverage, and tests; deleting needed behavior, changing languages, or excluding difficult files is not by itself evidence of improvement.

Compare function records by path, qualified name, and source-order occurrence for repeated definitions. Renames/moves appear as removal/addition; reordered repeated definitions can create ambiguous matches. The JSON retains locations so the agent can check that correspondence. Snapshot totals remain valid regardless of correspondence.

These metrics measure structural proxies. They cannot infer who wrote code, prove semantic equivalence, assess runtime speed, or certify security. A low erosion score can conceal a difficult function among many simple ones. The research motivates maintainability investigation; it does not establish that optimizing these ratios reliably improves correctness. Keep tests and human judgment separate from the formula.
