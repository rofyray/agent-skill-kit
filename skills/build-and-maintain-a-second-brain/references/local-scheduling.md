# Local scheduling safety and setup

Use this guide only when the user chooses automatic ingestion or maintenance of a vault on their own computer. Product Scheduled reminders are the safer fallback when no local agent can run unattended.

## Preconditions

Do not install a schedule until all of these are true:

1. The user approved the exact vault, cadence, timezone, executable, write policy, and schedule mechanism.
2. The agent CLI supports a documented non-interactive mode and is already authenticated in the background execution context. Every remote or connected source also works non-interactively. Never request or embed credentials.
3. The exact command succeeds from the vault with a minimal environment and no interactive prompt.
4. The scheduled executable can read and write the vault. On macOS, Desktop, Documents, Downloads, iCloud Drive, network volumes, and removable volumes may require user-granted Files & Folders or Full Disk Access. Explain the breadth of the permission; never relocate the vault to evade it.
5. The command is constrained to the vault and maintenance operation. Use the host's narrow sandbox or tool allowlist. Do not use `--dangerously-skip-permissions`, an equivalent blanket bypass, or a broadly privileged shell merely for convenience.
6. Standard output and error have explicit log destinations, and the user knows where to inspect them.

Resolve the executable to an absolute path. If that path is a symlink into a versioned installation, warn that an update may change the resolved binary and invalidate macOS privacy approval. Re-run the preflight after an agent CLI upgrade.

## Maintenance order

Prefer two independently observable jobs:

- lint first;
- review later, with enough offset for lint to finish;
- review must find the latest successful lint event for the same maintenance window and stop with a clear log message if it is missing.

If the scheduler supports reliable dependencies, use one sequential job instead. Never start lint and review simultaneously. Default writes are dated reports and append-only log entries; semantic fixes still require later approval.

Recurring ingestion may have its own cadence. Give each recurring source its own observable task or an explicitly bounded batch so one failing source cannot hide the status of the others. Do not make lint or review depend on every ingest run.
Configure each source task to prevent overlapping instances. Use the helper's atomic checkpoint compare-and-set; a scheduler success or non-overlap setting alone is not a substitute for checkpoint verification.

## macOS `launchd`

Use a per-user LaunchAgent with `StartCalendarInterval`; Apple recommends `launchd` rather than cron for timed macOS jobs. Calendar jobs missed while the Mac is asleep run after wake, but jobs missed while it is powered off wait until the next scheduled time.

Build the property list with:

- a unique `Label`;
- `ProgramArguments` as an array containing the absolute agent executable and each literal argument - do not rely on shell interpolation;
- `WorkingDirectory` set to the absolute vault path;
- `StartCalendarInterval` with the approved weekday, hour, and minute;
- `StandardOutPath` and `StandardErrorPath` pointing to an approved log directory;
- no credentials or tokens in arguments or environment variables.

Prefer invoking the agent binary directly. For a CLI with a positional prompt, pass a short literal argument such as `Read and execute automation/recurring-ingest.md in this vault.`, `Read and execute automation/lint-wiki.md in this vault.`, or `Read and execute automation/weekly-review.md in this vault.` after verifying the installed CLI's syntax. This keeps the durable prompt current without shell interpolation or embedding a stale copy in the property list.

On macOS, prefer an approved absolute log directory under the user's `Library/Logs/` rather than inside a protected vault. Create the parent directory before loading the job. This preserves authentication and privacy errors even when macOS denies vault access. Do not place logs in `raw/`, `wiki/`, or the report directories.

If the CLI cannot accept the maintenance prompt without shell redirection, use the smallest reviewable runner possible and explain that macOS privacy permission may then apply to the runner or interpreter rather than only the agent binary. Do not grant broad access to `/bin/zsh` or another general-purpose shell as the default solution.

Before loading the job:

1. Validate the property list with `plutil -lint`.
2. Show the property list and exact command to the user.
3. Run the exact agent invocation manually from the declared working directory.
4. Install the property list in the user's `~/Library/LaunchAgents/` only after approval.
5. Load it with the current `launchctl` workflow available on that macOS version, then run it once on demand.
6. Verify the expected new capture or report, append-only log event, checkpoint behavior, and scheduler stdout/stderr. A successful scheduler status alone is not proof that vault work completed.

If authentication, Keychain access, filesystem privacy, or permissions fail, leave the job disabled and give the user the smallest manual step needed. Never keep moving the vault or broadening permissions until something happens to work.

## Linux and Windows

On Linux, prefer a systemd user service and timer when available. Set the working directory, absolute executable, restricted permissions, persistent logs, and an explicit dependency or time offset. Use user cron only when systemd is unavailable and after previewing the exact entry.

On Windows, use a per-user Task Scheduler task. Set the full executable path, vault as the start-in directory, user context, recurrence, log output, and failure behavior. Verify whether the task should run only while the user is logged in; do not store a password on the user's behalf.

Apply the same authentication, least-privilege, first-run, and upgrade revalidation rules on every operating system.

## Native reminder fallback

For a local vault that the product's scheduled runtime cannot access, create a reminder whose output tells the user to:

1. open the desktop app or CLI;
2. select or attach the exact vault;
3. run `automation/recurring-ingest.md`, `automation/lint-wiki.md`, or both as configured;
4. after lint succeeds, run `automation/weekly-review.md` when review is due;
5. inspect the captures, reports, and proposed semantic fixes.

Do not call this automatic vault ingestion or maintenance. The scheduled event is automatic; the local edits are user-triggered.

## Probes, moves, and cleanup

- Test product-to-device access only when the user asks or when documentation is inconclusive and the result materially affects setup.
- Use a disposable vault or a uniquely named probe outside `raw/`, `wiki/`, and reports. Inventory it before running.
- Delete only artifacts created by the probe, then confirm the schedule and probe inventory are empty.
- Never move or rename the real vault to diagnose scheduler permissions without a separate migration approval. If the user does approve a move, snapshot or hash it first, close or reopen Obsidian as needed, verify the registered path, and update every absolute scheduler path.
- Initializing Git or adding a remote is a separate choice. For cloud automation, recommend a private remote and a review branch; never push a personal vault publicly by default.
