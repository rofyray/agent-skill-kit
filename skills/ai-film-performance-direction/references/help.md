# AI Film Performance Direction Help

## What this skill does

This skill develops and directs playable character behavior for live action, animation, voice production, and AI-generated video. It turns story intention into objectives, obstacles, tactics, beat changes, listening, physical behavior, subtext, dialogue delivery, voice direction, ensemble reactions, and continuity across scenes.

It can produce written acting profiles and scene direction, prepare final performance prompts, invoke compatible voice or performance tools, compare controlled rehearsal takes, inspect returned audio or video, and repair specific failures.

This skill does not replace screenplay writing, character visual design, cinematography, or full video prompting. It consumes those decisions when available and focuses on how the characters behave and sound.

## Modes

| Mode | Use it for |
| --- | --- |
| `develop` | Create or revise a recurring character performance bible, relationship behavior, physical baseline, and voice identity anchor. |
| `direct` | Adapt one or more characters to a scene, shot, line, or sequence with playable objectives, tactics, listening, behavior, and delivery. |
| `rehearse` | Design controlled alternative takes or invoke connected voice, avatar, animation, or performance tools for comparison. |
| `audit` | Inspect written direction, audio, animation, or video for artificial or inconsistent performance and repair when requested. |
| `prompt-only` | Return a model-ready performance packet, references, settings, and verification criteria without invoking a tool. |
| `help` | Display this guide without performing or generating performance work. |

Modes are natural-language hints, not slash commands. The user may name one or describe the desired outcome.

## Start here

Provide the screenplay scene, character notes, story state, dialogue, and any existing performance or voice bible. Attach relevant visual, voice, audio, animation, or video references and state what each should control.

Useful production context includes scene duration, shot size, blocking, physical conditions, exact lines, speaker ownership, language, lip-sync needs, prior and next scene states, and any performance choices that are already approved. State whether you want written direction, a prompt, a generated voice test, a generated performance clip, controlled alternatives, or an audit.

For real-person likeness or voice references, confirm that the intended use is authorized before asking an external tool to process them.

### Output choices

- **Profile or direction**: Performance bible, relationship map, beat map, line direction, or scene acting block.
- **Prompt-only**: Final performance prompt, reference roles, adapter settings, exact dialogue, and verification checklist.
- **Generate**: Invoke a compatible connected voice or performance tool and return the test asset.
- **Generate and refine**: Create a take, inspect it, make focused corrections, and version the accepted result.
- **Manual handoff**: Package everything needed to run the performance elsewhere when no compatible tool is connected.

### Connected performance tools

Installing this skill does not install or authenticate a voice, avatar, lip-sync, animation, or video model. The skill first inspects the tools already available in the active ChatGPT, Codex, Claude, or Claude Code conversation and uses their actual capabilities.

If no compatible tool appears, ask the skill to `show connection help for my current app and chosen performance service`. It will explain the appropriate plugin, connector, or remote MCP path, authentication, tool verification, permissions, and manual fallback. Only connect trusted services, review requested scopes, and never paste API keys into prompts or production files.

## Examples

| Mode | Starter | Another example |
| --- | --- | --- |
| `develop` | `Build a performance bible and voice identity anchor for the lead from this screenplay.` | `Create performance profiles for this four-person ensemble, including relationship-specific behavior, pressure responses, physical baselines, voice identity, and what must carry across the whole feature.` |
| `direct` | `Direct both characters in this breakup scene without changing the dialogue.` | `Adapt the existing performance bibles to this eight-second close shot. Mara is concealing that she already knows the truth; Idris realizes it halfway through his line. Keep the blocking and exact dialogue.` |
| `rehearse` | `Give me three controlled takes that change only Lena's tactic.` | `Use the connected voice tool to test the final line once as reassurance that fails and once as a threat disguised as reassurance. Preserve the same voice identity, wording, duration, and physical breath state.` |
| `audit` | `Audit this acting prompt for generic emotion and over-direction.` | `Inspect the generated confrontation clip for dead listening, synchronized reactions, voice drift, state resets, and lip-sync ownership. Diagnose first and do not regenerate until I approve.` |
| `prompt-only` | `Write the final performance block for this silent reaction shot without generating it.` | `Prepare a model-neutral two-character performance package with exact dialogue, identity and voice references, beat timing, physical state, and verification criteria, but do not call a tool.` |
| `help` | `Help` | `Show every performance mode, output level, connector option, and example without directing or generating a performance.` |

Choose a mode, provide the available scene and character material, or adapt an example above.
