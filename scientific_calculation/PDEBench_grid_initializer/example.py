import numpy as np


def make_uniform_grid(nx, ny, length_x=1.0, length_y=1.0, include_endpoint=True):
    if nx <= 0 or ny <= 0:
        raise ValueError("grid dimensions must be positive")
    if length_x <= 0 or length_y <= 0:
        raise ValueError("domain lengths must be positive")
    x = np.linspace(0.0, length_x, nx, endpoint=include_endpoint)
    y = np.linspace(0.0, length_y, ny, endpoint=include_endpoint)
    return np.meshgrid(x, y, indexing="ij")


def gaussian_initial_condition(x, y, center=(0.5, 0.5), width=0.1):
    if width <= 0:
        raise ValueError("width must be positive")
    cx, cy = center
    radius2 = (x - cx) ** 2 + (y - cy) ** 2
    values = np.exp(-radius2 / (2.0 * width * width))
    if values.ndim != 2:
        raise ValueError("grid must be two-dimensional")
    return values


def normalize_field(field):
    field = np.asarray(field, dtype=float)
    fmin = float(np.min(field))
    fmax = float(np.max(field))
    if fmax == fmin:
        return np.zeros_like(field)
    return (field - fmin) / (fmax - fmin)
