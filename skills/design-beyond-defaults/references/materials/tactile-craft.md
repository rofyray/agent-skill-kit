# Tactile Craft

Use when: Human-scale services, physical objects, and making. Treat this as a material direction, not an industry rule or page layout.

## Type

Readable serif heads with neutral sans controls; descriptive object names. Specimen fallback stack: `Georgia, serif`. Load a production font only after checking availability and rights; retain a usable local fallback.

## Surfaces and tokens

Soft warm planes and limited inset treatments; no texture behind small text. Example control radius: `0.65rem`; adapt it to existing components rather than imposing a new system.

| Semantic role | Example value |
| --- | --- |
| ground | `#eee9df` |
| surface | `#fffdf8` |
| ink | `#2c3228` |
| muted | `#59604f` |
| accent | `#35543a` |
| on_accent | `#ffffff` |
| focus | `#35543a` |

Map these roles onto the project's existing tokens. Verify the actual rendered combinations, including hover, selected, disabled, and supported theme variants. The catalog checks ink/muted on ground/surface, on_accent on accent, and focus on ground/surface; it cannot establish overall accessibility.

## Controls and focus

Comfortable rounded controls with clear pressed/selected states. Use a visible focus ring with separation from the control and sufficient contrast against its surrounding surface. Provide text or icon meaning in addition to color. Keep native keyboard and touch behavior.

## Motion

Small, responsive press feedback; no simulated physics without purpose. Respect reduced motion, keep useful content visible without animation, and allow interaction to interrupt transitions without corrupting state.

## Imagery

Real work and materials; visibly label stand-in photos. Preserve source and license metadata. Never present sample or generated content as a real customer fact.

## Failure modes

Avoid ornamental texture, fabricated maker stories, and expensive effects. Do not apply this direction when it contradicts brand locks, platform expectations, or the user's chosen materials.

## Two different jobs

- A repair workshop booking flow with services and times: organize around the visitor's choice and commitment, with the needed conditions visible.
- An inventory view with material, quantity, and restock action: organize around scanning, deciding, and acting, with meaningful data and non-default states.

The two jobs can share typography, color, controls, and surfaces while requiring different hierarchy and structure. The bundled specimens demonstrate a selection form and a decision workspace; their layouts and sample content are not production templates.

## What the specimen demonstrates

The specimen demonstrates a subtle panel edge, inset native select, and restrained pressed-button feedback. These cues remain optional; verify them in the actual interface rather than adding decorative textures. All twelve profiles use the same two tasks and fictional content, with a separate material legend. Check the live required-choice error, valid preview, row selection, filters, empty recovery, and keyboard focus before judging the visual treatment.
