from dataclasses import dataclass


@dataclass(frozen=True)
class Price:
    amount_cents: int


PRICES = {"pen": 150, "book": 900}


def price_for(sku):
    return Price(PRICES[sku])
