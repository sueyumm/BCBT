# Adapted from TheAlgorithms/Python numerical-analysis bisection routines.


def bisection_interval_status(f_left, f_mid, f_right, width, tolerance):
    if width < 0 or tolerance <= 0:
        raise ValueError("invalid width/tolerance")
    if f_mid == 0:
        return "root-found"
    if width <= tolerance:
        return "converged-width"
    if f_left * f_right > 0:
        return "not-bracketed"
    if f_left * f_mid < 0:
        return "keep-left"
    if f_mid * f_right < 0:
        return "keep-right"
    return "ambiguous"
