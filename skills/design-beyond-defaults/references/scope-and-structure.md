# Scope and structure

Choose the user's job before the visual materials. A style profile does not decide section order, navigation, density, or page length.

| Scope | Structure follows | Representative slice | Completion evidence |
| --- | --- | --- | --- |
| Marketing page | The visitor's decision and next action | First screen plus a meaningful content section | Complete page, truthful claims, working destination/form, responsive views |
| App screen/flow | Repeated tasks, information priorities, permissions, and state transitions | Central task with a meaningful non-default state | Relevant routes and journeys, data correctness, keyboard/touch, state transitions |
| Component | Its semantic purpose, integration contract, and states | The component's applicable state set | Parent integration, accessible interaction, long content, disabled/error/focus states |

For a booking page, make the offering, availability, terms, and booking action discoverable. For a shop, support choosing and buying. For a tool, make its real operation understandable. For an app, identify what the operator needs to decide and do, then organize information around that task. Do not force a hero, social-proof strip, word count, section count, or large display type onto every scope.

Select layout after establishing the necessary information. Compare plausible structures when exploring: a catalogue, chronological process, editorial argument, working demonstration, spatial map, or task workspace. These are examples, not an obligatory library. The same materials should support different structures; different products should not merely receive recolored copies.

Use actual content and states early. Include loading, empty, error/retry, success, disabled, focus, selected, and permission states only where they exist. Preserve meaningful zero values and units. Dense data can be correct; validate legibility and task speed instead of imposing marketing-page whitespace.

Plan responsive behavior from actual breakpoints and content. Sample a narrow phone, a typical phone, tablet/intermediate widths, desktop, wide screen, and both sides of changed breakpoints when relevant. Test long labels, localization, zoom/reflow, and supported themes. These samples do not require adding matching CSS breakpoints.

At phone and intermediate widths, inspect the path from proposition to first useful control and from action to result. Repeated explanations, stranded headline words, oversized empty regions, and navigation for a very small task can dilute hierarchy even without overflow. Adjust grouping, proportion, or type wrapping while preserving the direction's strongest visual idea. Do not impose an above-the-fold rule, uniformly compact spacing, or smaller headings on every design. Completion should give the result appropriate prominence and keep revision/recovery discoverable.

Build a representative slice, inspect the render, exercise its central interaction, and correct structural issues before propagating styles. If rendering is unavailable, finish the permitted implementation or specification but mark visual verification not run. Do not describe source inspection as rendered evidence.
