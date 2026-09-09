# Prompt Compiler

## Preserve one complete production specification

Resolve the brief, delivery contract, reference roles, core mechanic, visual system, subject identity, type and copy, global motion rules, timed states, audio, continuity, ending, execution route, and acceptance checks. Separate creative intent from provider settings. Keep the specification useful even when the chosen endpoint accepts a short prompt or requires several calls.

Use only sections that influence the result. Do not impose a universal block order, word count, language, aspect ratio, soundtrack, frame rate, style, or CTA. Write concrete observable instructions rather than brand-name software adjectives. Translate "premium render" into material, reflection, lighting, edge, texture, and motion behavior.

## A reusable structure

```text
DELIVERABLE: [duration, aspect, output, audio intention, take or cut structure]
PURPOSE: [one message and one visual mechanic]
REFERENCES: [asset IDs, role, property locks, allowed changes]
DESIGN: [shape or material system, palette roles, typography, layer rules]
SUBJECT: [identity and component/state invariants]
MOTION: [camera, object and graphic motion; transitions; blur and hold behavior]
TIMELINE:
[start-end] [entering state -> trigger -> action -> settled state]
[exact copy IDs; semantic audio cues; placement or anchors; next-beat relation]
COPY: [approved strings, exact spelling and punctuation, placement and reading windows]
AUDIO: [approved speech, speaker, cue timing, music/effects or intentional silence]
ENDING: [final state, what stays still or loops, hold and tail durations]
CONSTRAINTS: [critical exclusions or deviations from the normal visual rules]
ASSEMBLY: [segments, clean plates, deterministic layers, audio, edit seams]
CHECKS: [observable pass criteria and the highest-risk element's fallback]
```

This is a specification template, not mandatory API syntax. Resolve placeholders before presenting a finished prompt. For native generation, include essential copy directly in the timed beats and keep a canonical copy list. For deterministic overlays, keep exact text in the graphics specification and ask for a clean plate. Maintain logical copies from one source; use the optional validator's `copy_text` check when verifying exported beat text.

## Compile to the selected model

1. Read the actual tool schema and current official prompt guidance for the specific model and endpoint.
2. Resolve required modalities, input counts, asset order, identifiers, duration, aspect, output size, and audio fields.
3. Map each reference ID to a supported attachment and role. Replace neutral IDs with documented tokens only where required.
4. Move supported parameters into their actual fields. Writing "30fps" in prose does not configure a fixed-fps endpoint. Do not emit fields or reference weights the schema lacks.
5. Compress if necessary. Keep purpose, active identity constraints, causal motion, copy, and ending before decorative detail. Split into natural generation segments if the treatment exceeds prompt or clip limits. Do not simply truncate the tail of a prompt.
6. Translate the prompt language only when useful and supported, while preserving on-screen copy and dialogue in their approved languages.
7. Put essential exclusions in the tool's negative field when available; otherwise state a concise boundary in the prompt. Prefer desired behavior over a sprawling prohibition list.
8. Keep editor-only timing, tracking, text, and layer instructions in the assembly packet when the generator cannot execute them.

No universal prompt guarantees equal results across models. Preserve the production intent and adapt its expression to capability. If the chosen model cannot satisfy an essential requirement, identify the gap and use a viable route within the authorized tool choices; otherwise return the complete manual package.

## Resolve conflicts before rendering

Check global rules against local beats. Common conflicts include a continuously moving camera with a fully static end frame; a text-free film with embedded labels; no fades followed by a fade; exact end-image matching followed by an appended scene; pure flat graphics with cinematic depth of field; a permanent built state followed by an unexplained return to wireframe; and a script that cannot fit its allotted duration.

State the local exception explicitly or change the treatment. Prioritize the user's current request, approved assets and facts, output contract, and beat intent over inherited example defaults. Exact hue targets are design specifications, not proof that a generative renderer will reproduce every pixel.

## Revision and fallback

For a new product using the same look, keep the approved motion and design grammar only where the new product's function supports them. For a style change, rebuild primitives and motion behavior. For color changes, update palette roles, contrast, and materials. For localization or vertical versions, reflow and retime before recompiling.

Identify one major execution risk and a concrete alternative: fewer crossing objects, a shorter orbit, a deterministic label, a clean cut in place of a difficult morph, or a registered overlay over an approved plate. Explain when the fallback changes the mechanic or continuity so the user can assess it. Do not silently replace the central idea with a generic product montage.

## Output

For prompt-only work, give the final prompt in a copyable block, then the exact settings and attachments, route, assembly notes, highest risk, and checks. For segmented work, provide one self-contained block per segment and the shared continuity map. Do not hide multiple separately required submissions inside one prose blob. State clearly when no media was generated.
