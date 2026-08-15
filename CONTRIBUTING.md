# Contributing

## Add a skill

1. Start with concrete requests that should and should not trigger the skill.
2. Choose a short, outcome-focused, hyphenated name under 64 characters.
3. Copy `templates/skill/` to `skills/<skill-name>/` or use the active client's official skill creator.
4. Keep only `name` and `description` in portable `SKILL.md` frontmatter.
5. Write the essential workflow in imperative form.
6. Add reusable resources only when they improve reliability or reduce repeated context.
7. Validate the catalog and test the skill in fresh sessions.

## Split content by how it is consumed

- Put routing, decision points, and the core workflow in `SKILL.md`.
- Put detailed policies, schemas, variants, and longer examples in focused files under `references/`.
- Put deterministic or fragile repeated operations in tested files under `scripts/`.
- Put templates, images, boilerplate, and other output inputs under `assets/`.
- Put Codex presentation or dependency metadata in `agents/openai.yaml` when useful.
- Put evaluation prompts, fixtures, and grading criteria under `evals/<skill-name>/`.

Do not create a per-skill README, changelog, installation guide, or quick-reference file. Repository-level documentation owns those concerns.

## Progressive disclosure rules

- Keep `SKILL.md` under 500 lines and preferably below 5,000 tokens.
- Reference supporting files directly from `SKILL.md`; avoid reference-to-reference routing.
- State the condition for reading each reference.
- Add a table of contents to reference files longer than 100 lines.
- Avoid repeating the same guidance in `SKILL.md` and a reference file.
- Prefer several focused references over one large catch-all document.

## Portability rules

- Use relative paths from the skill root.
- Do not rely on Claude-only frontmatter, dynamic `!` command injection, or client-specific variables in a portable skill.
- Do not assume a specific shell, package manager, network connection, or installed CLI without checking it or documenting the requirement in the instructions.
- Put client-specific enhancements in client-owned metadata or an explicitly client-specific skill.
- Treat scripts as untrusted code during review; inspect them before execution and avoid secrets in arguments or output.

## Validation and evaluation

Run:

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests
```

For each non-trivial skill, test at least:

- requests that should trigger it;
- nearby requests that should not trigger it;
- the main successful workflow;
- missing dependency, missing input, and permission failure paths;
- behavior in fresh sessions with and without the skill.

Evaluate invocation and output quality separately. A skill can trigger correctly and still produce a poor result.

## Review checklist

- The name is narrow, clear, and matches its directory.
- The description explains both capability and triggering boundary.
- The core workflow is complete without unnecessary background.
- Optional resources have an explicit consumer and are linked from `SKILL.md`.
- Scripts are deterministic where practical and have been executed on representative inputs.
- No client-specific behavior leaks into the portable core unintentionally.
- Validation and relevant evaluations pass.

