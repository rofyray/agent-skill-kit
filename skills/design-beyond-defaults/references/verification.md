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

For an interactive task, judge the working and completed states alongside the opening view. A beautiful empty editor does not establish readable entered text; a working submit button does not establish a clear result. Compare the same meaningful states before and after. If only default screenshots exist, limit the conclusion to those views.

Capture the intended settled state: check loaded fonts/media where relevant and let transient UI finish opening. Use state/readiness checks rather than one universal sleep. Keep a failed or ambiguous capture identifiable, then recapture; do not silently turn a fade-in frame into an interface defect. Native validation UI may need a separate settled capture from the DOM state. Record the actual viewport and state, and distinguish narrow-viewport reflow from real browser-zoom testing.

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

Inspect the content and control bounds as well as document overflow. A field can break its content gutter before page overflow becomes conspicuous. For locally scrollable data, check whether users can discover the scroll and associate later values with their row identity; offscreen columns are not automatically missing data. Multi-route coverage needs representative content and states, not just the same shell under different headings.

Do not accept a visually striking hero if the remaining page, application state, or mobile layout is broken or generic.

## Accessibility and platform fit

Verify semantic controls, keyboard access, visible focus, useful labels, logical reading and tab order, text contrast, non-color status cues, touch target size, zoom behavior, and reduced-motion handling. Prefer native or established platform components when a custom version is less usable.

Accessibility requirements pass independently from visual preference.

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

For Full and substantial Redesign work, combine:

1. passing functional and accessibility requirements;
2. rendered evidence for required viewports and states;
3. a completed subtraction, default-pattern, and copy pass; and
4. an independent critic result when the host supports it.

Use task-specific acceptance evidence rather than a default numerical beauty target. Report strengths and gaps by relevant state/viewport, including meaningful tradeoffs or ties. If independent criticism is unavailable, disclose self-review. Neither a preference nor a high requested rating proves functional or accessibility requirements passed.

Return only the most useful evidence: artifact location, views inspected, tests or interactions exercised, critic outcome, and material limitations.

Record evidence against the tested revision, route, viewport, and state. Use pass, fail, not run, unsupported, and needs review distinctly. Recheck affected evidence after edits. Source inventories and screenshots cannot by themselves prove a journey works. Use the audit protocol selected from SKILL.md when a structured record is useful.
