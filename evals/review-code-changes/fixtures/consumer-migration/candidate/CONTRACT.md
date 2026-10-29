# Catalog contract

Catalog entries have integer amounts in cents. checkout.total(skus) returns the exact sum for the supplied known SKUs. A typed catalog return value is allowed provided all existing consumers are migrated. Unknown SKUs raise KeyError. This local fixture uses no external services or packages.
