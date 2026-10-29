PRICES = {"pen": 150, "book": 900}


def price_for(sku):
    return {"amount_cents": PRICES[sku]}
