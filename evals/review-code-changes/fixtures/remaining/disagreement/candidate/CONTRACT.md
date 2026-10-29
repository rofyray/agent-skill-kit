# Billing wire contract

During a rolling deploy, the previous reader remains active for 24 hours.
Every new writer must emit records that this reader can parse. Existing
integer cent values must be preserved exactly. Additional optional fields
are allowed; removing the amount_cents field requires a coordinated rollout
that this change does not authorize. There are no external dependencies.
