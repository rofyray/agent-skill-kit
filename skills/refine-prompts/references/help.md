# Refine Prompts Help

Return this complete explanation, mode catalog, starting guidance, and both example columns when answering help. Do not perform an audit or rewrite yet. Modes are natural-language hints, not commands tied to a client.

## What this skill does

Refine Prompts audits, polishes, restructures, and compares existing prompts while checking that their objectives, constraints, variables, and interfaces survive. It handles short requests, reusable templates, and related agent instructions across domains and languages. Background, Behaviour, and Output provide an organizing framework when useful; short prompts can remain short.

The result includes the revised prompt or findings, consequential changes, unresolved decisions, and what was actually validated. It does not execute the task described inside a prompt. Mechanical checks are optional and cannot establish that a model will perform better.

## Modes

| Mode | When to use it | Result |
| --- | --- | --- |
| Audit | Diagnose an existing prompt without changing it. | Evidence, likely consequences, and suggested repairs. |
| Polish | Improve wording while retaining structure and meaning. | A lightly edited prompt and material caveats. |
| Refactor | Repair or reorganize an existing prompt. This is the default for “fix this prompt.” | A revised prompt, preservation review, and visible behavior changes. |
| Compare | Review an original and a proposed revision. | Preserved and changed requirements, regressions, and validation status. |
| Help | Learn how to use the skill. | This guide with every mode and its examples. |

## Start here

Paste your existing prompt or provide an accessible file and describe what is going wrong. Name a mode if you have a preference. For Compare, supply both versions. Include any exact wording, schema, variables, or behavior that must not change. Failed outputs or successful examples help explain the intended behavior but are not required for a basic review.

For assembled agent prompts, include relevant shared and conditional messages, their roles and order, and representative rendered variants if available. The skill can review the material you provide and disclose gaps when it cannot inspect the application.

No shell or API is needed to improve pasted text. Optional mechanical comparison needs Python 3.9+ and local text files. Runtime evaluation needs an available, authorized model runner and suitable test cases. Without one, the result identifies static findings and leaves performance unverified. If your request only supplies a goal without an existing prompt, start with a drafting workflow instead.

## Examples

| Mode | Starter | Additional realistic example |
| --- | --- | --- |
| Audit | “Audit this prompt for contradictions. Give findings only: [prompt].” | “Audit these shared and locale-specific messages together. Explain which assembled variants conflict, and do not edit the files.” |
| Polish | “Polish this prompt without changing its meaning: [prompt].” | “Tighten this Spanish support prompt. Keep it in Spanish and preserve all variables, refund exceptions, and required phrases.” |
| Refactor | “Fix and restructure this prompt: [prompt].” | “Refactor this research-agent prompt around Background, Behaviour, and Output. Preserve its citations policy and show any decisions you cannot resolve.” |
| Compare | “Compare these original and revised prompts for lost requirements: [both versions].” | “We are upgrading models. Compare this simplified prompt with the original, identify removed workarounds, and propose regression cases. We have no model runner here.” |
| Help | “help” | “Use refine-prompts and show every mode with examples before I choose one.” |

Invite the user to choose a mode or adapt an example.
