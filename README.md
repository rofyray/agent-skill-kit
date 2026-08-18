# Agent Skill Kit

A collection of portable [Agent Skills](https://agentskills.io) for Codex, Claude Code, Cursor, Claude Desktop/Cowork, and ChatGPT. Current distribution supports coding-agent installs and individual skill ZIP uploads in Claude and ChatGPT Web. A whole-collection ChatGPT plugin is planned.

## Skills

| Skill | Description |
| --- | --- |
| [`create-and-edit-images`](skills/create-and-edit-images/) | Create photorealistic images or make precise, physically believable edits while preserving every unrequested detail. |
| [`craft-goal-driven-prompts`](skills/craft-goal-driven-prompts/) | Turn a goal into a structured agent prompt with measurable completion criteria and an optional evidence-driven improvement loop. |
| [`write-agent-briefs`](skills/write-agent-briefs/) | Create, improve, or audit an executable AI-agent brief with clear context, constraints, verification, and deliverables. |

## Install

### Coding agents

The community [`skills` CLI](https://github.com/vercel-labs/skills) installs skills into coding-agent discovery directories. It does not install skills into a Claude or ChatGPT account.

#### Install one skill

```bash
npx skills add rofyray/agent-skill-kit --skill craft-goal-driven-prompts
```

Choose specific clients when needed:

```bash
npx skills add rofyray/agent-skill-kit --skill craft-goal-driven-prompts -a codex -a claude-code -a cursor
```

Add `-g` for a user-wide installation instead of the current project.

#### Install the whole collection

```bash
npx skills add rofyray/agent-skill-kit --skill '*' -a codex -a claude-code -a cursor
```

Use `--all` to install every skill for every coding agent supported by the CLI without interactive selection.

#### Manual installation

Clone the repository, then copy or symlink the desired folder from [`skills/`](skills/) into a discovery directory:

| Client | User-wide | Project-local |
| --- | --- | --- |
| Codex and Cursor | `~/.agents/skills/<skill-name>/` | `.agents/skills/<skill-name>/` |
| Claude Code | `~/.claude/skills/<skill-name>/` | `.claude/skills/<skill-name>/` |

The installed folder must retain `SKILL.md` and every referenced resource.

### Claude Desktop / Cowork

1. Enable **Code execution and file creation** in **Settings > Capabilities**. Team and Enterprise owners must also enable Skills for the organization. See Anthropic's [skills setup guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
2. Download the ZIP for the individual skill from [GitHub Releases](https://github.com/rofyray/agent-skill-kit/releases).
3. In Claude, open **Customize > Skills**, click **+**, choose **Create skill > Upload a skill**, and select the downloaded ZIP.
4. Toggle the skill on if it is not already enabled. Claude can select it automatically, or you can ask for it by name.

Tagged releases publish one ZIP per skill. Each archive contains exactly one correctly rooted skill folder for Claude's uploader.

### ChatGPT Web

1. Download the ZIP for the individual skill from [GitHub Releases](https://github.com/rofyray/agent-skill-kit/releases).
2. Open ChatGPT in a web browser and select **Plugins** in the sidebar.
3. Open the **Skills** tab, click **+**, and choose **Upload from your computer**.
4. Select or drag in the individual skill ZIP.
5. In ChatGPT or Work, type `@` and select the skill, or let ChatGPT choose it from your request.

This is the currently verified manual-upload path. OpenAI's [skills documentation](https://learn.chatgpt.com/docs/build-skills) also describes standalone skills in the desktop app, but it does not currently document whether skills uploaded on the web sync to desktop. If the uploaded skill does not appear there, use it in the web app.

### ChatGPT Desktop / Work

Agent Skill Kit is not yet publicly available as a plugin, so there is no supported whole-collection installation for ChatGPT Desktop/Work. Importing a Claude Code or Cursor setup is not an account-level skill installer and is no longer recommended here. A single plugin containing the full collection is planned; until it is published, use the individual [ChatGPT Web](#chatgpt-web) upload flow above.

## Use a skill

| Client | Explicit use |
| --- | --- |
| ChatGPT Web | Type `@`, select the skill, then describe the task. |
| Codex CLI / IDE | Type `$` and select the skill, or run `/skills`. |
| Claude Desktop / Cowork | Enable the skill and ask Claude to use it by name. |
| Claude Code / Cursor | Select or mention the skill by name using the client's skill UI. |

Supported hosts may also select a skill automatically when the request matches its description.

## Permissions and safety

A skill supplies a workflow; it does not grant shell access, file access, network access, connectors, or permission to control apps. Those capabilities depend on the host, environment, organization policy, and approvals active for the task.

Review third-party skill instructions, scripts, and bundled resources before enabling them.

See [tool compatibility](docs/tool-compatibility.md) for the shared authoring contract. See [CONTRIBUTING.md](CONTRIBUTING.md) to add or improve a skill.
