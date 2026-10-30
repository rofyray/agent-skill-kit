# Expressive Print

Use when: Announcements with a strong voice and simple action. Treat this as a material direction, not an industry rule or page layout.

## Type

Heavy display for a few short statements; plain body at comfortable size. Specimen fallback stack: `"Arial Black", sans-serif`. Load a production font only after checking availability and rights; retain a usable local fallback.

## Surfaces and tokens

Bold flat fields and decisive edges; keep reading areas calm. Example control radius: `0`; adapt it to existing components rather than imposing a new system.

| Semantic role | Example value |
| --- | --- |
| ground | `#fff4dc` |
| surface | `#ffffff` |
| ink | `#281a25` |
| muted | `#68535e` |
| accent | `#a32243` |
| on_accent | `#ffffff` |
| focus | `#a32243` |

Map these roles onto the project's existing tokens. Verify the actual rendered combinations, including hover, selected, disabled, and supported theme variants. The catalog checks ink/muted on ground/surface, on_accent on accent, and focus on ground/surface; it cannot establish overall accessibility.

## Controls and focus

Large clear action labels; control structure remains familiar. Use a visible focus ring with separation from the control and sufficient contrast against its surrounding surface. Provide text or icon meaning in addition to color. Keep native keyboard and touch behavior.

## Motion

One purposeful entrance at most; no constant agitation. Respect reduced motion, keep useful content visible without animation, and allow interaction to interrupt transitions without corrupting state.

## Imagery

Use owned artwork or typographic compositions with readable fallbacks. Preserve source and license metadata. Never present sample or generated content as a real customer fact.

## Failure modes

Do not turn every label into a poster or introduce fake scarcity. Do not apply this direction when it contradicts brand locks, platform expectations, or the user's chosen materials.

## Two different jobs

- A community event page with a schedule and registration: organize around the visitor's choice and commitment, with the needed conditions visible.
- A release planning board with owners and milestones: organize around scanning, deciding, and acting, with meaningful data and non-default states.

The two jobs can share typography, color, controls, and surfaces while requiring different hierarchy and structure. The bundled specimens demonstrate a selection form and a decision workspace; their layouts and sample content are not production templates.

## What the specimen demonstrates

The specimen demonstrates a strong heading color field with conventional labels and working text underneath. The accent groups the task; it does not replace the task hierarchy. All twelve profiles use the same two tasks and fictional content, with a separate material legend. Check the live required-choice error, valid preview, row selection, filters, empty recovery, and keyboard focus before judging the visual treatment.
