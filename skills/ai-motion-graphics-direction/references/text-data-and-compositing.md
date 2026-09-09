# Text, Data, and Compositing

## Choose where precision lives

Use deterministic graphics for exact logos, copy, UI, numeric labels, chart geometry, and frame-level timing when suitable tools are available. Possible renderers include HTML/CSS, SVG, Canvas, a code-based video renderer, a compositor, or a 3D package. Choose from the user's environment and requested deliverable; do not install a preferred stack automatically.

Generated lettering is usable when it passes the actual quality contract. A generative-only request can still be attempted with a capable model, but exactness remains an inspection requirement. If the available route cannot deliver exact typography or editable vectors, say so and supply a workable graphics handoff.

## Keep a controlled layer stack

1. Picture or generated clean plate, with room for critical overlays.
2. World-anchored graphics and any perspective transforms.
3. Subject masks that should occlude graphics.
4. Screen-locked text, UI, annotations, and source notes.
5. Captions and final output adjustments as required.

This order is a starting point; assign actual front/behind relationships per shot. Store position, scale, rotation, perspective, opacity, and masks independently where the editor supports them. Inspect edge matte, motion blur, alpha handling, frame size, and cadence after compositing. A generated image with a checkerboard is not a transparent layer; verify actual alpha or choose another workflow.

For a physical callout, track its anchor and derive leader geometry from that anchor. Decide whether the text billboard stays upright or rotates in space. A screen-locked title behind a moving presenter uses a tracked matte but retains screen coordinates. Avoid conflating those behaviors.

## Exact copy and fonts

Keep one copy manifest with IDs, approved strings, language, font role, line breaks, and placement. Build animated layers from that manifest. Render sample glyphs and inspect whether the intended fonts loaded; document substitutions. Preserve exact strings unless the user authorizes copy edits. Do not treat a missing glyph or truncated line as a reason to rewrite a claim silently.

Validate contrast, cap height, line spacing, safe margins, clipping, overlap, and reading duration at actual output size. Inspect early, middle, and late frames of a type animation. OCR can locate potential errors but does not replace visible inspection of letterforms, punctuation, and animation stability. Do not claim OCR ran without a working tool and actual result.

For accurate type during high-speed action, use settled windows, isolated overlay movement, or a clean end card. Reduce type density before shrinking important text to illegibility. If a model adds stray copy to a clean plate, repair or replace that region before overlaying the final text.

## Data geometry

Calculate percentage fill as `track_length * percent/100`. Build labels and geometry from the same approved value, unit, denominator, and time period. Compare tracks on the same scale. For stacked bars, check component totals separately; the optional manifest helper only checks each bar's supplied fill ratio.

Keep fixed labels paired with fixed final geometry, or update both together during animation. Do not animate an irrelevant data value for visual excitement. A technical specification needs its real source just as a statistic does. Keep a source ledger and distinguish explanatory illustrations from measurements.

## Audio and output

Preserve the approved audio unless a change is requested. Align semantic events to the final narration, duck music beneath speech, and inspect caption sync after cuts. If the delivery must be silent, verify the actual audio track or remove it with an available editor; a prompt requesting silence is insufficient evidence.

Export the requested aspect, dimensions, duration, frame rate, codec, and audio state supported by the route. Inspect the final encode after assembly, not only source clips. Deliver editable layers or vector/3D sources only when they were created, and distinguish them from raster footage with a vector or 3D appearance.
