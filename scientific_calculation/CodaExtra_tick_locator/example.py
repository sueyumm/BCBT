def tick_step(span, target_ticks):
    if span <= 0 or target_ticks <= 0:
        raise ValueError("invalid axis")
    raw = span / target_ticks
    if raw <= 1:
        return 1
    if raw <= 2:
        return 2
    if raw <= 5:
        return 5
    return 10
