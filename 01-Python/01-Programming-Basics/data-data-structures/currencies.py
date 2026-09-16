# pylint: disable=missing-docstring

# 1. قاموس أسعار الصرف بالقيم المحددة في التحدي
RATES = {
    "USDEUR": 0.85,
    "GBPEUR": 1.13,
    "CHFEUR": 0.86,
    "EURGBP": 0.885,
}


def convert(amount, currency):
    """
    amount: tuple contains (value, initial_currency) e.g. (100, "USD")
    currency: target currency string e.g. "EUR"
    """
    value, from_curr = amount


    if from_curr == currency:
        return round(value)


    pair_key = from_curr + currency


    if pair_key not in RATES:
        return None


    converted_value = value * RATES[pair_key]
    return round(converted_value)
