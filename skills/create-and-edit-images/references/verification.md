# Image verification and revision

Use this reference after an image tool returns a result. Inspect at the highest practical detail level available.

## Verification order

1. **Requested outcome**: Confirm the requested subject, action, or edit is visibly present and correctly located.
2. **Preservation contract**: Compare identity, expression, pose, geometry, composition, crop, background, objects, labels, branding, and source text against the original where relevant.
3. **Physical integration**: Check scale, perspective, anatomy, occlusion, material texture, contact, shadows, reflections, depth of field, lighting direction, color temperature, and grain.
4. **Unintended content**: Look for added or missing people, objects, accessories, text, logos, duplicated elements, watermarks, and edge artifacts.
5. **Technical output**: Check aspect ratio, orientation, visible crop, resolution sufficiency, and transparent or seamless edges when required.
6. **Exact text**: Transcribe every requested word, including capitalization and punctuation. Treat unreadable text as unverified.

## Decide whether to revise

Revise only for a material failure:

- the requested change is absent, incomplete, or in the wrong location;
- a stated invariant visibly drifted;
- physical inconsistency makes the edit look composited or synthetic;
- exact text, branding, object count, or geometry is wrong; or
- the output ratio or crop violates the request.

Do not revise merely to explore alternatives after the image meets the request.

## Focus the correction

Name one defect class per correction when possible:

```text
Keep everything else unchanged. Correct ONLY [observable defect] by [specific target state]. Preserve [invariants most at risk]. Match [relevant physical properties] to the original.
```

Use the original source again when identity, geometry, layout, or background has drifted. Include the current result as an additional reference only when it contains an accepted edit that must be retained and the host supports multiple references.

If repeated edits create more drift, restart from the original with a clearer combined instruction rather than layering corrections indefinitely.

## Report honestly

- If inspection passes, return the artifact without a lengthy self-review.
- If the tool cannot preserve an exact invariant after focused retries, return the best result and name the remaining visible limitation.
- If the host cannot display or inspect the result, state that the edit was generated but not visually verified.
- If no image-generation capability exists, return a ready-to-run prompt and state that no artifact was produced.
