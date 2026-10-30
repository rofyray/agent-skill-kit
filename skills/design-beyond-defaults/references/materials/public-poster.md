# Public Poster

Use when: Public information that must be recognized quickly. Treat this as a material direction, not an industry rule or page layout.

## Type

Bold brief heads with plain sentence-case details. Specimen fallback stack: `"Arial Black", sans-serif`. Load a production font only after checking availability and rights; retain a usable local fallback.

## Surfaces and tokens

High-contrast fields and large hierarchy shifts; quiet areas for detail. Example control radius: `0`; adapt it to existing components rather than imposing a new system.

| Semantic role | Example value |
| --- | --- |
| ground | `#fff5a7` |
| surface | `#fffde8` |
| ink | `#1e2524` |
| muted | `#535943` |
| accent | `#1e2524` |
| on_accent | `#fff5a7` |
| focus | `#1e2524` |

Map these roles onto the project's existing tokens. Verify the actual rendered combinations, including hover, selected, disabled, and supported theme variants. The catalog checks ink/muted on ground/surface, on_accent on accent, and focus on ground/surface; it cannot establish overall accessibility.

## Controls and focus

Obvious high-contrast actions and strong focus indicators. Use a visible focus ring with separation from the control and sufficient contrast against its surrounding surface. Provide text or icon meaning in addition to color. Keep native keyboard and touch behavior.

## Motion

Immediate content; motion rarely improves urgency or public clarity. Respect reduced motion, keep useful content visible without animation, and allow interaction to interrupt transitions without corrupting state.

## Imagery

Official information graphics or owned imagery; no decoration required. Preserve source and license metadata. Never present sample or generated content as a real customer fact.

## Failure modes

Avoid shouting body copy, invented urgency, and inaccessible all-caps paragraphs. Do not apply this direction when it contradicts brand locks, platform expectations, or the user's chosen materials.

## Two different jobs

- A public programme with timetable and access instructions: organize around the visitor's choice and commitment, with the needed conditions visible.
- A service status board with affected routes and next steps: organize around scanning, deciding, and acting, with meaningful data and non-default states.

The two jobs can share typography, color, controls, and surfaces while requiring different hierarchy and structure. The bundled specimens demonstrate a selection form and a decision workspace; their layouts and sample content are not production templates.

## What the specimen demonstrates

The specimen demonstrates bold heading scale and stronger hierarchy rules with conventional readable controls. Test wrapping at small panel widths rather than shrinking labels to preserve a poster-like composition. All twelve profiles use the same two tasks and fictional content, with a separate material legend. Check the live required-choice error, valid preview, row selection, filters, empty recovery, and keyboard focus before judging the visual treatment.
