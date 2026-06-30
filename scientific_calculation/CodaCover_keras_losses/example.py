import numpy as np


def regression_loss(y_true, y_pred, loss="mse", delta=1.0):
    true = np.asarray(y_true, dtype=float)
    pred = np.asarray(y_pred, dtype=float)
    if true.shape != pred.shape:
        raise ValueError("inputs must have the same shape")
    error = pred - true
    if loss == "mse":
        return float(np.mean(error ** 2))
    if loss == "mae":
        return float(np.mean(np.abs(error)))
    if loss == "huber":
        if delta <= 0:
            raise ValueError("delta must be positive")
        abs_error = np.abs(error)
        quad = np.minimum(abs_error, delta)
        lin = abs_error - quad
        return float(np.mean(0.5 * quad ** 2 + delta * lin))
    raise ValueError("unknown loss")


def loss_quality(value, tolerance):
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    return "acceptable" if value <= tolerance else "large"
