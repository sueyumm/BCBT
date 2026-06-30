import math


def nice_step(span, target_ticks=5):
    if span <= 0:
        raise ValueError("span must be positive")
    if target_ticks <= 0:
        raise ValueError("target tick count must be positive")
    raw = span / target_ticks
    exponent = math.floor(math.log10(raw))
    fraction = raw / (10 ** exponent)
    if fraction <= 1:
        nice = 1
    elif fraction <= 2:
        nice = 2
    elif fraction <= 5:
        nice = 5
    else:
        nice = 10
    return nice * (10 ** exponent)


def tick_values(vmin, vmax, target_ticks=5):
    if vmax < vmin:
        vmin, vmax = vmax, vmin
    if vmax == vmin:
        return [vmin]
    step = nice_step(vmax - vmin, target_ticks)
    start = math.floor(vmin / step) * step
    ticks = []
    value = start
    while value <= vmax + 0.5 * step:
        if value >= vmin - 0.5 * step:
            ticks.append(round(value, 12))
        value += step
    return ticks
