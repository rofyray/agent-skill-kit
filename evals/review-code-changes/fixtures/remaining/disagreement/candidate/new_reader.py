import json


def read_amount(payload):
    return json.loads(payload)["amount_minor"]
