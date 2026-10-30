# Civic Clarity

Use when: Broad audiences, public services, and complex eligibility. Treat this as a material direction, not an industry rule or page layout.

## Type

Plain sans, descriptive headings, generous line height. Specimen fallback stack: `system-ui, sans-serif`. Load a production font only after checking availability and rights; retain a usable local fallback.

## Surfaces and tokens

Clear regions with reliable alignment; restrained ornament. Example control radius: `0.2rem`; adapt it to existing components rather than imposing a new system.

| Semantic role | Example value |
| --- | --- |
| ground | `#f2f4f3` |
| surface | `#ffffff` |
| ink | `#172c27` |
| muted | `#4b6059` |
| accent | `#185442` |
| on_accent | `#ffffff` |
| focus | `#185442` |

Map these roles onto the project's existing tokens. Verify the actual rendered combinations, including hover, selected, disabled, and supported theme variants. The catalog checks ink/muted on ground/surface, on_accent on accent, and focus on ground/surface; it cannot establish overall accessibility.

## Controls and focus

Native inputs, explicit errors, review step before consequential actions. Use a visible focus ring with separation from the control and sufficient contrast against its surrounding surface. Provide text or icon meaning in addition to color. Keep native keyboard and touch behavior.

## Motion

Minimal motion; maintain focus through step changes. Respect reduced motion, keep useful content visible without animation, and allow interaction to interrupt transitions without corrupting state.

## Imagery

Official maps or documents only when useful; plain text alternative. Preserve source and license metadata. Never present sample or generated content as a real customer fact.

## Failure modes

Avoid bureaucratic jargon, concealed eligibility rules, and style over comprehension. Do not apply this direction when it contradicts brand locks, platform expectations, or the user's chosen materials.

## Two different jobs

- A service application with eligibility and document requirements: organize around the visitor's choice and commitment, with the needed conditions visible.
- A case management queue with permissions and next actions: organize around scanning, deciding, and acting, with meaningful data and non-default states.

The two jobs can share typography, color, controls, and surfaces while requiring different hierarchy and structure. The bundled specimens demonstrate a selection form and a decision workspace; their layouts and sample content are not production templates.

## What the specimen demonstrates

The specimen deliberately retains familiar controls and complete status words. Its invalid choice, empty queue, recovery action, and explicitly local confirmation demonstrate clarity without requiring a more expressive visual system. All twelve profiles use the same two tasks and fictional content, with a separate material legend. Check the live required-choice error, valid preview, row selection, filters, empty recovery, and keyboard focus before judging the visual treatment.
