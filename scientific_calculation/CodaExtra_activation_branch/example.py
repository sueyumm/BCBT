import math


def activation(x, kind="relu", alpha=0.01):
    if kind == "relu":
        return x if x > 0 else 0
    if kind == "leaky_relu":
        return x if x > 0 else alpha * x
    if kind == "sigmoid":
        if x >= 0:
            return 1 / (1 + math.exp(-x))
        ex = math.exp(x)
        return ex / (1 + ex)
    raise ValueError("unknown activation")
