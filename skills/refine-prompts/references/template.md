# Prompt structure

Use this original template to organize a rewrite. The three-part organization is inspired by Wulfie Bain's article; the wording and extensions here are independently written. Keep only relevant subsections, preserve required ordering, and translate headings when appropriate. Existing output schemas take precedence over this presentation pattern.

```markdown
# Background

## Aim
[The outcome this agent or task should achieve, for whom, and within what scope.]

## Context
[Relevant facts, domain definitions, available inputs, and environment. Preserve template variables exactly. Distinguish provided facts from unresolved choices.]

# Behaviour

## Initiative and clarification
[Which decisions the agent may make; which missing facts require a question; which actions need approval under the existing authority.]

## Workflow
[Required procedures, important decision branches, and completion checks. Leave optional implementation choices open.]

## Tools
[Available tools and the conditions for choosing them. Describe dependencies before allowing parallel calls. Define relevant failure behavior without inventing capabilities.]

# Output

## Deliverable and format
[What the recipient receives, including any exact schema, required fields, or destination.]

## Response requirements
[Audience, language, tone, length when specified, evidence requirements, and content boundaries.]
```

## Place each rule deliberately

Background describes what is known. Behaviour describes actions and decisions, including clarification interactions. Output describes what is delivered and how it is presented. Do not prescribe visible reasoning merely because the working process is structured. Necessary progress updates or approval questions remain visible interactions; the backend analogy does not mean the agent must work silently.

Give each rule one authoritative location. Put examples alongside the rule they illustrate or in a clearly scoped examples section. Check them against the full instruction set. A short cross-reference can be preferable to another copy of a policy, but the final prompt must remain self-contained for its consumer.

The structure is an editing aid, not an instruction hierarchy or a proof of independence. Preserve actual message roles, tool definitions, template escaping, and application boundaries. Review the full prompt after local changes.

## Match detail to the task

For a general agent, define the destination and boundaries without guessing a rigid plan. For a prescribed workflow, retain necessary order, branch conditions, and failure paths. For a one-paragraph task, the three concerns can remain implicit in clear prose. Do not add empty tool or workflow sections.

When input does not specify a consequential preference, leave a visibly unresolved choice outside the ready-to-use artifact or label the artifact as a draft. Do not substitute generic “best practices” for a product decision.
