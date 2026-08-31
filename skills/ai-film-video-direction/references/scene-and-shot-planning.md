# Scene and Shot Planning

Use this reference to convert story material into a producible scene plan and to seal the context of every generated shot.

## Start from dramatic function

Before choosing camera or prompting syntax, state:

- What changes in the scene.
- What the audience must understand, feel, or anticipate.
- Which action, line, discovery, or decision carries that change.
- What enters the scene as established continuity and what must leave it changed.
- How the scene connects to the prior and next edit.

If the user supplies only a scene idea, create a compact local treatment. Do not expand it into an unsolicited screenplay rewrite.

## Seal the current-shot context

Each generation must be independently understandable. Do not rely on hidden conversational memory or phrases such as "same as before."

For each shot, declare:

- Scene and shot identifier plus version.
- Intended duration and real-time or compressed-time behavior.
- Exact visible character count and identity.
- Exact important prop, vehicle, creature, or mechanism count.
- Location and current state, including time, weather, damage, occupancy, and practical lights.
- The action and dramatic change contained in this shot.
- Continuity entering and leaving the shot.
- Only the references active for this shot.

Use exact counts when duplication or omission would damage the result. Do not count irrelevant background texture unless it must be controlled.

## Assign reference roles

Treat references as scoped evidence, not as a pile of inspiration. Give every attachment one or more explicit roles:

- Character identity or face.
- Current body, age, injury, dirt, wetness, transformation, or other state.
- Wardrobe state.
- Location identity and geography.
- Prop, vehicle, creature, or mechanism design and state.
- Style, palette, material, or rendering behavior.
- First frame, end frame, composition, motion, pose, or camera path.
- Voice or performance identity.

Keep only active references in the current shot. A location reference normally controls layout, landmarks, architecture, materials, and atmosphere, not its original framing. If references conflict, name which role wins. Do not use a flawed generated take as a new canonical identity reference when the approved source remains available.

## Map geography before motion

Describe the stable location in words that can survive a change of angle:

- Distinctive landmarks and what sits between them.
- Character and prop relations to those landmarks.
- Screen-left, center, screen-right, foreground, middle ground, and background relations for the current view.
- World-relative direction when it matters, such as northbound platform edge or the door behind the desk.
- Entrances, exits, paths, obstructions, sight lines, and interaction surfaces.

Landmarks and relational language are usually more useful than false precision. Add measurements only when scale or travel distance is materially important and the tool can use them.

## Design frame one

Treat the first frame as a contract. State:

- Who and what is already visible.
- Framing, shot size, horizon, and major negative space.
- Character positions in width and depth.
- Torso orientation, gaze, hand and prop ownership, and points of contact.
- The camera's side of the action and initial focus.
- The source and direction of motivated light.
- The first readable action or state.

Avoid an unintended empty establishing frame. If the first frame should be empty, state when and where the subject enters and why.

## Block readable action

For every active character, define only what the camera can observe:

- Starting position and depth plane.
- Facing, gaze, and relationship to partners or objects.
- Path, destination, and any crossing.
- Contact with floors, furniture, props, vehicles, or other bodies.
- Who owns each prop before, during, and after an exchange.
- End position and leaving state.

Use screen relations for the current composition and world relations for continuity across angles. Do not prescribe decorative movement that has no story, physical, or edit function.

## Choose a shot structure

Prefer a single take when continuous time, geography, performance pressure, choreography, or an irreversible event is the point and the selected tool can sustain it.

Use cuts when the scene needs a clear change of viewpoint, scale, information, time, location, reaction priority, insert, or visual class. If the model cannot reliably create multiple shots inside one generation, generate each shot separately and assemble them in the edit.

Do not force a master shot. A wide establishing view can lock geography when it is useful, but a scene may begin on a detail, face, threshold, moving subject, or offscreen cause.

## Write a shot card

Use fields proportionate to the task:

```text
SCENE AND SHOT
Intent:
Duration:
Format:
Visible characters and counts:
Important objects and counts:
Active references and roles:
Location state and landmarks:
First frame:
Blocking and action:
Camera and focus:
Dialogue and sound:
Continuity in:
Continuity out:
Edit relation:
Generation risk:
Pass criteria:
```

For an edited scene, make each shot card independently runnable while preserving shared continuity facts.

## Control complexity

Estimate the burden created by interacting characters, dialogue, precise hands, mechanisms, transformation, fast motion, camera movement, environmental effects, lighting changes, and multi-shot structure.

Split or simplify when too many uncertain systems must succeed at once. Useful separations include:

- Reaction from action.
- Insert from ensemble staging.
- Transformation stages from ordinary motion.
- Complex mechanism operation from dialogue.
- Audio generation from video when the tool lacks reliable sound or speaker control.

The correct complexity limit is model-specific. Inspect the actual tool rather than imposing a universal two-character, one-location, or fixed-duration rule.

## Plan threshold events

For doors, portals, vehicle entry, transformations, impacts, reveals, and other thresholds, describe:

1. The stable state before the threshold.
2. The initiating cause.
3. Contact or crossing.
4. The observable transition.
5. The stable state after it.

When appearance or mechanism states differ materially, use separate approved references for each visible state and assign them to the relevant phase.
