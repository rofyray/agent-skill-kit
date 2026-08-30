# Writing Guide

Use this guide for prose inspection, drafting, rewriting, or final prose verification.

## Interpret the four tells

Treat the tells as patterns of accumulated defaults. A single intentional device in source prose is not proof of poor writing or AI authorship. Prose created or revised by this skill uses the strict output policy below.

### Em dashes

Generated or revised prose must contain zero em dashes. Replace them according to the relationship between the clauses:

- Use a comma for a light interruption.
- Use a colon for an explanation or consequence.
- Use parentheses for a true aside.
- Use a new sentence when the thought deserves its own emphasis.

Do not alter a verbatim quotation merely to satisfy the rule. Identify the quoted exception outside the prose when it matters.

### Negative parallelism

Watch for stock contrasts built around forms such as “not just X, but Y,” “not merely X,” “it is not X, it is Y,” or repeated “rather than” framing. These constructions often simulate insight by making the second clause sound more revelatory than its substance warrants.

Revise by stating the real claim directly, naming the actual relationship, or separating distinct ideas. Preserve a negative contrast when the exclusion itself carries necessary meaning, such as a safety boundary or factual correction.

### Overly tidy rhetorical structure

Look for mechanical balance that makes the prose feel preassembled:

- Every paragraph has the same length or sentence pattern.
- Each section mirrors the previous section without a content reason.
- Transitions announce a perfectly orderly sequence that the ideas do not require.
- The conclusion restates the introduction with little added value.
- Headings, summaries, and setup sentences package material that is already clear.

Restore natural emphasis. Let important ideas take the space they need, combine minor points, remove ceremonial transitions, and vary paragraph rhythm according to meaning.

### Automatic triads

Find repeated three-item lists, three-adjective stacks, and conclusions that habitually resolve into three beats. Use the number of items the content actually supports. A factual three-part set can remain when all three members are necessary; do not manufacture or delete an item solely to change the count.

## Inspect prose

1. Read the full text and establish its genre, purpose, audience, and intended voice.
2. Identify what already works and must survive revision.
3. Locate the four tells with exact excerpts or positions. Explain the effect of each pattern in context.
4. Look beneath the surface for the underlying default: vague claims, generic transitions, repeated cadence, unnecessary abstraction, missing audience knowledge, or polished language without a decision behind it.
5. Distinguish high-impact patterns from harmless isolated uses. State confidence and avoid an overall AI-authorship verdict.
6. Recommend the smallest changes that restore specificity, rhythm, voice, and audience fit.

When the user requests critique only, do not silently rewrite the complete text. A short example revision may clarify a finding, but label it as an example.

## Draft or rewrite prose

Before drafting, lock the facts, intended meaning, audience, purpose, format, and any supplied voice attributes. When a voice sample exists, infer repeatable qualities instead of copying phrases. Without a sample, use clear direct prose and avoid inventing personality.

Draft around real decisions:

- Lead with the point the reader needs, not a ceremonial opening.
- Prefer concrete nouns, active verbs, and specific consequences.
- Keep transitions only where the logical relationship needs help.
- Vary sentence and paragraph length according to emphasis.
- Use structure because the reader needs it, not because symmetry looks complete.
- Preserve uncertainty, qualifications, and factual boundaries from the source.

For a rewrite, compare the result with the source. Confirm that names, numbers, claims, quotations, commitments, and tone constraints survived. Do not introduce anecdotes, metrics, emotion, expertise, or certainty the user did not provide.

## Verify the final prose

Reread the final artifact itself and confirm:

- No em dash appears in generated or revised prose.
- Negative constructions express a necessary exclusion rather than a stock reveal.
- Paragraph and section shapes follow the ideas instead of a template.
- Lists contain the items the content requires rather than defaulting to three.
- The piece sounds consistent with the supplied voice evidence.
- The writing is specific enough for its audience and purpose.
- Facts and intended meaning remain intact.

Do not add a verbose audit after a short piece. Return the ready-to-use prose first and mention only material assumptions or preserved constraints.

## Optional scanner

When a long file is locally available, run `<installed-skill-directory>/scripts/prose_scan.py` as a candidate finder. Exact em-dash matches are deterministic. Negative contrasts, triads, and orderly transitions are only leads for human judgment. Inspect every reported excerpt in context and review the full final text even when the scanner reports no candidates.
