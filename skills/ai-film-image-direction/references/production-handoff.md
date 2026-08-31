# Visual Production Handoff

Use this reference when organizing image assets for writing, performance, video generation, editing, or another production stage.

The handoff should preserve source authority, state, and reference roles. It must remain usable without this skill or any other skill.

## Visual bible package

Include the relevant subset:

- Project identity, version, format, medium, genre, tone, and audience.
- Style contract expressed through visible primitives.
- Palette and lighting logic.
- Character identity and costume system.
- Location geography and state system.
- Prop, vehicle, crowd, typography, and graphic rules.
- Technical output requirements.
- Locked, provisional, exploratory, rejected, and open decisions.
- Rights or permission notes needed for responsible use.

## Asset manifest entry

For every production asset, record:

- Asset ID, canonical name, type, project role, and version.
- Approval status and responsible source of truth.
- Visible state, view, expression, time, weather, damage, or transformation.
- Reference files with one role per input.
- Locked identity, design, geography, style, count, text, and technical properties.
- Properties that the asset must not control downstream.
- Provider, model, version, settings, and seed when available.
- Final prompt or edit contract when retention is useful.
- Output location, dimensions, file type, transparency, and crop.
- Verification status, known limitations, and generation-log link or summary.

Do not expose secrets or private permission evidence in the manifest.

## Reference-role map

For each downstream use, name the minimum approved inputs and their roles. Examples:

- Character identity plus scene-specific costume state.
- Base location geography plus a separate night or damage state.
- Prop construction plus the exact deployed mechanism state.
- Style contract plus palette reference, without the reference's characters or composition.
- First-frame composition plus canonical identity and location sources.

Avoid attaching the full library to every generation. More references can create more conflict rather than more control.

## Story and screenplay feedback

When sending findings upstream, report visual facts that may affect writing:

- A state, mechanism, costume, location, or prop requires a separate setup or transition.
- Two scripted locations cannot share geography without contradiction.
- A transformation or reveal needs a distinct pre-state and post-state.
- A protected likeness, design, logo, or private source needs a rights decision.

Do not rewrite story intent unless requested.

## Performance handoff

Provide the canonical character appearance, costume and physical state, scale, relevant prop relationships, and scene frame when they affect readable performance. Leave objectives, tactics, gesture, breath, eye behavior, and vocal delivery to performance direction.

## Video handoff

Provide:

- Canonical characters and exact scene states.
- Location geography, landmarks, and required lighting state.
- Prop or mechanism state and scale.
- Approved first frame, end frame, storyboard, or keyframe when available.
- Reference-role map and prohibited inheritance.
- Exact visible text and continuity constraints.

Do not add motion timing, shot count, optics, camera behavior, physics, dialogue ownership, or provider syntax unless those decisions were supplied by the video plan.

## Handoff verification

- Every file resolves or is attached through the host-supported mechanism.
- Canonical and state-specific assets are clearly distinguished.
- The consumer knows what each reference controls and must not control.
- Exact text, counts, geography, and visible state are explicit.
- No unapproved exploratory asset is presented as canonical.
- The packet identifies any property that remains unverified.
