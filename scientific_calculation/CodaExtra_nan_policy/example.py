import math


def reduce_with_nan_policy(values, policy="propagate"):
    has_nan = any(math.isnan(v) for v in values)
    if has_nan and policy == "raise":
        raise ValueError("nan present")
    if has_nan and policy == "omit":
        values = [v for v in values if not math.isnan(v)]
    if not values or (has_nan and policy == "propagate"):
        return math.nan
    if policy not in {"raise", "omit", "propagate"}:
        raise ValueError("bad policy")
    return sum(values) / len(values)
