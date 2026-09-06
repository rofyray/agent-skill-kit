# Interface verification

Verify the artifact itself after any build, redesign, or polish pass. Code structure and design rationale are supporting context, not proof of visual quality.

## Prepare representative evidence

Run the interface through its intended entry point. Capture or inspect:

- representative desktop and mobile views;
- the primary task and major navigation states;
- loading, empty, error, success, disabled, focus, and overflow states that exist;
- long and short realistic content where layout could shift; and
- before and after views for an existing design when practical.

Use the actual target runtime when available. If the page cannot be rendered, state that visual verification was not completed.

## Visual system

Check:

- the first point of attention matches the product priority;
- composition remains coherent at each viewport;
- typography has a deliberate scale, readable measure, and useful contrast;
- color and effects support hierarchy rather than compete with it;
- component shape, spacing, borders, and elevation follow a consistent logic;
- generated media fits the layout, palette, crop, and material treatment; and
- the distinctive idea remains visible without overwhelming the interface.

Run the subtraction and default-pattern passes against the rendered pixels, not only the source classes.

## Behavior and responsive layout

Exercise the primary user journey. Verify that controls, links, forms, navigation, scrolling, media, and state changes work. Check for clipping, overlap, unreadable wrapping, layout shift, hidden content, accidental horizontal scrolling, and pointer-only interactions.

Do not accept a visually striking hero if the remaining page, application state, or mobile layout is broken or generic.

## Accessibility and platform fit

Verify semantic controls, keyboard access, visible focus, useful labels, logical reading and tab order, text contrast, non-color status cues, touch target size, zoom behavior, and reduced-motion handling. Prefer native or established platform components when a custom version is less usable.

Accessibility requirements pass independently from any visual critic score.

## Generated media and motion

For image assets, inspect crop, resolution, unintended text, compositing, contrast, responsive treatment, and loading fallback.

For video or animated assets:

- scrub through representative frames and every transition seam;
- inspect start, midpoint, end, and loop continuity;
- test forward and reverse gesture-controlled playback;
- check object identity, camera, lighting, physics, transparency, and edge spill;
- verify poster, loading, failure, and reduced-motion states; and
- assess file size, decode cost, and interaction smoothness.

## Copy

Read every visible high-salience string in context. Confirm accuracy, hierarchy, action clarity, voice, and consistency between labels and behavior. Flag provisional or unapproved customer-facing copy in the handoff.

## Completion evidence

For Full mode, combine:

1. passing functional and accessibility requirements;
2. rendered evidence for required viewports and states;
3. a completed subtraction, default-pattern, and copy pass; and
4. an independent critic result when the host supports it.

A 9/10 critic result is an aspirational visual bar, not permission to ignore failed requirements. If independent criticism is unavailable, report the rubric findings without inventing a score.

Return only the most useful evidence: artifact location, views inspected, tests or interactions exercised, critic outcome, and material limitations.
