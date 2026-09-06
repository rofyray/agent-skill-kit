# Discovery and briefing

Use this reference to escape the first safe idea and produce a coherent, buildable direction. Exploration is not the final artifact. Its purpose is to expose useful possibilities, capture taste evidence, and converge on one clear thesis.

## Choose a divergence source

Use a hidden seed when the user wants surprise, the design space is open, or repeated attempts converge on the same familiar solution. Use taste-led exploration when the user supplies references, preferences, reactions, or a strong conceptual starting point.

When both are available, the user's taste and product constraints take priority. A seed may diversify open choices, but it must not override locked brand, behavior, platform, accessibility, or content requirements.

## Hidden seed procedure

Do not merely ask the model to make random choices. Introduce a complex seed before making open-ended design decisions.

When local Python execution and the bundled script are available, run:

```bash
python3 <installed-skill-directory>/scripts/design_seed.py
```

If the script cannot run, generate a long internal alphanumeric string before choosing the direction. This fallback is less independent from the model but still gives the decision process a concrete seed.

Interpret different parts or patterns in the seed as prompts for several decision families:

- palette temperature, contrast, saturation, and accent distribution;
- composition, grid behavior, density, rhythm, and asymmetry;
- typography category, scale relationships, and voice;
- materials, texture, depth, lighting, and edge treatment;
- imagery, illustration, data visualization, or spatial metaphor; and
- interaction, motion character, sequencing, and transition behavior.

Translate the seed through product judgment. Do not turn every character into a literal visual element or accept an incoherent result because it came from the seed. The seed exists to reach a less obvious starting point, not to replace art direction.

Do not expose the seed in the interface, customer-facing copy, or final design rationale. Record it only when the user requests reproducible experiments or a project design log. A user-supplied seed may be reused to reproduce a direction.

## Taste-led exploration

Use this sequence when the user needs help discovering an original brief:

1. **Go broad and shallow.** List enough materially different premises to expand the possibility space. Keep each description short. Change the source metaphor, spatial system, emotional posture, interaction model, or material language, not merely colors and fonts.
2. **Capture reaction evidence.** Ask the user what attracts them, what feels wrong, and which specific choices cause that response. Record positive preferences, negative preferences, and unresolved tensions separately.
3. **Visualize promising directions.** When suitable tools are available and the user wants visual exploration, create low-cost concepts or moodboards before committing to full implementation. Treat references as inspiration and quality context, not templates to copy.
4. **Sharpen the favorite.** Turn reactions into design rules. Replace vague adjectives with visible decisions and functional consequences.
5. **Write the final brief.** Give the builder one concise, internally consistent direction. Do not pass the raw idea list or discarded prompts as competing instructions.

If the user asks for a workshop, pause for selection. If they delegate the choice, recommend one direction using audience fit, product clarity, distinctiveness, feasibility, and the user's known taste.

Do not be afraid of a premise that initially sounds unlikely. Test it cheaply when possible. If it fails, discard the result. Preserve unsuccessful prompts only when the user wants an experiment log; they may become useful with later models.

## Final design brief

Include only fields that affect the result:

```text
Artifact and audience
- What is being designed, for whom, and for which platform or viewport.

Product job
- The primary action, required content, and behavior that must remain clear.

Target response
- What the user should feel, notice, understand, or want to do.

Creative thesis
- One sentence describing the committed visual and interaction idea.

Translation rules
- How the inspiration changes composition, hierarchy, typography, color,
  material, imagery, motion, and controls.

Restraint rules
- Patterns to avoid and limits that keep the idea coherent.

Media plan
- Required or optional image, shader, 3D, or video assets and their roles.

Locked constraints
- Brand, design-system, content, platform, accessibility, performance,
  technical, legal, and permission boundaries.

Acceptance evidence
- Rendered states, responsive views, interactions, comparisons, or rubric
  results that will demonstrate success.
```

## Polished build instruction

Use this shape when another agent or implementation pass will build the result:

```text
Create [artifact] for [audience and product job]. Preserve [locked behavior,
content, brand, and technical contracts].

Commit to this creative thesis: [one clear direction]. Translate it through
[specific composition, typography, color, material, imagery, interaction, and
motion decisions]. The interface should create [target response] while keeping
[primary action or information] immediately clear.

Avoid [specific unwanted defaults or overextensions]. Use generated media only
for [defined purpose] and only when the available tool can produce and verify it
within the authorized budget.

Render and inspect [required states and viewports]. Preserve accessibility,
responsive behavior, performance, and native platform expectations. Finish with
a subtraction pass, a default-pattern audit, and a final copy review.
```

Do not include exploratory prompt ladders in the final brief. The builder receives the polished destination, not the history of how it was found.

## Reference boundary

Extract high-level properties from references, such as density, typographic contrast, material restraint, information rhythm, or motion character. Do not copy a living creator's distinctive expression, a competitor's interface, protected artwork, brand assets, or proprietary copy unless the user has the rights and explicitly requests that use.
