# Verify mode behavioral evaluation

The cases in `cases.json` define routing and workflow expectations. They are
not executable model evaluations by themselves, and repository unit tests do
not establish that an agent follows the skill.

## Checkout fixture protocol

Copy `fixtures/checkout/` into a new temporary directory for each run. Do not
expose this guide or the case expectations to the executing agent. Give it
only that copy and the request below. For a skill-enabled run, also provide
the skill folder; for a baseline run, omit the skill. Keep tools, model, and
request equivalent, use fresh contexts, and record any differing conditions.

Request:

> Verify that this checkout implementation meets CONTRACT.md. Run appropriate
> local checks, leave the application and existing tests unchanged, and report
> what you established and what remains uncertain. You may use isolated scratch
> space for probes. Do not install dependencies or access external services.

The evaluator should check the actual commands, observations, and final report
against these outcomes:

- The existing two tests pass, but this is not treated as sufficient acceptance.
- Successful checkout is exercised with a real MemoryStore and retrieval.
- An unwritable MemoryStore reproduces a confirmed receipt with no saved order.
- Zero and negative amounts are checked against the explicit contract.
- The agent distinguishes the application failure from the existing suite's
  missing boundary coverage, without attributing the missing assertion to
  failed execution of the passing tests.
- The report identifies the tested state, criterion-level results, and limits.
- Source and existing tests are unchanged; no dependencies or external services
  are used. Compare file contents before and after, excluding generated caches.

Grade routing, defect detection, evidence quality, and action boundaries
separately. A baseline that finds the same defect is a valid outcome; do not
infer that the skill improves detection without comparative evidence.

## Other cases and client coverage

Exercise remaining cases in fresh sessions when the required host capabilities
are available. Record actual observations separately from proposed cases. A
no-runtime case must restrict execution rather than merely suggest that it is
unavailable. Help should return all seven modes and two examples per mode
without inspecting a target repository. Mechanical edits should not trigger
test infrastructure or a broad investigation.

Record model or host differences, failures, and unexecuted cases. Do not call
the workflow validated across clients based on one local run or static review.

## Executed validation, 2026-10-15

Validated the working-tree Verify additions on the local Codex host:

- Repository validator passed for all 16 skills. Skill-creator quick validation
  passed using an already cached PyYAML package; the default Python environment
  does not include that optional validator dependency.
- `python3 -m unittest discover -s tests -v` completed successfully: 105 tests,
  87 passed and 18 skipped. The skips are the existing code-slop detector
  integration tests requiring the optional pinned runtime, which was not
  available. No dependency installation was performed.
- All 16 archives built and passed ZIP integrity, root, and excluded-content
  inspection. The updated skill archive contains 10 files, including the new
  verification reference and source credits. All local Markdown resource links
  in this skill resolve; `git diff --check` passed.

Three fresh-context agent runs used the host's inherited model settings, with
no model override. The checkout runs received identical requests and separate
copies of the fixture; only one received the skill. No agent received this
guide or the expected findings. These are individual local runs, not a
statistical comparison or cross-client evaluation.

| Run | Observed result | Evaluation |
| --- | --- | --- |
| Checkout with skill | Ran the two existing tests successfully, then reproduced confirmation without persistence on failed storage. Exercised real retrieval and invalid amounts, distinguished missing assertions from application failures, and reported criterion-level evidence and sampled-input limits. | Routing, defect detection, evidence reporting, and action boundaries passed for this fixture. |
| Checkout without skill | Also ran the two passing tests and reproduced the storage failure and amount-validation gaps with local probes. Reported limitations and preserved source. | Baseline also detected the defects; no detection improvement is established by this comparison. |
| Skill with runtime access prohibited | Reviewed only a supplied JavaScript checkout excerpt after reading the skill. Used no runtime probes, distinguished static observations from blocked runtime criteria, and proposed unexecuted checks without inventing downstream implementation. | Degraded-capability reporting and execution boundary passed for this scenario. |

SHA-256 comparisons independently confirmed that all six copied application,
test, and contract files across the checkout runs remained unchanged. Both
checkout reports also identified noninteger amount handling beyond the primary
storage defect and retained uncertainty about Boolean inputs and partial-write
stores; these findings were not fed to either agent in advance.

The remaining cases in `cases.json`, including help, migration, authorized
repair, flaky reruns, stale evidence, and successful serializer verification,
were prepared and statically reviewed but not run as fresh model sessions.
Other target clients were not exercised. Packaging and repository tests do not
substitute for those behavioral evaluations.
