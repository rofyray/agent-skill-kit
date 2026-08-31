# Performance Tool Access, Connectors, and MCP

Use this reference when the user asks to connect a service, invoke a voice or performance model, choose among tools, persist outputs, or troubleshoot a missing generation capability.

## Separate the skill from generation access

This skill can always produce written performance direction and prompt packages. It can generate audio, animation, avatar, lip-sync, or video performance only when the active host exposes an authenticated compatible tool.

Do not assume a general video or audio connector supports voice identity, multiple speakers, performance control, or inspection. Use only capabilities exposed by the actual tool.

## Inspect the active capabilities

Before selecting a tool, determine:

- Current surface and project context.
- Available text-to-speech, speech-to-speech, voice-reference, avatar, animation, performance-transfer, lip-sync, audio, video, and media-inspection tools.
- Model and version actually exposed.
- Accepted text, audio, image, video, motion, identity, and pronunciation references.
- Voice cloning or identity controls and their authorization requirements.
- Language, accent, speaker-count, dialogue-length, timing, duration, emotion or style, and synchronization controls.
- Output format, sample rate, resolution, metadata, and synchronous or asynchronous behavior.
- Authentication, privacy, cost, destination, write behavior, and approval requirements.

Use the user's selected provider when available. If none is selected, prefer an already connected tool that satisfies the request. Ask for a choice only when options differ materially in identity, expressiveness, language, synchronization, reference handling, privacy, cost, or output format.

Do not rely on remembered provider capabilities or hardcoded model rankings. Inspect the tool schema and current provider instructions.

## ChatGPT and Codex

On supported ChatGPT web and desktop Chat or Work surfaces, performance tools may be native or supplied through installed plugins and their connectors or remote MCP servers. Open the Plugins area to install or enable a trusted compatible service, authenticate it, and start a new conversation when the host requires it.

ChatGPT web does not read local Codex MCP configuration. A server configured only for the local CLI will not automatically appear in a ChatGPT web conversation.

Codex desktop, CLI, and IDE can connect directly to MCP servers on the same Codex host. Use the MCP settings UI when available. For a remote Streamable HTTP server in the CLI, the current command pattern is:

```text
codex mcp add <server-name> --url <https://server.example/mcp>
codex mcp login <server-name>
codex mcp list
```

Use `codex mcp --help` for additional server options and `/mcp` to inspect active servers.

Official references:

- https://learn.chatgpt.com/docs/plugins
- https://learn.chatgpt.com/docs/extend/mcp?surface=cli

## Claude and Claude Code

For Claude web, desktop, Cowork, and mobile, a cloud voice or performance service can be exposed through a remote connector when it provides a public remote MCP endpoint. In an individual account, open Customize, choose Connectors, add the trusted custom connector URL, authenticate, and enable it for the conversation. Team and Enterprise workspaces may require an owner to add the connector first.

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

## Verify the connection

After setup:

1. Confirm the tool appears in the active conversation or MCP status view.
2. Confirm authentication, project selection, and allowed media types.
3. Inspect the tool schema and model or version offered.
4. Run a short low-risk identity or timing test before a large or paid batch when uncertainty remains.
5. Confirm that returned audio or video can be played or inspected in the host.

An installed connector is not proof that a specific voice, clone, language, lip-sync method, duration, or performance control is available.

## Protect voice, likeness, and private media

- Connect only trusted servers and review permission scopes.
- Confirm authorization before cloning, imitating, transforming, or externally processing a real person's voice or likeness.
- Never place API keys, bearer tokens, OAuth secrets, private URLs, or permission evidence in prompts, profiles, take logs, or media metadata.
- Do not upload unreleased scripts, private recordings, or actor references without authorization.
- Distinguish generating a private test from publishing, sharing, or deploying it. Obtain approval for external release.

## Invoke and track the test

- Send only the references required for declared roles.
- Map identity, delivery, exact dialogue, timing, and physical state to supported fields.
- Record provider, model, version, settings, references, take hypothesis, and returned asset or job identifier when production tracking requires it.
- For asynchronous tools, wait or poll through the supported mechanism. A queued job is not a completed take.
- Preview the destination before overwriting, publishing, or sharing a production asset.

## Manual fallback

If a compatible tool cannot be connected, return:

- Character and scene performance packet.
- Exact dialogue and speaker map.
- Voice identity and delivery layers.
- Reference roles and attachment checklist.
- Model-neutral prompt and selected-provider adapter notes when known.
- Settings, duration, output, and synchronization assumptions.
- Verification and take-comparison checklist.

State that no media asset was generated. Do not present setup instructions, a queued job, or a written prompt as a completed performance.
