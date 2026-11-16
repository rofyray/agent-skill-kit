# {{Feature}}

## Behavior and inputs

{{User journeys, behavior, exclusions, relevant constraints, and direct shared-contract references.}}

| Requirement | Acceptance | Tasks | Verification scenario |
| --- | --- | --- | --- |
| {{REQ-ID}} | {{observable result}} | {{IDs}} | {{scenario}} |

{{Short available code/data blocks, with language, purpose, status, and source. Direct relative links to larger code, images, and other original assets. Identify inputs that cannot yet be accessed.}}

Branch mapping: {{lowercase proposed branch name and purpose, canonical task/ticket associations, and direct link to the central driver's Git naming contract. Omit the branch ID segment unless inclusion is selected and an actual applicable ID exists. Preserve any existing branch name as historical/current state, separately from new naming proposals.}}

## Test applicability and coverage

{{Link the canonical unit/integration/E2E applicability decisions. Record any feature-specific differences with scope/impact reasons, requirement references, and an owner/task for pending discovery. Map each requirement to concrete checks and existing coverage to reuse or new tests to add. Missing access blocks required checks; it does not make them not applicable.}}

## Phase {{A}}: {{Milestone}}

Entry: {{dependencies}}. Exit: {{integrated observable outcome}}.

- [ ] {{TASK-ID}}: {{bounded result}}
  - State: {{TODO, READY, ACTIVE, BLOCKED, or DONE}}
  - Requirements and acceptance: {{IDs and precise behavior}}
  - Depends on: {{task IDs or none; external blockers}}
  - Reads/reuses: {{specification and resource links}}
  - Owns: {{scope, shared-file owner, conflict notes}}
  - Branch group: {{feature or reviewable slice; lowercase proposed name from the map}}
  - Verify: {{selected levels, checks, fixtures, and expected outcomes; link shared policy and applicable feature acceptance gates}}
  - Evidence: pending

{{Repeat tasks and phases where warranted, preserving one canonical checkbox per task. Include final feature acceptance work; add integration/E2E tasks where the selected levels require them. Resolve pending applicability before accepting affected work.}}

## Acceptance scenarios

{{For each check/scenario: ID, selected level, prerequisites/data, actions, observable results, relevant failure/boundary behavior, check method, responsible task, and evidence. For integration/E2E include the actual boundary or entry point and downstream effects. Link shared final acceptance without duplicating it. Acceptance proves this feature's full scope, not automatically a separate E2E suite.}}
