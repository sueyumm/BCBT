def underrelax(old, new, factor):
    if factor <= 0:
        return old
    if factor >= 1:
        return new
    mixed = old + factor * (new - old)
    if abs(mixed - old) < 1e-14:
        return old
    return mixed
