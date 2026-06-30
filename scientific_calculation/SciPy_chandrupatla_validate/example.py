def validate_bracket(x1, x2, f1, f2):
    if x1 == x2:
        raise ValueError("bracket endpoints must differ")
    if f1 == 0:
        return "left-root"
    if f2 == 0:
        return "right-root"
    if f1 * f2 > 0:
        raise ValueError("bracket does not change sign")
    return "valid"


def next_bracket(x1, x2, f1, f2, x_new, f_new):
    validate_bracket(x1, x2, f1, f2)
    if f_new == 0:
        return x_new, x_new
    if f1 * f_new < 0:
        return x1, x_new
    if f2 * f_new < 0:
        return x_new, x2
    raise ValueError("new point does not preserve bracket")
