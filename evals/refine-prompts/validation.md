# Validation record

## Executed locally

- Repository validator: all 15 skills passed.
- Skill-creator quick validator: passed using the existing isolated Python environment with PyYAML. The default Python lacks this optional validator dependency; the skill's helper uses only the standard library.
- New helper suite: 14 tests passed, including CLI behavior, variable loss, missing exact requirements, invalid input, input preservation, and explicit non-validation of semantic changes.
- Repository suite: all 100 tests passed with CODE_SLOP_TEST_PYTHON pointing to the existing isolated code-slop runtime, including the 18 detector integration tests skipped in the default environment.
- Packaging: all 15 archives passed integrity and layout inspection. The new archive contains 10 installable files; its helper ran successfully after extraction into a temporary directory.
- Every local Markdown resource link in the new skill resolves.

## Prepared, not runtime-evaluated

The 22 cases in cases.json describe routing and workflow expectations. They include ordinary repairs, conflicts, exceptions, assembly variants, examples, Spanish input, missing capabilities, model upgrades, injection attempts, and non-trigger requests.

These cases have not been run through fresh model sessions or across Codex, Claude, Cursor, Gemini, and ChatGPT clients. Static review and Python tests do not demonstrate improved model output quality. The packaged skill instructs consumers to label unrun behavioral comparisons explicitly.
