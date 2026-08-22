# Contributing

Every skill must work from one source folder across Codex, Claude Code, Cursor, Gemini CLI, Claude Web/Desktop/Cowork, ChatGPT Web, and ChatGPT Desktop/Work where standalone skills or the future plugin are available.

## Add a skill

1. Define concrete requests that should and should not trigger it.
2. Copy `templates/skill/` to `skills/<skill-name>/`.
3. Use a lowercase, outcome-focused, hyphenated name of at most 64 characters.
4. Keep only `name` and `description` in `SKILL.md` frontmatter. The description must be 200 characters or fewer and explain what the skill does and when to use it.
5. Write the core workflow in imperative, host-neutral language.
6. Add `agents/openai.yaml` with a 25–64 character `short_description` and an invocation-neutral `default_prompt` - do not hard-code `@`, `$`, or a client picker.
7. Add a portable help mode routed from `SKILL.md` to `references/help.md`. Explain the skill, list every named operational mode plus `help`, show how to begin, and provide at least two examples for each mode. Require the response to include the complete catalog rather than shorten it for brevity.
8. Add trigger and workflow cases under `evals/<skill-name>/`, including one case with `"mode": "help"`.
9. Update the README skill directory.

## Structure for efficient loading

- Keep routing, decision points, and the essential workflow in `SKILL.md`.
- Put detailed policies, schemas, variants, and longer examples in focused files under `references/`.
- Put deterministic or fragile repeated operations in tested files under `scripts/`.
- Put templates, images, boilerplate, and other output inputs under `assets/`.
- Put ChatGPT/Codex presentation or dependency metadata in `agents/openai.yaml`.
- Put evaluation prompts, fixtures, and grading criteria under `evals/<skill-name>/`.
- Keep the required help explanation, mode catalog, start guidance, and examples in `references/help.md` so normal workflows do not pay its context cost.

Do not add per-skill READMEs, changelogs, installation guides, or quick-reference files. Repository-level documentation owns those concerns.

## Credit sources and preserve licenses

- Distinguish learning from a public source from copying its protected expression. Public availability alone is not permission to copy.
- Add `assets/CREDITS.txt` when a skill is recognizably inspired by a named article, post, talk, podcast, methodology, or author. Identify the author, title or description, and canonical URL; describe the conceptual influence without implying endorsement.
- Add `assets/THIRD_PARTY_NOTICES.txt`, or a clearly named `assets/UPSTREAM_LICENSE.txt` for a single upstream work, when the package copies or adapts licensed code, templates, instructions, examples, or assets. Preserve every copyright and license notice required by the source license.
- Verify reuse rights before including third-party code or assets. Attribution does not replace permission or compliance with a source license.
- Do not add a credits file merely for general knowledge or independently developed ideas. Keep notices factual, concise, and outside agent instructions so they ship in the ZIP without consuming runtime context.

## Portability rules

- Do not use em dashes. Use commas, colons, parentheses, or ASCII hyphens instead.
- Do not put whitespace immediately before or after `/`. Write `Codex/IDE` and `and/or`.
- Keep `SKILL.md` under 500 lines and preferably below 5,000 tokens.
- Link supporting files directly from `SKILL.md`, state when to read them, and avoid reference-to-reference routing.
- Use relative paths from the skill root.
- Do not rely on client-specific frontmatter, invocation syntax, variables, or command interpolation in the portable core.
- Treat `help` as a natural-language mode after the skill is selected or named; do not implement it as a slash command or confuse it with ordinary “help me…” requests.
- Do not assume shell, package-manager, network, local-file, browser, connector, or desktop-control access.
- When optional scripts require capabilities or dependencies, check them, explain the requirement, and fail gracefully.
- Treat scripts as untrusted code during review; avoid secrets in arguments or output.
- Keep the skill self-contained so a future plugin can reference `skills/<name>/` without relocating content. Do not add a plugin manifest until the collection is intentionally packaged as a plugin.

The planned distribution model is one skills-only plugin containing every canonical skill in this repository. Plugin packaging and publication are deferred until that work is intentionally started.

## Validate and package

Run:

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
python3 scripts/package_skills.py
```

Inspect each generated archive in `dist/skills/`. It must contain one top-level folder whose name matches the skill and must exclude development files, evals, caches, and repository documentation.

For each non-trivial skill, test:

- requests that should and should not trigger it;
- the primary successful workflow;
- missing input, dependency, capability, and permission paths;
- fresh sessions with and without the skill; and
- Codex, Claude Code, Cursor, Claude Web/Desktop/Cowork, ChatGPT Web, and ChatGPT Desktop/Work where those clients are available.

Evaluate routing and output quality separately. Record meaningful client differences in the skill's eval cases or fixtures.

## Release versioning

Create releases from a clean, validated `main` branch using annotated tags in `vMAJOR.MINOR.PATCH` format. Follow semantic versioning for this catalog:

- `v0.1.1`: fixes to skills, documentation, or packaging;
- `v0.2.0`: new skills or meaningful capabilities; and
- `v1.0.0`: the collection and compatibility contract are considered stable.

Before pushing a release tag, run the validation, tests, and packaging commands above. Pushing a `v*` tag triggers the release workflow, which publishes one ZIP per skill plus checksums.

## Review checklist

- Name, directory, frontmatter, eval directory, and OpenAI metadata agree.
- Description is concise enough for every client and has a clear trigger boundary.
- Core instructions are complete without unnecessary background.
- Supporting resources are focused, directly linked, and loaded only when needed.
- Scripts are deterministic where practical and degrade safely when execution is unavailable.
- Source credits and third-party license notices are accurate, complete, and included in the installable package when applicable.
- Help mode routes to `references/help.md`, covers every named mode with examples, and has a matching help eval case.
- Text contains no em dashes and no whitespace immediately adjacent to a forward slash.
- No client-specific behavior leaks into the portable core.
- Validation, tests, packaging, and relevant forward evaluations pass.
