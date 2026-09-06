# Design Beyond Defaults Help

Use this reference to answer help mode. Present the explanation, modes, starting guidance, and examples in a detailed but scannable user-facing form. Include every named mode and both example columns. Do not explore, build, critique, or polish an interface while answering help.

## What this skill does

This skill helps an AI move beyond familiar interface defaults and produce web or app designs with a coherent identity. It supports the complete design arc: explore unusual directions, turn the selected direction into a buildable brief, implement it, improve the rendered result through independent visual critique when possible, and finish through subtraction, anti-default review, and copy refinement.

The skill protects required behavior, brand constraints, accessibility, responsiveness, and production practicality. Generated images or video are used only when they strengthen the design and suitable capabilities are available.

## Modes

| Mode | Use it for |
| --- | --- |
| `explore` | Generate and refine distinct creative directions, then produce a polished design brief without building. |
| `build` | Implement an already selected, supplied, or approved visual direction. |
| `critique` | Review rendered interface evidence and prioritize improvements without editing unless requested. |
| `polish` | Improve an existing interface through removal, anti-default review, copy refinement, and visual QA. |
| `full` | Run the complete Discover, Define, and Deliver workflow for a new design or substantial redesign. |
| `help` | Display this guide without beginning design work. |

The user can name a mode or describe the intended outcome naturally. No slash command is required.

## Start here

Provide the product or page, its audience and purpose, required behavior, and any brand or technical constraints that matter. Attach screenshots or references when available. State whether you want concepts, critique, implementation, or a completed end-to-end pass.

If you have a strong taste preference, describe what attracts or repels you and why. If you are starting from a blank page, the skill can use a hidden seed to introduce a less predictable direction. Tool-based generation, browser verification, and independent critic loops depend on capabilities and permissions available in the active host.

## Examples

| Mode | Starter | Another example |
| --- | --- | --- |
| `explore` | `Explore distinctive visual directions for a personal finance dashboard and stop before building.` | `Develop a bold design language for this education product. I like tactile controls and editorial typography, but dislike glassmorphism and cartoon skeuomorphism.` |
| `build` | `Build the supplied design brief as a responsive landing page.` | `Implement the selected isometric-city direction while preserving our current navigation, analytics hooks, and accessibility requirements.` |
| `critique` | `Critique this homepage screenshot and do not change the code.` | `Compare these responsive screenshots with the supplied reference set, identify the largest studio-quality gaps, and prioritize the next two fixes.` |
| `polish` | `Polish this existing dashboard so it feels less AI-generated and more intentional.` | `Simplify this mobile app, remove decorative clutter, preserve every workflow, and flag the customer-facing copy that still needs my approval.` |
| `full` | `Redesign and build this product page using the complete workflow.` | `Take this generic prototype from initial art direction through implementation, screenshot critique, generated media where useful, and final responsive verification.` |
| `help` | `Help` | `Show every design mode and examples without inspecting or changing an interface.` |

End the help response by asking which mode the user wants or inviting them to adapt an example.
