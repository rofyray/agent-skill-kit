# Build and Maintain a Second Brain Help

Use this reference to answer help mode. Present the explanation, modes, start guidance, and examples in a detailed but scannable user-facing form. Include every named mode and both example columns; do not collapse or omit them for brevity. Do not inspect, create, or change a vault while answering help.

## What this skill does

This skill builds and operates a persistent, source-grounded Markdown knowledge base that can be viewed in Obsidian or any file editor. It preserves original material in `raw/`, compiles durable linked notes into `wiki/`, tracks provenance and operations, answers questions across the collection, checks health, and can configure recurring work when the active runtime can really reach the vault and sources.

The vault - not the chat - is the durable state. The skill can work through a local coding agent, an approved desktop folder connection, or a downloadable handoff when direct file access is unavailable. It never treats Obsidian as mandatory and never claims local automation when the runtime cannot edit the folder.

## Modes

| Mode | Use it for |
| --- | --- |
| `set up` | Create a new vault or safely adapt an existing notes folder. |
| `ingest` | Preserve a file, URL, transcript, image, dataset, or other source and integrate its knowledge. |
| `query` | Ask a question across the wiki and underlying evidence; save durable synthesis when useful. |
| `lint` | Find broken links, weak provenance, contradictions, stale claims, or structural drift without destructive cleanup. |
| `review` | Summarize recent learning, connections, emerging hubs, gaps, and next explorations. |
| `schedule` | Configure recurring ingestion, lint, or review - or an honest reminder when automatic access is unavailable. |
| `help` | Display this guide without inspecting or changing a vault. |

The user can name a mode or describe the outcome naturally. No slash command is required.

## Start here

For a new system, provide the intended folder or say where you want the vault, what knowledge it should cover, and whether you already use Obsidian. For an existing vault, identify the exact folder and what must be preserved. For an operation, attach or connect the vault and provide the source or question.

The skill will check file, shell, browser, desktop, and scheduling capabilities before acting. Setup, app installation, broad folder access, recurring tasks, bulk ingestion, and material migrations may require confirmation.

## Examples

| Mode | Starter | Another example |
| --- | --- | --- |
| `set up` | `Set up a source-grounded second brain for my climate research in this folder.` | `Adapt my existing Obsidian vault without changing its plugins or breaking links.` |
| `ingest` | `Ingest this paper and connect it to what I already know about retrieval systems.` | `Add these meeting notes, preserve the original, and surface conflicts with existing pages.` |
| `query` | `What does my vault say about deliberate practice, and where do the sources disagree?` | `Find the non-obvious connection between feedback loops and organizational learning and save it if useful.` |
| `lint` | `Lint the wiki and report anything that needs attention without deleting content.` | `Check raw-source integrity, provenance, broken links, stale claims, and orphaned pages.` |
| `review` | `Review what I added this week and recommend the strongest thread to explore next.` | `Show the main hubs forming in my vault and the most important missing concept.` |
| `schedule` | `Schedule a local lint every Sunday and run the review afterward.` | `Every weekday at 6 PM, ingest new files from this exact inbox with safe checkpoints.` |
| `help` | `Help` | `Show me every second-brain mode and examples without opening a vault.` |

End the help response by asking which mode the user wants or inviting them to paste one of the examples with their details.
