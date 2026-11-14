# PRD structure

## Product before backlog

Start with the problem, intended users, desired outcomes, scope, exclusions, and observable user or system journeys. Describe behavior and relevant constraints without prescribing incidental implementation details. Include architecture decisions only when supplied, evidenced, or needed to settle a material interface. Label proposed decisions.

Assign stable requirement IDs and connect each to implementing tasks and acceptance scenarios. A compact table is enough. Success criteria must be observable; distinguish a product outcome measured after launch from a pre-release acceptance check. Do not invent numerical targets.

## Choose the document boundary

Use one file for a small feature whose context remains easy to navigate. Split when independent features, substantial shared contracts, or resource collections would otherwise force repeated reading. File count follows useful reading boundaries, not an arbitrary size quota.

Suggested layout, creating only needed files:

```text
project-prd/
  PRD.md
  features/
    accounts.md
    workspace.md
  contracts.md
  testing.md
  resources.md
  progress.md
  assets/
  examples/
```

The driver contains product context, global constraints, the phase and feature map, dependencies, branch groups, execution and completion rules, and a reading map. Details live in the document that owns them. Each link names its trigger, such as “Read the session contract before changing any session producer or consumer.” Link directly to needed content rather than through chains of indexes.

Detailed feature files own their requirements, phases, task checkboxes, and specific tests. Shared contracts define producer and consumer expectations once. For a single document, use linked sections with the same responsibilities. Keep receipts and lengthy logs out of the driver.

## Task contract

Use stable IDs such as `AC-03`, independent of phase numbering. Every task includes:

- an unchecked Markdown checkbox until complete;
- the observable result and requirement IDs;
- acceptance criteria, including relevant failure and boundary behavior;
- explicit dependencies by ID and any external blockers;
- input specifications, contracts, reusable resources, and their locations;
- a bounded implementation scope, ownership or conflict notes where needed;
- feature branch group and task-specific verification;
- state and evidence location, initially pending.

Use compact records for small tasks and more detail when ambiguity warrants it. File ownership may be provisional until repository discovery. Verification may be manual when that is the appropriate observable check; do not manufacture unit tests for prose edits.

Use one canonical checkbox and state per task. READY means dependencies and required inputs are satisfied; ACTIVE means claimed by a worker; BLOCKED names the missing condition; DONE requires passing acceptance and integration into its designated feature branch. TODO can represent work whose prerequisites are not yet satisfied. Preserve equivalent project vocabulary where it is clear.

## Milestones and traceability

A feature is a product capability. A phase is a milestone with entry conditions and an observable exit gate. A branch is a reviewable delivery scope. One feature can span phases; unrelated ready work can cross phase boundaries. Do not make all phase tasks wait unless an explicit gate requires it.

Decompose around independently verifiable outcomes. Avoid separate “write tests later” tasks that leave implementation tasks unchecked by evidence. A shared test harness or final cross-feature integration can be its own task, while each implementation task still owns relevant tests.

Review the requirements-to-tasks-to-verification map for missing behavior, orphan tasks, dependency cycles, dangling IDs, conflicting ownership, and scope changes. Include explicit final integration and end-to-end acceptance tasks. A checklist of finished files is not a working-product milestone.

## Revisions

Preserve IDs and genuine historical completion. When a requirement or resource changes, identify all consumers and mark affected verification stale. Reopen tasks whose acceptance no longer holds; retain the prior result as history. Add new IDs for new work and mark removed scope retired rather than silently dropping it. Keep dependent schedules, branch maps, and packaged files consistent.
