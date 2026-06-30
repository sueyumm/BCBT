def continued_fraction(a_terms, b_terms, maxiter=100, tolerance=1e-12):
    if maxiter <= 0:
        raise ValueError("maxiter must be positive")
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    if len(a_terms) != len(b_terms):
        raise ValueError("term arrays must have equal length")
    value = 0.0
    previous = None
    for index, (a, b) in enumerate(zip(reversed(a_terms), reversed(b_terms))):
        if index >= maxiter:
            break
        denom = b + value
        if denom == 0:
            raise ZeroDivisionError("zero denominator")
        value = a / denom
        if previous is not None and abs(value - previous) <= tolerance:
            return value
        previous = value
    return value


def convergence_state(error, tolerance):
    if error < 0 or tolerance < 0:
        raise ValueError("error and tolerance must be non-negative")
    return "converged" if error <= tolerance else "running"
