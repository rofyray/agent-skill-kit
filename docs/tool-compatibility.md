# Tool compatibility

## Shared baseline

All supported clients consume a directory with a `SKILL.md` entrypoint. The portable baseline is:

```yaml
---
name: prepare-release
description: Prepare and validate a safe software release. Use when the user asks to plan, check, or execute a release workflow.
---
```

Use standard Markdown and relative paths in the body. Treat client-specific fields as extensions, not part of the shared contract.

## Discovery locations

| Client | Project scope | User scope | Notes |
| --- | --- | --- | --- |
| Codex | `.agents/skills/<name>/` | `~/.agents/skills/<name>/` | Scans from the working directory to the repository root and follows skill-directory symlinks. |
| Claude Code | `.claude/skills/<name>/` | `~/.claude/skills/<name>/` | Supports project, personal, managed, and plugin scopes; follows symlinks for normal skill directories. |
| Cursor | `.agents/skills/<name>/` or `.cursor/skills/<name>/` | `~/.agents/skills/<name>/` or `~/.cursor/skills/<name>/` | Also recognizes Claude and Codex directories for compatibility. |

For a project that uses all three, one copy under `.agents/skills/` serves Codex and Cursor. Claude Code still needs the selected skill under `.claude/skills/`, typically as a symlink or copy.

## Client extensions

Codex can use optional `agents/openai.yaml` metadata for presentation and dependencies. Generate it from the finished skill so display text and the default prompt remain aligned with `SKILL.md`.

Claude Code supports extra frontmatter and runtime features such as invocation controls, arguments, subagent context, and dynamic command injection. Do not place those features in a portable skill. If needed, publish an explicit Claude-only variant or plugin that wraps the portable workflow.

Cursor supports additional frontmatter and can install skills from GitHub through its UI. Keep Cursor-specific hooks, path scoping, and invocation controls out of the portable core unless the skill is intentionally Cursor-only.

## Distribution policy

Use GitHub as the canonical distribution source. Until this repository adopts and tests a particular third-party installer, document native client installation and dependency-free copy or symlink workflows.

Do not claim that Anthropic officially documents `npx skills add`; its current first-party skill documentation describes project skills, plugins, and managed distribution instead. A community installer may be added later as an optional convenience after its behavior, security model, and monorepo selection semantics are verified.

Do not duplicate every skill into tool-specific directory trees inside this repository. Generate adapters only when a client requires behavior that cannot be represented by the portable core.

## Release compatibility checks

Before calling a skill cross-tool compatible:

1. Validate its portable structure.
2. Inspect scripts for shell and platform assumptions.
3. Run the same trigger and workflow cases in fresh Codex, Claude Code, and Cursor sessions.
4. Record meaningful behavior differences under `evals/<skill-name>/`.
5. Mark a skill client-specific if equivalent behavior depends on a proprietary extension.

