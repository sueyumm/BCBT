def ceil_div(numerator, denominator):
    if denominator == 0:
        raise ZeroDivisionError("denominator cannot be zero")
    quotient, remainder = divmod(numerator, denominator)
    if remainder == 0:
        return quotient
    if denominator > 0:
        return quotient + 1
    return quotient


def split_evenly(total, parts):
    if parts <= 0:
        raise ValueError("parts must be positive")
    base = total // parts
    extra = total % parts
    result = []
    for index in range(parts):
        if index < extra:
            result.append(base + 1)
        else:
            result.append(base)
    return result
