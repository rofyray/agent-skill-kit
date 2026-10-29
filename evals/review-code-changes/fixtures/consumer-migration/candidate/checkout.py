from catalog import price_for


def total(skus):
    return sum(price_for(sku)["amount_cents"] for sku in skus)
