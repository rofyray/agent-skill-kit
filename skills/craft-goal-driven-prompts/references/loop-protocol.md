# Evidence-driven loop protocol

Use this protocol to make “until done” operational rather than infinite or subjective.

## Preconditions

Before the first iteration, establish:

- the artifact or state being improved;
- the baseline condition;
- required and optional completion criteria;
- the verification method and evidence format;
- the actions already authorized;
- approval, cost, time, and environment boundaries;
- the location of any progress record.

If a criterion is vague, define a measurable proxy or an evidence-backed rubric before building.

Do not impose an arbitrary iteration limit when the user requested completion. Treat only a limit supplied or approved by the user as a resource-budget stop condition. If paid or scarce resources require a limit, obtain it before consuming them.

## Iteration cycle

1. **Observe**: Inspect the real current output and run the full relevant checks.
2. **Grade**: Mark each completion criterion pass or fail and attach evidence.
3. **Prioritize**: Rank failures by impact on the goal, risk, and dependency order.
4. **Improve**: Address the largest coherent gap without weakening a passing criterion.
5. **Re-test**: Re-run the affected checks and enough of the full bar to catch regressions.
6. **Record**: Note the change, evidence, remaining gaps, and next action.
7. **Repeat**: Continue until the pass or stop conditions below are met.

Avoid aimless polishing. Every iteration must target a named criterion or verified regression.

## Independent grading

Prefer a fresh-context evaluator that did not build the artifact. Give it:

- the goal and completion rubric;
- the actual artifact or direct access to it;
- the commands or observations needed to verify it;
- a mandate to find disconfirming evidence.

Do not give it the builder's reasoning, intended score, or a summary that could bias inspection. If independent evaluation is unavailable, re-run a criterion-by-criterion review and disclose that the same agent performed it.

## Pass conditions

Declare completion only when:

- every required criterion passes;
- the evidence comes from the current artifact;
- no required check is skipped or replaced by builder explanation;
- regressions and house-rule violations are absent;
- required deliverables and the verification summary exist.

## Stop conditions that are not success

Pause and report instead of looping when:

- a required action exceeds the user's authority grant;
- a destructive, external, production, privacy, or spending decision needs approval;
- a required input, credential, service, or environment is unavailable;
- the user-defined resource budget is exhausted;
- repeated cycles produce no measurable improvement and no materially different approach remains;
- completion criteria conflict or cannot be observed with available tools.

Report the blocker, evidence, alternatives attempted, and the smallest next decision needed.

## Progress record

Keep progress compact:

```text
Iteration: <n>
Changed: <largest gap addressed>
Evidence: <checks and results>
Remaining: <failed criteria in priority order>
Next: <next highest-value action>
```

Use a user-selected issue, document, board, or local file only when authorized. Do not create or update external tracking surfaces merely because the work is long-running.
