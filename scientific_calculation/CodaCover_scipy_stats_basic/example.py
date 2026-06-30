import math


def trimmed_mean(values, proportion):
    data = sorted(float(v) for v in values)
    if not 0 <= proportion < 0.5:
        raise ValueError("proportion must be in [0, 0.5)")
    if not data:
        raise ValueError("values cannot be empty")
    cut = int(len(data) * proportion)
    if cut:
        data = data[cut:-cut]
    return sum(data) / len(data)


def kendall_pair_count(x, y):
    if len(x) != len(y):
        raise ValueError("inputs must have equal length")
    concordant = 0
    discordant = 0
    for i in range(len(x)):
        for j in range(i + 1, len(x)):
            sign = (x[i] - x[j]) * (y[i] - y[j])
            if sign > 0:
                concordant += 1
            elif sign < 0:
                discordant += 1
    total = concordant + discordant
    if total == 0:
        return math.nan
    return (concordant - discordant) / total
