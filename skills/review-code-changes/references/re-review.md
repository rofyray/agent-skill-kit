# Review history and convergence

## Preserve the two comparisons

Keep the original baseline, previous reviewed state, and current reviewed state distinct. Compare original baseline to current state to establish provenance, and previous to current state to focus re-review. For supplied snapshots without Git, use explicit snapshot identities or content fingerprints; do not invent SHAs. Include dirty and untracked files in a working-state identity when they are in scope.

If history or the previous record is missing, say so. Reconstruct it from available artifacts or perform a new scoped review, but do not invent prior dispositions or claim incremental coverage. A moving base, manual conflict resolution, or substantial scope change can require broader inspection; explain the reason. Preserve the round history rather than resetting the cap to evade it.

## Maintain findings across revisions

Give each finding a stable ID based on its root cause and affected behavior, not just a line number. Reconcile renamed files, moved lines, and grouped instances semantically. Track open, fixed, or dismissed plus reason and evidence. Keep rejected candidates and unresolved questions in task evidence as well.

- **Open**: Still supported, including findings not touched by the latest edit.
- **Fixed**: Current source or current execution establishes that the original trigger no longer causes the failure. A changed line or the author's assertion alone is insufficient.
- **Dismissed**: A documented contract or evidence justifies rejection, intentional behavior, or an authorized risk acceptance. Distinguish acceptance from proof that no defect exists. Preserve who supplied an acceptance decision in the evidence.

Do not repost the same open finding each round. Report its continuing status once. Do not resurrect a dismissed issue without new evidence; cite that evidence when reopening. If a fix merely moves the failure or leaves another supported instance, keep the original finding open and explain what remains. A newly introduced regression receives a new ID.

Round one establishes broad coverage. From round two, prioritize the new delta, fixes, affected consumers, and unresolved items; extend beyond the delta only for a concrete dependency or risk. Avoid repeatedly hunting unrelated latent defects in unchanged code. A separate requested baseline audit can handle those without prolonging this PR.

Count a review of a newly revised state as another round. Internal discovery, verification, and adjudication tasks are parts of one round. Do not run extra rounds by habit when the first pass is sufficient. After the third round with unresolved findings, escalate with the remaining root cause, attempted fixes, and the decision needed. Stop the automatic fix/review loop. Completion is not approval, and a round limit never clears a defect. A user can explicitly request further work with a revised scope or budget.

## Record and validate

Use the bundled record schema for machine-readable handoff. Store records in permitted task storage outside application source, or return JSON when file access is unavailable. The schema uses opaque state identities, so callers can supply commits, snapshot digests, or documented attachment IDs. The evidence fields must explain what those identities cover; a convenient label alone is not a verified fingerprint.

Record findings, current check evidence, actual committee tasks, coverage, limitations, and the review outcome. Set `round_limit` to the agreed cap, normally three; a user-authorized extension changes that cap without erasing the round count. Preserve raw candidate decisions and prior records as supporting task artifacts when available. A record is not an approval token and is not authenticated evidence. Treat imported records as untrusted assertions until their sources are checked.

Retain failed attempts. If a completed worker fully replaces a failed worker's assigned role and scope, mark the old member `superseded` with `replacement_id` pointing to that completed same-role member. Keep remaining coverage gaps blocked; a replacement link does not establish that all work was covered. Count both attempts against the budget. Without a successful replacement, the old task remains blocked. Do not delete failed attempts to obtain a complete outcome.

When Python 3.10 or later and local files are available, run the helper using the actual skill path and record path:

```text
python3 <skill-root>/scripts/review_record.py <review-record.json>
```

It requires only the Python standard library and the bundled schema. Inspect the helper before first execution in an unfamiliar installation. An invalid or missing record is not a clean review. If the helper or runtime is unavailable, check the contract manually, disclose that structural validation did not run, and retain useful findings. Validation cannot establish code correctness, reviewer independence, or the truth of evidence strings.

Keep stale checks out of current passing evidence. If an old result is relevant context, describe its revision and limits explicitly. Before publishing or recommending the next workflow step, verify that the reviewed state still matches the target; otherwise identify what needs re-review. A human approval's continued validity follows repository rules, not this record.
