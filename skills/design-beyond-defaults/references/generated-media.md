# Generated media for interfaces

Use generated images, shaders, 3D, or video when they give the design a meaningful identity or enable an interaction that code-only decoration cannot achieve efficiently. Media must serve the product, not merely demonstrate that a generation tool was available.

## Decide whether media belongs

Add generated media only when it improves at least one of these:

- comprehension of the product or feature;
- emotional tone or brand identity;
- spatial storytelling or state transition;
- perceived material, depth, or physical behavior; or
- a memorable interaction that supports engagement.

Do not replace a strong native component, readable content, or simple CSS solution with heavy media when the visual benefit is minor. Avoid generic decorative output, stock-AI imagery, and generated text inside images.

## Image generation

Coding agents often fall back to gradients, geometric blobs, and basic patterns because those are easy to write. When imagery is central to the direction, explicitly use an available image-generation capability instead of simulating the asset with generic decoration.

Define the asset's role before generating it:

- required subject and state;
- composition and crop in the interface;
- palette and lighting relationship to the page;
- transparent, solid, or environment-matched background;
- required continuity across variants;
- interaction or shader treatment; and
- resolution and responsive behavior.

Combine imagery with shaders or 3D only when the integration strengthens the thesis. Verify the image in the actual layout, not as an isolated attractive asset. Check crops, legibility, contrast, loading behavior, and unintended text or artifacts.

## Looping animated graphics

For a graphic that should feel embedded rather than like a rectangular video:

1. Design a short loop with motion that can join cleanly at its start and end.
2. Render against a solid or page-matched background when the effect depends on reflected or refracted environment color.
3. Bake required lighting, refraction, caustics, or shadows into the source when appropriate.
4. Remove the background with chroma keying or a video-matting model when transparency is needed.
5. Composite the result into the interface and inspect edge quality, spill, shadows, scale, and looping seams.

Provide a poster frame and graceful fallback. Respect reduced-motion preferences and avoid autoplay behavior that conflicts with platform rules or user control.

## Transitions between states

Video interpolation can connect two designed states more fluidly than independent clips:

1. Create or capture the initial keyframe.
2. Define the next state with a physically and compositionally compatible endpoint.
3. Generate the transition from the initial frame to the next state.
4. Use the actual final frame of that transition as the seed for the following transition.
5. Continue the chain so object identity, camera, lighting, and spatial geometry remain continuous.
6. Bind playback to the intended action, such as navigation, scrolling, or swiping.

For gesture-controlled playback, test the sequence in both directions and at slow scrub speeds. Check the exact boundaries between clips, not only normal-speed playback.

## Choose tools at runtime

Inspect available tools and their current schemas. Prefer an already authenticated built-in capability when it meets the requirement. When multiple providers exist, choose based on required editing control, keyframe support, transparency or matting, consistency, physics, duration, output format, privacy, latency, and authorized cost.

An aggregator can simplify access to changing video models, but it is an option rather than a dependency. Do not assume a particular provider or model remains best.

If no suitable generation tool exists, return a complete asset prompt, integration specification, and verification checklist. Do not present a prompt or placeholder as generated media.

## Credentials and cost

- Never request that a secret be pasted into a design prompt.
- Never echo, screenshot, log, commit, or ship a credential.
- Prefer host-managed connections, environment variables, or an existing secret store.
- If the user chooses a direct provider, recommend a separate revocable credential with the narrowest scope and a strict spending limit.
- Create or edit credential files only when the user requests configuration and the host permits it. Ensure local secret files are ignored by version control before use.
- Obtain authorization before installing software, creating credentials, or starting unbudgeted paid generation.

## Verify generated media

Inspect the integrated result in the browser or target runtime:

- scrub animated output through representative frames, including start, midpoint, end, and loop or clip seams;
- confirm continuity, physics, lighting, reflections, transparency, and edge treatment;
- test responsive crop and layout stability;
- verify loading, error, poster, and reduced-motion states;
- measure or reasonably assess file size, decode cost, and interaction smoothness; and
- confirm that media never blocks the primary task or required text.
