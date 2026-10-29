# Cached quote contract

A quote may remain cached until its 30-second TTL expires. Values before
expiry are intentionally allowed to differ from storage. At exactly expiry,
refresh from storage. Inputs are valid integer timestamps. Renaming local
variables must not change observable behavior.
