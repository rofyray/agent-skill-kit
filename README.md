# Agent Skill Kit

Portable [Agent Skills](https://agentskills.io) for Codex, Claude Code, Cursor, Gemini CLI, Claude Web/Desktop/Cowork, and ChatGPT.

## Skills

| Skill | Description |
| --- | --- |
| [`build-and-maintain-a-second-brain`](skills/build-and-maintain-a-second-brain/) | Build and maintain a source-grounded, Obsidian-compatible wiki with ingestion, querying, health checks, and reviews. |
| [`create-and-edit-images`](skills/create-and-edit-images/) | Create photorealistic images or make precise edits while preserving unrequested details. |
| [`craft-goal-driven-prompts`](skills/craft-goal-driven-prompts/) | Turn a goal into a structured prompt with completion criteria and an optional improvement loop. |
| [`interview-coach`](skills/interview-coach/) | Coach role research, applications, interview prep, practice, debriefs, progress, and negotiation. |
| [`understand-before-coding`](skills/understand-before-coding/) | Understand, plan, implement, review, and document code changes using repository evidence. |
| [`write-agent-briefs`](skills/write-agent-briefs/) | Create, improve, or audit executable agent briefs with clear constraints, verification, and deliverables. |

## Install

### Claude Web/Desktop/Cowork

1. Enable **Code execution and file creation** in **Settings > Capabilities**. Team and Enterprise owners must also enable Skills. See Anthropic's [setup guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
2. Download an individual skill ZIP from [GitHub Releases](https://github.com/rofyray/agent-skill-kit/releases).
3. Open **Customize > Skills**, click **+**, choose **Create skill > Upload a skill**, and select the ZIP. Ensure the skill is enabled.

### ChatGPT Web

1. Download an individual skill ZIP from [GitHub Releases](https://github.com/rofyray/agent-skill-kit/releases).
2. Open **Plugins > Skills**, click **+**, and choose **Upload from your computer**.
3. Select the ZIP, then type `@` to choose the skill or let ChatGPT select it automatically.

Web upload is verified. Web-to-desktop skill sync is not, so use ChatGPT Web if the skill does not appear in the desktop app.

### Coding agents

The community [`skills` CLI](https://github.com/vercel-labs/skills) installs skills into coding-agent discovery directories.

#### One skill

```bash
npx skills add rofyray/agent-skill-kit --skill craft-goal-driven-prompts
```

Target specific clients when needed:

```bash
npx skills add rofyray/agent-skill-kit --skill craft-goal-driven-prompts -a codex -a claude-code -a cursor -a gemini-cli
```

#### Whole collection

```bash
npx skills add rofyray/agent-skill-kit --skill '*' -a codex -a claude-code -a cursor -a gemini-cli
```

Add `-g` for user-wide installation. Use `--all` to install every skill for every supported coding agent.

[Gemini CLI Agent Skills](https://geminicli.com/docs/cli/using-agent-skills/) require version 0.26.0 or later. Update with `npm install -g @google/gemini-cli@latest`, trust the workspace, then run `/skills reload` and `/skills list`.

#### Manual installation

Copy or symlink a complete folder from [`skills/`](skills/) into a discovery directory:

| Client | User-wide | Project-local |
| --- | --- | --- |
| Codex and Cursor | `~/.agents/skills/<skill-name>/` | `.agents/skills/<skill-name>/` |
| Claude Code | `~/.claude/skills/<skill-name>/` | `.claude/skills/<skill-name>/` |
| Gemini CLI | `~/.gemini/skills/<skill-name>/` or `~/.agents/skills/<skill-name>/` | `.gemini/skills/<skill-name>/` or `.agents/skills/<skill-name>/` |

Keep `SKILL.md` and every referenced resource together.

### ChatGPT Desktop/Work

No whole-collection plugin is available yet. Use individual skill uploads in [ChatGPT Web](#chatgpt-web).

### Gemini Web

Standalone Agent Skill installation is not currently documented.

## Use a skill

| Client | How to use it |
| --- | --- |
| ChatGPT Web | Type `@`, select the skill, and describe the task. |
| Codex CLI/IDE | Type `$` and select the skill, or run `/skills`. |
| Gemini CLI | Ask by name or allow automatic activation, then approve it. |
| Claude Web/Desktop/Cowork | Enable the skill and ask for it by name. |
| Claude Code/Cursor | Select or mention the skill by name. |

### Get started with `help`

After selecting or naming a skill, send `help` to see its purpose, modes, and examples. For example: `Use interview-coach and show help.`

## Permissions and safety

Skills provide instructions, not permissions. File, shell, network, browser, connector, and app access depend on the host and user approval. Review third-party skills before enabling them.

Maintainers: [tool compatibility](docs/tool-compatibility.md) and [contributing](CONTRIBUTING.md).
