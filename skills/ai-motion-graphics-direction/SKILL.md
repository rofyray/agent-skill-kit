---
name: ai-motion-graphics-direction
description: Plan, prompt, create, and audit motion graphics. Use when directing launch videos, footage overlays, product hyper-motion, architectural reveals, 2D explainers, or editorial graphics.
---

# AI Motion Graphics Direction

Turn a brief into a coherent motion system and a usable production package. Direct the relationship between message, typography, graphic layers, product identity, geometry, motion, sound, and time. The planning model, generation provider, renderer, and editor are independently configurable.

## Help mode

When the user sends `help`, `show help`, `what can this skill do?`, or `how do I use this skill?` after selecting or naming this skill, read [the help guide](references/help.md). Return its explanation, complete operation and profile catalogs, starting guidance, output choices, connection guidance, and examples. Include every named operation plus `help`, both explainer variants, and at least two examples per operation and per profile. Do not shorten the catalogs for brevity or start production. End by inviting the user to choose or adapt an example. Ordinary requests beginning with "help me create" are action requests.

## Scope and routing

Own branded and explanatory motion: launch systems, kinetic type, composited overlays, product choreography, architectural transformations, vector animation, mixed media, charts, and end cards. Exclude business building, pricing services, customer acquisition, and portfolio marketing.

Choose by the dominant deliverable. Narrative scenes, acting, dialogue blocking, and cinematic shot continuity belong with `ai-film-video-direction` when available. Use this skill for a product film whose central problem is product, graphic, or information choreography, even when its look is cinematic. In mixed projects, keep one shared brief and identify which portions each discipline owns. This skill remains usable by itself and does not require another installed skill.

Infer two independent choices:

| Operation | Result |
| --- | --- |
| `plan` | Brief, mechanic, design direction, storyboard, execution route, and risks. |
| `create` | Production package and, when requested and available, completed generated or composited media. |
| `revise` | Focused repair, extension, localization, restyling, or format adaptation. |
| `audit` | Evidence-based inspection of a brief, design sheet, prompt, plan, or actual render. Repair only when requested. |
| `prompt-only` | Complete prompts, reference map, settings, assembly notes, and checks without generation. |
| `help` | Usage guide only. |

Read only the selected profile, adding another when the treatment actually combines them:

| Profile | Read when |
| --- | --- |
| `launch-video` | [Launch video](references/launch-video.md): a product, feature, service, or brand reveal leads the story. |
| `live-footage-overlay` | [Live footage overlay](references/live-footage-overlay.md): graphics sit over supplied footage or an explicitly requested new performance. |
| `hyper-motion` | [Hyper-motion](references/hyper-motion.md): product assembly, decomposition, material action, or choreographed camera travel leads. |
| `real-estate-3d` | [Real estate 3D](references/real-estate-3d.md): architecture, plans, property geometry, and materialization lead. |
| `explainer-2d` | [2D explainer](references/explainer-2d.md): pure-vector or hybrid-2d-3d illustration explains a process. |
| `editorial-explainer` | [Editorial explainer](references/editorial-explainer.md): a sourced explanation, data, collage, or information design leads. |

Profiles are production methods, not fixed aesthetics. A restrained product study can use hyper-motion mechanics; an editorial explainer need not use paper collage. Requests for ideas may return a few meaningfully different mechanic and style options before expanding one. Do not force a concept-selection round when the user has already chosen or authorized a direction.

## Establish the brief and route

Read [production-system.md](references/production-system.md) for intake, defaults, production stages, variants, and delivery. Preserve the user's operation, brand, copy, assets, duration, destination, chosen model, budget, and prior approvals. Separate verified facts, approved creative choices, and labeled assumptions. Inspect available material before asking for missing inputs.

Choose the smallest viable path: direct generation, generation in segments, deterministic animation, or generated plates combined with deterministic graphics. Precise text, logos, UI, charts, and timing often require compositing. A request for one continuous shot remains a continuity requirement; explain the compromise before substituting visibly separate shots.

## Seal references and design

Read [reference-roles-and-design-systems.md](references/reference-roles-and-design-systems.md) for reference assignment, identity anchors, design sheets, typography, safe zones, and style adaptation. Name what each reference controls and what it does not control. A style sheet does not automatically define composition; an identity image does not prove unseen geometry.

Use supplied brand assets and facts. Invent original placeholders only when invention is requested or clearly appropriate, and label them. Do not carry example brands, house colors, promotional claims, or mandatory silence into a new project.

## Plan the motion

Read [storyboard-and-motion-spec.md](references/storyboard-and-motion-spec.md) for style frames, timed beats, state transitions, semantic cues, holds, and the optional validator schema. Establish one leading mechanic and one dominant focus per beat. Distinguish camera travel, element movement, screen-locked graphics, and world-anchored graphics. Preserve physical state after each action.

Use a design sheet, storyboard, or animatic to resolve expensive uncertainties. Respect existing approvals; do not impose another approval gate for every artifact. Match beat count and reading time to the content and output capability rather than a fixed interval.

## Compile and execute

Read [prompt-compiler.md](references/prompt-compiler.md) before writing a final prompt or adapting one to another model. Keep a complete production specification, then compile relevant details into supported inputs. Resolve contradictions, stale references, duplicated copy, and impossible timing before submission.

Read [text-data-and-compositing.md](references/text-data-and-compositing.md) when exact type, data, UI, masking, tracking, or editable layers matter. Route exactness to a deterministic renderer when available; treat generated lettering and graphics as candidates requiring inspection.

Read [tool-access.md](references/tool-access.md) when choosing a provider, connecting a service, submitting a job, or recovering a missing capability. Inspect actual model and endpoint schemas and current official documentation. Installing this skill does not install or authenticate generation tools. Preserve the chosen provider; do not silently switch models, upload destinations, or cost tiers.

## Verify, revise, and deliver

Read [verification-and-revision.md](references/verification-and-revision.md) before production, when inspecting outputs, and before revisions. Validate the plan when useful with [scripts/validate_motion_plan.py](scripts/validate_motion_plan.py), using the schema in the motion-spec reference. The helper needs Python 3.10+ and only the standard library; if execution is unavailable, apply the same checks manually. It checks declared structure, not pixels, audio, truth, or artistic quality.

Inspect actual media at transitions and holds and at normal playback speed when available. Report which checks were performed and which were unavailable. Fix the smallest failing part, preserve accepted work, and stop at the agreed attempt or spending limit. A job ID, written prompt, inaccessible link, or uninspected artifact is not a verified finished film.

Deliver the requested artifact first. For production, include the final media, editable layers when created, reference and copy manifests, prompts, actual provider settings, take status, assembly instructions, and unresolved limitations. Keep the package usable without this skill.
