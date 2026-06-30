def classify_boundary(point, nx, ny, boundary_value=0.0):
    x, y = point
    if nx < 2 or ny < 2:
        raise ValueError("grid must have at least two nodes per axis")
    on_left = x == 0
    on_right = x == nx - 1
    on_bottom = y == 0
    on_top = y == ny - 1
    count = sum([on_left, on_right, on_bottom, on_top])
    if count == 0:
        return "interior"
    if count >= 2:
        return "corner-nonzero" if boundary_value != 0 else "corner-zero"
    if on_left or on_right:
        return "vertical-edge"
    return "horizontal-edge"
def boundary_mask_type(mask):
    import numpy as np

    m = np.asarray(mask, dtype=bool)
    if m.ndim != 2 or min(m.shape) < 3:
        raise ValueError("mask must be a two-dimensional grid")
    boundary = np.zeros_like(m)
    boundary[0, :] = True
    boundary[-1, :] = True
    boundary[:, 0] = True
    boundary[:, -1] = True
    selected_boundary = m & boundary
    selected_interior = m & ~boundary
    if not np.any(m):
        return "empty"
    if np.any(selected_interior) and np.any(selected_boundary):
        return "mixed"
    if np.any(selected_interior):
        return "interior-only"
    return "boundary-only"
