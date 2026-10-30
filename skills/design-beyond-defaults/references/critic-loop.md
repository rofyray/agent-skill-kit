# Screenshot critic loop

Use this reference to improve an implemented design through fresh visual judgment. The critic evaluates pixels. The builder owns the code and applies the feedback.

## When to run the loop

Run a critic loop when:

- a rendered interface exists;
- the user requested iterative improvement, independent critique, a visual quality target, or Full or substantial Redesign mode;
- screenshots can be captured and inspected; and
- implementation changes are authorized when the request includes improvement.

For Critique mode, stop after the assessment unless the user also asks for edits.

## Preserve critic independence

Give the critic only the evidence needed to judge the rendered result:

- current screenshots covering the relevant task, including working and completion states as well as its opening view;
- a stable evaluation rubric; and
- optional professional references or a moodboard that establish the quality bar.

Do not give the critic source code, implementation details, the builder's rationale, time spent, earlier critiques, or a desired verdict. For a single-artifact iteration, withhold earlier designs too. For an explicitly requested comparison, supply matched anonymous views of both artifacts without their history. This prevents effort, history, and stated intent from softening the visual judgment.

When references are supplied, tell the critic to use them as a quality baseline or moodboard, not as targets to copy. The most concrete comparison method is to mix the current screenshot with several strong professional examples and ask the critic to rank them by polish and taste, explain the ranking, and identify the largest visible gaps.

## Stable critic prompt

Keep the rubric materially identical across iterations. Choose the important task states before judging; do not change their weighting to favor an outcome. A polished opening, a useful working state, and a clear completion can have different strengths.

```text
Judge only the rendered screenshots provided. Infer the aesthetic direction the
interface is pursuing and assess how coherently it serves the visible task.
Use supplied professional references as a quality baseline when available.

Evaluate both the high-level structure and the fine details: composition,
hierarchy, typography, color, spacing, components, imagery, motion evidence,
platform fit, and clarity of the primary task. Penalize choices that are
excessive, redundant, incoherent, or recognizable as unmotivated generation
defaults.

Return:
1. the strongest decisions worth preserving;
2. the largest visible gaps, ordered by impact;
3. tight, specific corrections for those gaps that preserve its identity; and
4. confidence, missing evidence, and tradeoffs between viewports and task states.

For a comparison, give a preference or tie with reasons. Do not force a winner
or infer working behavior from screenshots. Treat unobserved states as unknown.

Be bold and opinionated. Do not reward implementation effort or use vague praise.
```

Do not turn visual preference into a defect or a completion score. If the user requests a numerical rating, label it subjective and state its rubric and evidence limits; it is not a release gate.

## Iteration protocol

1. Capture settled current views using the verification guide. Include relevant entry, populated, failure/recovery, and completion states, scaled to the scope.
2. Invoke a fresh-context critic with the stable prompt and visual evidence.
3. Review the critic's evidence. Reject feedback that conflicts with locked requirements, accessibility, functionality, or the user's approved direction.
4. Fix the smallest set of highest-impact gaps. Do not churn every detail at once.
5. Recapture the same representative views and invoke a new fresh critic context with the same prompt.
6. Compare resolved findings, remaining gaps, and visible tradeoffs. Preserve what the earlier version did better. When a consequential preference remains close or disputed, use another fresh critic if useful and within budget; keep disagreement visible rather than averaging it away.

There is no default numerical completion target. Complete against the task's declared requirements, chosen visual direction, inspected states, and resolved material findings. Start with one or two correction rounds and check whether the artifact is visibly improving before continuing. Stop for repeated non-improvement, a missing capability, a required decision, or an exhausted user-defined budget; report remaining gaps.

Visual preference never overrides a required behavior, accessibility criterion, or explicit user constraint. Those must pass independently.

## Model and cost allocation

When the host offers model choice, prefer the strongest practical visual judgment capability for the critic and a capable, faster implementation model for routine execution. Do not choose an implementer so weak that it cannot follow the art direction. Use the critic at decision points rather than asking it to rebuild the page.

Do not hard-code a model name. Current quality, image understanding, latency, and price can change.

## Fallback without independent context

If a separate context or critic is unavailable, run the same rubric against fresh screenshots, withhold implementation rationale from the assessment where possible, and state that the review was self-critique rather than independent critique. Do not claim an independent score.

## Functional review and disagreements

Keep functional review separate from the pixels-only critic. A functional reviewer may receive requirements, source, and test results. Reject visual suggestions that break locked behavior. Resolve alleged defects by reproduction and requirement evidence; leave unresolved concerns marked needs review. Do not use votes or average scores to override a verified failure. For blind evaluation, randomize anonymous current/baseline labels and keep the builder history hidden.
