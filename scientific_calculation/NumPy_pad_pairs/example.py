import numpy as np


def as_pad_pairs(pad_width, ndim):
    if ndim < 0:
        raise ValueError("ndim must be non-negative")
    arr = np.asarray(pad_width, dtype=int)
    if arr.ndim == 0:
        if arr < 0:
            raise ValueError("pad width must be non-negative")
        return [(int(arr), int(arr)) for _ in range(ndim)]
    if arr.shape == (2,):
        if np.any(arr < 0):
            raise ValueError("pad width must be non-negative")
        return [tuple(map(int, arr)) for _ in range(ndim)]
    if arr.shape == (ndim, 2):
        if np.any(arr < 0):
            raise ValueError("pad width must be non-negative")
        return [tuple(map(int, row)) for row in arr]
    raise ValueError("invalid pad width shape")


def padding_mode(mode):
    if mode in {"constant", "edge"}:
        return "simple"
    if mode in {"reflect", "symmetric", "wrap"}:
        return "data-dependent"
    raise ValueError("unsupported padding mode")
