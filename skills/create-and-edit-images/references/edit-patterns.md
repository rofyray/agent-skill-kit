# Image-edit patterns

Read only the pattern that matches the requested edit. Preserve the base image unless a pattern explicitly says to reconstruct or replace part of it.

## Contents

- [Single-property edit](#single-property-edit)
- [Clothing replacement](#clothing-replacement)
- [Object or person removal](#object-or-person-removal)
- [Multi-image composite](#multi-image-composite)
- [Environmental transformation](#environmental-transformation)
- [Product photography](#product-photography)
- [Sketch to photorealistic image](#sketch-to-photorealistic-image)
- [Exact text correction](#exact-text-correction)
- [Restoration and corrective edits](#restoration-and-corrective-edits)

## Single-property edit

Use for one narrow adjustment such as color, shadow softness, material, position, or a small local feature.

```text
Edit the supplied image. Change ONLY [specific property in exact location] to [target state].

Preserve every other subject, object, identity feature, geometric relationship, label, text element, camera property, background detail, lighting property, and image-quality characteristic exactly.

Match the source perspective, texture, occlusion, shadows, reflections, depth of field, grain, and color grade. Keep the same aspect ratio and crop. Add no new text, watermark, or object.
```

Do not enumerate irrelevant invariants when a shorter, precise list is safer. Never say “keep everything identical” while also asking the model to change something physically coupled without explaining the allowed consequence.

## Clothing replacement

State the full garment description, including fabric, cut, color, construction, and fit.

Preserve the person's identity, face, hairstyle, skin tone, body shape, pose, expression, hands, camera, framing, and background unless the user changes one of them. Require natural fabric weight, folds, seams, drape, occlusion, and contact shadows. Match source lighting and temperature. Exclude unrequested jewelry, bags, text, logos, and accessories.

## Object or person removal

Identify the target and precise location. Remove only that target. Reconstruct newly visible content from the surrounding background, respecting texture continuation, perspective, depth of field, shadows, reflections, and plausible occluded geometry.

Preserve all other people, objects, labels, crop, camera properties, and color grade. Do not insert a replacement object or erase adjacent elements needed to understand the scene.

## Multi-image composite

Name each source by role:

- **Base image**: supplies the scene, people, camera, framing, and existing objects.
- **Element reference**: supplies the inserted person's or object's identity, geometry, material, or design.

Specify exact placement and contact surface. Match the base image's scale, perspective, focal depth, lighting direction, shadow softness, temperature, reflections, and grain. Add realistic occlusion and contact shadows. Preserve every non-target element of the base image.

Do not blend scene design from the element reference into the base image.

## Environmental transformation

Change only the environmental condition, time, weather, or season. Preserve architecture, subject identity, object placement, camera position, framing, and geometry.

Describe physically coupled effects that are allowed to change: sky illumination, key-light direction and intensity, shadow behavior, atmosphere, surface wetness, reflections, visible precipitation, or snow accumulation. Keep those effects internally consistent and avoid adding signs, props, people, or stylized cinematic effects.

## Product photography

Preserve exact product shape, proportions, color, material, label design, logo, and legible packaging text. Specify the seamless background color, product centering, output ratio, soft studio lighting, clean silhouette, and grounded contact shadow.

Do not restyle, relabel, invent claims, change packaging geometry, erase required branding, or introduce edge halos and background remnants. When source text is too small to verify, state that limitation instead of claiming exact preservation.

## Sketch to photorealistic image

Treat the sketch as the geometry and composition authority. Preserve object count, placement, proportions, silhouette, and perspective. Specify real-world materials, lighting, and camera language. Add only construction detail, surface texture, and shadows logically implied by the sketch.

Do not invent objects, writing, logos, openings, or design features not indicated by the drawing.

## Exact text correction

Quote the complete target text exactly, preserving capitalization, punctuation, spacing, and line breaks. Identify the precise text region. Instruct the tool to change only that text while preserving typography, size, weight, color, alignment, layout, surface perspective, texture, and every other design element.

After generation, visually transcribe the result character by character. If exact text remains wrong, report it and retry only when another focused edit is likely to help. Never claim exactness based only on the prompt.

## Restoration and corrective edits

Use a corrective prompt when a previous result drifted:

```text
Keep the accepted edit unchanged. Restore ONLY [drifted property] from the original source: [precise restoration]. Preserve [accepted change] and every other current element. Keep the original framing, perspective, lighting, and image quality.
```

Examples:

- Restore the original face, hairstyle, body proportions, and camera framing while retaining the approved outfit.
- Keep the composition unchanged; move only the product slightly lower and correct its contact shadow.
- Keep every design element unchanged; correct only the quoted text.

Anchor identity, geometry, branding, and composition to the original source. Anchor only the accepted requested change to the current result.
