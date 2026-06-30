# Adapted from TheAlgorithms/Python linear algebra utilities.


def projection_status(dot_ab, norm_b_squared, tolerance=1e-12):
    if tolerance <= 0:
        raise ValueError("invalid tolerance")
    if norm_b_squared < 0:
        raise ValueError("negative norm")
    if norm_b_squared <= tolerance:
        return "zero-target"
    scale = dot_ab / norm_b_squared
    if abs(scale) <= tolerance:
        return "orthogonal"
    if scale > 0:
        return "same-direction"
    return "opposite-direction"
