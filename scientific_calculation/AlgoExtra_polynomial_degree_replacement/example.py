# Adapted from TheAlgorithms/Python polynomial helpers.


def polynomial_degree_label(coefficients):
    if not coefficients:
        return "empty"
    first = None
    for index, value in enumerate(coefficients):
        if value != 0:
            first = index
            break
    if first is None:
        return "zero"
    degree = len(coefficients) - first - 1
    if degree == 0:
        return "constant"
    if degree == 1:
        return "linear"
    if degree == 2:
        return "quadratic"
    return "higher"
