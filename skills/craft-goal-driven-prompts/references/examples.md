# Worked examples

## Engineering: match a reference interface

Weak request:

> Make this settings page look exactly like the screenshot and keep improving it.

Goal-driven shape:

```markdown
# Goal
Make the settings page visually and behaviorally match the supplied reference at the supported desktop and mobile viewports.

# Context and inputs
- Inspect the current application and the supplied reference images before editing.
- Preserve the existing framework, public routes, and data behavior.

# House rules
- Do not replace working application architecture merely to simplify the page.
- Preserve keyboard access and visible focus states.
- Do not change unrelated screens.

# Definition of done
1. The page matches the reference layout at 1440×900 and 390×844 without overflow.
2. Every visible control has the same state and interaction represented in the reference.
3. Existing tests pass and no console error occurs during the settings flow.
4. An accessibility check finds no critical violations.

# Verification
- Capture the two required viewports and compare them with the references.
- Exercise every interactive control as a user.
- Run the existing test and accessibility commands.

# Iteration protocol
Evaluate the current screenshots and behavior, fix the largest observed mismatch, and repeat the full verification until all criteria pass. Use a fresh-context visual reviewer when available.
```

The prompt defines the visual and behavioral bar without prescribing CSS or component steps.

## Creative: produce a landing-page concept

Weak request:

> Write a really compelling, premium landing page.

Goal-driven shape:

```markdown
# Goal
Create a landing-page concept that makes operations leaders understand the product's value within ten seconds and motivates qualified visitors to request a demo.

# House rules
- Use only claims supported by the supplied product brief.
- Avoid generic AI language, invented customer quotes, and unsupported metrics.
- Preserve the approved brand voice examples.

# Definition of done
1. A cold reader can correctly state the audience, problem, and outcome after reading the hero.
2. Every factual claim maps to the product brief.
3. The page has one primary call to action and a coherent objection-handling sequence.
4. A rubric review scores clarity, specificity, credibility, and voice at least 4/5 each.

# Verification
Generate three materially different directions, grade them without author rationale, keep the strongest elements, and produce one final concept with the evidence table.
```

The rubric replaces subjective words such as “premium” with observable qualities.

## Research: decision brief

Weak request:

> Research our options thoroughly and recommend the best one.

Goal-driven shape:

```markdown
# Goal
Recommend the best option for the stated decision, using current primary evidence and making the tradeoffs auditable.

# House rules
- Separate sourced facts, calculations, and inferences.
- Use current primary sources for claims that can change.
- Do not silently fill missing decision criteria with personal preference.

# Definition of done
1. Every candidate is evaluated against the same weighted criteria.
2. Material claims have direct source links and dates.
3. Sensitivity analysis shows whether reasonable weight changes alter the recommendation.
4. Unknowns and disqualifying risks are explicit.

# Deliverables
- A concise recommendation.
- A comparison table with sources.
- Risks, unknowns, and the next validation step.
```

