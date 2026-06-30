def choose_quadrature(poly_order, curved=False, nonlinear=False):
    if poly_order < 0:
        raise ValueError("negative order")
    order = poly_order + 1
    if curved:
        order += 1
    if nonlinear:
        order *= 2
    if order <= 2:
        return "low"
    if order <= 5:
        return "medium"
    return "high"
