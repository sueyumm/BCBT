def choose_integral_rule(samples, smooth=True, singular=False):
    if samples < 2:
        raise ValueError("need at least two samples")
    if singular:
        return "adaptive"
    if samples % 2 == 1 and smooth:
        return "simpson"
    if samples > 20:
        return "composite-trapezoid"
    return "trapezoid"
