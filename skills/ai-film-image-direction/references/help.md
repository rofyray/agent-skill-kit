# AI Film Image Direction Help

## What this skill does

This skill develops and produces consistent still-image assets for live-action, animated, and hybrid film projects. It can build a visual bible, design characters and costumes, create location plates and props, separate story states, produce storyboards or keyframes, edit existing assets, audit continuity, and prepare final prompts for another image model.

When a compatible image tool is available and the user requests an asset, the skill can invoke it, inspect the returned image, and make focused corrections. When no tool is connected, it returns a complete manual generation package and clearly states that no image was produced.

This differs from a general image skill because it maintains cross-asset identity, geography, style, state, naming, and downstream production roles across a film or animation project.

## Modes

| Mode | Use it for |
| --- | --- |
| `develop` | Create or strengthen the visual bible, art direction, style contract, palette, asset plan, reference strategy, and continuity system. |
| `create` | Design and optionally generate a character sheet, costume, location, prop, vehicle, crowd, storyboard frame, keyframe, or production still. |
| `edit` | Make a controlled change, composite references, extend a view, or transform style while preserving required continuity. |
| `audit` | Inspect one asset or a full asset set for identity, state, style, geography, text, and technical drift, with repair when requested. |
| `prompt-only` | Produce a model-ready prompt, reference-role map, settings, and verification checklist without invoking a generator. |
| `help` | Display this guide without performing visual-development work. |

Modes are natural-language hints, not slash commands. The user may name one or describe the desired outcome.

## Start here

Provide the screenplay, story summary, scene intent, existing visual bible, or asset list when available. Attach every image that must control identity, design, style, location, composition, or editing, and explain each image's intended role if it is not obvious.

State the requested asset, visible state, intended downstream use, locked properties, and whether you want a brief, prompt, generated image, generated and refined image, or continuity audit. Model, provider, aspect ratio, resolution, file format, and budget are optional until they materially affect the result.

For projects with existing assets, identify the canonical versions. The skill will not silently replace the source of truth with a newly generated variation.

### Output choices

- **Brief**: Art direction, asset specification, reference plan, or visual-bible entry only.
- **Prompt-only**: Final prompt, reference roles, settings, constraints, and verification checklist.
- **Generate**: Invoke a compatible connected tool and return the asset.
- **Generate and refine**: Generate, inspect, make focused corrections, and version the accepted result.
- **Manual handoff**: Package everything needed for generation elsewhere when the requested tool is unavailable.

### Connected generation tools

Installing this skill does not install or authenticate an image model. The skill first inspects the tools already available in the active ChatGPT, Codex, Claude, or Claude Code conversation. If a suitable native image tool or connector exists, it maps the visual package to that tool's actual capabilities.

If no tool is visible, ask the skill to `show connection help for my current app and chosen image service`. It will explain the appropriate plugin, connector, or remote MCP path, how to authenticate, how to verify that the tools are active, and how to continue manually. Only connect trusted servers, review requested scopes, and never place API keys in prompts or project files.

## Examples

| Mode | Starter | Another example |
| --- | --- | --- |
| `develop` | `Build a visual bible and asset list for this animated short from the screenplay.` | `Reconcile these three conflicting style references into one production style contract. Label what controls line, shape, palette, material, and lighting, then identify the character, location, and prop assets we need before shot generation.` |
| `create` | `Create a turnaround and expression sheet for this lead character.` | `Generate a reusable apartment location package with an empty establishing plate, reverse view, doorway anchors, window-light direction, and a separate rain-at-night state.` |
| `edit` | `Change only the hero's jacket from blue denim to worn brown leather and preserve identity.` | `Use Image 1 for the canonical character, Image 2 for the approved winter coat, and Image 3 for drawing language only. Create the winter-state sheet without inheriting Image 3's character or background.` |
| `audit` | `Check these six character images for identity drift and tell me which one is canonical.` | `Audit the full asset library for costume-state leakage, duplicate props, inconsistent location geometry, palette drift, and unreadable labels. Repair only the approved failures.` |
| `prompt-only` | `Write a ready-to-run prompt for a neutral four-view vehicle sheet.` | `Prepare a model-neutral prompt package for a cinematic first frame using the supplied character, location, and prop references, but do not generate it.` |
| `help` | `Help` | `Show every mode, output level, connector option, and example without creating or changing an image.` |

Choose a mode, attach the available story and visual material, or adapt an example above.
