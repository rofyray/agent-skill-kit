# {{Product}} PRD

Status: {{reviewable draft or implementation-ready; blockers}}

## Product and scope

{{Problem, users, outcomes, in-scope journeys, exclusions, global constraints, and decision status.}}

## Read only what your task needs

| Document or input | Read when | Authoritative for |
| --- | --- | --- |
| {{relative feature link}} | {{task IDs or behavior}} | {{requirements and canonical task checkboxes}} |
| {{relative contract link, if needed}} | {{producer or consumer change}} | {{shared interface}} |
| {{testing link}} | {{selecting checks or accepting integrated work}} | {{commands, impact policy, final acceptance}} |
| {{resource inventory, if needed}} | {{selecting supplied code, data, or assets}} | {{versions, use, provenance, access}} |
| {{progress location}} | {{resuming or integrating work}} | {{branches, evidence, blockers}} |

{{Declare any required repository revision or external inputs. Do not use source-chat-only identifiers. Omit unnecessary files and rows.}}

## Feature, phase, and branch map

| Feature/branch group | Phases and canonical task links | Base and dependencies | Parallel ownership | Integrated exit gate |
| --- | --- | --- | --- | --- |
| {{group}} | {{links}} | {{base and prerequisites}} | {{owners or scope}} | {{observable result}} |

{{Requirements-to-tasks-to-verification map or direct links to the canonical feature maps. Avoid duplicate status checkboxes here.}}

## Implementation contract

1. Read applicable project instructions and relevant inputs, inspect actual code and Git state, and resolve only the decisions needed for ready work. Preserve unrelated changes.
2. Spawn as many useful subagents as available capacity and independent ready tasks allow; refill capacity as tasks finish. Phase numbers do not add dependencies. Without subagents, execute the same dependency plan sequentially.
3. Settle shared contracts before dependent work. Assign one writer per conflicting scope, use isolated worktrees or equivalent where supported, and sequence conflicts when isolation is unavailable. Workers do not independently consume unaccounted agent capacity.
4. Give workers task IDs, scope, spec and resource links, prerequisites, acceptance, tests, and branch context. Require a handoff of changes, evidence, commit or patch, and blockers. The coordinator owns shared status and integration.
5. Reuse supplied code and assets. Integrate worker changes and rerun affected checks on the combined state. Check canonical tasks only when their acceptance and required tests pass and their work reaches the designated feature branch.
6. Commit verified tasks or inseparable groups with tests and tracking. Follow branch and publication policy below. Distinguish saved commits, pushes, PRs, merges, and release.
7. Continue ready authorized work until complete or all remaining work is blocked. Record exact blockers and preserve unfinished work in isolation. Do not require repeated next-task prompts.
8. On resume, read this driver and compact progress record, compare with actual repository state, reuse valid results, and load only the specs needed for eligible work. Reopen evidence affected by changed requirements, resources, or integrations.

Branch policy: {{repository conventions, feature groups, base discovery, dependent/stacked branch rules, integration owner, and existing publication authorization. Use codex/<feature-slug> only as a fallback.}}

## Whole-product completion

{{Link to explicit final integration and acceptance tasks with prerequisites and owner.}}

Completion requires every in-scope requirement implemented, feature work combined and running, required resources functioning, all defined end-to-end journeys and the full applicable suite passing, and required nonfunctional checks satisfied on the integrated revision. Required service boundaries must be exercised in an authorized test environment. Mocked-only results, missing checks, and unavailable required services cannot establish completion.

Fix integration failures and rerun affected checks. Record revision, environment, checks, outcomes, and evidence. Keep implementation, verification, and release status separate. Scope changes must be explicit; do not silently defer requirements or weaken acceptance.

## Open decisions and delivery

{{Questions, assumptions, access limitations, and affected task IDs. State what remains unresolved and whether it blocks implementation.}}

{{Archive inventory summary and extraction entry point. State actual handoff checks performed. Product test results remain pending until implementation.}}
