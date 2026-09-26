# Scroll and Motion Engineering

Use only the sections needed by the chosen treatment. These are behavioral requirements and implementation options, not a mandatory framework or copied drop-in engine. Verify against the target browser and platform.

## Start with a complete page

Render meaningful content, navigation, and primary actions before activating media. A script failure must not leave headings transparent or essential sections inaccessible. Enable enhanced hidden/animated states only after their controller is ready.

For a scrub hero, a sticky stage inside a taller section is one useful architecture. Compute progress from the section's current geometry: clamp traveled distance divided by the available scroll range to zero through one. Account for header offsets and guard a zero or negative range. Recalculate on relevant layout changes, including font loading, viewport changes, and inserted content.

Set scroll length from the number and density of reading beats, not footage duration alone. Let ordinary wheel, keyboard, touch, anchor, and browser navigation work. Consider a skip-journey link for an extended sequence. Do not hijack scrolling to guarantee that every visitor watches the entire treatment.

## Treat loading as a state machine

Name and test static, loading, ready, failed, and disposed states. The static state carries its own readable composition; loading retains usable content and actions. Select motion mode before assigning heavy media URLs, including posters that the selected layout will not display. Load the actual static hero image when that mode needs it.

Use native media loading when it meets the actual seek behavior and budget. A fully downloaded Blob can be useful for a bounded small clip when native seeking is unreliable, but it consumes memory and delays media readiness. It is not a universal fix for codec, CORS, decode, or network failures. Avoid forcing a large full-file download on every device.

For a Blob loader:

1. Attach relevant media listeners before assigning the source and starting the load.
2. Check the response status and handle fetch, stream, and decode errors.
3. Show determinate progress only with a trustworthy size; otherwise use an indeterminate state without a fictional percentage.
4. Bound stalled transfer time, clear timers in success and failure paths, and provide an abort path.
5. Set an appropriate media type, retain the object URL while in use, and revoke it after detaching or replacing its media source.
6. On preference changes, teardown, or route changes, cancel unnecessary transfers and ensure late callbacks cannot reactivate disposed media. Use a request identity or equivalent lifecycle guard.
7. On failure, stop waiting indicators and expose a complete static reading path. Do not keep the visitor in an empty multi-screen hero.

Use the actual encoded asset size when estimating budgets, and distinguish network download completion from a decoded frame ready to display. Fade into the video only after usable media is ready at the current scroll position. Never hide the poster merely because a request was submitted.

## Map progress to decoded media safely

Wait for finite metadata and a usable duration before requesting a seek. Map progress into the valid timeline, avoiding a target beyond the last decodable frame. For a finite normalized clip, a small end margin based on its frame cadence may help, but inspect the intended ending rather than guessing a universal epsilon.

Coalesce rapid requests to the latest target and avoid setting `currentTime` while a previous seek is in flight. Skip effectively unchanged targets before setting a busy flag; a same-time assignment must not leave the controller waiting indefinitely for an event. Keep requested time distinct from completed media state.

When a seek completes, clear its timer and busy state, then issue at most one pending request if its target is meaningfully different. Handle assignment exceptions, media errors, aborts, source replacement, and teardown. A bounded seek watchdog should recover once or select the static path when progress stops; do not spin or repeatedly reset `currentTime` forever.

An optional eased progress controller should be time-normalized so it feels comparable at different display refresh rates. Stop scheduling when converged, outside the active region, or in a hidden tab. Reset its time origin on resume. On re-entry, recompute the current scroll target and synchronize, including direct anchor entry into the middle of the page.

Only change styles and text when their values change meaningfully. Group geometry reads separately from writes. Throttle rapidly changing counters. Inspect visible decoded frames as well as state variables; a requested timestamp does not prove the frame has been presented.

For API semantics, consult [MDN currentTime](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/currentTime) and [object URL cleanup](https://developer.mozilla.org/en-US/docs/Web/API/URL/revokeObjectURL_static). Implementation still requires lifecycle and visual testing.

## Make captions readable while moving

Assign each caption a progress interval with a brief entrance, a generous fully readable plateau, and an exit when appropriate. Keep the opening understandable immediately and the final action stable. Choose reading distance from copy density, viewport, and actual scrolling; do not prescribe the same long journey for every page.

Use the media's calm regions and test crop changes. Add local backing, scrims, text treatment, or a separate text panel as needed to satisfy contrast. A fixed shadow or alpha is not proof of legibility. Check the worst relevant composited backgrounds throughout each reading interval, including overlaps and transitions.

Readability takes priority over a nominal beat count. Shorten copy, merge beats, move text, or reduce media complexity when necessary. Critical claims must also exist in the normal reading order so a fast scroll or anchor jump cannot make them inaccessible.

Test slow and fast forward/reverse scrolling, several wheel-step sizes, keyboard paging, touch scrolling where available, and direct jumps. Check settled reading plateaus and the actual transition between them. Sample the whole journey rather than assuming a short fixed test loop covers every band.

## Choreograph intentionally

Choose motion that reinforces the subject: a line assembling with a product, a measured reveal of a diagram, or a quiet arrival after camera movement. Avoid giving every word a different effect merely because the engine supports it.

Prefer transform and opacity for frequent animation. Profile other properties when the effect requires them. Scope entrance styles so the cascade does not silently suppress them. Clear stagger delays before later hover/focus interactions, and keep persistent entrance effects from overriding dynamic styles on the same element.

If text is split for animation, preserve an accessible full-string representation and hide only the duplicate decorative fragments from assistive technology. Preserve Unicode graphemes, reading direction, real word wrapping, and glyph descenders. Leave links and controls as intact interactive elements. Do not split text when it adds no value.

Pause ornamental loops off-screen and on hidden tabs. Keep any ambient motion subordinate to content, and provide pause behavior where necessary for the chosen experience. A meaningful interaction needs keyboard and touch equivalents; a press-and-hold must not be the only way to obtain essential information. Do not rely on hover alone.

## Responsive and reduced-motion behavior

Choose the static/motion policy from composition, input methods, device performance, transfer budget, and available evidence. A still hero is a strong mobile default for heavy or poorly cropped media. Width alone does not prove device capability; a touch device can have a keyboard or pointer.

Use one authoritative policy so CSS layout and JavaScript asset loading agree. Reevaluate it on relevant media-query changes, resize, orientation, and user preference changes. Test both directions. Do not preserve obsolete hidden classes or leave an invisible tall stage after changing modes.

When motion is disabled, stop scrub drivers, seeks, decorative loops, and unnecessary downloads. Present a readable content sequence or designed static summary with all essential information. Do not force every overlapping caption into the same visible position. Preserve structural transforms needed for layout while removing motion transforms. Cover pseudo-elements and delayed animations as well as ordinary elements.

When motion is reenabled, reset stale caches, restore the intended layout, and synchronize to the current page position. Remove temporary final-state overrides that would otherwise keep later interactions frozen. On unmount, remove listeners and observers, cancel animation frames and timers, and release media resources.

Test short landscape viewports and zoom, not just narrow portrait screens. Hide or rearrange decorative readouts before they collide with real content. Repair actual overflow causes rather than using clipping to conceal broken layout or focus outlines.
