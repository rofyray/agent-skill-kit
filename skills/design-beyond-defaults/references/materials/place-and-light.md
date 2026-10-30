# Place and Light

Use when: Places and experiences supported by real imagery. Treat this as a material direction, not an industry rule or page layout.

## Type

Open sans headings, readable details, short useful captions. Specimen fallback stack: `"Trebuchet MS", sans-serif`. Load a production font only after checking availability and rights; retain a usable local fallback.

## Surfaces and tokens

Neutral surfaces let photos lead; preserve text contrast independently. Example control radius: `0.25rem`; adapt it to existing components rather than imposing a new system.

| Semantic role | Example value |
| --- | --- |
| ground | `#f4f1e9` |
| surface | `#ffffff` |
| ink | `#24342c` |
| muted | `#56635c` |
| accent | `#285d46` |
| on_accent | `#ffffff` |
| focus | `#285d46` |

Map these roles onto the project's existing tokens. Verify the actual rendered combinations, including hover, selected, disabled, and supported theme variants. The catalog checks ink/muted on ground/surface, on_accent on accent, and focus on ground/surface; it cannot establish overall accessibility.

## Controls and focus

Clear dates, availability, and accessible selectors. Use a visible focus ring with separation from the control and sufficient contrast against its surrounding surface. Provide text or icon meaning in addition to color. Keep native keyboard and touch behavior.

## Motion

Static useful defaults; optional subtle image transitions. Respect reduced motion, keep useful content visible without animation, and allow interaction to interrupt transitions without corrupting state.

## Imagery

Actual place photographs with provenance; substitute a map or text when absent. Preserve source and license metadata. Never present sample or generated content as a real customer fact.

## Failure modes

Do not imply stock images depict the venue or hide text over busy imagery. Do not apply this direction when it contradicts brand locks, platform expectations, or the user's chosen materials.

## Two different jobs

- A guided walk page with route, access details, and booking: organize around the visitor's choice and commitment, with the needed conditions visible.
- A venue operations view with rooms, capacity, and actions: organize around scanning, deciding, and acting, with meaningful data and non-default states.

The two jobs can share typography, color, controls, and surfaces while requiring different hierarchy and structure. The bundled specimens demonstrate a selection form and a decision workspace; their layouts and sample content are not production templates.

## What the specimen demonstrates

The bundled specimen demonstrates the no-photo branch: an original, labeled schematic for a fictional workshop with a text route caption. It is not a real venue map or documentary photograph. The profile’s photo-led branch still requires suitable authorized imagery and a fresh crop, caption, contrast, and responsive review. All twelve profiles use the same two tasks and fictional content, with a separate material legend. Check the live required-choice error, valid preview, row selection, filters, empty recovery, and keyboard focus before judging the visual treatment.
