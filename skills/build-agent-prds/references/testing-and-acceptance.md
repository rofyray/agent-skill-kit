# Test selection and complete acceptance

## Choose levels from the PRD's scope

Before assigning tests, inspect requirements, implementation boundaries, dependencies, complete user or system workflows, affected consumers, and existing project gates. Choose the smallest set of test levels that fully verifies this scope and its regression risks. Consider unit, integration, and end-to-end (E2E) separately; do not require all three for every PRD or every task.

| Level | What it establishes | Include when |
| --- | --- | --- |
| Unit | Individual logic or behavior in isolation, such as parsing, calculations, validation, or state transitions. | Requirements or affected behavior can be checked independently. |
| Integration | Actual collaboration across selected components or boundaries, such as a service using a database, filesystem, or API adapter. | Correctness depends on those interactions or the change may break existing consumers. |
| E2E | A complete user or system workflow through its real entry point and relevant downstream effects. | An in-scope or affected workflow needs proof that the assembled system delivers the required outcome. |

Classify by the boundary exercised, not the tool or filename. An API test may be unit, integration, or E2E depending on what it invokes. E2E can use a browser, CLI, API, or pipeline; it does not imply browser automation. Smoke/critical selects important checks, and full/regression selects suite scope; neither is a separate test level.

Record all three levels in a compact applicability table in the PRD or its linked testing document:

| Level | Applicability | Scope and reason | Requirement/task/scenario references |
| --- | --- | --- | --- |
| Unit | Required, not applicable, or pending discovery | What isolated behavior needs proof, or why none does | Relevant IDs |
| Integration | Required, not applicable, or pending discovery | Which actual boundaries need proof, or why none are affected | Relevant IDs |
| E2E | Required, not applicable, or pending discovery | Which complete workflows need proof, or why none are in scope or affected | Relevant IDs |

Examples, subject to actual impact and project rules:

- A standalone pure formatter with no consumers or external boundaries in scope may need unit tests only. Final acceptance checks the entire function contract; do not invent an app or E2E harness.
- A database adapter with independent validation and database behavior may need unit and integration tests. E2E may be not applicable when no complete application workflow is in scope or affected.
- A feature spanning UI, service, and persistence generally needs all three: isolated logic, actual boundary interactions, and complete user journeys. Its individual tasks need only the levels they own; feature acceptance covers the combined behavior.

These are examples, not a mandatory progression or fixed combinations. Omitted levels need a concrete scope-based reason. Preserve existing mandatory gates; small diffs and absent tests do not justify waiving them. Unknown architecture or impact is pending discovery with an owner/task to resolve it, not evidence of non-applicability. Resolve pending applicability before accepting affected work or declaring final completion.

Keep applicability separate from execution status. A required integration test with missing credentials is **required and blocked**, not not-applicable. Track runs as passed, failed, blocked, or not run. A newly discovered boundary or changed requirement reopens selection and affected evidence.

## Map tests to requirements and tasks

For each requirement, identify the selected levels, concrete behavior and expected result, fixture/environment, responsible task or feature gate, and existing test or new test to add. Reuse existing tests when their assertions and execution boundary actually cover the requirement. Add or extend coverage for gaps; do not duplicate tests merely to populate three categories.

Each task names the checks it owns and links any shared integration or E2E gate. A feature-level gate proves combined behavior where needed. Detailed edge cases usually belong in lower-level checks, with fewer complete workflow checks. Assertions must detect meaningful behavioral failures, not mirror implementation structure. For prose or asset-only changes, use appropriate observable verification; do not fabricate unit tests or executable product boundaries.

## Fully verify tasks with layered checks

Every implemented task needs evidence for all acceptance criteria and affected behavior. Run the selected levels at appropriate stages; applicability and execution timing are separate decisions. This does not require running the entire repository suite after every small edit. When all three levels apply, favor fast unit tests, integration checks for actual boundaries, and fewer high-value E2E journeys.

| Stage | Required scope |
| --- | --- |
| Development | Changed tests and nearby fast checks. |
| Task completion and commit | Acceptance criteria, affected module tests, relevant integration checks, applicable lint/typecheck, and triggered smoke checks. |
| Feature or phase completion | All milestone criteria; combined behavior and impacted integration/E2E checks where required. |
| PR gate | Impacted tests, applicable static checks, and required critical smoke checks. |
| Merge to main | Broader impacted checks, including integration tests where applicable. |
| Nightly and release candidate | Full applicable regression suite, including E2E and supported browsers where relevant. |
| Before risky refactor or release; final implementation handoff | Full applicable suite plus acceptance checks not represented in that suite. |

Adapt cadence to the product and existing policy; state reasons for material deviations. Scheduled full-suite checks are a regression safety net, not a substitute for task verification. If required scheduling or test infrastructure is absent, name a setup task and interim required checks. Do not invent CI or introduce irrelevant test levels to fill this schedule. The full applicable suite means the complete suite required by scope, impact, and project policy; for an isolated unit-only PRD it may be entirely unit tests.

## Select by impact

- Isolated changes require their tests and relevant component or service checks.
- Shared libraries, authentication, routing, database models, clients, design systems, and build configuration require dependent coverage. If dependency mapping is unclear, run the full relevant suite.
- Payments, permissions, migrations, deployment configuration, and other high-impact behavior require broader regression and complete workflow checks wherever those workflows are affected. Decide from the actual boundary and risk, not a keyword alone.
- In monorepos, package filters must include dependents of changed shared packages. Affected-test selection is a speed optimization and must be paired with scheduled full-suite runs.

Keep tests isolated, deterministic where feasible, and independent of execution order or shared mutable state. Parallelize independent test files when supported. Favor unit or API checks over browser tests when they establish the behavior. Keep smoke coverage short enough to serve as a frequent gate. Track flaky or slow checks; do not hide a new regression by deleting assertions or quarantining required coverage without an explicit resolution.

## Commands and evidence

For required levels, identify existing or needed unit, integration, and E2E suites and smoke/critical/full selections. Record actual commands, working directory, environment, fixtures, and dependencies. Verify commands in repository scripts or configuration. Mark proposed commands pending the task that creates them. Do not add commands for not-applicable levels or assume a universal `test:full` command.

Evidence identifies task or scenario, code revision, environment, command or manual procedure, expected and actual outcome, and an artifact or log location. Distinguish passed, failed, blocked, and not run. Label existing failures separately, but keep unmet required gates visible. Rerun checks affected by integration or subsequent changes; evidence from incompatible revisions cannot be combined into a final pass.

## Final acceptance and required workflow tests

Always include explicit final acceptance work with an owner and dependencies; a small project can include it in an existing task or phase. Add distinct integration and E2E tasks only where the applicability decision requires them. Final acceptance proves the entire agreed scope, but is not itself a requirement for a separate E2E suite. A unit-only PRD can complete through unit coverage of its full contract plus applicable project checks.

Where integration or E2E applies, map each required boundary or complete workflow to a scenario. Every in-scope or affected journey must have acceptance evidence; use lower-level checks for detailed edge cases rather than multiplying slow E2E tests unnecessarily.

For each scenario specify:

1. User or system entry point, prerequisites, environment, and test data.
2. Actions, expected visible or machine-observable results, and persistence or downstream effects.
3. Relevant failure, boundary, permission, and recovery behavior.
4. Check method, evidence to retain, responsible task, and pass condition.

Use a browser for browser journeys, CLI for command workflows, API for service workflows, or appropriate pipeline checks. Required real service boundaries must be exercised in an authorized test or sandbox environment. Mocks are useful for isolated logic and controlled failure cases but do not prove the actual boundary they replace. Missing service access leaves a required check blocked; it does not require a production action.

## Final completion gate

Write this contract into the delivered PRD:

- Every in-scope requirement is implemented and mapped to passing acceptance evidence. Scope changes are explicit.
- All test levels have a resolved applicability decision with reasons for omissions; no required gate is reclassified merely because it cannot run.
- Changes are combined in the designated delivery state and the in-scope artifact functions in its specified environment. Require application build/run checks when there is an application in scope.
- Required code, data, images, and other resources are used correctly and verified as applicable to the deliverable.
- All required test levels, acceptance checks, the full applicable suite, and required nonfunctional checks pass against the final relevant code state. This includes integrated and end-to-end checks whenever required by scope or impact.
- Discovered defects are fixed and affected checks rerun. No required work or verification remains blocked or unrun.
- The final handoff records revision, environment, results, evidence, and release status separately.

“Completely tested” means satisfying this explicit acceptance and coverage contract. It is not proof that every conceivable defect is absent. Drafting the PRD can establish these gates but cannot produce future implementation results.
