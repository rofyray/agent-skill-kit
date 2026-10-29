# Evaluate a reviewer

## Build a defensible corpus

Use expert-confirmed incidents, reverts, or independently constructed changes with observable defects. Include clean changes and tempting non-bugs. Separate target inputs from evaluator-only answers, later fixes, incident descriptions that reveal the defect, and prior reviewer output. A reviewer must receive the same information it would legitimately have had at review time.

For each case record the baseline, candidate state, requirement, defect's trigger and location, accepted alternative findings, and evidence establishing ground truth. Add sequential revisions to test convergence, stale evidence, ineffective fixes, and genuinely new defects. Include repository policy adherence as a separate scoring dimension.

Run fresh contexts with and without the skill on equivalent inputs and capabilities. Keep the model and settings equivalent unless testing those differences explicitly. Use isolated copies and compare target contents before and after. Record actual host restrictions: an agent instructed not to execute is a policy-limited run, not proof that the host technically lacks execution.

For committee evaluations, capture actual worker tasks, context independence, coverage changes, and validation decisions. Do not grade a narrative that says "the committee checked" as proof of delegation. A fallback evaluation should constrain delegation and check that the limitation is accurately reported.

## Score behavior, not wording

Measure independently:

- Trigger precision: dedicated reviews activate; explanation, mechanical edits, prompt writing, and structural metrics do not get hijacked.
- Defect recall: confirmed target defects found, separated by severity and provenance.
- False positives: unsupported defects and harmful suggested changes on clean or intentional behavior.
- Evidence quality: reachable triggers, correct locations, valid baseline attribution, and honest execution claims.
- Committee behavior: complementary tasks, real independent challenge, justified adaptation, bounded tasks, and handling of missing workers or disagreement.
- Convergence: repeated findings, ineffective-fix detection, new-regression detection, and rounds until resolution or escalation.
- Scope and action boundaries: source preservation for review-only work and no unauthorized publication or configuration.
- Efficiency: observed worker tasks, time, tokens or cost when the host exposes them, and human follow-up needed. Missing telemetry is unavailable, not zero.

A small known-bug fixture can establish that a workflow ran correctly; it cannot establish production recall, calibrated confidence, or Anthropic-scale throughput. A baseline that finds the same bug is a valid result, not a failed experiment. Do not tune on the only held-out examples or claim statistical improvement from a few runs.

## Iterate on demonstrated failures

Keep each raw report and grade with the prompt, available tools, skill version or content fingerprint, model settings where known, and target identity. Inspect defects in the skill separately from fixture ambiguity and host limitations. Make the narrowest supported correction and replay the failed case, plus related cases affected by that correction.

Use blind independent evaluators when available and authorized. Do not supply the expected finding in the executing agent's task. Evaluate any reviewer prompt, model, tool, or filtering change against the retained corpus, including clean cases. Human triage determines whether a new finding should expand the ground truth.

Return executed results separately from prepared but unexecuted cases. List untested clients. Repository validation, unit tests, and ZIP inspection establish packaging and helper behavior; none substitutes for executing the review workflow.
