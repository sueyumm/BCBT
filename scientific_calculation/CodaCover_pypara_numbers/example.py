from decimal import Decimal, ROUND_HALF_UP


def make_quantizer(places):
    if places < 0:
        raise ValueError("decimal places must be non-negative")
    return Decimal("1").scaleb(-places)


def quantize_decimal(value, places=2):
    quantizer = make_quantizer(places)
    amount = Decimal(str(value))
    return amount.quantize(quantizer, rounding=ROUND_HALF_UP)


def optional_sum(values, start=Decimal("0")):
    total = Decimal(start)
    seen = False
    for value in values:
        if value is None:
            continue
        total += Decimal(str(value))
        seen = True
    if not seen:
        return None
    return total
