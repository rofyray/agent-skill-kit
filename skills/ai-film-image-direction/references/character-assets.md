# Character and Costume Assets

Use this reference for humans, creatures, stylized characters, costumes, expressions, identity references, and character-state variants.

## Define the identity contract

Record the visible features that make the character recognizable across angle, scale, expression, costume, and light:

- Silhouette, height relationships, body proportions, posture baseline, and distinctive asymmetry.
- Face shape, feature spacing, eyes, brows, nose, mouth, ears, jaw, and age-relevant detail.
- Skin, hairline, hair mass or strand logic, facial hair, texture, and color.
- Hands, footwear, recurring accessories, marks, scars, tattoos, prosthetics, or nonhuman anatomy when story-relevant.
- Costume construction, fit, material, wear, closures, pockets, seams, and signature color relationships.
- Style-specific drawing or rendering rules that must remain stable.

Prefer visible discriminators over vague labels such as attractive, heroic, or cinematic. Do not invent demographic, medical, or identity facts that the user did not establish.

## Build the right sheet

Choose views according to downstream need. A robust source may include:

- Front, three-quarter, profile, and back full-body views at consistent scale.
- Neutral or recognition-critical head close-ups.
- A controlled expression range tied to the project's acting needs.
- Costume or equipment views that reveal construction.
- Hand, footwear, hair, or nonhuman-detail callouts only when those areas repeatedly fail or carry story information.

Do not crowd every useful view into one sheet if panel density reduces facial or material fidelity. Split identity close-ups, body or wardrobe construction, expressions, and special details into separate canonical assets when needed.

Keep reference-sheet poses readable and hands free unless an object is part of the identity state. Create important props separately so the model does not attach them to every appearance.

## Separate character states

Create a state asset when a visible change must appear only in specific scenes:

- Costume, disguise, armor, uniform, or era change.
- Wet, dirty, burned, frozen, wounded, exhausted, aged, transformed, or repaired state.
- Hair, makeup, prosthetic, tattoo, or accessory change.
- Hidden versus revealed identity or anatomy.
- Closed, open, retracted, extended, powered, damaged, or deployed equipment.

Do not display inactive mechanisms or all transformation stages on the universal master sheet. A small annotation may not prevent a video or image model from reproducing the visible state everywhere. Use a separate state reference and describe the required operation in the downstream prompt.

## Declare reference roles

Label every character input by role, for example:

- `IDENTITY`: face, body, hair, and recognition anchors only.
- `WARDROBE`: garment construction and material only.
- `STYLE`: drawing or rendering language only; do not copy the depicted character or scene.
- `POSE`: body arrangement only.
- `EXPRESSION`: facial state only.
- `DETAIL`: mechanism, tattoo, jewelry, hand, or material detail only.

State what each reference must not control when cross-contamination is likely.

## Test before scaling production

Stress-test an approved character across a representative matrix rather than a single flattering portrait:

- Close, medium, full-body, and wider environmental scale.
- Front, profile, three-quarter, back, high, and low views as relevant.
- Neutral, restrained, intense, and asymmetric expressions.
- Sitting, walking, reaching, handling a prop, contact with another character, and project-specific action.
- Neutral reference light and at least one important scene-light condition.
- Solo, paired, and group contexts when the character must coexist with others.

Choose a small set that exposes the project's main risks. Do not impose a fixed number of tests. If identity fails, repair the source design or reference strategy before generating many scene assets.

## Handle likeness and protected material

For a real person's likeness, a private reference, branded costume, or protected character design, confirm the user's intended use and do not imply that rights or consent have been cleared. Preserve required provenance or permission notes in the asset record without placing private evidence into prompts unnecessarily.

When transforming style, describe observable visual primitives. Do not rely solely on a living creator's name or a protected title when the look can be expressed through line, shape, palette, material, and rendering behavior.
