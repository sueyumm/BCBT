def cholesky_pivot_status(pivot, accumulated, tol=1e-12):
    value = pivot - accumulated
    if value < -tol:
        return "not-positive-definite"
    if abs(value) <= tol:
        return "semidefinite"
    if value < 1:
        return "small-positive"
    return "positive"
