# Documentation

Use this playbook for PR descriptions, engineering summaries, product-impact notes, architecture updates, and notification recommendations.

## Ground the document

Inspect the actual diff or implementation, its callers and consumers, relevant tests, and existing documentation. Use the requested audience and destination when supplied. Do not infer a deployment, rollout, owner, ticket, or user impact without evidence.

Separate:

- what changed technically;
- what behavior changes for users or downstream systems;
- what remains compatible or intentionally unchanged;
- how the result was verified;
- what is deferred, risky, or still unknown.

## Describe product and downstream impact

Trace changed behavior through public interfaces, data formats, errors, events, permissions, performance characteristics, feature flags, and operational workflows.

State “no user-visible change” only after checking the relevant path. Qualify impacts that depend on rollout state, configuration, data shape, or external consumers.

## Update architecture descriptions

Make documentation match the implemented system, not the original plan. Include only components and relationships affected by the change.

When updating a diagram:

- preserve its established format when practical;
- add, remove, or relabel the exact changed nodes and edges;
- include important data, control, permission, or error flow when relevant;
- verify diagram labels against current symbols and behavior;
- label inferred external relationships.

Do not create a diagram when a short paragraph or table communicates the change more clearly.

## Identify notification candidates

Use evidence in this order:

1. declared ownership such as `CODEOWNERS` or repository ownership metadata;
2. maintainers named in project documentation;
3. reviewers or owners associated with the affected component;
4. recent contributors from version history.

Describe recent contributors as contribution evidence, not definitive ownership. Explain why each person or team may need notification, based on the affected boundary or responsibility. Never invent names or contact anyone unless the user explicitly authorizes communication.

## Shape the requested artifact

For a PR description, prefer:

1. **What changed**
2. **Why**
3. **User and downstream impact**
4. **Architecture or data-flow change**, only when material
5. **Verification**
6. **Rollout, risk, or follow-up**, only when applicable

For an engineering summary, lead with the outcome and decisions, then provide enough evidence for another engineer to understand the change without reconstructing the entire investigation.

Return the ready-to-use artifact first. Add assumptions or unresolved facts only when material.
