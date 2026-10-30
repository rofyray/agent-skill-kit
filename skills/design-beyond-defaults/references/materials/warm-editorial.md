# Warm Editorial

Use when: Reading, explanation, and considered decisions. Treat this as a material direction, not an industry rule or page layout.

## Type

Serif headings with plain sans-serif reading text and utility controls. Specimen fallback stack: `Georgia, serif` for headings. Load a production font only after checking availability and rights; retain a usable local fallback.

## Surfaces and tokens

Warm paper tones and generous reading measure; rules separate real sections. Example control radius: `0.15rem`; adapt it to existing components rather than imposing a new system.

| Semantic role | Example value |
| --- | --- |
| ground | `#f7f1e7` |
| surface | `#fffaf2` |
| ink | `#30281f` |
| muted | `#655747` |
| accent | `#704522` |
| on_accent | `#ffffff` |
| focus | `#704522` |

Map these roles onto the project's existing tokens. Verify the actual rendered combinations, including hover, selected, disabled, and supported theme variants. The catalog checks ink/muted on ground/surface, on_accent on accent, and focus on ground/surface; it cannot establish overall accessibility.

## Controls and focus

Plain language labels; filled primary and underlined text links. Use a visible focus ring with separation from the control and sufficient contrast against its surrounding surface. Provide text or icon meaning in addition to color. Keep native keyboard and touch behavior.

## Motion

Content is visible immediately; transitions should not interrupt reading. Respect reduced motion, keep useful content visible without animation, and allow interaction to interrupt transitions without corrupting state.

## Imagery

Source-led photography or diagrams; omit imagery if it adds no evidence. Preserve source and license metadata. Never present sample or generated content as a real customer fact.

## Failure modes

Avoid vague literary copy, faux authority, and decorative chapter numbers. Do not apply this direction when it contradicts brand locks, platform expectations, or the user's chosen materials.

## Two different jobs

- An editorial membership page with sample reading and terms: organize around the visitor's choice and commitment, with the needed conditions visible.
- A research reading list with filters and annotations: organize around scanning, deciding, and acting, with meaningful data and non-default states.

The two jobs can share typography, color, controls, and surfaces while requiring different hierarchy and structure. The bundled specimens demonstrate a selection form and a decision workspace; their layouts and sample content are not production templates.

## What the specimen demonstrates

The specimen demonstrates serif heading hierarchy, a measured reading width, and more open line spacing. Body and control text remain conventional; this does not require a magazine layout for every product. All twelve profiles use the same two tasks and fictional content, with a separate material legend. Check the live required-choice error, valid preview, row selection, filters, empty recovery, and keyboard focus before judging the visual treatment.
