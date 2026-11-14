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
  - Verify: {{selected test levels, concrete checks and expected outcomes; reuse existing coverage and link shared feature gates}}
  - Evidence: pending

{{Repeat phases and tasks as the work requires. Include explicit final acceptance work with dependencies and an owner, within an existing task when sufficient. Add integration and E2E tasks where required by the applicability decision below. Each task has only one canonical checkbox.}}

## Verification and final acceptance

| Test level | Applicability | Scope and reason | Requirement/task/scenario references |
| --- | --- | --- | --- |
| Unit | {{required, not applicable, or pending discovery}} | {{isolated behavior or omission reason}} | {{IDs; discovery owner/task if pending}} |
| Integration | {{required, not applicable, or pending discovery}} | {{actual boundaries or omission reason}} | {{IDs; discovery owner/task if pending}} |
| E2E | {{required, not applicable, or pending discovery}} | {{complete workflows or omission reason}} | {{IDs; discovery owner/task if pending}} |

{{Select from requirements, dependencies, impact, and existing project gates. For each requirement, map selected checks, existing tests to reuse or new coverage, fixtures, expected outcomes, and an owner. Actual command map for required levels only, with working directories and environments; unknown commands need a discovery/setup task.}}

Applicability and execution status are separate. Missing access or tools leave a required check blocked, not not-applicable. Resolve pending selection before accepting affected work. Do not invent an application, browser harness, or duplicate tests to fill categories; preserve existing required gates.

Use targeted checks while coding; complete acceptance and selected affected checks before task completion. Run required critical smoke and applicable static checks at PR gates, broader affected checks after merge, and scheduled regression checks according to project policy. Shared or high-risk changes widen scope; uncertain impact requires discovery and the full relevant suite. Run the full applicable suite before risky refactors, releases, and final handoff. For unit-only scope that suite may consist entirely of unit tests.

| Check/scenario and level | Prerequisites and data | Actions | Expected result and applicable downstream effects | Failure/boundary checks | Owner, method, and evidence |
| --- | --- | --- | --- | --- | --- |
| {{ID and selected level}} | {{inputs}} | {{steps}} | {{observations}} | {{cases}} | {{task, procedure, and receipt}} |

Completion requires every in-scope requirement implemented and verified, all test-level decisions resolved with omission reasons, the deliverable functioning in its stated environment, required resources working, and all required test levels, acceptance checks, the full applicable suite, and nonfunctional checks passing on the final relevant code state. Final acceptance is not automatically a separate E2E suite. Where integration/E2E is required, exercise the assembled behavior and actual boundaries in an authorized test environment; mocks cannot prove the boundaries they replace. Fix failures and rerun affected checks. Missing required tests or services leave verification blocked. Record revision, environment, actual results, and evidence. Release status is separate.

## Progress and resume

{{Compact branch, commit, integration, blocker, evidence, and next-ready-work record.}}

Check a task only after acceptance and required tests pass and its changes are integrated into its feature branch. Phase exit and final completion require their scope-appropriate acceptance gates. Git integration does not automatically require an integration-test level. On resume compare this record with actual repository state, preserve valid results, reassess changed test-level applicability, and reopen stale evidence. Keep unfinished work isolated and record the exact blocker. Do not silently defer scope or weaken acceptance to claim completion.
