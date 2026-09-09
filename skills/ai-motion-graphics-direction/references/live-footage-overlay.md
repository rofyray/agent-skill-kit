# Live Footage Overlay Profile

Default to augmenting the actual supplied picture and sound. Generating a new viewpoint, changing dialogue, replacing a voice, or recreating a presenter is a separate requested transformation, not an automatic part of adding graphics. Confirm the intended scope from the conversation; reuse existing authorization when present.

## Analyze and design

Inspect the footage's duration, cadence, shot changes, transcript, word timing, camera movement, focus, lighting, face and hand positions, and likely graphic zones. Assign the footage, voice, graphic style, and exact-copy references separate roles. If a new performance is explicitly requested, preserve approved identity, wardrobe, environment, and voice properties; confirm authorization for the relevant likeness and voice processing before submitting private material externally.

Prepare an HTML/CSS or SVG design sheet when the tools permit. Show the actual typeface, outlined and filled treatments, pills, underlines, leader lines, bracket corners, badges, and active palette. Font approval is useful when it remains an open decision; do not require it again when the supplied brand system is already approved. Render a still of the sheet for image-only endpoints and retain its editable source.

## Define placement precisely

Classify each graphic:

- Screen-locked: fixed screen position after landing, regardless of footage movement.
- World-anchored: follows a scene point with appropriate translation, scale, rotation, and perspective.
- Occluded overlay: can remain screen-locked while a tracked person mask passes in front of it. Specify its layer order explicitly rather than pretending it is attached to the room.

Reserve safe regions per shot. Keep graphics clear of faces, hands, demonstrations, and other subjects whose action matters. A behind-presenter title requires an inspected matte for hair, fingers, motion blur, and fine edges. Track a surface for perspective-bound graphics; stabilize only the layer that needs stabilization. Do not stabilize the whole source merely to make text easier to place.

## Synchronize to meaning

Give each event an exact string, target spoken phrase, cue time or word alignment, entry duration, hold, exit, zone, anchor, and layer. The default semantic cue is at or just after the relevant words, not ahead of the reveal. If the user wants anticipatory captions, make that an explicit editorial choice.

Use one leading graphic animation at a time when emphasis matters. A letter cascade can arrive in a short stagger, settle fully, and remain crisp before a coordinated exit. Do not stretch every word or animate decorative elements continuously. Preserve room tone and intelligibility; effects should support emphasis without competing with speech. Ordinary captions and emphasis graphics are separate layers and can coexist when requested.

For new dialogue, fit the text to plausible delivery before synthesizing speech. The original voice reference need not impose original wording or timing. Generated camera angles should match the established room and light but must not be represented as actually recorded footage.

## Original prompt pattern

Over an approved interview clip, let a two-line phrase appear in the empty wall area when the speaker describes a delay. Keep the phrase fixed in screen coordinates, draw a short underline only after its last word lands, and remove both before the next shot. In the next shot, anchor one callout to the demonstrated object and inspect that it follows the object through rotation. Preserve the source performance and audio.

## Acceptance and fallback

Check exact lettering, semantic sync, stable holds, protected zones, anchor drift, occlusion edges, skin and room continuity, and the final audio mix. Compare the original and final footage for unintended face, hand, camera, or dialogue changes. If generative editing alters the presenter, return to the original plate and composite graphics. If tracking is weak, move the callout to a screen-locked zone or simplify the anchor; do not call a drifting label motion-tracked. If a mask fails, use a clear foreground placement unless behind-subject depth is essential.
