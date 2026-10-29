# Repository review policy

Adapt this template to established owner decisions and remove inapplicable guidance. This file guides the reviewer; repository controls enforce approvals and merging. Record which trusted revision supplies this policy.

## What failure means here

Describe the concrete behaviors and contracts the repository must preserve, including configuration routing or documentation accuracy where applicable. Name important trust, persistence, compatibility, and recovery boundaries. Refer to authoritative specifications and existing checks.

## Evidence and severity

Require a reachable trigger, precise source location, consequence, and evidence for each defect. Distinguish static reasoning from executed checks and current evidence from old logs. Keep severity separate from introduced or pre-existing provenance. Report verification gaps separately from confirmed defects. Omit style preferences unless a stated policy makes them relevant.

## Scope and ownership

List any justified exclusions and their coverage limitations. Identify sensitive paths and actual human approval requirements. Do not infer that an author is trusted or count an agent as a required human. Changes to this policy do not weaken the review of the same change.

## Review effort and resolution

Use Standard depth unless semantic risk or an explicit request calls for Quick or Deep. Start with complementary independent discovery and reserve capacity for separate validation. Expand for named coverage gaps within the agreed task budget. Report incomplete coverage rather than treating an unavailable reviewer as clean.

Preserve finding identities and evidence across revisions. Verify fixes against the current state, avoid duplicate comments, and escalate unresolved work after the agreed round cap. Record reasons for dismissals and risk acceptance. Do not interpret an empty finding list as merge approval.

## Verification and recovery

Document the appropriate test environments and checks, their limits, and the evidence needed for the reviewed revision. Identify how to undo consequential changes and where an apparent rollback would not restore data. Keep deployment and publication authority separate from review.
