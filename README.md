# Agent Skill Kit

A collection of portable [Agent Skills](https://agentskills.io) for Codex, Claude Code, Cursor, Claude Desktop/Cowork, and ChatGPT Desktop/Work. This repository currently distributes desktop skills individually, not as a whole-collection plugin.

## Skills

| Skill | Description |
| --- | --- |
| [`craft-goal-driven-prompts`](skills/craft-goal-driven-prompts/) | Turn a goal into a structured agent prompt with measurable completion criteria and an optional evidence-driven improvement loop. |
| [`write-agent-briefs`](skills/write-agent-briefs/) | Create, improve, or audit an executable AI-agent brief with clear context, constraints, verification, and deliverables. |

## Install in desktop apps

### Claude Desktop / Cowork

1. Enable **Code execution and file creation** in **Settings > Capabilities**. Team and Enterprise owners must also enable Skills for the organization. See Anthropic's [skills setup guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
2. Download the individual skill ZIP from [GitHub Releases](https://github.com/rofyray/agent-skill-kit/releases) when a tagged release is available, or build it from a clone:

   ```bash
   git clone https://github.com/rofyray/agent-skill-kit.git
   cd agent-skill-kit
   python3 scripts/package_skills.py --skill craft-goal-driven-prompts
   ```

3. In Claude, open **Customize > Skills**, click **+**, choose **Create skill > Upload a skill**, and select `dist/skills/craft-goal-driven-prompts.zip`.
4. Toggle the skill on. Claude can select it automatically, or you can ask for it by name.

Tagged releases publish one ZIP per skill. Each archive contains exactly one correctly rooted skill folder for Claude's uploader.

### ChatGPT Desktop / Work

[Standalone skills](https://learn.chatgpt.com/docs/build-skills) are available in the ChatGPT desktop app. The documented cross-agent installation path is:

1. Install the individual skill for Claude Code or Cursor using the command in [Coding agents](#coding-agents).
2. In ChatGPT Desktop, open **Settings > Import**. If that section is not visible, use **Settings > General > Import other agent setup**. See OpenAI's [import guide](https://learn.chatgpt.com/docs/import).
3. Select Claude Code or Cursor, choose the skill under **Tools & setup**, and finish the import.
4. Open **Skills** in the sidebar. In ChatGPT or Work, type `@` and select the skill, or let ChatGPT choose it from your request.

Use **Work locally** when a task needs files or apps on your computer. Use **Cloud** for background work that only needs uploaded files and approved remote tools. See [Get started with ChatGPT Work](https://learn.chatgpt.com/docs/get-started-with-work).

## Coding agents

The community [`skills` CLI](https://github.com/vercel-labs/skills) installs skills into coding-agent discovery directories. It does not install skills into a Claude or ChatGPT account.

### Install one skill

```bash
npx skills add rofyray/agent-skill-kit --skill craft-goal-driven-prompts
```

Choose specific clients when needed:

```bash
npx skills add rofyray/agent-skill-kit --skill craft-goal-driven-prompts -a codex -a claude-code -a cursor
```

Add `-g` for a user-wide installation instead of the current project.

### Install the whole collection

```bash
npx skills add rofyray/agent-skill-kit --skill '*' -a codex -a claude-code -a cursor
```

Use `--all` to install every skill for every coding agent supported by the CLI without interactive selection.

### Manual installation

Clone the repository, then copy or symlink the desired folder from [`skills/`](skills/) into a discovery directory:

| Client | User-wide | Project-local |
| --- | --- | --- |
| Codex and Cursor | `~/.agents/skills/<skill-name>/` | `.agents/skills/<skill-name>/` |
| Claude Code | `~/.claude/skills/<skill-name>/` | `.claude/skills/<skill-name>/` |

The installed folder must retain `SKILL.md` and every referenced resource.

## Use a skill

| Client | Explicit use |
| --- | --- |
| ChatGPT Desktop / Work | Type `@`, select the skill, then describe the task. |
| Codex CLI / IDE | Type `$` and select the skill, or run `/skills`. |
| Claude Desktop / Cowork | Enable the skill and ask Claude to use it by name. |
| Claude Code / Cursor | Select or mention the skill by name using the client's skill UI. |

All five clients may also select a skill automatically when the request matches its description.

## Permissions and safety

A skill supplies a workflow; it does not grant shell access, file access, network access, connectors, or permission to control apps. Those capabilities depend on the host, environment, organization policy, and approvals active for the task.

Review third-party skill instructions, scripts, and bundled resources before enabling them.

See [tool compatibility](docs/tool-compatibility.md) for the shared authoring contract. See [CONTRIBUTING.md](CONTRIBUTING.md) to add or improve a skill.
