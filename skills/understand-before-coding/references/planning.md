# Planning

Use this playbook to plan a feature or code change without editing the codebase.

## Define the decision

- Restate the intended user or system outcome, not merely the proposed implementation.
- Identify the current behavior, desired behavior, non-goals, and compatibility constraints.
- Resolve only questions that would change architecture, scope, safety, or acceptance criteria.
- Keep optional future work separate from the present requirement.

## Find the existing shape

Inspect the narrowest complete slice that can answer the design question:

- entry points and public contracts;
- domain or service boundaries;
- data models, persistence, events, APIs, and external systems;
- sibling features that solve a similar problem;
- shared functions and extension mechanisms;
- call sites and downstream consumers;
- tests, docs, flags, migrations, observability, and rollout patterns.

Prefer an established pattern when its responsibility, lifecycle, failure behavior, and ownership fit the new feature. Do not copy a pattern solely because its code looks similar.

## Design the minimal architecture

Describe:

1. the components that change or remain untouched;
2. the request, event, or data flow through them;
3. contracts at each boundary;
4. validation, permissions, and trust boundaries;
5. error propagation, recovery, retries, and partial failure behavior where relevant;
6. state transitions, concurrency, caching, or idempotency where relevant;
7. logging, metrics, or audit evidence required to operate the feature.

Explain how the design limits impact on unrelated code. Name the seam that isolates the behavior, such as an existing interface, adapter, handler, strategy, feature flag, event, or data boundary.

## Test reuse and extensibility claims

For each proposed reuse point, confirm:

- semantic behavior matches, not just types or syntax;
- inputs, outputs, errors, authorization, and side effects remain compatible;
- the dependency direction stays appropriate;
- changing the shared code will not force unrelated consumers to adopt new behavior.

Evaluate extensibility against a concrete anticipated variation. Identify what would change, what would stay stable, and whether the proposed seam supports that variation without speculative frameworks or generalized configuration.

## Locate bottlenecks and risks

Ground performance claims in a hot path, multiplicity, blocking resource, observed measurement, algorithmic cost, or known capacity constraint. If no evidence exists, describe a risk to measure rather than declaring a bottleneck.

Check the material concerns selected by the core workflow, especially:

- correctness and edge cases;
- security and permissions;
- compatibility and downstream effects;
- migration and rollback;
- operational visibility;
- testability.

## Return a decision-ready plan

Use only sections that help the decision:

1. **Recommendation**
2. **Evidence and existing patterns**
3. **Architecture and flow**
4. **Affected and isolated boundaries**
5. **Alternatives and tradeoffs**
6. **Risks and verification**
7. **Open decisions**

Use a diagram only when it clarifies relationships that prose cannot express as efficiently. Do not include implementation steps more detailed than the evidence supports.
