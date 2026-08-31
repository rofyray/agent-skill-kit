# Video Production Handoff

Use this reference to package approved video direction and generated assets for collaborators, downstream skills, another chat, or editorial.

## Handoff principles

- Make the packet understandable without conversational memory.
- Separate locked creative facts from model settings and experiments.
- Give every reference and output a stable identifier, version, role, and status.
- Preserve accepted takes and clearly label superseded or rejected work.
- Record uncertainty and unverified media instead of implying approval.
- Keep provider-neutral direction separate from provider-specific adapters.

## Core package

Include only the fields the production needs, selected from:

```text
PROJECT AND SCENE
Project title and version
Scene identifier, purpose, story state, and duration
Prior and next scene or edit relation

MODEL PROFILE
Host, tool, provider, model, version, capabilities, limitations, and cost assumptions

SCENE PLAN
Shot order, duration, dramatic intent, edit logic, and complexity decisions

SHOT CARDS
Exact counts, active references, geography, first frame, blocking, camera, optics, action, physics, lighting, audio, performance, continuity, risk, and pass criteria

PROMPT PACKAGE
Provider-neutral prompts, model adapters, negative fields, settings, seeds, and attachment order

REFERENCE REGISTRY
Asset ID, version, role, source, rights or privacy status, and affected shots

OUTPUT REGISTRY
Shot and take ID, job ID, asset location, duration, settings, status, inspection result, and approval

EDIT MAP
Cut order, handles, match points, sound bridges, transitions, and replacement status

CONTINUITY LOG
Entering and leaving character, prop, location, light, weather, damage, performance, action, and audio states

AUDIO PACKAGE
Dialogue map, speaker ownership, voice references, effects, ambience, music, sync landmarks, and separate audio tasks

TAKE LOG
Hypothesis, changed variable, result, failure class, decision, and next action

OPEN ISSUES
Missing sources, unverified media, capability gaps, paid decisions, safety or rights questions, and responsible owner
```

## Coordinate with adjacent work

When available, consume:

- Scene intent, dialogue, structure, and continuity from screenwriting.
- Character, location, prop, vehicle, state, and style assets from image direction.
- Performance identity, objectives, tactics, voice, and scene behavior from performance direction.

Return actionable feedback when production reveals an upstream problem, such as impossible timing, missing state art, contradictory geography, unclear speaker ownership, or an unplayable beat. Do not silently rewrite canonical upstream material.

The video handoff must still work when none of those skills exists. Include the minimum local assumptions and identify them as assumptions.

## Name and version assets

Use a stable project convention such as:

```text
scene-014_shot-03_take-02_v001
scene-014_shot-03_prompt_v004
scene-014_continuity_v003
```

Do not encode transient approval language such as `final-final` in filenames. Store approval and replacement status in the registry.

## Manual execution package

When no compatible generator is connected, include:

- Final provider-neutral prompt and any selected-provider adapter.
- Reference-role map and attachment checklist.
- Tool settings and capability assumptions.
- Shot order and edit map.
- Audio or lip-sync handoff when separate.
- Output naming and destination.
- Verification and continuity checklist.
- A clear statement that no video was generated.

## Final handoff check

Before delivery, verify that:

- Every shot is independently runnable.
- Every reference has a declared role and no stale reference remains.
- Exact dialogue, counts, ownership, duration, and continuity are consistent.
- Model-specific settings match the actual tool schema.
- Generated assets exist, are accessible, and have been inspected as claimed.
- Accepted, rejected, superseded, queued, and unverified states are unmistakable.
