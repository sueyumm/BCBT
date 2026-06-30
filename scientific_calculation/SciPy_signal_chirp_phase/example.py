import math


def chirp_phase(t, f0, f1, t1, method="linear"):
    if t1 == 0:
        raise ValueError("t1 cannot be zero")
    if method == "linear":
        beta = (f1 - f0) / t1
        return 2 * math.pi * (f0 * t + 0.5 * beta * t ** 2)
    if method == "quadratic":
        beta = (f1 - f0) / (t1 ** 2)
        return 2 * math.pi * (f0 * t + beta * t ** 3 / 3.0)
    if method == "logarithmic":
        if f0 <= 0 or f1 <= 0:
            raise ValueError("logarithmic chirp frequencies must be positive")
        beta = math.log(f1 / f0) / t1
        return 2 * math.pi * f0 * (math.exp(beta * t) - 1.0) / beta
    raise ValueError("unknown chirp method")


def chirp_direction(f0, f1):
    if f1 > f0:
        return "up"
    if f1 < f0:
        return "down"
    return "constant"
