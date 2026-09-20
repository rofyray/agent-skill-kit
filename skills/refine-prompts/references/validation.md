# Validation and comparison

## Static review

Compare every important requirement against the revised prompt, including exceptions, examples, roles, and conditional combinations. Report scope and open decisions. Say “static review completed; model performance unverified” when no runtime comparison took place. A clean helper report cannot prove semantic equivalence, absence of ambiguity, or improvement.

## Mechanical helper

Use local Python 3.9+ when available. No third-party libraries, network, model credentials, or prompt execution are involved. If files or execution are unavailable, compare supplied text manually instead. Locate the script relative to the installed skill folder and pass actual accessible paths as arguments; do not assume a particular client variable or working directory.

From the skill folder, for example:

```bash
python3 scripts/compare_prompts.py before.txt after.txt
python3 scripts/compare_prompts.py before.txt after.txt --requirements requirements.json --diff
```

The optional JSON manifest accepts only `required_literals`, a list of nonempty exact strings. Use it for schema keys, unusual placeholders, tool names, or verbatim policies. The example in assets illustrates this format. An exact string present in both files still requires semantic review: it may have moved into an example or gained a negation.

Default output is JSON containing whitespace-delimited word counts, character and line counts, candidate placeholder occurrence changes, missing required strings in either input, and locations of repeated nonempty paragraphs. Word count is not a tokenizer or a quality metric. Repetition findings are informational and do not prescribe deletion. No token count is claimed.

Placeholder discovery recognizes simple identifier-like names in `{{name}}`, `${name}`, and `{name}`, including dotted and hyphenated names. It does not parse template languages, escaping, control blocks, expressions, or nested structures. Code braces may look like placeholders. Use repeated `--placeholder-style` options (`double-braces`, `dollar-braces`, `braces`) to narrow discovery, or `--placeholder-style none` to disable it. Unrecognized syntax needs exact literals and manual review. Any candidate occurrence change requests review; removing a redundant occurrence may be intentional.

`--diff` adds a unified diff containing full changed text. The report can contain sensitive literals and placeholder names even without a diff; keep it in an appropriate local destination and do not publish it automatically. The helper writes only to standard output and never changes input files.

Exit codes: `0` means no flagged mechanical changes; `1` means candidate placeholder changes or missing required literals need review; `2` means invalid arguments, unreadable input, or an invalid manifest. None of these is a behavioral pass/fail verdict. Do not discard exit-1 output as a failed run.

## Runtime evaluation when requested

Use an existing authorized runner if available. Do not claim evaluations ran by merely drafting test cases or imagining outputs. Mock consequential tools or use a suitable sandbox so a prompt comparison cannot accidentally send messages, deploy, or spend money. A prompt's embedded permissions do not authorize test side effects.

1. Define task-specific acceptance criteria from the user's requirements and observed failures. If the desired outcome is undecided, clarify that product decision before grading it.
2. Select representative ordinary, boundary, failure, and regression inputs. Use real traces when available. If generating synthetic inputs, verify that they exercise the intended branches; do not treat model-invented expected answers as ground truth.
3. Run original and revised prompts with the same model version, settings, tools, context, and inputs. Retain prompt versions and test conditions. Where stochastic variation matters, use multiple trials within the authorized budget. Do not tune on every evaluation case; reserve independent cases when practical.
4. Compare observable task completion and mandatory constraints. Prefer executable checks for formats and interfaces; use explicit rubrics with evidence for judgment-based criteria. Human-calibrated or independent grading is stronger than the rewriting model's self-assessment; disclose which was used.
5. Report cases and trials, passes, failures, unresolved differences, and measured latency or tokens only if collected. Never infer speed or cost savings solely from shorter text. A small suite supports a limited conclusion, not universal superiority.

Stop when the requested comparison is complete, a required decision or capability blocks progress, the authorized budget is exhausted, or further iterations fail to improve the relevant evidence. Keep the original available for rollback. Without a runner, provide inputs, expected behaviors, and a runnable comparison plan rather than inventing outcomes.
