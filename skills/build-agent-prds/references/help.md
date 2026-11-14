# Build Agent PRDs Help

## What this skill does

Creates product requirements that coding agents can implement through phased checkbox tasks, parallel workstreams, feature branches, and complete end-to-end acceptance. Preserves existing code, data, images, and links so a new agent can use the handoff without the original chat. Delivers a small PRD as one file or a larger set with its resources as one ZIP.

It writes and assesses the implementation plan; it does not start building the product unless separately requested. A PRD can define tests without claiming they have already passed.

## Modes

- **Create:** draft a PRD from goals, conversation context, existing code, and resources.
- **Revise:** change an existing PRD while preserving IDs, valid history, and asset provenance; reopen affected work and rebuild the ZIP.
- **Audit:** identify missing requirements, broken handoffs, infeasible parallelism, and weak completion gates. Rewrite only when requested.
- **Help:** explain the skill and examples without drafting or editing a PRD.

Modes are natural-language hints, not slash commands.

## Start here

Describe the product, intended users, desired outcomes, and known scope. Supply relevant project material and reusable assets if available. For revisions or audits, provide the existing PRD file or bundle. State constraints and preferred output destination when known.

The skill first uses accessible evidence, then asks about material gaps. It can draft without repository access, but labels unknown architecture and commands for discovery. File and archive capabilities determine whether it can deliver the ZIP directly; missing capabilities and inaccessible resources remain explicit.

## Examples

| Mode | Starter | Additional example |
| --- | --- | --- |
| Create | “Write a small PRD for adding CSV export to our task list.” | “Turn this project chat, API example, approved mockup, and sample records into a phased PRD. Plan parallel feature branches and package everything as a ZIP.” |
| Revise | “Add password recovery to this PRD and update its acceptance tests.” | “Replace the old design with the approved assets, preserve completed task IDs, reopen affected verification, and rebuild the PRD ZIP.” |
| Audit | “Audit this PRD for gaps before an agent implements it.” | “Check whether a new agent can use this ZIP without our chat, build the parallel workstreams, and prove the full product works end to end.” |
| Help | “help” | “Show how to use this skill to turn an existing project conversation into an implementation handoff.” |

Invite the user to choose a mode or adapt an example.
