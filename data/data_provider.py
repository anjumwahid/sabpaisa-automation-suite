import json, os

_DATA_DIR = os.path.dirname(__file__)

def _load(filename):
    with open(os.path.join(_DATA_DIR, filename), "r") as f:
        return json.load(f)

def get_checkout_data():
    return _load("checkout_data.json")

def get_customer_data():
    return get_checkout_data()["customer"]

def get_payment_data():
    return get_checkout_data()["payment"]

def get_card_data():
    return get_checkout_data()["card"]

def get_upi_data():
    return get_checkout_data()["upi"]


# ── Negative Test Data ──

def get_negative_data():
    return _load("negative_data.json")

def get_invalid_merchant():
    return get_negative_data()["invalid_merchant"]

def get_empty_merchant():
    return get_negative_data()["empty_merchant"]

def get_special_char_merchant():
    return get_negative_data()["special_char_merchant"]

def get_empty_customer_fields():
    return get_negative_data()["empty_customer_fields"]

def get_invalid_email_data():
    return get_negative_data()["invalid_email"]

def get_invalid_phone_data():
    return get_negative_data()["invalid_phone"]

def get_zero_amount_data():
    return get_negative_data()["zero_amount"]

def get_negative_amount_data():
    return get_negative_data()["negative_amount"]

def get_large_amount_data():
    return get_negative_data()["very_large_amount"]

def get_non_existent_bank():
    return get_negative_data()["non_existent_bank"]
