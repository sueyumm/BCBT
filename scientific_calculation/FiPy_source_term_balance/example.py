import numpy as np


def source_balance(source, sink, volume):
    source = np.asarray(source, dtype=float)
    sink = np.asarray(sink, dtype=float)
    if source.shape != sink.shape:
        raise ValueError("source and sink must have the same shape")
    if volume <= 0:
        raise ValueError("volume must be positive")
    return float((source - sink).sum() * volume)


def classify_balance(balance, tolerance=1e-10):
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    if balance > tolerance:
        return "source_dominated"
    if balance < -tolerance:
        return "sink_dominated"
    return "balanced"
