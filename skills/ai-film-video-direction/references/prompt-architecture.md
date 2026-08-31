# Video Prompt Architecture

Use this reference to compile a provider-neutral production packet and then adapt it to the selected tool.

## Treat the prompt as a production contract

The prompt should make the current shot reconstructable without hidden memory. Use a rigid information architecture but flexible contents. Omit irrelevant sections; never omit a causal or continuity fact merely to shorten the prompt.

```text
SCENE CONTRACT
Exact visible characters, exact important objects, event, duration, and dramatic purpose.

ACTIVE REFERENCES
Each attachment or tag with one declared role.

LOCATION AND SPATIAL MAP
Location state, landmarks, paths, screen relations, world relations, and scale evidence.

FIRST FRAME AND BLOCKING
Initial occupancy, framing, depth, facing, gaze, contacts, prop ownership, and action readiness.

FORMAT
Single take or explicit shots, real-time behavior, duration, aspect ratio, and edit relation.

OPTICS AND FOCUS
Observable perspective, depth behavior, focus subject, and transfers.

CAMERA
Start, support, path, speed, inertia, motivation, restrictions, and end.

ACTION TIMELINE
Chronological triggers, actions, contacts, reactions, results, and holds.

PHYSICS
Weight, inertia, friction, collision, material response, mechanism, environmental motion, and persistent consequences.

LIGHTING
Motivated source hierarchy, direction, exposure, shadows, practicals, atmosphere, and changes.

AUDIO
Exact dialogue and ownership, voice delivery, nonverbal sound, effects, ambience, music, and sync.

PERFORMANCE
Entering state, want, obstacle, hidden information, tactic, listening, triggered change, physical rhythm, and leaving state.

STYLE
Observable medium, palette, contrast, texture, motion character, period, and finish.

QUALITY
Identity and geometry stability, temporal coherence, clean motion, output requirements, and shot-specific technical priorities.

POSITIVE CONTINUITY CONSTRAINTS
Explicit desired counts, ownership, state, geography, direction, and elements that remain stable.
```

## Compile signal, not ceremony

- Use concise present-tense clauses and chronological order.
- State one source of truth for each fact.
- Repeat a locked fact only when the provider requires local reinforcement at a shot boundary.
- Remove stale characters, references, props, states, and old camera instructions.
- Translate emotional adjectives into behavior, timing, voice, posture, or interaction.
- Translate style labels into observable primitives when the label may be ambiguous or unsupported.
- Keep dialogue exact and separate from descriptive prose.
- Keep tool settings outside prose when the schema offers dedicated fields.

Long prompts can work when every section controls a material result. Short prompts can work for simple shots. Prompt length is not a quality target.

## Use positive constraints

State the desired frame and relationships:

- `Exactly two named characters occupy the frame.`
- `Mara holds the red folder in her right hand throughout.`
- `The camera remains on the platform side of the track.`
- `The doorway stays behind Idris after he crosses.`
- `Only Lena speaks; Niko listens with his mouth closed.`

Use a small local exclusion when a likely failure cannot be stated positively. Put it in a negative-prompt field when the provider exposes one. Do not append a universal wall of bans that competes with the shot.

## Adapt to the selected model

Before invoking a tool, map the neutral packet to supported inputs:

- Prompt and negative prompt.
- Source video, first frame, end frame, or storyboard frames.
- Character, object, location, style, motion, and voice references.
- Reference tags, weights, or roles.
- Duration, aspect ratio, resolution, frame rate, seed, and output count.
- Camera or motion presets.
- Dialogue, audio, music, or lip-sync fields.
- Multi-shot, extend, edit, inpaint, replace, or video-to-video controls.

If a field is unsupported, decide whether to express the concept in prose, move it to another production stage, split the shot, or disclose the limitation. Never invent provider syntax.

## Structure an edited sequence

When the tool reliably supports multiple shots, give each segment its own:

- Shot identifier and time range or relative phase.
- First frame, active references, blocking, camera, action, and audio.
- Cut type and reason.
- Continuity entering and leaving.

When it does not, return separate prompts and a simple edit map. A separate generation per shot is often more controllable than a single overloaded prompt.

## Return a prompt-only package

A complete prompt-only delivery contains:

- Provider-neutral production prompt.
- Selected-provider adapter or clearly labeled capability assumptions.
- Active reference-role map and attachment order.
- Tool settings and fields.
- Output naming, version, and destination.
- Verification checklist and pass criteria.
- Known risks and manual fallback.
- A clear statement that no video was generated.
