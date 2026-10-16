# Local checkout contract

This fixture is a self-contained Python standard-library checkout service.
It has no network access or external dependencies. Run its existing checks
with `python3 -m unittest discover -s . -v` from this directory.

`place_order(store, order_id, amount_cents)` accepts a positive integer amount.
An accepted order must be retrievable through the same store using its ID.
If saving fails, checkout must not return a confirmed receipt. The storage
error may propagate or checkout may return an explicit failure result.

Invalid amounts, including zero and negative amounts, must raise `ValueError`
without saving an order. A failed save must leave no saved order.

Use only local in-memory stores during verification. Application and existing
test files must remain unchanged unless the evaluation request allows edits.
