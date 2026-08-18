# Scheduled wiki lint

Operate on the vault containing this prompt. Read `SECOND_BRAIN.md` first and follow its LINT procedure.

1. Verify recorded raw-source integrity.
2. Run available deterministic checks for metadata, broken links, index drift, orphans, and duplicate page identities.
3. Inspect semantic contradictions, stale claims, weak provenance, missing concepts, misleading summaries, and unsupported conclusions.
4. Create a maintenance-run identifier and write a collision-safe timestamped report under `reports/lint/` with exact evidence and proposed fixes ordered by impact and risk. Never overwrite an existing report.
5. Append a lint event to `log.md` with the maintenance-run identifier, report path, and `status: success` only after the report is complete.

Ignore fenced examples, inline code, template instructions, and format demonstrations when identifying placeholders or claims. An empty wiki is valid, and a sole first page is not an orphan merely because no second page exists. Do not delete pages, rewrite disputed claims, fetch new sources, or apply semantic fixes. Report any capability or extraction limitation.
