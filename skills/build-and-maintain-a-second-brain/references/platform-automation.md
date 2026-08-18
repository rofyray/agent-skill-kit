# Platform automation and fallbacks

Use this guide to select an honest execution path. Product capabilities, organization policy, regional availability, and approvals can differ; inspect the active host rather than relying on its name alone.

## Capability matrix

| Environment | Vault setup and operation | Obsidian UI | Recurring maintenance |
| --- | --- | --- | --- |
| Codex, Claude Code, or Cursor with local file/shell access | Full setup and file operations inside an approved vault | Open with an available desktop-control capability; otherwise give the user the folder path | Use a native local scheduler when available, or an approved OS scheduler command |
| ChatGPT Desktop/Work with local project access | Full setup within the connected project, subject to sandbox and approvals | Use Computer Use only when installed, enabled, and approved | If the active Scheduled UI offers that local project, use the live project while the computer and app are available; otherwise use a fallback |
| ChatGPT Work on the web or in cloud mode | Operate on uploaded/account files, skills, plugins, and connected storage; no direct arbitrary local-folder access | Use the cloud browser for websites, not local Obsidian | Web schedules can use available uploads and connected tools, but do not retain a local folder or worktree |
| Claude Cowork on desktop, web, or mobile with an active desktop bridge | Full setup inside a folder explicitly connected through Claude Desktop while that app and computer remain available | Use approved computer use through Claude Desktop when available | Use a local-file schedule only when the UI explicitly binds that folder and indicates local execution |
| Claude Cowork cloud session without a desktop bridge | Operate on account files, skills, plugins, and remote connectors; no direct local-vault access | Cannot operate local Obsidian | Remote schedules use account files and connectors; use an accessible remote vault or reminder |
| Ordinary ChatGPT or Claude web chat without Work/Cowork file tools | Use attached or connected snapshots only | Cannot operate local Obsidian | Use a reminder or accessible remote copy |
| Chrome extension alone | Capture and download web sources only | No general local-app control | Browser schedules can automate web tasks, not local wiki maintenance |

Never turn a capability limitation into a claim of success. Deliver a starter bundle and a precise handoff when the host cannot write locally.

## Local and CLI setup

1. Ask the user to choose or approve the vault folder. Do not default to a broad home directory.
2. Initialize files with `scripts/second_brain.py` or copy the templates.
3. If the user wants Obsidian and it is unavailable, offer the official Obsidian download. Installing an application or package requires confirmation.
4. Open the folder as a vault. Let Obsidian create `.obsidian/`; do not fabricate app state.
5. Prefer filesystem operations over UI automation for repeatable wiki edits. Use the UI to open, inspect, or configure only what files cannot express safely.

## Desktop and bridged app control

Desktop control is optional and permissioned. Before operating Obsidian:

- verify the host exposes computer-use or an equivalent approved capability;
- request access to Obsidian and the specific vault only;
- keep account, privacy, plugin installation, and security changes user-supervised;
- confirm saves landed on disk and run a structural scan afterward.

If desktop control is unavailable, the setup is still complete when the markdown folder is valid. Tell the user how to open it in Obsidian.

Claude Cowork sessions started on the web or mobile can use approved local folders, browser access, and computer use through Claude Desktop. Treat this as a desktop bridge, not native browser filesystem access: the desktop app must be open, the computer available, and the exact folder connected. If any condition fails, switch to the cloud-only fallback.

ChatGPT Work on the web can perform cloud work with files, plugins, connectors, and a cloud-operated browser. Local files, apps, and Obsidian control remain desktop capabilities unless the active product explicitly exposes a separate verified local connection.

## Cloud-only setup

1. Build a downloadable folder or ZIP from `assets/vault-template/` and include the bundled helper as `automation/second_brain.py`.
2. Substitute the vault name, creation date, and review mode in the text templates. Generate `.second-brain/config.json` and `.second-brain/raw-manifest.json`.
3. Preserve the required empty directories with directory entries or harmless placeholders, then verify the extracted structure against the vault contract.
4. Tell the user to extract the folder and choose **Open folder as vault** in Obsidian.
5. To continue in the web host, prefer a connected repository or storage location. An upload is a point-in-time snapshot, not sync: request the engine, index, log, affected wiki pages, and underlying raw evidence, then return an explicit change set or replacement bundle for the user to merge. Alternatively, switch to a desktop/local agent.

A browser extension or cloud browser may clip or download a source. It does not, by itself, place that file into a chosen Obsidian vault or provide continuing filesystem access.

## Scheduling decision tree

### Native scheduler with the live vault

Use it when the scheduled run can open the same folder and retain the skill or engine instructions. Obtain consent for a manual preflight that writes to the live vault, or test in a safe copy and disclose the limitation. Schedule separate tasks for lint and review so a failure is easy to diagnose. Give them distinct times or a supported dependency; without dependency chaining, run review later and require it to confirm that the current lint report completed.

For ChatGPT Desktop local-project schedules:

- use this path only when the active schedule UI explicitly offers the local project and a test run proves it can update that exact vault;
- bind the task to the non-version-controlled vault directory, or choose the local project mode for a Git-backed vault;
- do not choose an isolated worktree when the task must update the live vault;
- keep the computer on, the desktop app running, and the vault available for local-file runs.

For ChatGPT Work schedules created on the web:

- use uploaded/account files, skills, plugins, and connected tools for cloud runs;
- do not claim a persistent local vault or worktree is available between web runs;
- route local-vault maintenance to a desktop local-project schedule, or keep the canonical vault in genuinely connected storage.

For Cowork schedules:

- schedules can be created and reviewed from web, desktop, or mobile;
- select the local vault folder only when the schedule UI provides that option and clearly indicates local execution;
- recognize that local-file or local-app work requires the desktop bridge, while remote runs use account files and connectors;
- verify the first scheduled run actually touched the expected vault before relying on it.

### CLI host without a native scheduler

1. Identify the installed agent CLI and confirm it supports the intended non-interactive invocation.
2. Put the durable prompt in the vault's `automation/` directory.
3. Preview the exact command, working directory, environment, cadence, log destination, and approval behavior.
4. Obtain explicit approval before creating a cron entry, launchd job, Task Scheduler task, or equivalent.
5. Avoid putting secrets in the command line. Do not assume unattended login or permission bypasses.
6. Run once manually and inspect the report and `log.md` entry.

### No persistent local access

Create one of these honest fallbacks:

- a recurring reminder telling the user to open the vault and run the prompt;
- a task over a repository or storage connector that truly contains the vault;
- a web-source harvesting task that produces source files for later local ingestion.

State that the local wiki will not be modified automatically.

## Default maintenance proposal

If the user asks for automation but gives no cadence, propose rather than silently create:

- structural and semantic lint: weekly;
- weekly loop review: weekly, after lint completes;
- manual verification: inspect the first three runs;
- timezone: the user's confirmed local timezone;
- write policy: reports and log entries only, with semantic fixes requiring later approval.

Report how to pause, edit, run now, and remove every schedule you create.
