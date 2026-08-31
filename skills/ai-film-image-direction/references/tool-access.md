# Image Tool Access, Connectors, and MCP

Use this reference when the user asks to connect an image service, invoke a native or external model, choose among tools, persist assets, or troubleshoot a missing generation or editing capability.

## Separate the skill from generation access

This skill supplies visual-development and continuity logic. It can invoke an image model only when the active host exposes an authenticated image-generation or image-editing tool.

The user may still use the skill without a generation tool for art direction, asset planning, prompt-only packages, reference maps, audits of supplied images, and manual handoffs.

## Inspect the active capabilities

Before selecting a tool, determine:

- Current surface and project context.
- Available native image tools, plugins, connectors, MCP servers, and file or project storage.
- Generate, edit, mask, composite, outpaint, variation, and visual-inspection support.
- Accepted reference types, role or weight controls, reference-count limits, and maximum input sizes.
- Model and version exposed by the tool.
- Aspect ratio, resolution, seed, transparency, negative prompt, text rendering, and output-count fields.
- Synchronous or asynchronous execution and how completed artifacts are returned.
- Authentication, cost, privacy, write behavior, and approval requirements.

Use the user's chosen provider when available. If none is chosen, prefer an already available tool that satisfies the request. Ask for a choice only when options differ materially in continuity, editing fidelity, reference support, style control, privacy, cost, or output format.

Do not claim a capability based on a provider's marketing or a remembered model version. Inspect the actual tool schema and current provider instructions.

## ChatGPT and Codex

On supported ChatGPT web and desktop Chat or Work surfaces, image tools may be native or supplied through installed plugins and their connectors or remote MCP servers. Use the native tool when it satisfies the request and the user has not selected another provider. Otherwise open the Plugins area, install or enable a trusted compatible plugin, authenticate, and start a new conversation when the host requires it.

ChatGPT web does not read local Codex MCP configuration. A connector configured only in the CLI will not automatically appear in a ChatGPT web conversation.

Codex desktop, CLI, and IDE can connect directly to MCP servers on the same Codex host. Use the MCP settings UI when available. For a remote Streamable HTTP server in the CLI, the current command pattern is:

```text
codex mcp add <server-name> --url <https://server.example/mcp>
codex mcp login <server-name>
codex mcp list
```

Use `codex mcp --help` for additional server options and `/mcp` to inspect active servers in the Codex interface.

Official references:

- https://learn.chatgpt.com/docs/plugins
- https://learn.chatgpt.com/docs/extend/mcp?surface=cli

## Claude and Claude Code

For Claude web, desktop, Cowork, and mobile, a cloud image service can be exposed through a remote connector when it provides a public remote MCP endpoint. In an individual account, open Customize, choose Connectors, add the trusted custom connector URL, authenticate, and enable it for the conversation. Team and Enterprise workspaces may require an owner to add the connector first.

Remote Claude connectors are reached from Anthropic's cloud infrastructure. A server available only on localhost, a private network, or an unexposed VPN endpoint will not work as a web connector.

For Claude Code, add a remote HTTP server with:

```text
claude mcp add --transport http <server-name> <https://server.example/mcp>
claude mcp list
claude mcp get <server-name>
```

Use `/mcp` inside Claude Code to inspect status and complete supported authentication. Add project or user scope only when that persistence is intended.

Official references:

- https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp
- https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors
- https://code.claude.com/docs/en/mcp

## Verify before production

After connection:

1. Confirm the tool appears in the active conversation or MCP status view.
2. Confirm authentication and any required project selection.
3. Inspect the tool schema and model or version actually offered.
4. Run a low-risk test asset before a large or paid batch when uncertainty remains.
5. Confirm the artifact, metadata, output location, and visual-inspection path.

An installed connector is not proof that editing, multiple references, masks, transparency, exact text, or a particular model is available.

## Invoke and track a generation

- Send only the source images needed for the declared roles.
- Keep API keys, bearer tokens, OAuth secrets, and private URLs out of prompts and manifests.
- Do not send confidential story material, private likenesses, or unreleased assets to an external service without authorization.
- Record provider, model, version, settings, prompt, references, and returned job or asset identifier when production tracking requires it.
- For asynchronous tools, wait or poll through the supported mechanism. A job identifier is not a completed image.
- Preview the target before overwriting, publishing, or sharing a project asset.

## Manual fallback

If a compatible tool cannot be connected, return:

- Asset specification and intended use.
- Final prompt and provider adapter notes.
- Reference-role map and attachment checklist.
- Settings and capability assumptions.
- Output naming and destination guidance.
- Verification checklist.

State that no image was generated. Do not represent setup instructions, a queued job, or a copy-and-paste package as a completed asset.
