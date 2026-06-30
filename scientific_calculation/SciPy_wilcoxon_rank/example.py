import numpy as np


def signed_rank_statistic(differences, zero_method="wilcox"):
    diff = np.asarray(differences, dtype=float)
    if zero_method == "wilcox":
        diff = diff[diff != 0]
    elif zero_method != "pratt":
        raise ValueError("unknown zero method")
    if diff.size == 0:
        return 0.0
    order = np.argsort(np.abs(diff))
    ranks = np.empty(diff.size, dtype=float)
    for rank, index in enumerate(order, start=1):
        ranks[index] = rank
    return float(ranks[diff > 0].sum())


def alternative_tail(statistic, midpoint, alternative="two-sided"):
    if alternative == "greater":
        return statistic > midpoint
    if alternative == "less":
        return statistic < midpoint
    if alternative == "two-sided":
        return abs(statistic - midpoint)
    raise ValueError("unknown alternative")
