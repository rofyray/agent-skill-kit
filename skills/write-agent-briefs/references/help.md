# Write Agent Briefs Help

Use this reference to answer help mode. Present the explanation, modes, start guidance, and examples in a detailed but scannable user-facing form. Include every named mode and both example columns; do not collapse or omit them for brevity. Do not draft, revise, audit, or execute a brief while answering help.

## What this skill does

This skill turns work into a self-contained brief another AI agent can execute without silently guessing the objective, context, inputs, constraints, authority, verification, or required output. It uses the three C's - Context, Constraints, and Composition - and makes completion depend on observable evidence rather than the executing agent's confidence.

It normally returns the brief instead of performing the delegated task. If the user also wants execution, that must be requested explicitly and remains subject to the active environment and permissions.

## Modes

| Mode | Use it for |
| --- | --- |
| `draft` | Create a complete agent brief from a goal or rough task description. |
| `improve` | Strengthen an existing brief while preserving its intent. |
| `audit` | Identify missing or weak context, constraints, verification, and deliverable structure; optionally return a corrected version. |
| `help` | Display this guide without drafting, improving, or auditing a brief. |

The user can name a mode or describe the outcome naturally. No slash command is required.

## Start here

Provide the task and any known audience, source files or URLs, required output, constraints, and definition of done. A rough request is enough to begin. The skill will inspect supplied artifacts when accessible, ask only high-value blocking questions, and use visible placeholders instead of inventing missing paths or facts.

## Examples

| Mode | Starter | Another example |
| --- | --- | --- |
| `draft` | `Write an agent brief to create our Q3 board deck from the metrics workbook and last quarter's deck.` | `Turn this bug report into an executable coding-agent brief with reproduction and regression checks.` |
| `improve` | `Improve this brief: Fix the checkout total bug.` | `Strengthen this research prompt so its sources, comparison criteria, and final decision memo are explicit.` |
| `audit` | `Audit this brief: Research our competitors and tell me what to do.` | `Find hidden assumptions and weak verification in this agent task, then show me a corrected brief.` |
| `help` | `Help` | `Show me every agent-brief mode and examples without drafting a brief yet.` |

End the help response by asking which mode the user wants or inviting them to paste a task or existing brief.
