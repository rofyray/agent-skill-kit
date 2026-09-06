# Screenshot critic loop

Use this reference to improve an implemented design through fresh visual judgment. The critic evaluates pixels. The builder owns the code and applies the feedback.

## When to run the loop

Run a critic loop when:

- a rendered interface exists;
- the user requested iterative improvement, independent critique, a visual quality target, or Full mode;
- screenshots can be captured and inspected; and
- implementation changes are authorized when the request includes improvement.

For Critique mode, stop after the assessment unless the user also asks for edits.

## Preserve critic independence

Give the critic only the evidence needed to judge the rendered result:

- current screenshots at representative viewports or states;
- a stable evaluation rubric; and
- optional professional references or a moodboard that establish the quality bar.

Do not give the critic source code, implementation details, the builder's rationale, time spent, earlier designs, earlier critiques, or the score needed to pass. This prevents effort, history, and stated intent from softening the visual judgment.

When references are supplied, tell the critic to use them as a quality baseline or moodboard, not as targets to copy. The most concrete comparison method is to mix the current screenshot with several strong professional examples and ask the critic to rank them by polish and taste, explain the ranking, and identify the largest visible gaps.

## Stable critic prompt

Keep the critic instruction materially identical across iterations so scores remain comparable. Adapt the artifact and rubric, not the critic's standards.

```text
Judge only the rendered screenshots provided. Infer the aesthetic direction the
interface is pursuing, then compare its execution with what a top design studio
would deliver for that direction and product.

Evaluate both the high-level structure and the fine details: composition,
hierarchy, typography, color, spacing, components, imagery, motion evidence,
platform fit, and clarity of the primary task. Penalize choices that are
excessive, redundant, incoherent, or recognizable as unmotivated generation
defaults.

Return:
1. the strongest decisions worth preserving;
2. the largest visible gaps, ordered by impact;
3. tight, specific corrections for those gaps; and
4. an evidence-based score from 1 to 10 against the studio-quality bar.

Be bold and opinionated. Do not reward implementation effort or use vague praise.
```

Do not place the builder's target score inside this prompt.

## Iteration protocol

1. Capture the current design rather than relying on memory or code inspection.
2. Invoke a fresh-context critic with the stable prompt and visual evidence.
3. Review the critic's evidence. Reject feedback that conflicts with locked requirements, accessibility, functionality, or the user's approved direction.
4. Fix the smallest set of highest-impact gaps. Do not churn every detail at once.
5. Recapture the same representative views and invoke a new fresh critic context with the same prompt.
6. Compare score movement and visible evidence, not just prose.

A 9/10 critic score is the default aspirational completion bar for Full mode. Start with one or two iterations and check whether the artifact is visibly converging before authorizing more. Continue only while the work is safe, permitted, within any cost limit, and producing measurable improvement. Stop for repeated non-improvement, a missing capability, a required decision, or an exhausted user-defined budget.

The score never overrides a required behavior, accessibility criterion, or explicit user constraint. Those must pass independently.

## Model and cost allocation

When the host offers model choice, prefer the strongest practical visual judgment capability for the critic and a capable, faster implementation model for routine execution. Do not choose an implementer so weak that it cannot follow the art direction. Use the critic at decision points rather than asking it to rebuild the page.

Do not hard-code a model name. Current quality, image understanding, latency, and price can change.

## Fallback without independent context

If a separate context or critic is unavailable, run the same rubric against fresh screenshots, withhold implementation rationale from the assessment where possible, and state that the review was self-critique rather than independent critique. Do not claim an independent score.
