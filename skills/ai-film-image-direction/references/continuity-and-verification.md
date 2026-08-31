# Continuity Verification and Repair

Use this reference after generation, during an asset audit, or when repairing continuity drift. Inspect the actual images rather than grading prompts or filenames.

## Verify in risk order

1. Requested asset: correct type, subject, state, view, action, and production purpose.
2. Count and ownership: exact people, props, limbs, accessories, labels, and no duplicates.
3. Character continuity: face, silhouette, proportions, hair, skin, marks, costume construction, and style-specific anatomy.
4. State continuity: correct costume, damage, dirt, weather, age, transformation, open or closed mechanism, and hidden or revealed detail.
5. Location continuity: architecture, landmarks, entrances, exits, scale, reverse-view logic, permanent dressing, and motivated light sources.
6. Prop and vehicle continuity: geometry, material, size, orientation, markings, condition, mechanism state, and contact with characters or surfaces.
7. Style continuity: shape, line, rendering, palette, values, texture, background density, and finish.
8. Composition and physics: crop, hierarchy, perspective, anatomy, occlusion, weight, contact, shadows, reflections, and depth.
9. Text and technical output: exact writing, ratio, resolution, transparency, file type, edge quality, and unintended watermarking or logos.

Compare against canonical references at useful scale. Do not call two assets consistent merely because they share a prompt or model seed.

## Audit the asset system

For a library audit, classify each asset:

- Canonical and approved.
- Approved for a specific state or use only.
- Exploratory, superseded, or rejected.
- Visually inconsistent with an identified canonical source.
- Missing a required state, view, role, rights note, or technical property.
- Ambiguous enough to cause downstream misuse.

Look for systemic failures:

- Character identity changes with angle, scale, expression, co-actors, or light.
- Costume, weapon, hatch, injury, prop, or transformation state leaks into unrelated scenes.
- Location reverse views contradict architecture or landmark placement.
- Style references introduce their own characters, objects, settings, or logos.
- Palette and rendering drift between asset types.
- Multiple files claim canonical status without a recorded decision.

## Diagnose before retrying

Classify the failure source:

- Source design is ambiguous or inconsistent.
- Too many roles or states share one reference.
- Prompt hierarchy is unclear.
- The selected model lacks the required edit or reference control.
- The reference set exceeds a limit or contains conflicting information.
- A previous output, rather than the canonical source, accumulated drift.
- The requested composition or interaction is too complex for one pass.

Repair the cause, not only the visible symptom.

## Make a focused correction

Name the observable defect and the target state. Reassert the canonical properties most at risk and preserve accepted changes. Prefer:

- A localized edit for a localized failure.
- The original source plus the accepted donor reference for drifted edits.
- A separate state asset when one sheet causes leakage.
- A simpler reference set when roles conflict.
- A redesigned source asset when repeated failures expose an unstable identity or geography system.

Do not keep refining an asset that already passes merely to explore alternatives. Mark alternatives as exploration instead of silently replacing the accepted version.

## Control retries and cost

Track each attempt with model, version, settings, source references, requested change, outcome, and accepted or rejected status. Stop when:

- The asset passes the required checks.
- The user-defined generation or cost budget is exhausted.
- Another paid attempt needs authorization.
- Repeated attempts show no measurable improvement.
- The failure requires redesign, a different capability, or missing source material.

Do not impose a universal retry count. Escalate from prompt repair to source redesign or provider change only when the evidence supports it.

## Report verification honestly

Return the accepted asset and a concise status. Record remaining limitations that affect downstream use. If inspection was unavailable, state what could and could not be verified. If the tool returned only a queued job, link, error, or partial output, report that exact state.
