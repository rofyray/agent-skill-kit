# Craft Goal-Driven Prompts Help

Use this reference to answer help mode. Present the explanation, modes, start guidance, and examples in a detailed but scannable user-facing form. Include every named mode and both example columns; do not collapse or omit them for brevity. Do not draft or execute the user's task while answering help.

## What this skill does

This skill turns a goal into a ready-to-use agent prompt that is precise about the desired outcome, context, constraints, authority, deliverables, verification, and definition of done without unnecessarily dictating every implementation step.

It can create a normal prompt, add an evidence-driven improvement loop, or execute the resulting prompt when the user explicitly asks this agent to perform the underlying work. It asks only for missing choices that materially change the result and labels safe assumptions instead of blocking on trivia.

## Modes

| Mode | Use it for |
| --- | --- |
| `draft` | Turn a goal or rough request into a polished prompt. This is the default. |
| `loop-ready` | Add an observe, grade, improve, and retest loop with a measurable pass bar. |
| `execute` | Perform the underlying task and iterate against the prompt's completion criteria. Use only when execution is explicitly requested. |
| `help` | Display this guide without drafting a prompt or executing a task. |

The user can name a mode or describe the outcome naturally. No slash command is required.

## Start here

Provide the goal and, when known, the target agent or tool, important inputs, non-negotiable rules, desired output, and what success should look like. A rough one-line goal is enough to begin; the skill will propose observable completion criteria when the user has not defined them.

Draft and loop-ready modes return a prompt rather than running it. Execute mode remains limited by the active host's tools, permissions, approvals, and the scope the user authorized.

## Examples

| Mode | Starter | Another example |
| --- | --- | --- |
| `draft` | `Turn this goal into a ready-to-use prompt: redesign our onboarding so more users finish setup.` | `Improve this prompt for a research agent and make the required evidence and deliverable explicit.` |
| `loop-ready` | `Create a prompt that keeps improving a landing page until the real user flow and visual rubric pass.` | `Make this image-generation prompt loop-ready so each result is compared with the reference before the next revision.` |
| `execute` | `Use the finished prompt to improve this local page and continue until its acceptance checks pass.` | `Execute this research prompt, verify every material claim, and return the completed brief with evidence.` |
| `help` | `Help` | `Show me every prompt-crafting mode and examples without drafting anything yet.` |

End the help response by asking which mode the user wants or inviting them to paste a goal or existing prompt.
