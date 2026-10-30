# Friendly Forms

Use when: Guided setup and supportive task completion. Treat this as a material direction, not an industry rule or page layout.

## Type

Friendly sans with strong labels; avoid infantilizing voice. Specimen fallback stack: `"Trebuchet MS", sans-serif`. Load a production font only after checking availability and rights; retain a usable local fallback.

## Surfaces and tokens

Soft corners and separate groups; depth only for transient layers. Example control radius: `0.9rem`; adapt it to existing components rather than imposing a new system.

| Semantic role | Example value |
| --- | --- |
| ground | `#f7f0f7` |
| surface | `#ffffff` |
| ink | `#33263b` |
| muted | `#69576d` |
| accent | `#733f83` |
| on_accent | `#ffffff` |
| focus | `#733f83` |

Map these roles onto the project's existing tokens. Verify the actual rendered combinations, including hover, selected, disabled, and supported theme variants. The catalog checks ink/muted on ground/surface, on_accent on accent, and focus on ground/surface; it cannot establish overall accessibility.

## Controls and focus

Native controls, helpful errors, clear progress; preserve back navigation. Use a visible focus ring with separation from the control and sufficient contrast against its surrounding surface. Provide text or icon meaning in addition to color. Keep native keyboard and touch behavior.

## Motion

Small feedback movements; no bouncing repetitive controls. Respect reduced motion, keep useful content visible without animation, and allow interaction to interrupt transitions without corrupting state.

## Imagery

Optional owned illustrations; clear text works without imagery. Preserve source and license metadata. Never present sample or generated content as a real customer fact.

## Failure modes

Avoid mascot clutter, excessive roundness, and hiding necessary complexity. Do not apply this direction when it contradicts brand locks, platform expectations, or the user's chosen materials.

## Two different jobs

- A course signup with choices and eligibility: organize around the visitor's choice and commitment, with the needed conditions visible.
- A team onboarding workspace with completion and retry states: organize around scanning, deciding, and acting, with meaningful data and non-default states.

The two jobs can share typography, color, controls, and surfaces while requiring different hierarchy and structure. The bundled specimens demonstrate a selection form and a decision workspace; their layouts and sample content are not production templates.

## What the specimen demonstrates

The specimen demonstrates soft group boundaries, a specific inline required-choice error, focus returned to that choice, and an explicitly local success message. No reservation is submitted. All twelve profiles use the same two tasks and fictional content, with a separate material legend. Check the live required-choice error, valid preview, row selection, filters, empty recovery, and keyboard focus before judging the visual treatment.
