# Design Beyond Defaults evaluation protocol

Routing, instruction following, functional correctness, and visual preference are separate results. A zero-error helper result is not a design score or proof of a working journey.

## Behavioral cases

`cases.json` contains the original 15 cases, 20 expansion cases, and seven cases informed by the fuller visual review. Give a fresh evaluator only a natural request, the selected skill, and the minimum relevant artifacts. Do not give the `expect` assertions to the acting evaluator. Grade its actual response/artifacts afterward. Keep unavailable capabilities explicit rather than treating a written plan as executed verification.

The settings fixture provides working local persistence, native email validation, a billing anchor, and an analytics hook. Serve it locally; clear the fixture's localStorage between independent arms. No real account, payment, booking, or external endpoint is involved. Test invalid submission and save/reload, not just a success message or unchanged handler name.

## Rendered comparison

`rendered-briefs.json` defines the original eight pairs. Its historical held-out flags describe the first expansion run only. All eight are now familiar regression briefs; do not reuse those flags to claim new held-out evidence. Create fresh held-out briefs after the instruction freeze, before exposing the evaluator to either arm's output. `heldout-briefs-2026-10-29.json` records the two briefs authored after this revision's freeze; they are held-out evidence for that run only and become regression cases for subsequent revisions.

1. Snapshot the previous skill before changes.
2. Use a fresh builder context per brief and arm, with matched task, fixture, available tools, model setting, and resource constraints. Record any difference. Do not show builders the other arm or intended outcome.
3. Write artifacts and capability reports to an ignored output directory. If builders cannot render, record that limitation and test centrally. This measures artifact generation under that constraint, not the entire interactive workflow.
4. Capture the same desktop and phone views in both arms with identical entered text, quantities, filter combinations, validation triggers, and route state. Record those inputs with the source hashes. Matching a state category alone is insufficient when content length or errors can change layout. Verify functional requirements independently through actual browser interactions. Record failures before any repair.
5. Randomize anonymous labels per pair. A fresh critic sees only the rendered images and a stable rubric: hierarchy, typography, spacing, coherence, task clarity, and responsive craft. It infers the pursued direction and returns a preference or tie with visible reasons. Do not expose skill identity, source, builder rationale, prior findings, or desired score.
6. Repeat uncertain judgments within the authorized budget. Do not turn a small model-judged sample into a statistically general claim. Preserve losses and ties in the report.
7. If a defect requires instruction changes, rerun the affected case in a fresh context, distinguish initial versus revised results, and invalidate stale evidence. A visual preference loss alone is not a requirement failure.

For a browser-enabled workflow evaluation, give both arms equal browser access, independent visual feedback, and bounded correction opportunities. Use isolated browser contexts and local storage per arm. A shared browser service is acceptable only if each builder controls its own context/pages and cannot navigate or close another task's page. Preserve initial artifacts and evidence before corrections, and use a fresh critic for final comparisons. Judge the whole relevant task using matched states, not only the opening page. Keep state-level tradeoffs, ties, confidence, and unresolved preferences visible.

Wait for the intended state and capture settled native UI. A transient validation popover image does not establish unreadable authored messaging. Do not infer data loss from locally scrollable tables or text fields; inspect reachability and row association. Check content bounds in addition to document overflow. `fixtures/annotation-workspace-before.html` deliberately retains the observed narrow-width containment defect for a scoped forward test; it is not a production template.

Use meaningful route-specific content and non-default states for multi-route evaluation. Repeated shell cards under different headings establish shared styling only. Frozen instructions, generated briefs, arm mappings, capability constraints, initial/final artifacts, and actual browser results belong in the run manifest. A score or preference tally never substitutes for those records.

## Deterministic and browser checks

Run the repository validator and unit suite. The new helpers require only Python 3.10+ and the standard library. `test_design_expansion.py` checks stale and missing evidence, false completion, changed/removed contracts, malformed inputs, safe initialization, catalog containment, declared contrast pairs, and specimen/profile parity.

`browser-specimens.js` is an optional function for an available Playwright-compatible host, not a required skill dependency. It assumes a loopback preview server on port 8765. It checks every material at 320, 390, 768, 780, 781, 1280, and 1920 pixels, including both sides of the current layout breakpoint. At 320 and 1280 pixels it captures invalid, confirmed, and empty states and exercises keyboard submission, visible focus, selection, zero counts, filters, recovery, and clearing stale confirmation. It returns explicit failures; its caller should fail the run if that list is nonempty. Inspect the screenshots separately; overflow measurements cannot establish visual quality. Adapt the preview origin to the actual test environment.

Use native host browser tools or the project's existing stack elsewhere. Do not install a browser runtime just because a fixture file exists. Include observed coverage and untested clients in the results, then inspect the packaged ZIP for references, assets, notices, and exclusion of eval/development files.

`browser-comparisons.js` runs selected journeys against the sixteen generated comparison artifacts under `output/design-expansion/renders/`, using the same loopback preview. Read [the expansion results](results-2026-10-29.md) for actual coverage, failures, visual preferences, protocol deviations, and limits.

The [revision evaluation](results-revision-2026-10-29.md) records the later whole-task review changes, seven additional behavioral cases, stronger material-state checks, and browser-enabled paired workflow run. Keep its initial/final outcomes separate from the historical expansion run. If a comparison later needs normalized-input evidence, preserve the original verdict and obtain a fresh blind supplemental judgment; report disagreement instead of silently replacing the result.
