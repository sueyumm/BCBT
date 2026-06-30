import numpy as np


def upwind_face_values(cell_values, velocity):
    values = np.asarray(cell_values, dtype=float)
    if values.ndim != 1:
        raise ValueError("cell_values must be one-dimensional")
    if len(values) < 2:
        return values.copy()
    faces = np.empty(len(values) + 1, dtype=float)
    faces[0] = values[0]
    faces[-1] = values[-1]
    if velocity >= 0:
        faces[1:-1] = values[:-1]
    else:
        faces[1:-1] = values[1:]
    return faces


def convection_residual(cell_values, velocity, dx):
    if dx <= 0:
        raise ValueError("dx must be positive")
    faces = upwind_face_values(cell_values, velocity)
    flux = velocity * faces
    return -(flux[1:] - flux[:-1]) / dx
