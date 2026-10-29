import json


def encode_amount(amount):
    return json.dumps({"amount_cents": amount})
