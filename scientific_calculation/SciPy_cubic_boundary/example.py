def validate_boundary_condition(bc_type, y_shape):
    if len(y_shape) == 0:
        raise ValueError("y_shape cannot be empty")
    if bc_type == "not-a-knot":
        if y_shape[0] < 4:
            return "fallback-parabolic"
        return "not-a-knot"
    if bc_type == "periodic":
        if y_shape[0] < 2:
            raise ValueError("periodic data requires at least two points")
        return "periodic"
    if bc_type in {"clamped", "natural"}:
        return bc_type
    raise ValueError("unknown boundary condition")


def derivative_order(order):
    if order < 0:
        raise ValueError("order must be non-negative")
    if order == 0:
        return "value"
    if order == 1:
        return "slope"
    if order == 2:
        return "curvature"
    return "higher"
