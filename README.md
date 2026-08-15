# Skill Kit

A collection of portable [Agent Skills](https://agentskills.io) for Codex, Claude Code, Cursor, and compatible agents. Skills can be installed individually or as a collection.

## Available skills

| Skill | Description |
| --- | --- |
| [`craft-goal-driven-prompts`](skills/craft-goal-driven-prompts/) | Turn an objective into a detailed, structured agent prompt with explicit constraints, measurable completion criteria, verification evidence, and an optional loop-until-done protocol. |
| [`write-agent-briefs`](skills/write-agent-briefs/) | Create, improve, or audit complete AI-agent task briefs using context, verifiable constraints, and an exact deliverable composition. |

## Installation

The community [`skills` CLI](https://github.com/vercel-labs/skills) installs into the current project by default. In the examples below, replace `OWNER/REPO` with this repository's GitHub slug.

### Install one skill

```bash
npx skills add OWNER/REPO --skill craft-goal-driven-prompts
```

Choose specific clients when needed:

```bash
npx skills add OWNER/REPO --skill craft-goal-driven-prompts -a codex -a claude-code -a cursor
```

Add `-g` to install a skill for the current user instead of the current project.

### Install the whole collection

```bash
npx skills add OWNER/REPO --skill '*' -a codex -a claude-code -a cursor
```

Use `--all` to install every skill for every agent supported by the CLI without interactive selection.

### Manual installation

Clone the repository, then copy or symlink the desired directory from [`skills/`](skills/) into your agent's skill directory:

| Client | User-wide | Project-local |
| --- | --- | --- |
| Codex and Cursor | `~/.agents/skills/<skill-name>/` | `.agents/skills/<skill-name>/` |
| Claude Code | `~/.claude/skills/<skill-name>/` | `.claude/skills/<skill-name>/` |

The installed directory must contain `SKILL.md` and its referenced resources.

## Using a skill

Ask your agent to use the installed skill by name, for example:

```text
Use $write-agent-briefs to turn this request into a complete, verifiable agent brief.
```

Activation syntax varies by client; compatible agents may also select a skill automatically from its description.

## Compatibility and safety

Each skill is self-contained under [`skills/`](skills/) and uses the portable `SKILL.md` format. See the [compatibility guide](docs/tool-compatibility.md) for client-specific discovery paths and behavior.

Review a skill's instructions and bundled scripts before installation or execution, especially when using third-party skills.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) to propose a skill or improve an existing one.
