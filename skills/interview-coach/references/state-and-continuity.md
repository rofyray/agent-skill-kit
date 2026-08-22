# State and Continuity

Use this reference only when persistent continuity exists or the user asks to create, migrate, export, validate, or update coaching state.

## Capability and consent gate

Before writing state:

1. Confirm the exact workspace folder or connected storage target.
2. Explain that resumes, interview transcripts, feedback, contact details, and compensation can be sensitive.
3. Ask whether the user wants durable state and which categories may be stored. Default to summaries and evidence locators rather than unnecessary verbatim copies.
4. Keep writes inside the approved workspace. Prefer a folder-scoped capability over a connector with broader filesystem access.
5. Never store credentials, authentication cookies, private connector tokens, protected-trait inferences, or third-party personal data that is not needed for coaching.

State creation is optional. An urgent coaching request must still work without it.

## Workspace contract

Use one candidate-selected workspace:

```text
<workspace>/
├── coaching_state.md
├── coaching_state.storybank.md
├── coaching_state.loops.md
├── coaching_state.history.md
└── materials/
    └── <company>/
```

Keep the four state files private by default. If the workspace is a Git repository, offer to add `coaching_state*.md` and candidate-specific `materials/` to `.gitignore`; do not modify ignore rules without approval.

### `coaching_state.md`: always-load core

Keep this file compact enough to read in full at every session start.

```markdown
# Interview Coaching State — [Candidate]

Last updated: YYYY-MM-DD

## Current Truth
- Profile: [one-line candidate summary]
- Positioning spine: [current differentiating throughline]
- Conversion thesis: [what evidence currently says helps or hurts]
- Primary bottleneck: [latest synthesis]
- Secondary bottleneck: [latest synthesis or none]
- Calibration tendency: [accurate / over-rates / under-rates / unknown]
- Target filters: [role, level, domain, location, constraints]
- Live pipeline: [one line per active loop]
- Open corrections — do not relapse: [confirmed corrections]

## Profile
- Target roles and level:
- Location and work authorization, if volunteered and relevant:
- Timeline:
- Background and strengths:
- Constraints:
- Career-transition context:

## Active Coaching Strategy
- Directness: [1-5]
- Current focus:
- Next drill stage:
- Immediate recommendation:

## Coaching Preferences
- Helpful formats:
- Friction or anxiety patterns volunteered by candidate:
- Accessibility or pacing needs volunteered by candidate:

## State Files
- Storybank: coaching_state.storybank.md
- Loops and materials: coaching_state.loops.md
- Scores, outcomes, intelligence, and sessions: coaching_state.history.md
```

`Current Truth` wins when a lower historical entry conflicts. Update it in the same transaction whenever a confirmed correction, new target, outcome pattern, or strategy change lands. Do not let it become an append-only log.

### `coaching_state.storybank.md`: load for stories and delivery

```markdown
# Interview Coaching Storybank

## Story Index
| ID | Title | Competencies | Strength | Last used | Evidence status |

## Story Details
### S001 — [Title]
- Situation:
- Task:
- Actions:
- Result:
- Candidate contribution and scope:
- Evidence and metrics:
- Earned secret:
- Competencies:
- Risks or unverifiable claims:
- Versions: [30s / 60s / 90s / full]
```

Use stable story IDs. Never create facts to complete STAR. Mark missing evidence as a gap.

### `coaching_state.loops.md`: load for company and role work

```markdown
# Interview Coaching Loops

## Active Loops
### [Company] — [Role]
- Status and next date:
- Role source and captured date:
- Fit verdict and confidence:
- Interview format and round:
- Interviewers and verified evidence:
- Known evaluation signals:
- Likely concerns:
- Story mapping:
- Material paths:
- Open questions:

## Past Loops
| Company | Role | Outcome | Closed | Durable lesson |

## Materials Index
| Company | Artifact | Path | Updated |
```

Compress closed loops into `Past Loops` only after preserving durable lessons in history and the storybank. Do not delete source materials without approval.

### `coaching_state.history.md`: load for learning and trends

```markdown
# Interview Coaching History

## Score History
| Date | Company/role | Format | Evidence | Substance | Structure | Relevance | Credibility | Differentiation | Confidence |

## Outcome Log
| Date | Company/role | Stage | Outcome | Evidence | Notes |

## Interview Intelligence
### Effective Patterns
### Ineffective Patterns
### Question Bank
### Company-Specific Evidence

## Feedback Log
| Date | Source | Provenance | Feedback | Interpretation | State changes |

## Session Log
| Date | Operations | Durable changes | Recommended next |

## Meta-Check Log
| Date | Candidate feedback | Coaching adjustment |
```

Use provenance values such as `transcript`, `written feedback`, `candidate paraphrase`, `candidate memory`, or `coach inference`. Never mix memory-only impressions into numeric score history.

## Initialize and locate

When the user approves state creation and Python is available, resolve the skill's installed directory through the active host and run:

```bash
python3 <installed-skill-directory>/scripts/coach_state.py init <workspace> --name "<candidate>"
python3 <installed-skill-directory>/scripts/coach_state.py validate <workspace>
```

Pass `--target-role`, `--timeline`, and `--directness` when known. Preview the resolved path before execution. The helper creates missing files but preserves existing ones.

At session start, resolve state in this order:

1. Explicit path named by the user.
2. Workspace already connected to the session.
3. Current project directory when it contains `coaching_state.md`.
4. Ask for the folder or uploaded bundle.

Do not search broad home directories for private state merely for convenience.

## Load by operation

- Always: core file in full.
- `stories`, `prep`, `practice`, `mock`, `present`, `resume`, `pitch`, `apply`: storybank.
- `research`, `decode`, `prep`, `questions`, `concerns`, `thankyou`, `salary`, `negotiate`, company-specific materials: loops.
- `debrief`, `analyze`, `round`, `feedback`, `progress`, `reflect`, calibration or aggregate claims: history.
- Load more than one sibling only when cross-file evidence changes the result.

## Write with Scan → Tag → Update → Verify

1. **Scan**: read every relevant destination before editing. Note its last-updated value and locate the affected stable IDs or headings.
2. **Tag**: assign each new fact to all required destinations before writing. Candidate-wide facts go to core; stories to storybank; company-specific details to loops; scores, outcomes, feedback, and longitudinal intelligence to history.
3. **Update**: make one coherent write per affected file. Use a temporary file and atomic replace when supported. Preserve unrelated user content and do not append a second contradictory truth.
4. **Verify**: reread changed sections, confirm row/ID counts and cross-file pointers, run `coach_state.py validate`, and report any incomplete destination.

If a save fails halfway, stop. Do not claim success. Preserve the last good files, identify which destinations changed, and provide a recovery plan.

### Global-learning rule

After every substantial interaction, ask internally: “Did this reveal something candidate-wide?” Examples include location, role preference, leadership scope, a new accomplishment, a rejected framing, delivery preference, interview pattern, or evidence that changes the conversion thesis. If yes, update core or storybank as well as the local loop. If uncertain, propose the update rather than silently promoting it to truth.

## Migrate a legacy monolith

When a single large `coaching_state.md` contains story details, many job descriptions, loops, and history:

1. Validate that no sibling files already contain divergent state.
2. Run `python3 <installed-skill-directory>/scripts/coach_state.py migration-plan <workspace>` to capture the source hash, exact section hashes, proposed destinations, duplicate headings, and sections requiring manual review.
3. Show the planned section routing and request approval for the migration write.
4. Create a timestamped backup beside the source and verify its hash matches the plan.
5. Split on the manifest's complete Markdown heading boundaries; never truncate by byte ranges. Preserve the original preamble and every original section block exactly during the split. Add required wrapper sections around those blocks rather than rewriting them in place.
6. Build a concise `Current Truth` from confirmed profile, active strategy, current pipeline, and explicit corrections. Chronology alone does not prove which conflicting entry is current; ask the user when confirmation is ambiguous. When replacing an old Current Truth, retain its exact original block in history until migration verification succeeds.
7. Write storybank, loops, and history siblings; leave pointers in the core.
8. Run `python3 <installed-skill-directory>/scripts/coach_state.py verify-migration <workspace> --backup <backup-file> --expected-source-sha256 <hash-from-plan>`. Do not claim a lossless migration unless it verifies the backup hash, preamble, every original section block, stable story IDs, and the final schema.
9. After verification, apply confirmed Current Truth corrections as a normal Scan → Tag → Update → Verify transaction. Keep the backup until the user confirms the result.

Do not auto-migrate merely because a file is large. Read-discipline and a current authoritative head are required even after splitting.

## Archive without losing learning

- Keep recent score and session rows directly readable; summarize older rows only after preserving counts, ranges, recurring evidence, and material exceptions.
- Move closed loops to the past table and retain any reusable question, outcome, story, or pattern in history.
- Mark stale external facts with their captured date; do not silently treat them as current.
- Never delete source resumes, transcripts, offer documents, state, or materials without explicit approval.

## Web and no-file fallback

Uploads are snapshots. To continue in another session, request the complete core plus every sibling needed for the operation, not a random subset. Return a replacement bundle or explicit per-file change set and warn against merging stale copies blindly. Prefer an approved connected repository or storage location when the host can maintain it consistently.
