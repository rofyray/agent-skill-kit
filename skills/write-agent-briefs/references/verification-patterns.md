# Verification patterns

Select only checks that can reveal a real failure in the requested work.

## Documents, decks, and PDFs

- Open or render the final artifact, not only its source representation.
- Inspect every page or slide for overflow, clipping, overlap, broken fonts, and template drift.
- Reconcile every displayed number and material claim to its source.
- Confirm links, navigation, notes, and exports work when relevant.
- Provide screenshots or rendered pages when visual review is part of acceptance.

## Research and recommendations

- Open the current primary source for each material claim.
- Verify that every citation directly supports the sentence attached to it.
- Record source date, uncertainty, and whether a claim is fact or inference.
- Apply the same criteria to every compared option.
- Try to disprove the leading conclusion with its weakest assumption and strongest counterargument.

## Code changes

- Reproduce the defect or baseline behavior before changing code.
- Add a failing test first when the failure is deterministic and testable.
- Run the narrow relevant checks during iteration, then the broader regression suite warranted by the change.
- Run type, lint, build, or static checks used by the repository.
- Inspect the final diff for unrelated changes, debug residue, and contract violations.
- Exercise the real public behavior when tests alone do not establish correctness.

## Data analysis

- Inspect schemas, units, time zones, missing values, duplicates, and population filters.
- Reconcile row counts and key totals before and after transformations.
- Spot-check representative records against the source.
- Make calculations reproducible and label assumptions.
- Test whether the conclusion changes under plausible alternative filters or definitions.

## Browser and interface work

- Load the actual page and exercise the complete target flow.
- Check required viewports, states, and interaction paths.
- Inspect screenshots as well as DOM or source code.
- Check console errors, network failures, keyboard operation, and relevant accessibility signals.
- Re-run existing UI checks and inspect nearby flows for regression.

## Content and messaging

- Compare tone and structure against named reference material.
- Verify every factual statement and remove unsupported specifics.
- Re-read for audience comprehension, repetition, and generic filler.
- Check the exact length and required format.
- State meaningful editorial choices and unresolved claims separately.

## Universal closeout

- List checks performed with results.
- List checks not performed with reasons.
- Confirm the output exists at the promised location and opens successfully.
- Do not claim completion when a required check is unavailable or failing.

