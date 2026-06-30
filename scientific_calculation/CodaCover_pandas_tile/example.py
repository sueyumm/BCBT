import numpy as np


def assign_bins(values, bins, right=True):
    vals = np.asarray(values, dtype=float)
    edges = np.asarray(bins, dtype=float)
    if edges.ndim != 1 or edges.size < 2:
        raise ValueError("bins must contain at least two edges")
    if np.any(np.diff(edges) <= 0):
        raise ValueError("bins must be strictly increasing")
    side = "left" if right else "right"
    labels = np.searchsorted(edges, vals, side=side) - 1
    labels[(vals < edges[0]) | (vals > edges[-1])] = -1
    if right:
        labels[vals == edges[0]] = 0
    else:
        labels[vals == edges[-1]] = edges.size - 2
    return labels


def quantile_edges(values, q):
    vals = np.asarray(values, dtype=float)
    if vals.size == 0:
        raise ValueError("values cannot be empty")
    if q <= 0:
        raise ValueError("q must be positive")
    probs = np.linspace(0.0, 1.0, q + 1)
    edges = np.quantile(vals, probs)
    if np.unique(edges).size != edges.size:
        raise ValueError("quantile edges are not unique")
    return edges
