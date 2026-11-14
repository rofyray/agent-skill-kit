# Parallel delivery and Git plan

Write these rules into the generated driver's execution contract, adapting them to actual project conventions and host capabilities. They govern later implementation, not PRD authoring.

## Schedule independent ready work

The coordinator spawns as many useful subagents as available capacity and independent ready tasks permit. Keep capacity occupied by assigning newly ready work as tasks finish. Do not impose an arbitrary one-worker or one-task-per-turn limit. If subagents are unavailable, follow the same dependency order sequentially and report the limitation.

Eligibility requires satisfied dependencies, available required inputs, an agreed contract where needed, and no conflicting writer. Phase numbering alone does not serialize work. Explain actual dependencies or conflicts when tasks cannot run together. A worker does not recursively fan out without the coordinator accounting for capacity and ownership.

Define shared interfaces before consumers depend on them. API and UI work can proceed concurrently against an agreed contract, but tests against a stub do not prove integrated behavior. Assign overlapping files, schemas, lockfiles, and shared infrastructure to a designated owner, or sequence the changes. Use isolated worktrees or equivalent isolation where supported. When isolated editing is unavailable, serialize conflicting mutations while retaining independent work.

Each worker receives task IDs, bounded scope, required spec and asset links, dependencies, acceptance criteria, tests, branch context, and a handoff format. The handoff states changes, evidence, commit or patch, blockers, and interface changes. One coordinator owns shared task status and integration records. Workers report completion rather than racing to edit the driver.

Integrate worker output, inspect compatibility, and rerun affected checks on the combined state. Worker success alone cannot close an integration milestone.

## Branch and commit mapping

Group tasks into coherent features or independently reviewable slices. Record each branch group's scope, task IDs, base, dependencies, and review gate. A feature can span phases. Split large features only when the slices have meaningful integration boundaries.

Independent feature branches may proceed concurrently. Dependent branches wait for their prerequisite integration or use an explicit stacked plan when project policy permits it. Determine default branch and remote from the repository; do not guess. Follow repository naming conventions, otherwise propose `codex/<feature-slug>`.

Commit each completed, verified task, or tightly coupled group that cannot be verified separately. Include its code, tests, and relevant tracking changes; keep unrelated and unfinished changes out. In parallel work, workers commit in their isolated branches and the coordinator integrates into the designated feature branch. Record commit references after creation rather than requiring a commit to contain its own hash.

Distinguish saving a commit, pushing a branch, opening a PR, and merging. State the project's delivery policy and honor existing authorization. The PRD itself grants no new permission. Do not make unrelated work wait on publication unless policy or a dependency requires it. Reuse existing branches and PRs on resume; never recreate completed work merely because publication was unavailable.

## Completion, blockers, and resume

Check a task only when its acceptance criteria and selected required checks pass and its changes are integrated into its designated feature branch. A phase additionally requires its exit behavior. Final completion requires the complete in-scope acceptance gate, including integration and E2E wherever selected, even if every worker task has passed. Git integration into a branch does not by itself require a separate integration-test level; test selection follows behavioral boundaries and impact.

Keep a compact durable record of task states, active branch or worktree, commit references, integration status, evidence locations, blockers, and next eligible tasks. A single small PRD may hold this inline. Preserve unfinished work in isolation before assigning a different task.

Continue authorized ready work until the in-scope product is complete or no unblocked authorized work remains. Record the exact missing input or failing prerequisite when blocked, not just “needs review.” Do not bypass a required gate, weaken criteria, or silently defer scope to create a completion claim.

On resume, read the driver, compact progress record, and relevant canonical task records. Compare them with actual Git and code state. Reuse valid results, check for changed dependencies and stale evidence, and load only specifications needed for eligible work. Separate implementation, verification, PR readiness, and release status.
