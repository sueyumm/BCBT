def apply_constraint(value, lower=None, upper=None, mask=False):
    if mask:
        return value
    result = value
    if lower is not None and result < lower:
        result = lower
    if upper is not None and result > upper:
        result = upper
    if lower is not None and upper is not None and lower > upper:
        raise ValueError("lower greater than upper")
    return result
