# Delivery, AI tells, and copy ownership

Use these passes after the direction is working. The goal is not to sterilize the interface. It is to remove choices that look unexamined and leave a smaller number of stronger decisions.

## Pass 1: subtraction

Inspect every visible element and ask what role it serves:

- function or interaction;
- necessary information;
- hierarchy or navigation;
- trust, safety, or status;
- accessibility or platform expectation; or
- the intended emotional experience.

Remove, merge, or simplify an element that has no defensible role. Prefer the smallest change that clarifies the design.

Pay special attention to:

- glows, gradients, shadows, and colored highlights added without purpose;
- containers around content that already groups itself;
- labels that repeat what an image, value, or position makes obvious;
- oversized empty regions that weaken information density;
- decorative badges, icons, dividers, and metadata;
- text that restates a nearby heading or control;
- custom buttons, fields, switches, and navigation that work worse than native or established components;
- excessive type sizes, weights, and colors; and
- motion that does not explain state, hierarchy, causality, or progress.

After removal, rebalance spacing and hierarchy. Deleting an element without recomposing the layout can leave the design feeling accidental.

## Pass 2: recognizable default patterns

An AI tell is evidence of an unexamined default, not proof that AI created the interface. Never condemn a single choice in isolation. Look for clusters, repetition, lack of product rationale, and mismatch with the committed direction.

### Layout and composition

- a centered hero followed by a uniform three-card feature row and generic call to action;
- text on one side and an interchangeable decorative graphic on the other;
- identical section rhythm, alignment, and density throughout the page;
- random asymmetry that follows no grid or compositional principle; or
- excessive whitespace used as a substitute for hierarchy.

### Typography

- a default font stack chosen without a platform or brand reason;
- every important phrase set in bold, uppercase, or gradient text;
- too many type sizes or weights without a stable scale;
- an ornamental display face introduced only to appear unusual; or
- loose marketing typography applied to dense product workflows.

### Color, surface, and effects

- purple-to-blue gradients, aurora backgrounds, or neon accents with no product connection;
- frosted glass, backdrop blur, glows, and floating shadows applied across most surfaces;
- an accent color sprayed across every interactive element;
- gradients on every surface to simulate depth; or
- inconsistent radii, borders, highlights, and elevation.

### Components and icons

- every piece of content wrapped in a large rounded card;
- icon-in-rounded-square patterns repeated for every feature;
- pills and badges used where plain text would communicate better;
- familiar sparkle, lightning, arrow, or magic icons used as generic decoration;
- custom controls that ignore platform conventions; or
- several redundant cues for one state, such as color, icon, badge, and label together.

### Imagery and motion

- generic gradient placeholders, abstract blobs, anonymous avatars, or stock-AI illustrations;
- generated media whose style does not match the interface;
- identical fade-and-rise animation on every element;
- staggered entrances that delay access to content; or
- motion added everywhere without a state or storytelling purpose.

## Repair the cause, not the symptom

For each cluster, ask:

1. What design decision was the model avoiding?
2. What does the product, audience, platform, or creative thesis actually call for?
3. Can the interface become clearer by removing the pattern?
4. If the feature remains, how can it become specific and intentional?

Do not replace one trend with another arbitrary trend. Recommit to the chosen design logic and make the fewest decisive repairs.

## Pass 3: human-owned interface copy

Copy is part of the design system. It controls hierarchy, density, trust, and the clarity of every action.

Prefer user-approved product language, brand examples, research, and factual source material. Preserve names, prices, dates, legal meaning, commitments, and technical claims exactly. Never invent customer quotes, testimonials, metrics, urgency, capabilities, or social proof to make a design feel complete.

Review high-salience strings:

- page title and primary headline;
- value proposition and subhead;
- navigation and section headings;
- buttons and calls to action;
- form labels, helper text, validation, and errors;
- empty, loading, success, and failure states;
- plan, pricing, trust, and legal language; and
- onboarding or transactional instructions.

Apply these tests:

- The headline names a concrete product, outcome, or tension rather than a generic aspiration.
- The subhead adds information instead of paraphrasing the headline.
- Calls to action describe the action or destination.
- Labels use the audience's vocabulary and match the underlying behavior.
- Every claim is supported by supplied evidence or removed.
- Inflated adjectives, filler, repeated explanations, and vague promises are cut.
- Sentence length, tone, and terminology remain consistent with the user's voice and context.
- Important caveats and error messages are clear without sounding punitive or evasive.

An AI cannot honestly claim that it rewrote copy by hand. If the user delegates copy drafting or revision, produce the strongest evidence-grounded version and identify it as AI-assisted. Ask the user to approve or revise important customer-facing language before publication when approval is not already present.

For a fast internal prototype, do not block the entire build on copy approval. Mark provisional strings clearly in the handoff and list the small set requiring human ownership.

## Final restraint check

Compare the finished interface with the selected thesis and required product job. The result should contain fewer arbitrary decisions, clearer hierarchy, more specific language, and no loss of essential behavior. If subtraction makes the artifact less understandable or less usable, restore the necessary element in a simpler form.
