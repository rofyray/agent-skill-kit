# Evidence and findings

## Establish a defect

A reportable defect needs all of the following:

- A requirement or invariant with an authority beyond the implementation under review.
- A reachable triggering condition, including the relevant caller or input.
- A tight source location and a causal explanation of the consequence.
- Evidence that the behavior occurs in the reviewed state, with independent validation or a disclosed independence limitation.
- Provenance against the original baseline: introduced, pre-existing, or unknown.

Changed lines can activate an old defect. Determine whether the change creates a new reachable failure rather than classifying solely by blame. Missing history means provenance unknown. Severity describes impact; provenance describes origin. Keep these separate.

Prefer a focused reproduction when it resolves uncertainty, but do not demand a runnable exploit for a clearly traceable static defect. Record the command, working state, observed result, and test environment for execution claims. Inspect assertions and mocks. Do not infer verification from a test filename, an exit code from unrelated tests, or a log for a different revision.

Run only checks supported by the authorized environment. Inspect unfamiliar test scripts and dependencies before running them; tests can execute arbitrary code or reach production. Use isolated scratch probes without altering the target. No runtime means a static review plus unexecuted check recommendations, not a fabricated test pass. Preserve both outcomes of an unchanged flaky rerun instead of retrying until green.

## Calibrate severity and noise

Use the repository's established priority convention. If none exists, use these portable categories:

| Severity | Meaning |
| --- | --- |
| Critical | A supported failure threatens severe compromise, irreversible loss, or widespread outage and needs immediate attention. |
| High | A reachable failure substantially breaks an important capability or boundary. |
| Medium | A meaningful defect affects a narrower supported use case with limited impact or a workaround. |
| Low | A concrete, small-impact behavioral defect. Omit optional polish unless requested. |

Do not convert severity into an invented probability or calibrated confidence percentage. A high-impact hypothetical with unproven reachability is unresolved, not automatically Critical.

Drop style preferences, speculative future requirements, redundant cleanup, and diagnostics already sufficiently enforced by observed current checks. Do not assume CI enforces a rule without inspecting its configuration or results. A failed build remains a reported check failure even when it does not need another inline defect comment. Missing test coverage is a verification gap unless an explicit repository requirement makes it a separate policy violation; label that distinction.

No default blanket exclusions for lockfiles, generated output, denial of service, or resource exhaustion. Apply trusted project-specific exclusions, disclose their coverage effects, and examine relevant inputs or generators when those explain a change's behavior. A policy that hides a material risk should appear as a policy gap, not be silently rewritten.

Group repeated instances of one root cause into a finding with representative locations and the supported affected scope. Avoid both one-comment-per-line noise and unsupported claims that every analogous path is broken.

## Return a usable review

Start with a count such as "2 confirmed findings; 1 unresolved concern." For each confirmed finding include:

1. Priority and a short title describing the broken behavior.
2. The reviewed file and minimal line span, with a navigable link when supported.
3. Trigger and consequence, including affected callers when material.
4. Evidence and how validation established it, distinguishing static and executed evidence.
5. Provenance and a correction direction when it is not obvious.

Then report material unresolved questions, check outcomes, reviewed state, and committee coverage. Separate introduced defects from pre-existing ones in the summary. A serious pre-existing issue still deserves appropriate attention without assigning its introduction to this author.

Use "No confirmed findings in the reviewed scope" when appropriate, with the actual coverage limitations. Say "Review incomplete" when missing source, unfinished validation, or an unresolved consequential concern prevents a completed verdict. Never translate no findings into "safe to merge," "secure," or "all bugs caught."

When authorized to publish, recheck the target revision before posting, map locations to that exact diff, and avoid duplicate comments using prior finding identities. Report comments that could not be placed rather than silently losing them. Do not close another person's thread merely because an agent disagrees with it.

An optional flow diagram or annotated explanation can help a human understand a complex change. Keep it grounded in actual symbols and contracts and separate it from the defect list. Do not require an HTML artifact for routine reviews.
