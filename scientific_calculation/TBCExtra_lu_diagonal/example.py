def diagonal_status(diagonal, tol=1e-12):
    if len(diagonal) == 0:
        return "empty"
    zeros = sum(1 for value in diagonal if abs(value) <= tol)
    negatives = sum(1 for value in diagonal if value < -tol)
    if zeros:
        return "singular"
    if negatives:
        return "indefinite"
    return "positive"
