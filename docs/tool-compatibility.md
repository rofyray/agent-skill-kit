# Tool compatibility

Every skill in this repository targets Codex, Claude Code, Cursor, Claude Web/Desktop/Cowork, and ChatGPT from one canonical folder under `skills/`.

## Shared contract

Each skill must:

- contain a portable `SKILL.md` with only `name` and `description` in its YAML frontmatter;
- use a lowercase hyphenated name of at most 64 characters;
- keep its description at 200 characters or fewer, state both capability and trigger boundary, and front-load the main use case;
- use host-neutral instructions, relative paths, and progressive disclosure;
- include `agents/openai.yaml` with concise UI metadata and an invocation-neutral default prompt;
- avoid assuming shell, network, local-file, browser, connector, or app-control access;
- fail gracefully or state requirements when an optional script needs unavailable capabilities; and
- include matching evaluation cases under `evals/<skill-name>/`.

## Availability and installation

| Surface | Standalone skill availability | Installation or discovery |
| --- | --- | --- |
| Codex CLI / IDE | Yes | `.agents/skills/<name>/` at project or user scope |
| Claude Code | Yes | `.claude/skills/<name>/` at project or user scope |
| Cursor | Yes | `.agents/skills/<name>/` or `.cursor/skills/<name>/` |
| Claude Web / Desktop / Cowork | Yes | Upload a single rooted ZIP through **Customize > Skills**; code execution and file creation must be enabled |
| ChatGPT Web | Yes where the Skills upload UI is available | Upload an individual ZIP through **Plugins > Skills > + > Upload from your computer** |
| ChatGPT Desktop / Work | OpenAI documents standalone desktop skills, but web-upload synchronization is not currently documented or verified here | No public Agent Skill Kit plugin yet; use ChatGPT Web for the currently verified individual upload flow |

The community `npx skills` installer targets coding-agent discovery directories. It is not an account-level installer for Claude Web/Desktop/Cowork or ChatGPT.

## Invocation

- ChatGPT uses `@` for explicit skill selection when the skill is available on that surface.
- Codex uses `$` or `/skills`.
- Claude can select an enabled skill automatically; users can also ask for it by name.
- Cursor and Claude Code can select skills through their client UI or by name.

Descriptions remain the common implicit-routing mechanism, so they must work without client-specific syntax.

## Execution boundaries

Skills provide instructions and resources, not permissions. Hosts decide whether a task can use files, a shell, the network, connectors, browser control, or desktop apps. A portable workflow must inspect available capabilities, request approval when required, and offer a non-executing fallback when practical.

For ChatGPT Work, local execution in the desktop app is appropriate when the task needs files or apps on the user's computer. ChatGPT Work on the web can use uploaded/account files, plugins, connected tools, and cloud browser work, but web tasks do not retain an arbitrary local folder.

Claude Cowork is available on web, desktop, and mobile. A Cowork session on web or mobile can reach approved local folders and apps only through an open Claude Desktop bridge; without that bridge it uses account files, skills, plugins, and remote connectors. Claude skills require code execution and file creation to be enabled even when the skill itself contains no scripts.

## Distribution and plugin readiness

GitHub is the canonical source. Tagged releases produce one deterministic ZIP per skill for Claude and ChatGPT Web upload flows; coding agents can install from the repository or copy a skill folder directly.

The shallow `skills/<name>/` layout, portable frontmatter, OpenAI metadata, self-contained resources, and deterministic archives keep the catalog ready for a future whole-collection plugin without moving or duplicating skill content. No plugin package or whole-collection ChatGPT installer is included yet.

Do not duplicate the catalog into client-specific trees. Add a client adapter only when a capability cannot be expressed in the portable core, and clearly label any client-specific behavior.

## Release checks

Before calling a skill cross-client compatible:

1. Run the repository validator and unit tests.
2. Build its ZIP and inspect the archive root and contents.
3. Inspect scripts for operating-system, shell, package, network, and permission assumptions.
4. Test trigger, non-trigger, primary workflow, and degraded-capability cases in fresh sessions.
5. Exercise the skill on every available target surface and record meaningful differences in its evals.
