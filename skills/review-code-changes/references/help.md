# Review Code Changes Help

Return the full catalog and both examples for every mode, without inspecting a target or starting a committee. End by inviting the user to choose a mode or supply a change.

## What this skill does

This skill reviews a specific change with an adaptive committee: independent agents investigate complementary risks, separate validators challenge candidate defects, and an adjudicator investigates material disagreements when needed. It tracks findings across revisions so reviews converge. Findings need evidence; committee agreement never guarantees that every bug was caught.

Review defaults to read-only Standard depth. Quick starts smaller, while Deep adds specialist scrutiny and two independent validators. The coordinator can expand the committee for named coverage gaps within a bounded budget, normally eight worker tasks per round and three review/fix rounds. No subagents means a disclosed sequential fallback. No runtime means static evidence and checks clearly marked as unexecuted.

## Modes

| Mode | Use it for |
| --- | --- |
| Review | Independently assess a PR, branch, commit range, or supplied working changes. |
| Re-review | Check revisions, retain unresolved findings, verify fixes, and detect new regressions. |
| Configure | Draft repository review guidance and map desired controls to actual integrations. |
| Evaluate | Test reviewer detection, noise, evidence, committee behavior, and convergence against hidden ground truth. |
| Help | Show this guide and examples without running a review. |

Depth settings Quick, Standard, and Deep are not additional modes. A request to fix findings authorizes scoped repair; a request to review alone does not. External comments, merge actions, or protection changes need their own authorization. Existing authorization is reused rather than requested repeatedly.

## Start here

Provide the repository or PR, the change or baseline, and its intended behavior. Include risk focus, previous findings, or limits if known. The skill will inspect accessible context before asking for missing information. Supplied files or diffs are enough to start a limited review; unavailable callers or history will be reported as gaps.

Use code understanding or implementation workflows for ordinary development, and a structural audit for numerical code-quality metrics. This skill is for independent review and its lifecycle. It can operate without other skills or a specific hosting provider.

## Examples

| Mode | Starter | Another example |
| --- | --- | --- |
| Review | `Review my working changes against main and report confirmed defects. Leave the code unchanged.` | `Deep-review this authorization PR with an adaptive committee. Focus on tenant boundaries and use only local test fixtures.` |
| Re-review | `Re-review this revision against the attached findings and verify which fixes hold.` | `Check the latest migration fix for new regressions, preserve dismissed findings, and stop after three rounds with a clear escalation if needed.` |
| Configure | `Draft a REVIEW.md for this repository using its contracts and existing checks.` | `Prepare a review integration plan that preserves our human approval rules and distinguishes missing results from clean reviews.` |
| Evaluate | `Evaluate this reviewer on the supplied buggy and clean snapshot pairs.` | `Compare fresh runs with and without the skill, keep answers hidden, and report detection, harmful findings, committee coverage, and rounds.` |
| Help | `Help` | `Show every review mode with examples and explain the fallback when subagents are unavailable.` |
