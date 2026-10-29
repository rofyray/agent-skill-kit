# Review instructions

Review changed behavior against CONTRACT.md. Tenant isolation and stale data
past the TTL are material defects. Trace the service, cache, and repository
together before concluding that a boundary is protected. Keep unchanged
legacy defects distinct from regressions. Use file locations and a concrete
trigger for findings. Do not request style changes or treat passing tests as
proof that every contract holds.
