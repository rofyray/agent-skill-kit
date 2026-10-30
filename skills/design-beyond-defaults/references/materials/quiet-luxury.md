# Quiet Luxury

Use when: Considered purchases and high-touch services. Treat this as a material direction, not an industry rule or page layout.

## Type

Measured serif contrast with readable body; hierarchy through spacing and scale. Specimen fallback stack: `"Palatino Linotype", Palatino, Georgia, serif`. Load a production font only after checking availability and rights; retain a usable local fallback.

## Surfaces and tokens

Clean surfaces, controlled margins, minimal elevation. Example control radius: `0`; adapt it to existing components rather than imposing a new system.

| Semantic role | Example value |
| --- | --- |
| ground | `#f5f2ec` |
| surface | `#ffffff` |
| ink | `#272524` |
| muted | `#625c56` |
| accent | `#4e4238` |
| on_accent | `#ffffff` |
| focus | `#4e4238` |

Map these roles onto the project's existing tokens. Verify the actual rendered combinations, including hover, selected, disabled, and supported theme variants. The catalog checks ink/muted on ground/surface, on_accent on accent, and focus on ground/surface; it cannot establish overall accessibility.

## Controls and focus

Understated but obvious actions; never sacrifice hit area for delicacy. Use a visible focus ring with separation from the control and sufficient contrast against its surrounding surface. Provide text or icon meaning in addition to color. Keep native keyboard and touch behavior.

## Motion

Short opacity changes; no delays before useful content. Respect reduced motion, keep useful content visible without animation, and allow interaction to interrupt transitions without corrupting state.

## Imagery

Owned product photography at useful crops; no-image specifications fallback. Preserve source and license metadata. Never present sample or generated content as a real customer fact.

## Failure modes

Avoid faint text, tiny controls, generic superlatives, and hidden prices. Do not apply this direction when it contradicts brand locks, platform expectations, or the user's chosen materials.

## Two different jobs

- A furniture collection with dimensions and ordering details: organize around the visitor's choice and commitment, with the needed conditions visible.
- A client appointment ledger with availability and confirmation: organize around scanning, deciding, and acting, with meaningful data and non-default states.

The two jobs can share typography, color, controls, and surfaces while requiring different hierarchy and structure. The bundled specimens demonstrate a selection form and a decision workspace; their layouts and sample content are not production templates.

## What the specimen demonstrates

The specimen demonstrates lighter serif headings and deliberate spacing while preserving readable labels and controls. It does not depend on low contrast, tiny type, or extra empty sections. All twelve profiles use the same two tasks and fictional content, with a separate material legend. Check the live required-choice error, valid preview, row selection, filters, empty recovery, and keyboard focus before judging the visual treatment.
