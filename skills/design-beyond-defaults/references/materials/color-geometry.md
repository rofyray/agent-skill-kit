# Color Geometry

Use when: Clear categorization with an expressive visual identity. Treat this as a material direction, not an industry rule or page layout.

## Type

Geometric-feeling sans headings; body remains conventional. Specimen fallback stack: `"Arial", sans-serif`. Load a production font only after checking availability and rights; retain a usable local fallback.

## Surfaces and tokens

Flat color regions with one dominant accent; shape communicates grouping. Example control radius: `0.2rem`; adapt it to existing components rather than imposing a new system.

| Semantic role | Example value |
| --- | --- |
| ground | `#edf4fc` |
| surface | `#ffffff` |
| ink | `#182c47` |
| muted | `#4c617c` |
| accent | `#2154a1` |
| on_accent | `#ffffff` |
| focus | `#2154a1` |

Map these roles onto the project's existing tokens. Verify the actual rendered combinations, including hover, selected, disabled, and supported theme variants. The catalog checks ink/muted on ground/surface, on_accent on accent, and focus on ground/surface; it cannot establish overall accessibility.

## Controls and focus

Explicit labels; selected state uses shape/text as well as color. Use a visible focus ring with separation from the control and sufficient contrast against its surrounding surface. Provide text or icon meaning in addition to color. Keep native keyboard and touch behavior.

## Motion

Brief transitions tied to grouping changes; no constant decorative loops. Respect reduced motion, keep useful content visible without animation, and allow interaction to interrupt transitions without corrupting state.

## Imagery

Simple semantic diagrams or real product imagery; text fallback. Preserve source and license metadata. Never present sample or generated content as a real customer fact.

## Failure modes

Avoid color-only coding and too many equally loud regions. Do not apply this direction when it contradicts brand locks, platform expectations, or the user's chosen materials.

## Two different jobs

- A learning catalogue with paths and enrolment: organize around the visitor's choice and commitment, with the needed conditions visible.
- A resource planner with categories, filters, and allocation: organize around scanning, deciding, and acting, with meaningful data and non-default states.

The two jobs can share typography, color, controls, and surfaces while requiring different hierarchy and structure. The bundled specimens demonstrate a selection form and a decision workspace; their layouts and sample content are not production templates.

## What the specimen demonstrates

The specimen groups task headings in a dominant accent field. An outlined diamond and filled circle supplement complete status text, so category meaning survives without color. The same queue and controls remain comparable with the other materials. All twelve profiles use the same two tasks and fictional content, with a separate material legend. Check the live required-choice error, valid preview, row selection, filters, empty recovery, and keyboard focus before judging the visual treatment.
