def summarize_cents(amounts):
    return sum(amount - amount % 100 for amount in amounts)
