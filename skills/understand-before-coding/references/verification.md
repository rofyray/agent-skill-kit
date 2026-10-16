# Verification

Use this playbook to establish evidence about a specified behavior, change, or migration. In Plan, design the checks without claiming execution. In Implement, apply them while making authorized changes. In Review, assess whether the evidence supports the claims. In Verify, investigate and execute within the user's requested boundary.

## Establish the verification target

- Identify the behavior, relevant revision or working-tree state, affected paths, and intended environment. Distinguish existing failures from regressions introduced by the change.
- Translate material requirements into observable acceptance criteria before implementing or repairing. Name the authority for each expected result: user requirements, a documented contract, a domain rule, or an explicitly chosen compatibility baseline.
- Treat current code and its tests as evidence to inspect, not automatic authority. If they disagree with a requirement, expose the conflict. If an expectation is unsupported, label it as a proposal or uncertainty instead of inventing an oracle.
- Preserve explicit scope and non-goals. Resolve an ambiguous requirement only when it materially changes the verdict; continue checks whose expectations are already clear.

For each criterion, identify the check, expected observation, and material failure it should detect. Keep this compact; do not create a new framework or repository-wide inventory for a narrow task.

## Check capabilities and side effects

Discover the project's existing commands, fixtures, launch instructions, and test environments. Do not assume shell, browser, network, package installation, or a particular testing library. Inspect unfamiliar commands before execution when their setup or effects are unclear.

Verification alone does not authorize repairs, dependency changes, test deletion, deployments, or real transactions. Use controlled local or sandbox state for probes, with cleanup limited to artifacts created for this task. A read-like user journey can still send email, charge money, or alter shared data; choose an available test path within existing authority. Report a blocked check when no such path exists.

When execution is unavailable, inspect supplied evidence and provide a concrete check plan with prerequisites and expected observations. Mark runtime criteria blocked or not run. Distinguish a proposed command from one actually executed.

## Select checks by the failure they can expose

Use the smallest combination that addresses the material risks. Existing unit, integration, type, lint, and build checks remain useful; no single test type is mandatory for every change.

| Risk or question | Useful evidence | What to inspect |
| --- | --- | --- |
| A user journey crosses several boundaries | A focused end-to-end flow against a running test system | Follow the relevant action through responses and durable outcomes. A success screen alone cannot establish persistence, delivery, or authorization. Use traces, logs, or screenshots only where they clarify the result. |
| Many inputs must obey a domain rule | Property-based checks | State the property independently of the implementation; choose valid input domains, boundary cases, reproducible seeds, and a bounded sample appropriate to the risk. Retain minimized failures as regression cases when test edits are authorized. |
| A replacement must preserve behavior | Differential checks against the agreed baseline | Apply the same representative or generated inputs to both systems. Compare meaningful outputs, errors, and side effects. Normalize only semantically irrelevant differences. Record each intended divergence and its requirement; legacy bugs are not automatically desired behavior. |
| An existing regression or local contract | A focused example or integration check | Reproduce the failure or baseline when possible, then exercise the affected boundary and nearby failure paths. |
| A subtle concurrency or state-transition claim resists ordinary checks | A small model or formal analysis, when justified and supported | State modeling assumptions and connect counterexamples to the real implementation. A model result does not establish correctness outside those assumptions. |

For runtime work, record only the feature path needed to reproduce the result: how to launch or reach it, the relevant actions, expected outcomes, and environment constraints. Reuse an existing feature map when available.

Generated input volume, test count, coverage percentage, and a clean build do not establish that the acceptance criteria were checked. Describe sampled domains and untested boundaries.

## Assess the checks themselves

Ask what plausible incorrect implementation each important check would reject. Inspect assertions and mocks for shared assumptions, tautologies, bypassed boundaries, and missing negative cases. Derive expected results independently of the function under test.

When practical, demonstrate sensitivity using a known failing baseline, a concrete counterexample, or a controlled fault in an isolated copy. Do not alter the user's working tree just to inject a defect. A failing test must fail for the intended reason, not because setup is broken.

For high-risk or ambiguous work, an independent reviewer can assess the requirements and actual evidence if the host supports and authorizes delegation. Provide the raw artifacts and acceptance criteria without the builder's preferred conclusion. If unavailable, perform a separate evidence review and disclose that it was not independent; do not block ordinary verification on a second agent.

## Operate the feedback loop

1. Run focused baseline checks when feasible. Record commands or interactions, state, environment, and results, including pre-existing failures.
2. Classify a failure as evidence of application behavior, a check defect, or an environment problem; keep uncertain causes explicit. Diagnose before retrying.
3. If repair is authorized, make the smallest change addressing that cause. Keep acceptance criteria stable unless requirements justify a visible change. Never weaken assertions, normalize a meaningful mismatch, or remove checks merely to produce a pass.
4. Rerun affected checks after relevant changes, then broader existing checks according to regression risk. Final evidence must describe the final tested state. Do not reuse a pre-edit pass as post-edit evidence.
5. Stop when the requested assessment is complete, or the authorized repair meets its criteria. Otherwise report the specific missing capability, authority, input, user-defined budget limit, or repeated lack of progress. Do not loop without new evidence or treat a stop as success.

Prefer quick focused checks during iteration and reserve expensive flows for the relevant integration boundary. Control randomness, clocks, networking, and state where appropriate, while retaining separate checks for real integration behavior. Keep diagnostics short enough to locate the failing criterion and reproduce it.

If an unchanged rerun passes, retain the failure and investigate instability; the later pass does not erase it. Do not silently delete or quarantine a flaky test. If test-infrastructure changes are authorized, make lost coverage and any quarantine explicit, with a repair owner or follow-up where available. Never call a required criterion verified solely because its flaky check was excluded.

## Return evidence, not a blanket guarantee

Lead with the conclusion for the requested scope. Include the tested revision or working state and relevant environment, then a compact criterion-level record:

| Criterion and authority | Check and evidence | Result | Limitation or next action |
| --- | --- | --- | --- |
| Required observable outcome and its source | Actual command or interaction, relevant observation, artifact path if saved | Pass, fail, blocked, or not run | Missing coverage, instability, or smallest necessary next step |

Use **pass** only when the criterion has supporting observations; **fail** when evidence contradicts it; **blocked** when a required prerequisite prevents assessment; **not run** when the check was not attempted. Explain exclusions and avoid converting a static review into a runtime pass.

Separate defects in the application from deficiencies in the checks. Retain conflicting observations and distinguish proposed checks from executed ones. If material criteria fail or remain unverified, say so. Even when all selected checks pass, limit the conclusion to their scope and conditions.
