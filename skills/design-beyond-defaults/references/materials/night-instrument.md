# Night Instrument

Use when: Low-light workspaces and media tools. Treat this as a material direction, not an industry rule or page layout.

## Type

Clear sans hierarchy and aligned numeric readouts. Specimen fallback stack: `system-ui, sans-serif`. Load a production font only after checking availability and rights; retain a usable local fallback.

## Surfaces and tokens

Dark blue surfaces distinguished by lightness; overlays visibly separated. Example control radius: `0.3rem`; adapt it to existing components rather than imposing a new system.

| Semantic role | Example value |
| --- | --- |
| ground | `#111b2b` |
| surface | `#1c2b40` |
| ink | `#eff6ff` |
| muted | `#bbcbdc` |
| accent | `#99d4f0` |
| on_accent | `#102232` |
| focus | `#e7f6ff` |

Map these roles onto the project's existing tokens. Verify the actual rendered combinations, including hover, selected, disabled, and supported theme variants. The catalog checks ink/muted on ground/surface, on_accent on accent, and focus on ground/surface; it cannot establish overall accessibility.

## Controls and focus

High-contrast active states; text plus symbols for status. Use a visible focus ring with separation from the control and sufficient contrast against its surrounding surface. Provide text or icon meaning in addition to color. Keep native keyboard and touch behavior.

## Motion

Changes track actual values; reduced motion keeps final state. Respect reduced motion, keep useful content visible without animation, and allow interaction to interrupt transitions without corrupting state.

## Imagery

Real media or tool output; no-image workspace remains complete. Preserve source and license metadata. Never present sample or generated content as a real customer fact.

## Failure modes

Avoid ambient glow that obscures state or untested dark-mode contrast. Do not apply this direction when it contradicts brand locks, platform expectations, or the user's chosen materials.

## Two different jobs

- A listening session page with a programme and booking: organize around the visitor's choice and commitment, with the needed conditions visible.
- An export monitor with progress, retry, and completed files: organize around scanning, deciding, and acting, with meaningful data and non-default states.

The two jobs can share typography, color, controls, and surfaces while requiring different hierarchy and structure. The bundled specimens demonstrate a selection form and a decision workspace; their layouts and sample content are not production templates.

## What the specimen demonstrates

The specimen demonstrates dark surface separation, bright focus treatment, and aligned numeric readouts. The data is fictional, including zero; it is not telemetry or a product performance claim. All twelve profiles use the same two tasks and fictional content, with a separate material legend. Check the live required-choice error, valid preview, row selection, filters, empty recovery, and keyboard focus before judging the visual treatment.
