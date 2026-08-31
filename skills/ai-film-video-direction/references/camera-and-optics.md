# Camera and Optics

Use this reference to make camera and lens direction observable, physically coherent, and adaptable to the selected video model.

## Direct the image result first

Describe the visual consequence before numerical syntax:

- How much environment is visible.
- How close or distant the audience feels.
- Whether depth appears expanded, neutral, or compressed.
- Whether faces distort or remain natural.
- How foreground, subject, and background separate.
- What stays sharp and when focus changes.

Translate that result into focal length, field of view, named presets, or UI controls only when the tool supports them. Do not assume the same number means the same framing across formats, crops, and providers.

## Choose optics from content

Use shot size and optical behavior to serve the scene:

- Spatial context or unstable proximity may benefit from a wider view, but protect faces and edge geometry.
- Intimate observation may benefit from natural perspective and controlled background separation.
- Distant observation, isolation, or layered staging may benefit from compressed depth.
- A critical object may require an insert or macro behavior rather than an overloaded wide shot.

Do not hardcode a lens ladder, fashionable focal length, or cinematographer reference. Style should remain explainable through framing, depth, movement, light, color, texture, and timing.

## Specify the camera as a physical object

When camera movement matters, resolve:

- Starting position, height, side, orientation, distance, and framing.
- Support or stabilization character: locked, handheld, shoulder, dolly, crane, vehicle-mounted, aerial, or another physically meaningful behavior.
- Path relative to the subject and environment.
- Direction, speed, acceleration, deceleration, mass, and settle.
- Whether the subject, camera, or both motivate reframing.
- Obstacle avoidance, occlusion, parallax, and physical clearance.
- Final position, framing, focus, and whether the move resolves or remains in motion.

Prefer one legible move over stacked instructions such as orbit, push, crane, whip, zoom, and rack focus simultaneously. If the model exposes a named camera preset, map the desired path to it only after the physical behavior is clear.

## Keep camera behavior intentional

- A locked camera is still a choice; describe composition and what changes inside it.
- Handheld motion needs scale, rhythm, inertia, and recovery. "Shaky" alone produces random vibration.
- Smooth motion needs a path, speed change, and stopping behavior. "Cinematic" alone is not direction.
- A pan or tilt rotates from a position. A track, dolly, crane, or orbit changes position. A zoom changes focal length. Do not combine their meanings carelessly.
- Camera response should follow dramatic cause. Avoid autonomous wandering, unmotivated reframing, and floating through solid objects.

## Plan focus

Name the focus subject or plane at the start, any trigger for a focus transfer, its speed and character, and the final focus state. Use deep focus when geography or simultaneous action must remain readable. Use selective focus when the edit or performance benefits from controlled attention.

Do not request shallow depth merely as a quality synonym. It can erase blocking, props, mechanisms, and reactions the shot needs.

## Protect edit continuity

Track when relevant:

- Screen direction and which side of the action line the camera occupies.
- Eyelines and relative heights.
- Subject size and movement carried across a cut.
- Entry and exit direction.
- Match points for action, gaze, shape, sound, or camera motion.
- Deliberate axis crossings and the visual event that makes them readable.

The 180-degree convention is a tool, not a universal ban. Cross the line intentionally when geography, camera movement, a neutral shot, or a motivated reveal keeps the change legible.

## Direct cuts only when supported

For a model that can render an edited sequence, declare shot boundaries and the reason for each cut. Keep continuity facts repeated where the model requires them.

For a model that cannot control cuts reliably, generate separate clips from separate shot cards. Do not ask one prompt to simulate an entire edited scene and then blame continuity failures on wording alone.

## Verify the camera

Inspect whether the rendered clip preserves:

- Intended frame-one occupancy and composition.
- Shot size, perspective, depth, and subject separation.
- Camera side, path, speed, inertia, and final state.
- Focus subject and any transfer.
- Subject framing during movement.
- Readable geography and edit match.

If the camera fails while action and performance pass, repair the camera block without rewriting unrelated scene content.
