# AI Film Screenwriting Help

## What this skill does

This skill develops, writes, revises, and evaluates feature-length screenplays. It can start from a rough idea, treatment, outline, unfinished script, or complete draft. It maintains story causality, character arcs, scene purpose, setups and payoffs, dialogue voice, and continuity across a long project.

It can also prepare narrative handoffs for visual development, performance direction, and video production. Those handoffs communicate story facts and dramatic intent without replacing the specialized work of those disciplines.

The active language model can write directly in the conversation. Connected tools are optional and become useful when the user wants to import project sources, maintain screenplay files, research facts, export to another application, or use a chosen external model.

## Modes

| Mode | Use it for |
| --- | --- |
| `develop` | Build or strengthen a premise, story bible, characters, treatment, feature structure, sequence map, scene list, or step outline. |
| `draft` | Write new screenplay scenes, sequences, or a complete feature in controlled units. |
| `revise` | Diagnose and rewrite existing material while preserving locked choices and accepted strengths. |
| `coverage` | Evaluate an outline or screenplay and return evidence-based strengths, concerns, and priorities without rewriting unless requested. |
| `help` | Display this guide without performing screenplay work. |

Modes are natural-language hints, not slash commands. The user can name one or simply describe the outcome.

## Start here

Provide whatever already exists: a premise, genre, character idea, treatment, outline, screenplay pages, notes, or a complete draft. State any decisions that must not change and the desired output, such as a beat sheet, treatment, screenplay sequence, revision, coverage report, Fountain file, or production handoff.

Useful but optional context includes the audience, tone, target length, rating, language, comparable works, ending, real-world research requirements, and intended production method. The skill will ask only when a missing choice would materially change the story.

For a long project, identify the canonical draft if more than one version exists. When the host supports files or project storage, the skill can maintain a story bible, outline, screenplay, continuity ledger, and revision log. Without file access, it can still work in conversation and will state exactly which portion has been completed.

### Output choices

- **Conversation**: Return the requested development artifact, screenplay pages, revision, or coverage directly in chat.
- **Persistent project**: Create or update screenplay artifacts in the user's project when file access is available and the user wants persistence.
- **Connected workflow**: Read from or write to an authenticated service, or use a user-selected external model, when the host exposes the required tool.
- **Manual handoff**: Produce a complete copy-and-paste package when the requested service is not connected.

### Connected tools and MCP

Installing this skill does not install a writing, storage, research, or production connector. If the user asks to use one, the skill first checks whether its tools are already available and authenticated.

If no compatible tool is visible, ask the skill to `show connection help for my current app`. It will explain the appropriate ChatGPT, Codex, Claude, or Claude Code path, what capability to look for, how to verify the connection, and how to continue manually. Only connect remote MCP servers from trusted providers, review requested permissions, and never paste API keys into the screenplay or chat prompt.

## Examples

| Mode | Starter | Another example |
| --- | --- | --- |
| `develop` | `Develop this premise into a feature story bible and sequence outline: a paramedic begins receiving emergency calls from tomorrow.` | `Turn these character notes and research files into a restrained historical thriller treatment. Preserve the real timeline, but propose three possible endings before choosing one.` |
| `draft` | `Write the opening ten screenplay pages from this approved outline.` | `Continue the screenplay through sequence four. Use the existing project draft and continuity ledger, preserve all locked dialogue, and update the canonical Fountain file.` |
| `revise` | `Help me fix the slow second act without changing the ending.` | `Rewrite scenes 42 through 48 so Mara causes the midpoint reversal rather than merely witnessing it. Preserve the location, planted evidence, and final line of scene 48.` |
| `coverage` | `Give me coverage on this screenplay and prioritize the three highest-leverage changes.` | `Compare draft three with draft four. Evaluate whether the protagonist became more active, cite affected scenes, and do not rewrite any pages.` |
| `help` | `Help` | `Show me every screenwriting mode, output choice, connector option, and example without working on my screenplay.` |

Choose a mode, attach or identify the available material, or adapt any example above.
