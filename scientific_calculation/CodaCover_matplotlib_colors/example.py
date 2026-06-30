import numpy as np


def normalize_rgb(color):
    arr = np.asarray(color, dtype=float)
    if arr.shape != (3,):
        raise ValueError("RGB color must contain exactly three channels")
    if np.any(arr < 0):
        raise ValueError("RGB channels must be non-negative")
    if np.any(arr > 1.0):
        if np.any(arr > 255):
            raise ValueError("8-bit RGB channels cannot exceed 255")
        arr = arr / 255.0
    return arr


def luminance(color):
    rgb = normalize_rgb(color)
    lum = float(np.dot(rgb, [0.2126, 0.7152, 0.0722]))
    if lum < 0.25:
        return "dark"
    if lum > 0.75:
        return "light"
    return "medium"
