# References and Design Systems

## Assign reference roles

Give assets stable IDs, a role, the specific properties to preserve, permitted changes, and the beats that use them. Useful roles include product identity, character identity, existing footage, environment, geometry, materials, typography, graphic vocabulary, palette, layout, motion, voice, first frame, and end frame.

Separate properties that happen to coexist in one file. A presenter video may control identity, wardrobe, room, and lens character while its dialogue remains unchanged by default. A design sheet can control letterforms, pill shapes, brackets, outlines, badges, and strokes while its background and arrangement remain irrelevant. A motion reference can control timing and easing without authorizing reuse of its logo, music, or distinctive assets.

Map abstract IDs to the selected endpoint's actual attachment order and reference syntax. Do not send unsupported tags such as `Image 1` by habit. Do not call a file an end-frame constraint unless the tool can use it that way; otherwise plan a deterministic final-card insertion and transition.

## Identity and state

Define the recurring subject by silhouette, proportions, component count, materials, label placement, color roles, and one diagnostic feature when useful. Identify which views must expose the feature and which may intentionally occlude it. Do not demand that every feature be visible from impossible angles. Canonical source assets own identity; a flawed generated take is evidence of failure, not the new reference standard.

For assemblies, record the ordered component list, where each component starts, how it travels, and what remains after landing. For architecture, plans or approved geometry own structure; renders own only the geometry they demonstrate. A still image cannot establish hidden rooms, precise dimensions, or mechanical internals.

For original concepts, create a coherent placeholder identity and label it as fictional. For supplied brands and designs, preserve them within the requested use. Do not automatically replace real assets with fictional ones or apply blanket exclusions to people, logos, and landmarks.

## Design sheet

Build a concise visual specimen before complex typography or overlays: headline and body styles, exact font and fallback, font weight, tracking, line height, alignment, palette roles, graphic primitives, sizes, hierarchy, margins, surface texture, and layer ordering. Include an actual sample phrase at intended output size and at least one crowded frame.

Prefer HTML/CSS or SVG when the host can render them and exact lettering matters. Inspect the actual font load and glyph support; a named font in HTML does not guarantee it exists. Keep licensed font files or a documented substitution in the handoff. Export a rendered image for a generator that cannot accept HTML; retain editable source for compositing. Never upload HTML and assume it becomes a usable video reference.

Define type in observable terms: weight, shape, size relative to frame, number of lines, contrast, spacing, entry, settle, hold, and exit. Specify whether a word accent belongs behind or within the glyphs. Treat outlined type, filled type, pills, badges, leader lines, and underlines as named components with consistent anatomy.

## Motion grammar

Set entry acceleration, overshoot, settle, hold, exit, stagger, blur, and allowed transitions for each layer family. Clean typography may have fast arrival and a long quiet settle; cartoon shapes may stretch and rebound; mechanical parts may remain rigid and stop on contact. "Premium" and "dynamic" alone do not define any of these choices.

Keep blur local to the moving object when sharp typography or a fixed background is required. Use intentional smear drawings in a flat style only if approved; do not conflate them with optical blur. Call out the exceptional beat if a global restriction changes there. Screen-locked text retains screen coordinates; a leader attached to a moving product follows a world anchor and perspective.

## Frame formats and safe zones

Derive safe zones from the delivery surface and current overlay UI when known. When unknown, top 12% and bottom 15% in a vertical draft are provisional starting margins, not universal platform specifications. Reserve side clearance too, including interface controls and caption regions. Check actual reference cropping and output dimensions before rendering.

Recompose vertical versions: stack information, rebalance cap height, move callouts away from the hero, and convert travel directions when helpful. A horizontal component spread may become a vertical exploded stack; a lateral reveal may become a rise. Preserve the intended physical action if changing its direction would break the mechanism. Localize copy before locking line breaks.
