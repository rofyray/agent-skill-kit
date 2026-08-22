---
name: replace-me
description: Describe the outcome and trigger boundary in 200 characters or fewer. Use when the user asks for the concrete tasks that should activate this skill.
---

# Replace Me

## Help mode

When the user sends `help`, `show help`, `what can this skill do?`, or `how do I use this skill?` after selecting or naming this skill, read [the help guide](references/help.md). Return its explanation, modes, starting guidance, and examples without performing the normal workflow. Include every named mode and at least two examples for each mode: one simple starter and one additional realistic example. Do not omit modes or examples for brevity. End by inviting the user to choose a mode or adapt an example.

Do not confuse help mode with an action request that begins with “help me.”

## Workflow

1. Inspect the task, relevant inputs, host capabilities, and permissions.
2. Apply the smallest reliable workflow that produces the requested outcome.
3. Verify the result in proportion to its risk.
4. Report the outcome, evidence, and any remaining limitations.

When a required capability is unavailable, explain the limitation and use a non-executing fallback when practical.

## Resources

Add only the resources this skill needs. Link each resource directly from this file and state when to use it.

- Read `references/help.md` only for help mode. Keep its explanation, mode catalog, start guidance, and examples current.
- Read `references/<topic>.md` only when the task needs that detailed knowledge.
- Run `scripts/<helper>` when the repeated operation requires deterministic behavior.
- Reuse `assets/<file>` when producing the corresponding output.

Keep the help reference even when the skill has no other bundled resources. Remove unused example resource lines.
