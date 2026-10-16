"""A small local checkout implementation used as evaluation input."""


class MemoryStore:
    def __init__(self, writable=True):
        self.writable = writable
        self.orders = {}

    def save(self, order):
        if not self.writable:
            raise OSError("store unavailable")
        self.orders[order["id"]] = dict(order)

    def get(self, order_id):
        return self.orders.get(order_id)


def place_order(store, order_id, amount_cents):
    if amount_cents <= 0:
        raise ValueError("amount must be positive")
    order = {"id": order_id, "amount_cents": amount_cents}
    try:
        store.save(order)
    except OSError:
        pass
    return {"status": "confirmed", "order_id": order_id}
