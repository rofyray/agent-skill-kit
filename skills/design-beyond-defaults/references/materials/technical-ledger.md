# Technical Ledger

Use when: Precise workflows, comparisons, and technical explanation. Treat this as a material direction, not an industry rule or page layout.

## Type

Strong compact headings; monospace only for machine values and code. Specimen fallback stack: `"Arial", sans-serif`. Load a production font only after checking availability and rights; retain a usable local fallback.

## Surfaces and tokens

Crisp rules and aligned columns; use fill to indicate selection. Example control radius: `0.1rem`; adapt it to existing components rather than imposing a new system.

| Semantic role | Example value |
| --- | --- |
| ground | `#eef3f7` |
| surface | `#ffffff` |
| ink | `#142838` |
| muted | `#435866` |
| accent | `#124c77` |
| on_accent | `#ffffff` |
| focus | `#124c77` |

Map these roles onto the project's existing tokens. Verify the actual rendered combinations, including hover, selected, disabled, and supported theme variants. The catalog checks ink/muted on ground/surface, on_accent on accent, and focus on ground/surface; it cannot establish overall accessibility.

## Controls and focus

Visible labels and explicit status text; focus cannot depend on a fine rule. Use a visible focus ring with separation from the control and sufficient contrast against its surrounding surface. Provide text or icon meaning in addition to color. Keep native keyboard and touch behavior.

## Motion

Quick state transitions; avoid decorative cursor tracking. Respect reduced motion, keep useful content visible without animation, and allow interaction to interrupt transitions without corrupting state.

## Imagery

Real diagrams or captures with meaningful labels; no fake telemetry. Preserve source and license metadata. Never present sample or generated content as a real customer fact.

## Failure modes

Technical does not mean terminal cosplay or unreadably dense tables. Do not apply this direction when it contradicts brand locks, platform expectations, or the user's chosen materials.

## Two different jobs

- A developer tool walkthrough with a live input/output example: organize around the visitor's choice and commitment, with the needed conditions visible.
- A transaction reconciliation workspace with exceptions: organize around scanning, deciding, and acting, with meaningful data and non-default states.

The two jobs can share typography, color, controls, and surfaces while requiring different hierarchy and structure. The bundled specimens demonstrate a selection form and a decision workspace; their layouts and sample content are not production templates.

## What the specimen demonstrates

The specimen uses a filled selected row, explicit selection text, crisp rules, and aligned tabular quantities. Monospace is confined to the readout and column labels; the open-check values are fictional and include zero. All twelve profiles use the same two tasks and fictional content, with a separate material legend. Check the live required-choice error, valid preview, row selection, filters, empty recovery, and keyboard focus before judging the visual treatment.
