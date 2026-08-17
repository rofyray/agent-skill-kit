# New-image creation brief

Use this reference only for generating a new image. Convert the user's request into the smallest complete visual brief; omit fields that do not affect the intended result.

## Brief fields

### Purpose and image type

Name the deliverable and intended use: portrait, product photograph, editorial image, architectural visualization, advertisement background, social post, or another concrete type. Let the use inform polish, crop, negative space, and visual hierarchy.

### Subject

Describe the subject's visible properties. For people, include only relevant age range, appearance, clothing, and expression. For products and objects, specify geometry, material, finish, color, and condition.

### Action and interaction

State what is happening, gaze direction, gesture, motion, and how subjects touch or occlude one another. Prefer one readable action over several competing moments.

### Setting

Specify location, era, weather, time of day, and only the background details that establish the scene. Avoid decorative clutter that the user did not request.

### Composition

Define:

- aspect ratio;
- shot size, such as close-up, medium, wide, or full-body;
- camera height and angle;
- subject position and visual hierarchy;
- lens or photographic perspective when relevant; and
- negative space required for a layout purpose.

If the user provides no ratio, infer one from the intended use and state it in the instruction without pausing the task.

### Lighting

Describe the motivated light source, direction, softness, color temperature, contrast, and expected shadows. Use a coherent setup such as overcast daylight, soft window light, golden-hour backlight, or clean studio lighting.

### Photographic language

Choose one compatible look: candid documentary, clean ecommerce studio, editorial portrait, phone snapshot, macro product photography, or another recognizable photographic treatment. Request natural textures, believable materials, realistic skin, and subtle imperfections when photorealism matters.

### Constraints

Include only constraints relevant to likely failure modes. Common examples are no watermark, no unintended writing, no duplicate objects, no malformed hands, and no unrequested trademarks.

## Prompt assembly

Use this order:

```text
Create a photorealistic [image type] for [intended use].

SUBJECT: [visible description]
ACTION: [action, pose, gaze, interactions]
SETTING: [location, time, weather, background]
COMPOSITION: [ratio, shot, camera, placement, negative space]
LIGHTING: [source, direction, softness, temperature, shadows]
PHOTO LOOK: [coherent photographic treatment and material realism]
CONSTRAINTS: [short list of relevant exclusions]
```

Do not pad the instruction with synonyms for quality. Concrete visual relationships are more useful than repeated claims that the result should be beautiful or professional.
