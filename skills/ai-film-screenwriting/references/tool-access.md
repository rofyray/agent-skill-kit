# Tool Access, Connectors, and MCP

Use this reference only when the user asks to connect a service, invoke an external model, import or export material, persist project files, or troubleshoot a missing capability.

## Separate the skill from the tool

This skill supplies the screenwriting workflow. It does not itself grant file, research, cloud-storage, application, or external-model access. The host must expose an authenticated tool before the agent can invoke that capability.

Core screenplay writing remains available without a connector. A connector becomes useful for:

- Reading treatments, research, notes, and earlier drafts from an authorized source.
- Maintaining canonical screenplay files in a project or storage service.
- Researching current or specialized facts.
- Exporting to a document or production application.
- Invoking a user-selected external text model or screenplay service.

## Inspect before configuring

1. Identify the current surface: ChatGPT Chat or Work, Codex desktop, Codex CLI, Claude, Claude Desktop or Cowork, or Claude Code.
2. Inspect the tools already exposed in the conversation.
3. Match the requested operation to tool capabilities, not to a provider name alone.
4. Confirm authentication, accepted input types, output destination, write behavior, and approval requirements.
5. Ask the user to choose only when multiple available tools differ materially in quality, privacy, cost, or output format.

Do not assume a connector exists because the user named it. Do not install, configure, or authenticate an unrelated service.

## ChatGPT and Codex

In ChatGPT Chat or Work on supported web and desktop surfaces, remote tools are supplied through installed plugins and their connectors or MCP servers. Open the Plugins area, install or enable a trusted plugin that exposes the required service, complete authentication, then begin a new chat when the host requires it.

ChatGPT web does not read a local Codex MCP configuration. Do not tell a web-only user that a local CLI configuration will make the tool appear in ChatGPT web.

Codex desktop, CLI, and IDE can connect directly to MCP servers on the same Codex host. Use the MCP settings UI when available. For a remote Streamable HTTP server in the CLI, the current command pattern is:

```text
codex mcp add <server-name> --url <https://server.example/mcp>
codex mcp login <server-name>
codex mcp list
```

Use `codex mcp --help` when the server needs additional authentication or configuration options. In the Codex interface, `/mcp` displays active servers.

Official references:

- https://learn.chatgpt.com/docs/plugins
- https://learn.chatgpt.com/docs/extend/mcp?surface=cli

## Claude and Claude Code

For Claude web, desktop, Cowork, and mobile, use a remote connector when the service has a public remote MCP endpoint. In an individual account, open Customize, choose Connectors, add a custom connector, provide the trusted remote MCP URL, authenticate, and enable it for the conversation. Team and Enterprise workspaces may require an owner to add the connector first.

Remote Claude connectors are reached from Anthropic's cloud infrastructure. A server limited to localhost, a private network, or an unexposed VPN endpoint will not work as a web connector.

For Claude Code, a remote HTTP server can be added with:

```text
claude mcp add --transport http <server-name> <https://server.example/mcp>
claude mcp list
claude mcp get <server-name>
```

Use `/mcp` inside Claude Code to inspect status and complete supported authentication. Add project or user scope only when the user wants that persistence and understands who will inherit access.

Official references:

- https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp
- https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors
- https://code.claude.com/docs/en/mcp

## Verify the connection

After setup:

1. Confirm the tool appears in the active conversation or MCP status list.
2. Confirm authentication succeeded.
3. Inspect the tool schema and determine whether it can read, create, update, export, or only return links.
4. Prefer a harmless read, list, or draft operation before a consequential write when the service supports one.
5. Preview the target, destination, and content before overwriting or publishing anything.

An installed connector is not proof that a particular model, export format, or write action is available. Use only capabilities exposed by the actual tool.

## Protect scripts and credentials

- Connect only to servers and plugins the user trusts.
- Grant the smallest useful permission scope.
- Never place API keys, bearer tokens, OAuth secrets, or private URLs inside prompts, screenplay files, notes, or logs.
- Do not upload confidential drafts or source material to an external model without authorization.
- Distinguish saving a private draft from publishing or sharing it externally. Obtain approval for the latter.

## Manual fallback

If the required tool cannot be connected, continue with safe work that does not need it. Return a manual handoff containing:

- The exact requested operation.
- The relevant story context and canonical version.
- The complete text, prompt, or export-ready content.
- Required source attachments and their roles.
- Output format and destination instructions.
- A verification checklist.

State that the external operation was not executed. Do not present a copy-and-paste package as a generated, saved, imported, or exported artifact.
