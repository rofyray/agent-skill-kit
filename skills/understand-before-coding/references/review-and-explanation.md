# Review and Explanation

Use this playbook for code reading, caller tracing, architecture or user-flow explanation, and code review. Remain read-only unless the user separately asks for changes.

## Explain code

For a function, module, or component, establish only the dimensions needed by the question:

- purpose and responsibility;
- inputs, outputs, and contract;
- control flow and important branches;
- state changes and side effects;
- collaborators and external dependencies;
- validation and permissions;
- errors, retries, fallbacks, and cleanup;
- tests, comments, and documentation that define or contradict behavior.

Explain behavior in domain terms before line-by-line mechanics. Cite the symbols or paths that support the explanation.

## Trace callers and effects

Search definitions, imports, references, registrations, routes, events, configuration, generated code, and external contracts as relevant to the language and framework.

Classify results:

- **Confirmed direct callers**: explicit static call sites.
- **Registered or indirect callers**: dependency injection, callbacks, routes, events, reflection, framework registration, templates, or configuration.
- **Potential external callers**: exported or public contracts not fully represented in the repository.

State what was searched. Report an exact number only for the class of references actually counted; do not turn “three static call sites found” into “exactly three callers exist.”

Trace downstream effects through changed return values, errors, side effects, schemas, events, caches, permissions, and user-visible behavior.

## Explain architecture or user flow

Identify the entry point, components, boundaries, data stores, external systems, and terminal outcome. Describe both the happy path and material failure or permission paths.

Create a diagram only when requested or when three or more interacting components make prose materially harder to follow. Use the smallest supported format and distinguish verified edges from inferred ones.

For a page or user flow, connect visible actions to handlers, network or service calls, state transitions, persistence, errors, retries, and user feedback. Do not stop at the UI layer when the question asks about the full flow.

## Review code

Inspect the relevant baseline, diff, surrounding code, callers, and tests. Prioritize findings by impact, not by the order encountered.

A useful finding must include:

1. the behavior or invariant at risk;
2. concrete evidence and a tight location;
3. the condition that triggers the problem;
4. the resulting user, system, security, or maintenance impact;
5. a correction direction when it is not obvious.

Check the relevant analysis lenses, including correctness, edge cases, error propagation, permissions, performance, compatibility, tests, and documentation. Do not report speculative style preferences as defects.

Compare documentation, inline comments, and tests against functional logic. A test's existence does not prove it covers the changed behavior; inspect its assertions and path.

## Return the result

- For explanation, answer directly and separate material unknowns from facts.
- For review, lead with actionable findings ordered by severity. Include residual uncertainty or coverage gaps afterward.
- If no material findings exist, say so plainly and identify any verification limitation that prevents a stronger conclusion.
