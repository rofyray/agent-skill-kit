# Analysis Lenses

Use only the lenses relevant to the user's question, the code path, and observed risk. Do not mechanically apply every lens.

## Reuse and patterns

- Is there existing code with the same responsibility and contract?
- Is the apparent pattern intentional and current, or merely repeated legacy code?
- Would reuse preserve dependency direction, ownership, lifecycle, errors, and permissions?
- Would changing the shared code alter unrelated consumers?

## Architecture and isolation

- What are the component boundaries and sources of truth?
- Where do data, control, permissions, and errors cross boundaries?
- Can the change enter through an existing seam without affecting unrelated behavior?
- Does the design introduce cycles, hidden coupling, duplicated state, or split authority?

## Extensibility and simplicity

- What concrete future variation is expected?
- Which contract should remain stable if that variation arrives?
- Is a local implementation sufficient now?
- Does a proposed abstraction remove a proven source of duplication or merely add indirection?

## Correctness and edge cases

- What inputs, states, ordering, absence, duplication, retries, partial failures, and concurrency conditions matter?
- Which invariants must remain true before and after the change?
- How does the system behave at boundaries and during recovery?
- Are failure paths observable and actionable?

## Performance

- Is the path hot, repeated, blocking, unbounded, or multiplicative?
- What are the relevant input sizes, query counts, allocations, network calls, locks, or cache behaviors?
- Is there measurement or only a hypothesis?
- Does an optimization change correctness, consistency, or operability?

## Security and permissions

- Where is identity established and authorization enforced?
- Are tenant, role, ownership, and object-level boundaries preserved?
- Can untrusted input reach code execution, queries, paths, templates, logs, or outbound requests?
- Could secrets, personal data, internal errors, or privileged state leak?
- Do defaults fail closed, and are denied actions auditable where required?

## Callers and downstream effects

- Which direct, registered, generated, configured, reflective, or external callers may exist?
- What contracts do they depend on: types, values, errors, timing, side effects, schemas, or ordering?
- Will caches, events, jobs, integrations, analytics, or user workflows observe different behavior?
- Is a migration, compatibility layer, versioning change, or coordinated rollout required?

## Error propagation and resilience

- Where are errors created, translated, logged, retried, swallowed, or shown to users?
- Are cleanup, rollback, timeout, cancellation, and partial-success semantics preserved?
- Can retries duplicate work or corrupt state?
- Do callers receive stable, useful error behavior?

## Tests, comments, and documentation

- Which assertions exercise the behavior rather than merely execute the code?
- Are boundary, failure, permission, and regression paths covered where material?
- Do comments explain current intent rather than stale mechanics?
- Do public docs, examples, diagrams, and API descriptions match functional logic?

## Product and ownership

- What changes for users, operators, administrators, or downstream engineers?
- Does the change alter discoverability, accessibility, latency, permissions, data, or failure experience?
- Who is declared to own the affected boundary?
- If only history is available, which recent contributors are relevant and how uncertain is that signal?

## Focus and deferral

- What concern did the user explicitly prioritize?
- What was explicitly deferred, and does it remain safe to defer?
- Is a supposedly out-of-scope issue critical enough to block or require disclosure?
- What is the smallest result that satisfies the current request without closing off a known necessary next step?
