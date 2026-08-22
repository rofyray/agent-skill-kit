# Agent brief template

Use this template as a drafting scaffold, not a requirement to include empty sections.

```markdown
# Context

## Situation and objective
[Explain the current situation, the outcome, and the decision or downstream use this work supports.]

## Audience
[Name the users, reviewers, or decision-makers and what matters to them.]

## Working materials
- [Exact file, repository, URL, dataset, ticket, prior version, or reference]
- [Existing standard, template, design system, test, or example]
- [Known current state and relevant history]

## Unknowns and assumptions
- [Known uncertainty the agent must preserve or investigate]
- [Explicit low-risk assumption, if needed]

# Task

[State the concrete work to perform and the outcome to produce.]

# Constraints

## House rules
- [Non-negotiable scope, policy, safety, compatibility, or quality rule]
- [Behavior or existing contract that must not change]

## Authority and approvals
- Decide independently: [in-scope reversible decisions]
- Ask before: [destructive, production, spending, external, or scope-changing action]
- If blocked: [evidence and smallest decision needed]

# Verification - do not finish until

1. [Inspect or run a check against the actual artifact.]
2. [Reconcile facts, data, behavior, or appearance to the named source of truth.]
3. [Re-run relevant existing checks and confirm no regression.]
4. [List anything that could not be verified and why.]

Record the evidence for each check. Do not substitute an implementation summary for inspection.

# Output format

- Primary deliverable: [file type and user-supplied path, or proposed filename plus a visible destination placeholder]
- Required structure: [sections, fields, slides, tables, order]
- Supporting deliverable: [summary, evidence, limitations, decision log]
- Length, tone, or style: [only if relevant]
```

## Compression rules

- Merge context subsections when the task is small.
- Omit audience when it cannot affect the result.
- Omit approvals when the brief is read-only and low risk.
- Keep verification even in short briefs; use one or two proportionate checks.
- Prefer exact resource locations over long descriptions of their contents.
- State a missing path as a placeholder instead of inventing one.
- Do not derive an output directory from the location of an input or reference artifact.
