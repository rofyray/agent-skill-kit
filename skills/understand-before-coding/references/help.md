# Understand Before Coding Help

Use this reference to answer help mode. Present the explanation, modes, start guidance, and examples in a detailed but scannable user-facing form. Include every named mode and both example columns; do not collapse or omit them for brevity. Do not inspect or modify code while answering help.

## What this skill does

This skill builds the smallest evidence-backed understanding needed to reason correctly about a codebase. It finds existing patterns, traces control and data flow, distinguishes verified behavior from inference, scopes downstream impact, and preserves the user's requested action boundary.

It defaults to read-only investigation for explanation, planning, review, and documentation. It edits code only in implement mode or when the user otherwise clearly requests a change.

Verify mode inspects and runs appropriate checks in an authorized test environment. It reports evidence and gaps without automatically repairing application code or rewriting tests. Requests to add tests or fix failures authorize those scoped changes. Temporary probes may use isolated scratch space. Without runtime access, it returns a check plan and labels execution as unavailable.

## Modes

| Mode | Use it for |
| --- | --- |
| `understand` | Explain functions, callers, architecture, user flow, errors, permissions, tests, or documentation. |
| `plan` | Design a feature after inspecting reuse opportunities, boundaries, bottlenecks, isolation, and concrete future extensions. |
| `implement` | Make the smallest justified code change and verify it. |
| `review` | Assess a diff or code path for correctness, regressions, security, permissions, performance, consistency, and missing coverage. |
| `verify` | Check whether specified behavior meets its requirements, assess the checks themselves, and report pass, fail, blocked, or not-run evidence. |
| `document` | Produce a PR description, engineering summary, architecture update, product-impact note, or notification plan grounded in the code. |
| `help` | Display this guide without inspecting or changing code. |

The user can name a mode or describe the outcome naturally. No slash command is required.

Use review for actionable findings about code; use verify for evidence about behavior. Planning can specify acceptance checks, and implementation can run them during authorized repairs, without requiring a separate invocation.

Dedicated independent change reviews, adaptive review committees, and tracked re-reviews can use `review-code-changes` when installed. This skill retains ordinary Review mode and works on its own; an explicit selection is respected. Neither workflow automatically runs the other.

## Start here

Identify the repository, feature, symbol, flow, or diff and the question or action you care about. Add focus such as “minimize the change,” “prioritize permissions,” or “keep billing isolated” when relevant. The skill will inspect available evidence before asking for context it can discover itself.

If access is limited to a single file or excerpt, say so; the skill will provide a narrow conclusion and identify what remains unknown rather than inventing the rest of the architecture.

For verification, identify the behavior or change and any required outcomes, compatibility baseline, or environment constraints you already know. Existing commands and test setup will be discovered where accessible. State whether you also want tests added or failures repaired; a request to verify alone preserves application and test code.

## Examples

| Mode | Starter | Another example |
| --- | --- | --- |
| `understand` | `Explain what resolvePolicy does, how many callers it has, and how its errors propagate.` | `Map the checkout user flow and show where permissions and retries are enforced.` |
| `plan` | `Plan audit-log export by finding existing export patterns and keeping the design isolated from billing.` | `Design team invitations so scheduled reminders could be added later without building them now.` |
| `implement` | `Implement the smallest fix for duplicate webhook processing and preserve the current API behavior.` | `Add this feature using the existing repository pattern and verify the affected edge cases.` |
| `review` | `Review this admin endpoint for object-level permissions, error propagation, and missing tests.` | `Review the diff for downstream regressions and report only actionable findings with evidence.` |
| `verify` | `Verify that checkout creates a saved order in the local test environment. Run existing checks and leave the code unchanged.` | `Verify this parser migration against the old version, add focused compatibility tests, and report unexplained differences without repairing the parser.` |
| `document` | `Write a PR description covering product implications, downstream callers, architecture changes, and verification.` | `Update the architecture explanation and identify likely engineers to inform using repository evidence.` |
| `help` | `Help` | `Show me every code-understanding mode and examples without inspecting the repository yet.` |

End the help response by asking which mode the user wants or inviting them to paste a code question, change request, or diff.

For substantial visual redesign or interface-quality auditing, use `design-beyond-defaults` when available. Its Redesign mode preserves required behavior; Audit measures the implemented interface; Critique reviews rendered visuals. Mechanical CSS fixes and code-defect review remain scoped here. The specialist is optional and does not require a second complete workflow.
