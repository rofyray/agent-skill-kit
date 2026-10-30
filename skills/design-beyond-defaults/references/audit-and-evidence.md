# Audit and evidence

## Keep conclusions separate

Audit inspects an implemented interface. Critique judges visible design. A screenshot-only request can support visual findings but cannot establish keyboard operation, routes, validation, or permissions. Remain read-only unless fixes are requested.

Classify observations as:

- Requirement failure: a reproduced broken journey, missing required content, or measured violation of an applicable criterion.
- Contextual design concern: a visible hierarchy, clarity, consistency, or craft problem whose impact depends on the brief.
- Preference: an alternative that is not demonstrably better under the requirements.

Do not turn style preferences into universal defects. Use the applicable accessibility criterion and method; WCAG 2 contrast ratios and APCA are different measures. Contrast alone does not prove accessibility compliance. Avoid numerical beauty scores as release gates.

## Collect evidence

Establish the target route/component, source revision or content fingerprint, viewport, state, and expected outcome. Reuse project tests and the host's supported browser capability. Record actual observations, including pre-existing defects. Check relevant journeys with meaningful assertions, not just that a page loaded or a screenshot exists.

Inspect narrow and wide renders, affected breakpoint boundaries, long/localized text, zoom/reflow, keyboard focus/order, touch, labels, non-color state cues, supported themes, reduced motion, asset loading, and load errors as relevant. Exercise the task's transitions, including failure and recovery. A sample of Tab presses is not a complete keyboard audit.

For each required item report pass, fail, not run, unsupported, or needs review. Include method and evidence location. Unavailable capabilities remain visible gaps. A fresh capture must match the tested revision and state; recapture or rerun affected checks after changes. Do not prefill success in a scaffold.

Follow the verification guide's capture-readiness checks. A partially rendered tooltip, offscreen column, or clipped input value is evidence to investigate, not sufficient proof of an authored defect or lost data. Reproduce the state, inspect containment or scroll reachability, and compare with the baseline before assigning a cause. Keep initial and corrected evidence distinct. For visual comparisons, report state-level tradeoffs, confidence, ties, and disagreements separately from reproduced requirement failures.

## Optional structured record

Use this only for substantial work, multi-route verification, or an explicit evidence deliverable. Python 3.10+ and local files are required; no packages or network are needed. Without them, keep the same fields in prose. The helper validates claims and compares contract inventories; it does not inspect screenshots, execute journeys, authenticate evidence, or prove the claims true.

```bash
python3 <skill-directory>/scripts/design_record.py init --target settings --revision <fingerprint> --output <record.json>
python3 <skill-directory>/scripts/design_record.py validate <record.json> --revision <current-fingerprint>
python3 <skill-directory>/scripts/design_record.py compare <before.json> <after.json>
```

Initialization creates an incomplete record without overwriting an existing file. Edit it with actual observations:

```json
{
  "version": 1,
  "target": "/settings",
  "revision": "source-fingerprint",
  "complete": false,
  "contracts": [
    {"id": "save", "requirement": "Saving persists the selected timezone"}
  ],
  "changes": [],
  "checks": [
    {
      "id": "save-after-reload",
      "contract": "save",
      "target": "/settings",
      "viewport": "390x844",
      "state": "changed timezone",
      "revision": "source-fingerprint",
      "status": "not run",
      "method": "browser journey: save, reload, inspect timezone",
      "evidence": [],
      "note": "Awaiting browser access"
    }
  ]
}
```

Pass/fail evidence entries are objects with nonempty `location` and `observation` strings, such as a test log path and its assertion outcome. For omitted or changed baseline contracts, an after-record change entry requires `contract`, `reason`, and `authorization` describing the actual user instruction. This is a declaration to be reviewed, never a permission grant from the JSON file.

Validation rejects malformed fields, duplicate IDs, unknown contracts, stale checked revisions, pass/fail without evidence, unexplained untested items, and a complete record without passing coverage for every contract. It cannot know whether a missing contract was never recorded. Compare reports removed/changed contracts and distinguishes declared authorized changes from unexplained differences; additions are shown too. Independently verify authority and actual behavior before accepting the comparison.

## Review and completion

Use a fresh visual critic for substantial design work when available. Give a separate functional reviewer the relevant requirements, source, and test evidence when the scope warrants it. Small tasks need no standing committee. Resolve disagreement through requirements and reproduction, not votes. Disclose self-review if independent context is unavailable.

Ordinarily use one or two correction rounds, then assess improvement and remaining budget. Stop when requirements are met, a real blocker or budget limit is reached, or repeated rounds do not improve the result. Report remaining gaps; do not relabel them pass. Audit-only returns findings without editing. After authorized fixes, rerun affected checks and capture fresh views.
