import unittest
from unittest.mock import Mock

from orders import MemoryStore, place_order


class CheckoutTests(unittest.TestCase):
    def test_checkout_receipt(self):
        store = Mock()
        receipt = place_order(store, "order-1", 1250)
        self.assertEqual(receipt, {"status": "confirmed", "order_id": "order-1"})
        store.save.assert_called_once_with({"id": "order-1", "amount_cents": 1250})

    def test_rejects_zero(self):
        store = MemoryStore()
        with self.assertRaises(ValueError):
            place_order(store, "order-2", 0)
        self.assertIsNone(store.get("order-2"))


if __name__ == "__main__":
    unittest.main()
