# Prompting, Editing, and Model Adaptation

Use this reference to compile an image-production packet for a new asset, precise edit, composite, style transformation, or prompt-only handoff.

## Choose generation or edit

- Generate when the asset does not yet exist or a new view cannot be derived reliably from a source.
- Edit when a canonical image already has the correct identity, geometry, composition, or environment and the requested change is bounded.
- Composite when different references must supply distinct roles to one result.
- Restart from the canonical source when accumulated edits have drifted beyond a reliable repair.

Do not use a broad regeneration when a local edit can preserve more of the accepted asset. Do not demand a local edit when the requested change necessarily alters composition, pose, or physical relationships across the image.

## Compile a new-asset prompt

Include only fields that affect the result:

1. Asset identity and intended production use.
2. Exact subject, count, visible state, and recognition anchors.
3. Reference-role declarations and prohibited inheritance.
4. Action, pose, interaction, or neutral presentation.
5. Location, era, weather, time, and required landmarks.
6. Composition, view, scale, hierarchy, and negative space.
7. Motivated light and shadow logic.
8. Style primitives, palette, materials, texture, and finish.
9. Required text, symbols, transparency, layout, or technical properties.
10. Positive continuity constraints and only the exclusions needed for likely failure modes.

Write coherent visible relationships rather than a pile of disconnected adjectives. There is no universal prompt length. Use enough detail to disambiguate the asset without burying its hierarchy.

State exact counts positively, such as "three distinct characters are visible," and verify them after generation. Use a negative-prompt field only when the selected model supports it and the exclusions target known risks. Do not append a universal ban dictionary.

## Adapt to the selected model

Keep a provider-neutral production packet, then map it to the tool:

- Put aspect ratio, resolution, seed, output count, transparency, reference strength, mask, and negative prompt into dedicated fields when available.
- Convert reference roles into the tool's supported attachment, tag, control-image, or weighting mechanism.
- Use only syntax confirmed by the actual tool or current provider instructions.
- Respect reference-count, file-size, image-type, resolution, and text limits exposed at runtime.
- Preserve the user's selected provider, model, and version. Do not silently substitute a hardcoded default.

If the tool lacks a needed control, simplify the request, split the asset, or explain the limitation. Do not pretend unsupported tags or weights will be honored.

## Build a strict edit contract

For an edit, separate the instruction into:

### Change

- Name the exact target, location, property, and desired state.
- Describe physically coupled consequences that are allowed to change, such as garment folds, shadow, reflection, revealed background, or contact.

### Preserve

- Identity, anatomy, proportions, pose, expression, and gaze when relevant.
- Geometry, layout, object count, camera, framing, crop, and background.
- Style, line, palette, material, light direction, grade, grain, and texture.
- Logos, labels, exact text, state, and all accepted production details.

Prioritize invariants at genuine risk rather than listing every property in the universe. Make one high-risk change per pass when combining changes would make failure impossible to diagnose. Multiple tightly coupled changes may remain together when separating them would create an incoherent result.

Use a mask or localized edit mechanism when supported and when it reduces drift. Keep the original canonical image available throughout revision.

## Composite references without contamination

Declare a base image and every donor role. State which source controls scene geometry, character identity, wardrobe, object design, pose, style, light, or texture. Specify placement, scale, perspective, occlusion, contact, shadow, reflection, and depth.

State what must not transfer from each donor when likely, such as its background, depicted character, composition, lighting, or color grade.

## Handle exact text and symbols

Quote required text exactly, including case, punctuation, spacing, and line breaks. Identify its location, typography role, surface, perspective, material, and surrounding design. After generation, transcribe it character by character. Treat small or unreadable text as unverified.

## Return a prompt-only package

When the user requests prompt-only output or no image tool exists, return:

1. Asset name, type, state, and intended use.
2. Final provider-neutral prompt.
3. Reference list with one role per input and prohibited inheritance where relevant.
4. Tool settings and capability assumptions.
5. Provider adapter notes only for the selected model.
6. Expected output count and naming guidance.
7. Verification checklist.

State that no image was generated. Do not describe the prompt as an artifact result.
