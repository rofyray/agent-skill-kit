# Video Tool Access, Connectors, and MCP

Use this reference when the user asks to connect a video service, invoke a native or external model, choose among tools, persist clips, or troubleshoot a missing generation, editing, audio, or inspection capability.

## Separate the skill from generation access

This skill supplies scene planning, video direction, prompting, continuity, and verification logic. It can invoke a video model only when the active host exposes an authenticated compatible tool.

The user may still use the skill without a generator for shot planning, prompt-only packages, audits of supplied media, provider adapters, continuity repair, and manual handoffs.

## Inspect the active capabilities

Before selecting a tool, determine:

- Current host, surface, project, and storage context.
- Available native tools, plugins, connectors, remote MCP servers, and media inspection.
- Text-to-video, image-to-video, reference-to-video, video-to-video, extend, edit, replace, inpaint, upscale, interpolation, lip-sync, and audio support.
- First-frame, end-frame, storyboard, character, object, location, style, motion, and voice reference support.
- Reference-count limits, role or weight controls, and accepted file types and sizes.
- Model and version exposed by the actual tool.
- Duration, aspect ratio, resolution, frame rate, output count, seed, negative prompt, camera, multi-shot, dialogue, music, and sound fields.
- Synchronous or asynchronous execution, status checks, expiry, output delivery, and cancellation.
- Authentication, cost, privacy, moderation, persistence, and approval requirements.

Use the user's chosen provider when available. If none is chosen, prefer an already available tool that satisfies the request. Ask for a choice only when options differ materially in reference fidelity, motion quality, editing, audio, privacy, cost, duration, output, or another project-critical capability.

Do not rely on a hardcoded provider ranking or remembered model version. Inspect the actual tool schema and current provider instructions.

## ChatGPT and Codex

On supported ChatGPT web and desktop Chat or Work surfaces, video tools may be supplied through installed plugins and their connectors or remote MCP servers. Open the Plugins area, install or enable a trusted compatible plugin, authenticate, and start a new conversation when the host requires it.

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

For Claude web, desktop, Cowork, and mobile, a cloud video service can be exposed through a remote connector when it provides a public remote MCP endpoint. In an individual account, open Customize, choose Connectors, add the trusted custom connector URL, authenticate, and enable it for the conversation. Team and Enterprise workspaces may require an owner to add the connector first.

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
2. Confirm authentication, project selection, permissions, and write destination.
3. Inspect the exact tool schema, model, version, limits, cost behavior, and output lifecycle.
4. Run a low-risk test clip before a large or paid batch when uncertainty remains.
5. Confirm the completed media, metadata, output location, playback, and inspection path.

An installed connector is not proof that multiple references, start and end frames, cuts, camera controls, audio, lip sync, extension, editing, or a named model is available.

## Invoke and track production

- Send only the source media required for declared roles.
- Keep API keys, bearer tokens, OAuth secrets, signed URLs, and private endpoints out of prompts and manifests.
- Do not send confidential scripts, private likenesses or voices, unreleased footage, or restricted assets to an external service without authorization.
- Record provider, model, version, settings, prompt, references, job ID, asset ID, and output location when production tracking requires it.
- For asynchronous tools, wait or poll through the supported mechanism. A job identifier is not a completed video.
- Preview the target before overwriting, publishing, sharing, or replacing a project asset.

## Manual fallback

If a compatible tool cannot be connected, return:

- Scene and shot specification.
- Final provider-neutral prompt and adapter notes.
- Reference-role map and attachment checklist.
- Settings and capability assumptions.
- Output naming, destination, and edit guidance.
- Audio or lip-sync handoff when separate.
- Verification and continuity checklist.

State that no video was generated. Do not represent connection instructions, a queued job, a remote identifier, or a copy-and-paste package as a completed clip.
