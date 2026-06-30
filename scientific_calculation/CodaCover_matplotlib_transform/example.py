import numpy as np


def affine_transform(points, matrix, offset=None):
    pts = np.asarray(points, dtype=float)
    mat = np.asarray(matrix, dtype=float)
    if pts.ndim != 2:
        raise ValueError("points must be two-dimensional")
    if mat.shape != (pts.shape[1], pts.shape[1]):
        raise ValueError("matrix shape does not match point dimension")
    out = pts @ mat.T
    if offset is not None:
        off = np.asarray(offset, dtype=float)
        if off.shape != (pts.shape[1],):
            raise ValueError("offset shape does not match point dimension")
        out = out + off
    return out


def transform_type(matrix):
    mat = np.asarray(matrix, dtype=float)
    if mat.shape[0] != mat.shape[1]:
        raise ValueError("matrix must be square")
    det = float(np.linalg.det(mat))
    if np.isclose(det, 0.0):
        return "singular"
    if det < 0:
        return "orientation-reversing"
    return "orientation-preserving"
