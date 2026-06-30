def finite_difference_step(x, rel_step=None, abs_step=None):
    if abs_step is not None:
        if abs_step <= 0:
            raise ValueError("absolute step must be positive")
        return abs_step
    if rel_step is None:
        rel_step = 1e-6
    if rel_step <= 0:
        raise ValueError("relative step must be positive")
    return rel_step * max(1.0, abs(x))


def derivative_status(error_estimate, tolerance):
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    if error_estimate is None:
        return "unknown"
    if error_estimate <= tolerance:
        return "accurate"
    if error_estimate <= 10 * tolerance:
        return "rough"
    return "poor"
