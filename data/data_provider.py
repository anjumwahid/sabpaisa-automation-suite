import json, os

_DATA_DIR = os.path.dirname(__file__)


def _load(filename):
    with open(os.path.join(_DATA_DIR, filename), "r") as f:
        return json.load(f)


def get_checkout_data():
    data = _load("checkout_data.json")
    # Env var override (for parallel batch runs)
    override = os.environ.get("MERCHANT_ID_OVERRIDE")
    if override:
        data["merchant_id"] = override
    return data


def get_customer_data():
    return get_checkout_data()["customer"]


def get_payment_data():
    return get_checkout_data()["payment"]


def get_card_data():
    return get_checkout_data()["card"]


def get_upi_data():
    return get_checkout_data()["upi"]
