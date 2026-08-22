---
name: craft-goal-driven-prompts
description: Turn a goal into a structured agent prompt with constraints, measurable completion criteria, verification, and an optional improvement loop. Use when drafting or strengthening an agent prompt.
---

# Craft Goal-Driven Prompts

Turn an intended outcome into a prompt that gives the executing agent freedom over the method while holding it to explicit constraints and an observable completion bar.

## Help mode

When the user sends `help`, `show help`, `what can this skill do?`, or `how do I use this skill?` after selecting or naming this skill, read [the help guide](references/help.md). Return its explanation, modes, starting guidance, and examples without drafting or executing a prompt. Include every named mode and at least two examples for each mode: one simple starter and one additional realistic example. Do not omit modes or examples for brevity. End by inviting the user to choose a mode or adapt an example.

Do not confuse help mode with an action request such as “help me write a prompt.”

## Choose the mode

Infer the mode from the request:

- **Draft**: Produce a ready-to-paste prompt. Use by default.
- **Loop-ready draft**: Add a bounded evaluate-improve protocol to the prompt.
- **Execute**: Carry out the prompt and iterate when the user explicitly asks this agent to do the work, not merely write the prompt.

Do not begin execution when the user only asks to craft, rewrite, or improve a prompt.

## Build the prompt

1. Inspect the conversation and available artifacts before asking for information already provided.
2. Extract the outcome, relevant context, reusable prior work, non-negotiable rules, success evidence, authority boundaries, deliverables, and known risks.
3. Separate the **goal** from the **method**. Preserve required procedures, but remove speculative step-by-step directions that unnecessarily override the executing agent's judgment.
4. Replace vague quality adjectives with tests, comparisons, rubrics, or observable acceptance criteria. If the user cannot supply a bar, propose one and label the assumption.
5. Distinguish hard constraints from preferences. Include only house rules that must remain true regardless of the chosen method.
6. Specify what the agent may decide independently and what requires approval. A request to loop does not authorize purchases, destructive actions, production changes, credential handling, or external communication.
7. Preserve an explicit “until done” instruction. Do not invent a fixed iteration cap; ask for a cost or time budget only when it materially affects the work, or leave it as an explicit open choice in a draft.
8. Use [the prompt schema](references/prompt-schema.md) to assemble the prompt. Omit sections that do not affect execution.
9. Ask at most a small set of grouped questions only when an unanswered choice would materially change the prompt. Otherwise proceed with explicit assumptions.

Keep the prompt detailed about the destination, boundaries, and proof, but economical about the route.

## Design the completion bar

Make every required criterion independently checkable. Prefer evidence from the real output or environment: tests, rendered pixels, observed behavior, source citations, measurements, user journeys, or artifact inspection.

When no direct metric exists:

1. Define a short rubric with observable anchors.
2. Identify a reference artifact or baseline when available.
3. Require the evaluator to cite evidence for each score.
4. Set a pass threshold and declare any criterion that must pass absolutely.

Do not let the builder's explanation substitute for inspecting the output.

## Add or run the loop

Read [the loop protocol](references/loop-protocol.md) when the user requests a loop-ready prompt or execution until done.

During execution, continue while safe, authorized, and making measurable progress. Evaluate the actual artifact against the completion bar, identify the largest remaining gap, improve it, and re-evaluate. Use an independent or fresh-context grader when the host supports one; give the grader the artifact and rubric, not the builder's rationale.

Do not replace “until done” with an arbitrary attempt count. When paid services, scarce compute, or a real deadline make a budget necessary and none is provided, obtain the budget before incurring that cost; continue safe in-scope work that does not need the missing authority.

Finish only when every required criterion passes with evidence. Stop earlier only for a genuine blocker, a required approval, an exhausted user-defined budget, or repeated lack of measurable progress. Report the specific condition rather than claiming success.

## Return the result

For draft modes, return:

1. **Ready-to-use prompt** in one copyable block.
2. **Assumptions or open choices** only when material.
3. **Usage note** only when the target tool needs a known invocation detail.

For execute mode, keep a concise progress record and return the completed artifact or location, the acceptance evidence, material decisions, and any remaining limitations.

Read [worked examples](references/examples.md) only when the user requests examples or the domain is ambiguous enough that a pattern would materially improve the prompt.
