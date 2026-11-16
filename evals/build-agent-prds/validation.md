# Validation record

Initial release validated November 13, 2026; testing-selection update validated November 14, 2026; Git naming update validated November 15, 2026 as recorded below. The evaluation artifacts are synthetic and contain no customer data. Product implementation was deliberately outside the evaluation scope.

## Executed checks

- Repository validation: all 18 skills passed, including frontmatter, metadata, Help, eval catalog, and text conventions.
- Skill-creator quick validation: passed. The default Python lacks PyYAML; the check used an existing cached PyYAML import path. The installed skill's packaging helper requires only Python 3.10 or newer and the standard library.
- New packaging tests: 14 passed. Coverage includes byte-preserving extraction with binary and Unicode assets, deterministic output, relative layout, metadata exclusion, missing entry point, existing-output protection, nested-output rejection, unwanted files, symlink files/directories/roots, nonportable separators, partial-copy cleanup, and CLI behavior.
- Final repository suite: 185 tests discovered, 167 passed, 18 optional code-slop detector integration tests skipped because the dedicated detector runtime was not configured. The first sandboxed run could not bind the existing localhost HTTP test; the final complete run with localhost access passed.
- Packaging: all 18 skill archives passed integrity and layout inspection. The final new archive contains 13 installable files, no evals/tests/caches, and matches its source bytes. Its helper executed successfully from a fresh extraction and produced a valid PRD ZIP.
- All local Markdown resource links in the new skill resolve. The core entry point is 64 lines.

## Executed behavior checks

Separate agents received realistic requests and permitted local inputs. The resource-rich authoring agent did not receive grading criteria. The receiving agent saw only the resulting ZIP, not the source chat, fixtures, or skill. No external services were used.

| Scenario | Observed result |
| --- | --- |
| Resource-rich Create | Produced a 12-file ZIP with a root PRD.md, focused specs, eight unique acyclic tasks, shared contracts, branch groups, coordinator rules, and full integrated acceptance. Actual setup commands remained proposed. |
| Asset preservation | Independently verified 67 extracted local file links and exact bytes for four supplied resources. The approved mark is selected; the old mark is preserved separately as history and excluded from runtime use. Accepted code and sample data are retained. |
| Single small PRD | Produced one Markdown PRD with canonical checkbox tasks and final acceptance; did not invent framework, storage, or verified commands. No unnecessary ZIP was required. |
| Audit | Identified contradictory dependencies and a cycle, conflicting schema writers, unsupported DONE status, and missing combined-app acceptance. Returned findings without implementing or rewriting the plan. |
| Help | Returned all four modes with two examples each and clarified asset/ZIP handoff and the authoring boundary. |
| Missing capabilities and source | Explicitly identified inaccessible screenshot, affected blocked work, and incomplete ZIP delivery; provided named copyable content without inventing a screenshot or download. |
| Revise | Preserved IM-02 and prior evidence as history, reopened changed acceptance, updated contracts and final tests, retained the original fixture, and generated a new verified ZIP. |
| Fresh-recipient intake | Located reusable code/data/media, selected the approved asset, identified SH-01 as initially eligible and the two parallel streams after SH-02, and recovered branch/resume/final acceptance rules. Found no execution-blocking contradiction or missing linked input. |

The generated product was not built. Passing handoff checks do not establish that its future application acceptance tests pass. Documented implementation proposals still require implementation-time discovery and confirmation as specified in the generated PRD.

## Without-skill comparison

A separate fresh agent received the same Reading Shelf request and attachments with instructions not to load skills. It also produced a usable ZIP and preserved the required assets. Its plan used a task table and README entry point and did not spell out the skill's maximum-useful-subagent scheduling or durable resume protocol. The skill-assisted result supplied those contracts and canonical checkbox state as intended.

This is one qualitative paired exercise, not a benchmark or proof of a general quality improvement. Both outputs had useful requirements, parallel feature scopes, and integration scenarios. No token, latency, or statistical quality claim is made.

## Limits and retained artifacts

These behavior checks ran through the available Codex agent runtime. Claude, Cursor, Gemini, ChatGPT Web, and desktop import behavior were not exercised. Remaining cases in cases.json, including a standalone no-subagent-resume scenario and embedded source-instruction/non-trigger routing cases, are prepared for future runs and are not claimed as executed model evaluations. Some equivalent boundaries were inspected in generated outputs and source, which is weaker evidence than running each case.

Local working artifacts are retained under `output/build-agent-prds-evaluation/`, outside the installable package and version control: skill-assisted creation, single-file and audit results, edge cases, baseline, and recipient intake. The reusable fixture inputs and case expectations are versioned here. The distributable skill is `dist/skills/build-agent-prds.zip`.

## Testing-selection update: November 14, 2026

Replaced unconditional integration/E2E requirements with explicit unit, integration, and E2E applicability decisions based on scope, boundaries, impact, and existing project gates. Final acceptance still covers the entire agreed scope. Required, not applicable, and pending discovery are distinct from execution status; unavailable required checks remain blocked. Updated all output templates, related guidance, metadata, Help, and the catalog entry consistently.

Three fresh evaluating agents used the revised skill for seven requests, without access to case expectations or each other's outputs. The primary agent inspected the generated artifacts against the expected behavior:

| Case ID | Observed result |
| --- | --- |
| unit-only-contract | Selected required unit coverage for the complete clamp contract; integration and E2E were not applicable with concrete reasons. Final acceptance did not invent an application or workflow harness. |
| adapter-unit-integration | Selected unit checks for pure key validation and integration checks against actual SQLite, including rollback and persistence; no separate E2E workflow was invented. |
| all-three-service-workflow | Required all three levels and used actual public HTTP workflows for E2E without browser tests. Produced a six-file ZIP with concrete unit, boundary, and workflow scenarios; commands and fixture access remained setup work. Independently verified extracted bytes and all 36 local file links. |
| blocked-is-not-inapplicable | Rejected the checkout completion claim; actual provider and complete checkout checks remained required and blocked by missing sandbox access. Preserved unit results as limited evidence. |
| shared-change-existing-gates | Expanded a one-line helper change to dependent API/worker coverage and required access-control workflows. Preserved mandatory gates and reused existing coverage subject to assertion/boundary inspection; did not invent commands or prior evidence. |
| pending-impact-discovery | Required parser units while leaving integration/E2E pending caller and policy discovery with an owner/task. Required resolved selection before final acceptance. |
| revision-new-boundary | Preserved reported FM-01 identity/history for unchanged formatter behavior, introduced new CLI task IDs, and required actual file-boundary and CLI workflow coverage for expanded scope. Historical units did not count as final CLI acceptance. |

All seven artifacts met the evaluated test-selection expectations. They are plans, not evidence that the described products have been implemented or that their future tests pass. The executed requests are now included in cases.json, which contains 18 cases in total; this update does not claim that all 18 were rerun.

Technical checks: repository validator passed for all 18 skills; skill-creator quick validation passed with cached PyYAML; the repository suite discovered 185 tests, with 167 passed and the same 18 optional detector integration tests skipped. All 18 skill archives passed integrity/layout checks. The updated 13-file archive matched source bytes, all skill-local links resolved, and its extracted standard-library helper successfully created and verified a sample PRD ZIP. The core is now 66 lines. No executable helper code changed in this update.

Current artifacts are retained locally under `output/build-agent-prds-testing-evaluation/`. No new without-skill comparison or other-client runtime/import test was performed for this correction; the earlier baseline exercise and client limitations above remain historical evidence only.

## Git naming update: November 15, 2026

Added a complete lowercase commit and branch naming contract to the generated driver and single-file PRD templates, with all eleven commit types, purpose-based selection, optional branch ticket IDs, canonical ID mapping, history preservation, and explicit handling of conflicting repository rules. Removed the previous codex branch-prefix fallback. Generated handoffs contain the contract inline and require no access to the installed skill.

Three fresh evaluating agents used the revised skill for six requests without case expectations or access to each other's outputs. The primary agent inspected the resulting documents:

| Case ID | Observed result |
| --- | --- |
| git-no-ticket | Kept F-01/F-02 task IDs while proposing `feat/format-integers-with-commas`, with no invented ticket. Included the complete lowercase contract and selected unit-only coverage for the standalone helper. |
| git-ticket-bundle | Mapped canonical PROJ-42 and AUTH-01/AUTH-02/AUTH-03 to one `feat/proj-42-google-sign-in` branch. Produced a four-file ZIP with full inline naming guidance, lowercase proposed commits, required unit/integration/E2E coverage, and explicit repository/access blockers. Independently verified ZIP integrity, inventory, and source-byte equality; the evaluator also verified all 20 relative file/anchor links. |
| git-purpose-selection | Correctly selected feat for a UI feature with tests, fix for a visual bug, style for indentation, build for a dependency, test for test-only changes, and ci for CI caching. Used hotfix and release as branch categories with valid commit types. Preserved actual product-copy and source-path casing. |
| git-conflicting-repository-rule | Identified the enforced feature prefix, uppercase ticket requirement, and exact Signed-off-by trailer as conflicts. Required an authoritative resolution before affected mutations without bypassing hooks or corrupting metadata. |
| git-existing-history | Preserved the existing mixed-case branch, historical commit, completed AUTH-01, and canonical PROJ-42. Applied lowercase naming only to the new password-recovery work and did not invent implementation scope or historical evidence. |
| git-id-preference-unclear | Asked one concise ticket-inclusion question, retained canonical TASK-88, and delivered a draft using an explicitly provisional ID-free branch. Did not assume that an available ticket automatically belonged in the branch. |

All six artifacts met the evaluated naming expectations. Proposed product tests were not executed and do not constitute product implementation evidence. The catalog now contains 24 cases; this update does not claim that all earlier cases were rerun.

Technical checks: all 18 skills passed repository validation; skill-creator quick validation passed with cached PyYAML. The full repository suite discovered 188 tests: 170 passed and 18 optional detector integrations skipped because their dedicated runtime was not configured. All 18 skill archives passed integrity/layout checks. The updated skill archive contains 14 installable files, matches source bytes, and excludes evaluation artifacts. All skill-local links resolve; its freshly extracted helper successfully produced a sample PRD ZIP. Fourteen commit examples and eleven branch examples in the new contract passed lowercase and read-only Git branch-syntax checks. Generated outputs were also inspected for lowercase examples, resolved template prompts, and independence from installed-skill links. No executable helper code changed.

Current artifacts are retained locally under `output/build-agent-prds-git-evaluation/`. No new without-skill comparison or other-client runtime/import test was performed; prior baseline and client limitations remain historical evidence only.
