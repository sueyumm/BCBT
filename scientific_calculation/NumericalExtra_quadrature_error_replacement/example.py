# Adapted from arash79/Numerical-methods integration routines.


def quadrature_error_label(error_estimate, tolerance, order):
    if tolerance <= 0 or order <= 0:
        raise ValueError("invalid tolerance/order")
    scaled = abs(error_estimate) / tolerance
    if scaled <= 1:
        return "accepted"
    if order >= 4 and scaled <= 4:
        return "refine-once"
    if scaled <= 16:
        return "refine"
    return "reject"
