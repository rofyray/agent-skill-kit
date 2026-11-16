# Build Agent PRDs Help

## What this skill does

Creates product requirements that coding agents can implement through phased checkbox tasks, parallel workstreams, feature branches, and complete acceptance of the agreed scope. Selects unit, integration, and E2E tests according to behavior, boundaries, and impact: an isolated function may need unit tests only, while an application workflow may need all three. Preserves existing code, data, images, and links so a new agent can use the handoff without the original chat. Delivers a small PRD as one file or a larger set with its resources as one ZIP.

It writes and assesses the implementation plan; it does not start building the product unless separately requested. Every test level is required, not applicable with a reason, or pending discovery. Missing access blocks required checks rather than removing them. A PRD can define tests without claiming they have already passed.

Every generated PRD carries a lowercase Git contract: commits use `type(optional-scope): short description`; branches use `<type>/<short-description>` or optionally `<type>/<ticket-id>-<short-description>`. Internal PRD task IDs remain stable even when branch names omit IDs. The guide distinguishes commit types, formatting from UI changes, and hotfix/release branch categories. Existing history is preserved and conflicts with enforced repository rules are surfaced.

## Modes

- **Create:** draft a PRD from goals, conversation context, existing code, and resources.
- **Revise:** change an existing PRD while preserving IDs, valid history, and asset provenance; reopen affected work and rebuild the ZIP.
- **Audit:** identify missing requirements, broken handoffs, infeasible parallelism, and weak completion gates. Rewrite only when requested.
- **Help:** explain the skill and examples without drafting or editing a PRD.

Modes are natural-language hints, not slash commands.

## Start here

Describe the product, intended users, desired outcomes, and known scope. Supply relevant project material and reusable assets if available. For revisions or audits, provide the existing PRD file or bundle. State constraints, preferred output destination, and whether available ticket IDs should appear in branch names when known. Without an established ID preference, names can omit IDs while planning proceeds.

The skill first uses accessible evidence, then asks about material gaps. It can draft without repository access, but labels unknown architecture and commands for discovery. File and archive capabilities determine whether it can deliver the ZIP directly; missing capabilities and inaccessible resources remain explicit.

## Examples

| Mode | Starter | Additional example |
| --- | --- | --- |
| Create | “Write a small PRD for a standalone formatting function and select the tests its scope needs.” | “Turn this project chat, API example, approved mockup, and sample records into a phased PRD. Select unit, integration, and E2E coverage, plan parallel feature branches, and package everything as a ZIP.” |
| Revise | “Add password recovery to this PRD and update its acceptance tests.” | “Update this PRD to lowercase commits and branches, include PROJ-42 in the feature branch name, preserve existing history and assets, and rebuild its ZIP.” |
| Audit | “Audit this PRD for gaps before an agent implements it.” | “Check whether a new agent can use this ZIP without our chat, build the parallel workstreams, and prove the full product works end to end.” |
| Help | “help” | “Show how to use this skill to turn an existing project conversation into an implementation handoff.” |

Invite the user to choose a mode or adapt an example.
