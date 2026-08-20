# Implementation

Use this playbook only when the user clearly asks to generate or change code.

## Confirm the change boundary

- Identify the requested behavior and the smallest observable completion condition.
- Inspect repository instructions, working-tree state, relevant implementation, callers, tests, and established patterns.
- Preserve unrelated user changes and avoid broad cleanup.
- Carry forward explicit priorities and deferred concerns.

If the request is underspecified but a reversible minimal interpretation exists, state it and proceed. Ask before coding when different interpretations change public behavior, data, permissions, compatibility, or architecture.

## Choose the smallest justified design

- Reuse code when its contract and responsibility fit.
- Prefer a local change when a shared abstraction would expand the blast radius without proven benefit.
- Extract a shared function only when it creates a stable, coherent contract used by multiple real consumers or removes meaningful duplication without coupling unrelated behavior.
- Preserve public APIs and data formats unless changing them is part of the request.
- Avoid preparing infrastructure for hypothetical future features.

Before editing, understand the affected path far enough to predict inputs, outputs, side effects, errors, authorization, and downstream behavior.

## Implement against relevant risks

Apply only the lenses supported by the task and evidence:

- validate boundaries and meaningful edge cases;
- preserve or strengthen permission checks at the correct layer;
- avoid exposing secrets, sensitive data, internal errors, or cross-tenant state;
- assess performance on actual hot or multiplicative paths;
- preserve transactionality, ordering, idempotency, and concurrency invariants where present;
- maintain error semantics expected by callers;
- update tests, comments, or documentation when behavior or contracts change.

When the user defers a concern, do not implement it. Record it in the handoff if it remains material. Still stop or seek direction for a critical security, data-loss, privacy, permission, or regression problem.

## Verify the real change

1. Add or adjust the narrowest test that would fail before the change and pass after it when practical.
2. Run focused checks first, then broader existing checks in proportion to regression risk.
3. Inspect the actual diff for unintended behavior, duplicate logic, stale comments, and unrelated formatting.
4. Exercise the user or system flow when the environment permits it.
5. Report checks that could not run and why.

Do not claim success from code inspection alone when executable verification is available.

## Return the handoff

Lead with the completed behavior. Include:

- the minimal design choice and reused pattern;
- changed files or components;
- verification evidence;
- downstream or compatibility implications;
- explicitly deferred concerns and remaining limitations.

Do not bury the implemented result beneath a long design essay.
