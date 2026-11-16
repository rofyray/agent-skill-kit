# Parallel delivery and Git plan

Write these rules into the generated driver's execution contract, accounting for actual project rules and host capabilities. Include the complete lowercase Git naming contract in that driver; surface any conflict with enforced rules rather than silently replacing it. These rules govern later implementation, not PRD authoring.

## Schedule independent ready work

The coordinator spawns as many useful subagents as available capacity and independent ready tasks permit. Keep capacity occupied by assigning newly ready work as tasks finish. Do not impose an arbitrary one-worker or one-task-per-turn limit. If subagents are unavailable, follow the same dependency order sequentially and report the limitation.

Eligibility requires satisfied dependencies, available required inputs, an agreed contract where needed, and no conflicting writer. Phase numbering alone does not serialize work. Explain actual dependencies or conflicts when tasks cannot run together. A worker does not recursively fan out without the coordinator accounting for capacity and ownership.

Define shared interfaces before consumers depend on them. API and UI work can proceed concurrently against an agreed contract, but tests against a stub do not prove integrated behavior. Assign overlapping files, schemas, lockfiles, and shared infrastructure to a designated owner, or sequence the changes. Use isolated worktrees or equivalent isolation where supported. When isolated editing is unavailable, serialize conflicting mutations while retaining independent work.

Each worker receives task IDs, bounded scope, required spec and asset links, dependencies, acceptance criteria, tests, branch context, and a handoff format. The handoff states changes, evidence, commit or patch, blockers, and interface changes. One coordinator owns shared task status and integration records. Workers report completion rather than racing to edit the driver.

Integrate worker output, inspect compatibility, and rerun affected checks on the combined state. Worker success alone cannot close an integration milestone.

## Branch and commit mapping

Group tasks into coherent features or independently reviewable slices. Record each branch group's lowercase proposed name, purpose/type, scope, canonical task/ticket mapping, base, dependencies, and review gate. A feature can span phases and include commits of different types. Split large features only when the slices have meaningful integration boundaries.

Independent feature branches may proceed concurrently. Dependent branches wait for their prerequisite integration or use an explicit stacked plan when project policy permits it. Determine default branch and remote from the repository; do not guess. New branches use `<type>/<short-description>` or `<type>/<ticket-id>-<short-description>` when ID inclusion is selected and an actual ID exists. All branch text is lowercase; the PRD retains canonical source IDs. Internal task IDs do not automatically become branch IDs. Prefer an ID-free feature name for a group without one applicable ticket; never concatenate its task IDs. Clarify a material ID preference when needed without blocking independent planning.

Commit each completed, verified task, or tightly coupled group that cannot be verified separately. Include its code, tests, and relevant tracking changes; keep unrelated and unfinished changes out. Use `type(optional-scope): short description`, with lowercase type, scope, description, and any authored body/footer. Choose the type by primary intent, not by the branch prefix or presence of tests. In parallel work, workers commit in their isolated branches and the coordinator integrates into the designated feature branch. Record commit references after creation rather than requiring a commit to contain its own hash.

Copy enough naming guidance into the delivered driver for workers without this skill: all eleven commit types with their meanings, formatting-only `style`, specific types before `chore`, optional scope, lowercase branch examples, optional ticket mapping, and the distinction between `hotfix`/`release` branch categories and commit types. Check conflicts with existing enforced naming or required case-sensitive metadata before new Git mutations. Do not lowercase canonical source references or rewrite existing Git history to satisfy the new policy.

Distinguish saving a commit, pushing a branch, opening a PR, and merging. State the project's delivery policy and honor existing authorization. The PRD itself grants no new permission. Do not make unrelated work wait on publication unless policy or a dependency requires it. Reuse existing branches and PRs on resume; never recreate completed work merely because publication was unavailable.

## Completion, blockers, and resume

Check a task only when its acceptance criteria and selected required checks pass and its changes are integrated into its designated feature branch. A phase additionally requires its exit behavior. Final completion requires the complete in-scope acceptance gate, including integration and E2E wherever selected, even if every worker task has passed. Git integration into a branch does not by itself require a separate integration-test level; test selection follows behavioral boundaries and impact.

Keep a compact durable record of task states, active branch or worktree, commit references, integration status, evidence locations, blockers, and next eligible tasks. A single small PRD may hold this inline. Preserve unfinished work in isolation before assigning a different task.

Continue authorized ready work until the in-scope product is complete or no unblocked authorized work remains. Record the exact missing input or failing prerequisite when blocked, not just “needs review.” Do not bypass a required gate, weaken criteria, or silently defer scope to create a completion claim.

On resume, read the driver, compact progress record, and relevant canonical task records. Compare them with actual Git and code state. Reuse valid results, check for changed dependencies and stale evidence, and load only specifications needed for eligible work. Separate implementation, verification, PR readiness, and release status.
