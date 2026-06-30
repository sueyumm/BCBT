import numpy as np


def classify_diffusion_tensor(tensor):
    a = np.asarray(tensor, dtype=float)
    if a.shape == ():
        return "scalar-positive" if float(a) > 0 else "scalar-nonpositive"
    if a.shape != (2, 2):
        raise ValueError("expected scalar or 2x2 tensor")
    eig = np.linalg.eigvalsh(a)
    if np.all(eig > 0):
        return "positive-definite"
    if np.any(eig < 0):
        return "indefinite"
    return "semidefinite"
