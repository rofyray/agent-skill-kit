# AI Film Video Direction Help

## What this skill does

This skill turns scripts, scene ideas, storyboards, visual assets, and performance direction into producible AI film or animation shots. It plans the edit, seals each shot's context, assigns active references, maps geography, establishes the first frame, blocks characters, directs camera and optics, times action, describes physics and lighting, integrates dialogue and acting, and protects continuity.

It can return shot cards or final prompts, invoke a compatible connected video service, inspect generated clips, diagnose failures, make focused revisions, and package approved takes for editing. The model and provider remain configurable.

This skill does not replace long-form screenwriting, canonical image development, or a full performance bible. It uses those inputs when supplied and creates only the minimum local direction needed when they are absent.

## Modes

| Mode | Use it for |
| --- | --- |
| `plan` | Break a scene, treatment, storyboard, or idea into a generation strategy and continuity-aware shot cards. |
| `create` | Compile a production-ready video prompt and optionally invoke a compatible connected generation tool. |
| `revise` | Repair, extend, adapt, or regenerate a shot while preserving accepted identity, geography, action, and edit continuity. |
| `audit` | Inspect a shot plan, prompt, or actual clip for ambiguity, overload, artifacts, and continuity failures. |
| `prompt-only` | Return a complete model-ready prompt, reference map, settings, and verification checklist without invoking a tool. |
| `help` | Display this guide without planning, prompting, generating, or auditing video. |

Modes are natural-language hints, not slash commands. The user may name one or describe the desired outcome.

## Start here

Provide the scene or story beat, intended duration, visible characters, location, important props, exact dialogue, and prior or next shot when continuity matters. Attach relevant character, state, wardrobe, location, prop, vehicle, style, first-frame, end-frame, motion, voice, or performance references and state what each should control.

Useful production constraints include aspect ratio, resolution, single take or edited sequence, camera preferences, audio needs, model or provider choice, budget, destination, and any approved details that must not drift. If you do not know the model, the skill can inspect available tools or return a model-neutral package.

For real-person likenesses, private voices, confidential footage, or unreleased story material, confirm that external processing is authorized before generation.

### Output choices

- **Plan or shot cards**: Scene strategy, shot list, active references, blocking, timing, continuity, risks, and edit relation.
- **Prompt-only**: Final production prompt, provider adapter, tool settings, attachment map, and verification checklist.
- **Generate**: Invoke a compatible connected video tool and return the completed clip or clips.
- **Generate and refine**: Create a take, inspect it, make focused corrections within a stated budget, and version the accepted result.
- **Manual handoff**: Package everything required to run the shot elsewhere when no compatible tool is connected.

### Connected video tools

Installing this skill does not install or authenticate a video model. The skill first inspects tools already available in the active ChatGPT, Codex, Claude, or Claude Code conversation, including native tools, plugins, connectors, and remote MCP servers.

If no compatible tool appears, ask the skill to `show connection help for my current app and chosen video service`. It will explain the appropriate plugin, connector, or remote MCP path, authentication, capability verification, permissions, asynchronous jobs, and manual fallback. ChatGPT web does not inherit a local Codex MCP configuration. Only connect trusted services, review requested scopes and cost, and never paste API keys into prompts or production files.

## Examples

| Mode | Starter | Another example |
| --- | --- | --- |
| `plan` | `Turn this scene into shot cards for a 20-second sequence.` | `Plan the subway-platform reveal from the locked screenplay and visual bible. Preserve platform geography, screen direction, exact dialogue, the wet-coat state, and the cut into scene 18. Flag any shot that should be generated separately.` |
| `create` | `Generate an eight-second single-take confrontation from these references.` | `Create this four-shot animated escape using the connected video service. Assign each reference by role, keep the broken windshield and dusk lighting continuous, preserve speaker ownership, inspect every returned clip, and stop before extra paid retries.` |
| `revise` | `Fix the floating suitcase without changing the accepted framing or acting.` | `Extend the approved shot by three seconds so the train clears frame. Preserve character identities, eyelines, camera inertia, rain direction, light state, ambience, and the exact end position needed for the next cut.` |
| `audit` | `Audit this video prompt for stale references and contradictory camera instructions.` | `Inspect the generated chase clips for duplicate characters, geography drift, broken screen direction, weightless impacts, lighting resets, dead listening, dialogue ownership, lip sync, flicker, and unstable heads or tails. Diagnose before regenerating.` |
| `prompt-only` | `Write the final model-neutral prompt for this silent reaction shot without generating it.` | `Prepare a complete prompt-only package for a ten-second threshold transformation with active references, first-frame occupancy, spatial map, camera, focus, timed mechanism states, scale proof, physics, lighting, performance, audio handoff, and pass criteria.` |
| `help` | `Help` | `Show every video-direction mode, output level, connector option, and example without planning or generating a scene.` |

Choose a mode, provide the available scene and production material, or adapt an example above.
