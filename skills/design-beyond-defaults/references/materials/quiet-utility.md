# Quiet Utility

Use when: Repeated tasks with low visual interruption. Treat this as a material direction, not an industry rule or page layout.

## Type

Moderate weight and compact headings; align quantities with tabular numerals. Specimen fallback stack: `system-ui, sans-serif`. Load a production font only after checking availability and rights; retain a usable local fallback.

## Surfaces and tokens

Subtle surface steps and restrained rules; depth only for overlays. Example control radius: `0.4rem`; adapt it to existing components rather than imposing a new system.

| Semantic role | Example value |
| --- | --- |
| ground | `#f5f6f7` |
| surface | `#ffffff` |
| ink | `#182128` |
| muted | `#4b555d` |
| accent | `#174a66` |
| on_accent | `#ffffff` |
| focus | `#174a66` |

Map these roles onto the project's existing tokens. Verify the actual rendered combinations, including hover, selected, disabled, and supported theme variants. The catalog checks ink/muted on ground/surface, on_accent on accent, and focus on ground/surface; it cannot establish overall accessibility.

## Controls and focus

Labels lead; one filled action and quiet secondary controls. Use a visible focus ring with separation from the control and sufficient contrast against its surrounding surface. Provide text or icon meaning in addition to color. Keep native keyboard and touch behavior.

## Motion

Immediate feedback; short fades only where state would otherwise be ambiguous. Respect reduced motion, keep useful content visible without animation, and allow interaction to interrupt transitions without corrupting state.

## Imagery

Use actual product views when useful; a no-image route is complete. Preserve source and license metadata. Never present sample or generated content as a real customer fact.

## Failure modes

Do not confuse quiet with tiny text, hidden actions, or low contrast. Do not apply this direction when it contradicts brand locks, platform expectations, or the user's chosen materials.

## Two different jobs

- A service booking form with grouped choices: organize around the visitor's choice and commitment, with the needed conditions visible.
- An incident queue with priority, owner, and next action: organize around scanning, deciding, and acting, with meaningful data and non-default states.

The two jobs can share typography, color, controls, and surfaces while requiring different hierarchy and structure. The bundled specimens demonstrate a selection form and a decision workspace; their layouts and sample content are not production templates.

## What the specimen demonstrates

The specimen deliberately retains a restrained baseline for comparison: consistent controls, complete state labels, aligned fictional counts, and visible selection. Its quiet character is not evidence that it needs extra ornament. All twelve profiles use the same two tasks and fictional content, with a separate material legend. Check the live required-choice error, valid preview, row selection, filters, empty recovery, and keyboard focus before judging the visual treatment.
