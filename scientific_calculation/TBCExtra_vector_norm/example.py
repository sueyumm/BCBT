import math


def norm_category(values, ord=2):
    if not values:
        return "zero"
    if ord == 1:
        norm = sum(abs(v) for v in values)
    elif ord == 2:
        norm = math.sqrt(sum(v * v for v in values))
    elif ord == float("inf"):
        norm = max(abs(v) for v in values)
    else:
        raise ValueError("unsupported norm")
    if norm == 0:
        return "zero"
    if norm < 1:
        return "small"
    if norm < 10:
        return "medium"
    return "large"
