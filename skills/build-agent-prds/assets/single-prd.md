# {{Product}} PRD

Status: {{reviewable draft or implementation-ready; unresolved inputs}}

## Product contract

{{Problem, users, outcomes, in-scope journeys, exclusions, and relevant constraints. Distinguish requirements, facts, assumptions, and decisions.}}

| Requirement | Observable acceptance | Implementing tasks | Verification scenario |
| --- | --- | --- | --- |
| {{REQ-ID}} | {{behavior}} | {{task IDs}} | {{scenario ID}} |

## Inputs and reuse

{{Embed available short code and data in language-labeled blocks. Identify purpose, source, status, and dependencies. Link larger examples, original images, and declared repository inputs. Missing required inputs name affected blockers. Companion files make this a ZIP delivery.}}

## Execution and branch plan

{{Branch groups, task IDs, bases, dependency gates, ownership, and integration owner.}}

The coordinator starts every ready independent workstream that fits available subagent capacity and refills capacity as work finishes. Use explicit dependencies, agreed interfaces, and exclusive file ownership. Isolate concurrent changes where supported; serialize conflicting writers. If subagents are unavailable, follow the same plan sequentially. Workers receive their task scope, inputs, acceptance criteria, and tests, and return changes, evidence, commit or patch, and blockers. The coordinator integrates results and owns canonical task status.

Commit each verified task or inseparable group with its tests and tracking on the designated feature branch. Follow repository conventions and existing publication authorization. Distinguish commits, pushes, PRs, merges, and release. Continue eligible authorized work without another kickoff prompt; stop when complete or no eligible work remains.

## Phase {{A}}: {{Milestone}}

Entry: {{explicit prerequisites}}. Exit: {{integrated observable result}}.

- [ ] {{TASK-ID}}: {{bounded result}}
  - State: {{TODO, READY, ACTIVE, BLOCKED, or DONE}}
  - Requirements: {{IDs}}
  - Acceptance: {{observable success, failure, and boundary behavior}}
  - Depends on: {{IDs or none; missing external inputs}}
  - Reads/reuses: {{section, code, data, and asset links}}
  - Owns: {{scope and conflict boundaries}}
  - Branch group: {{feature}}
  - Verify: {{checks and expected outcomes}}
  - Evidence: pending

{{Repeat phases and tasks as the work requires. Include explicit integration and final acceptance tasks with dependencies and an owner; do not leave them implicit. Each task has only one canonical checkbox.}}

## Verification and final acceptance

{{Actual command map with working directories, environments, fixtures, and selection scope. Mark unknown commands pending a named discovery or setup task.}}

Use targeted checks while coding; complete acceptance and affected module/integration checks before task completion. Run critical smoke and applicable static checks at PR gates, broader integration checks after merge, and scheduled full regression checks. Shared or high-risk changes widen scope; uncertain impact requires the full relevant suite. Run the full applicable suite before risky refactors, releases, and final handoff.

| Scenario | Prerequisites and data | Actions | Expected result and downstream effects | Failure/recovery checks | Method and evidence |
| --- | --- | --- | --- | --- | --- |
| {{E2E-ID}} | {{inputs}} | {{steps}} | {{observations}} | {{cases}} | {{procedure and receipt}} |

Completion requires every in-scope requirement implemented, combined feature work building and running in the stated environment, required assets working, and all defined end-to-end scenarios plus the full applicable suite and required nonfunctional checks passing on the integrated revision. Exercise required real boundaries in an authorized test environment; mocks do not prove those integrations. Fix failures and rerun affected checks. Missing required tests or services leave verification blocked. Record revision, environment, actual results, and evidence. Release status is separate.

## Progress and resume

{{Compact branch, commit, integration, blocker, evidence, and next-ready-work record.}}

Check a task only after acceptance and required tests pass and its changes are integrated into its feature branch. Phase exit and final product completion need their own integrated checks. On resume compare this record with actual repository state, preserve valid results, and reopen evidence affected by later changes. Keep unfinished work isolated and record the exact blocker. Do not silently defer scope or weaken acceptance to claim completion.
