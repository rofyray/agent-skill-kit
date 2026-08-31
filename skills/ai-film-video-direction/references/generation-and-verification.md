# Generation and Verification

Use this reference to preflight production, invoke a video tool, inspect the returned clip, diagnose failures, and make focused repairs.

## Preflight before spending

Confirm:

- The active tool, provider, model, version, and current schema.
- Supported input mode and reference roles.
- Duration, aspect ratio, resolution, frame rate, output count, and seed behavior.
- First-frame, end-frame, multi-shot, camera, audio, dialogue, lip-sync, edit, extend, and enhancement support.
- Authentication, privacy, rights, content policy, cost, storage, and asynchronous job behavior.
- The shot's exact count, current references, first frame, blocking, timing, continuity, and pass criteria.

Run a low-cost representative test before a large batch when model behavior, reference handling, or spend is uncertain.

## Track generation honestly

Record the prompt version, tool settings, input references, job identifier, returned asset identifier, output location, and generation status when the workflow needs reproducibility.

For asynchronous tools, wait or poll through the supported mechanism. Distinguish queued, processing, succeeded, failed, expired, and cancelled states. Never label a job ID or unavailable remote URL as a finished clip.

## Inspect the actual clip

Review at normal speed, frame by frame where needed, and with audio when present.

### Content and continuity

- Exact character and important-object counts with no duplicates.
- Identity, body, wardrobe, injury, dirt, wetness, damage, and transformation state.
- Location identity, landmarks, weather, time, scale, and prop ownership.
- First-frame occupancy, end state, screen direction, eyelines, and edit relation.

### Camera and image

- Framing, optical perspective, depth, focus, camera side, path, speed, inertia, and settle.
- Lighting source, direction, exposure, shadows, practicals, and temporal stability.
- Style, material, color, texture, geometry, and detail continuity.

### Motion and physics

- Chronological action and timing.
- Body contact, footing, grip, weight transfer, collision, recoil, and recovery.
- Prop, cloth, hair, liquid, particle, vehicle, and mechanism behavior.
- Persistent physical consequences and readable scale.

### Performance and sound

- Objective, listening, triggered changes, physical state, and reaction timing.
- Exact dialogue, speaker ownership, voice identity, intelligibility, lip sync, effects, ambience, and music.

### Technical integrity

- Flicker, ghosting, warping, extra limbs, merged subjects, sliding, popping, blur, broken edges, frozen regions, audio artifacts, and unstable opening or closing frames.

If the host cannot display or analyze the output, state what remains unverified and give the user an inspection checklist.

## Diagnose before revising

Classify the primary cause:

- **Source failure**: The canonical reference is ambiguous, contradictory, low quality, or missing the required state.
- **Prompt failure**: Counts, ownership, geography, timing, camera, or cause are underspecified or contradictory.
- **Complexity failure**: Too many interacting systems must resolve at once.
- **Continuity failure**: The current shot conflicts with an approved prior or next state.
- **Capability failure**: The model lacks the required reference, duration, edit, audio, camera, or precision control.
- **Artifact failure**: The plan is sound but the sampled result contains local stochastic defects.
- **Rights or safety constraint**: The requested processing is unauthorized or unsupported.

Do not keep expanding the prompt when the actual problem is a bad source, unsupported capability, or overloaded shot.

## Apply the smallest effective repair

- Preserve accepted identity, composition, performance, motion, lighting, and timing.
- Change one material variable or one causal block at a time when practical.
- Reinforce exact counts, reference roles, first frame, ownership, contacts, or state transitions locally.
- Simplify or split the shot when complexity is the cause.
- Replace a source reference when the source is the cause.
- Move audio, lip sync, cleanup, or compositing to a separate stage when the generator cannot control it.
- Revert to canonical references instead of recursively using a drifted take.

Record what changed and why. Keep accepted versions available; do not overwrite them silently.

## Protect continuity across shots

Compare the leaving state of one shot with the entering state of the next:

- Character positions, screen direction, eyelines, body state, and performance state.
- Prop ownership and placement.
- Wardrobe, hair, dirt, wetness, injury, damage, transformation, and environment.
- Weather, light, crowd, vehicle, smoke, debris, and mechanism state.
- Movement phase, camera motion, focus, dialogue, effects, ambience, and music.

Use a continuity log to record intentional changes and the story event that causes them.

## Finish for editorial

Trim unstable heads or tails only when the edit can spare them. Do not impose a fixed trim length. Preserve handles when clean material exists.

When post-production is in scope, apply geometry or artifact cleanup before final color treatment, then confirm that cleanup did not damage identity, edges, texture, motion, or sync. Use ambience and sound bridges intentionally across cuts.

## Stop deliberately

Stop when:

- The user-approved pass criteria are met.
- The agreed retry or cost budget is exhausted.
- Another paid attempt needs authorization.
- Repeated takes do not improve the measured failure.
- A different reference, shot design, duration, workflow stage, or model capability is required.

"Perfect" is not a usable completion criterion. Convert it into observable scene-specific checks before beginning an open-ended paid loop.
