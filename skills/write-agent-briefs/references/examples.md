# Worked examples

## Contents

- [Customer feedback analysis](#customer-feedback-analysis)
- [Current competitor pricing](#current-competitor-pricing)
- [Checkout bug](#checkout-bug)
- [Brief audit](#brief-audit)

## Customer feedback analysis

Weak request:

> Analyze our customer feedback.

Brief shape:

```markdown
# Context
Analyze `/data/feedback-q3.csv` for the product team. The decision is whether next quarter's retention investment should prioritize onboarding or pricing. Focus on SMB customers who churned this quarter. Use `/docs/feedback-q2.md` as the structural reference.

# Task
Identify the three strongest churn themes, quantify their prevalence, and include representative quotes with record identifiers.

# Constraints
- Preserve the source population and distinguish direct feedback from inference.
- Do not expose customer names or contact details.

# Verification — do not finish until
1. Reconcile the analyzed row count to the filtered source population.
2. Trace every quote to a source record.
3. Re-check theme counts against the coded data and disclose ambiguous classifications.

# Output format
A Markdown memo with an executive recommendation, a theme table, supporting quotes, limitations, and the next question to validate.
```

## Current competitor pricing

Weak request:

> Research competitor pricing.

Brief shape:

```markdown
# Context
Compare the current public pricing of [A], [B], and [C] to inform our packaging review. Our current pricing table is at `[path]`.

# Task
Capture tier names, prices, included usage or seats, add-ons, and material restrictions.

# Constraints
- Use live official pricing and documentation pages.
- Separate public facts from inferences and mark contact-sales values unknown.

# Verification — do not finish until
1. Open every cited page and confirm each extracted value.
2. Record the access date and a screenshot or archived evidence where authorized.
3. Remove any value that cannot be verified.

# Output format
One comparison table followed by a short narrative describing the largest differences from our current model and the strongest caveat.
```

## Checkout bug

Weak request:

> Fix the checkout bug.

Brief shape:

```markdown
# Context
Ticket `#4421` reports that removing a coupon does not refresh the cart total. Relevant code is under `/src/cart`; tests are under `/tests/cart`. Preserve the public checkout API and existing analytics behavior.

# Task
Reproduce the defect, identify its root cause, implement the smallest durable fix, and prepare the change for review.

# Constraints
- Add a failing regression test before the fix when the defect is reproducible.
- Do not change unrelated checkout behavior or production configuration.

# Verification — do not finish until
1. The regression test fails before the fix and passes after it.
2. The full cart suite and repository-required type and lint checks pass.
3. The real coupon-removal flow updates totals correctly without console errors.
4. The final diff contains no unrelated changes.

# Output format
The code and test changes, plus a concise root-cause explanation and the commands and results used to verify them.
```

## Brief audit

Input:

> Make a polished Q3 deck for leadership.

Material audit findings:

- Missing source data and prior-deck or brand-template locations.
- Missing audience priorities and the decision the deck supports.
- “Polished” has no visual inspection procedure.
- No slide count, narrative structure, file format, or reconciliation requirement.

Ask for the blocking inputs or return a template with those fields visibly marked; do not fabricate paths or executive priorities.
