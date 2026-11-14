# Testing and whole-product acceptance

## Fully verify tasks with layered checks

Every implemented task needs evidence for all acceptance criteria and affected behavior. This does not require running the entire repository suite after every small edit. Use mostly fast unit tests, integration tests for boundaries, and fewer high-value end-to-end checks for behavior that lower layers cannot establish.

| Stage | Required scope |
| --- | --- |
| Development | Changed tests and nearby fast checks. |
| Task completion and commit | Acceptance criteria, affected module tests, relevant integration checks, applicable lint/typecheck, and triggered smoke checks. |
| Feature or phase integration | Combined behavior, shared interfaces, impacted integration tests, and critical journeys. |
| PR gate | Impacted tests, applicable static checks, and critical smoke tests. |
| Merge to main | Broader impacted integration checks. |
| Nightly and release candidate | Full applicable regression suite, including E2E and supported browsers where relevant. |
| Before risky refactor or release; final implementation handoff | Full applicable suite plus acceptance checks not represented in that suite. |

Adapt to the product and existing policy; state reasons for material deviations. Scheduled full-suite checks are a regression safety net, not a substitute for task verification. If scheduling or test infrastructure is absent, name a setup task and interim required checks. Do not claim CI exists because a template lists it.

## Select by impact

- Isolated changes require their tests and relevant component or service checks.
- Shared libraries, authentication, routing, database models, clients, design systems, and build configuration require dependent coverage. If dependency mapping is unclear, run the full relevant suite.
- Payments, permissions, migrations, deployment configuration, and other high-impact behavior require broader regression and critical end-to-end coverage.
- In monorepos, package filters must include dependents of changed shared packages. Affected-test selection is a speed optimization and must be paired with scheduled full-suite runs.

Keep tests isolated, deterministic where feasible, and independent of execution order or shared mutable state. Parallelize independent test files when supported. Favor unit or API checks over browser tests when they establish the behavior. Keep smoke coverage short enough to serve as a frequent gate. Track flaky or slow checks; do not hide a new regression by deleting assertions or quarantining required coverage without an explicit resolution.

## Commands and evidence

Identify how the project selects unit, integration, E2E, smoke/critical, and full/regression suites. Record actual commands, working directory, environment, fixtures, and dependencies. Verify commands in repository scripts or configuration. Mark proposed commands pending the task that creates them. No universal `test:full` command should be assumed.

Evidence identifies task or scenario, code revision, environment, command or manual procedure, expected and actual outcome, and an artifact or log location. Distinguish passed, failed, blocked, and not run. Label existing failures separately, but keep unmet required gates visible. Rerun checks affected by integration or subsequent changes; evidence from incompatible revisions cannot be combined into a final pass.

## End-to-end acceptance design

Include explicit integration and final acceptance tasks, with an owner and dependencies. A small project can put them in its single phase; a larger project may have a dedicated final phase. Map every in-scope journey and cross-feature interaction to an acceptance scenario, using lower-level tests for detailed edge cases rather than multiplying slow E2E tests unnecessarily.

For each scenario specify:

1. User or system entry point, prerequisites, environment, and test data.
2. Actions, expected visible or machine-observable results, and persistence or downstream effects.
3. Relevant failure, boundary, permission, and recovery behavior.
4. Check method, evidence to retain, responsible task, and pass condition.

Use a browser for browser journeys, CLI for command workflows, API for service workflows, or appropriate pipeline checks. Real service boundaries must be exercised in an authorized test or sandbox environment. Mocked tests alone do not prove real integration. Missing service access leaves that check blocked; it does not require a production action.

## Final completion gate

Write this contract into the delivered PRD:

- Every in-scope requirement is implemented and mapped to passing acceptance evidence. Scope changes are explicit.
- Feature work is combined in the designated integration state; the application builds and runs in the specified environment.
- Required code, data, images, and other resources are used correctly and load in the running product.
- All defined end-to-end scenarios, the full applicable suite, and required nonfunctional checks pass against the integrated revision.
- Discovered defects are fixed and affected checks rerun. No required work or verification remains blocked or unrun.
- The final handoff records revision, environment, results, evidence, and release status separately.

“Completely tested” means satisfying this explicit acceptance and coverage contract. It is not proof that every conceivable defect is absent. Drafting the PRD can establish these gates but cannot produce future implementation results.
