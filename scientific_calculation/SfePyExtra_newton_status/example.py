def newton_status(residuals, max_iter=10):
    if not residuals:
        return "not-started"
    if residuals[-1] < 1e-10:
        return "converged"
    if len(residuals) >= max_iter:
        return "max-iter"
    if len(residuals) >= 2 and residuals[-1] > residuals[-2]:
        return "diverging"
    if len(residuals) >= 3 and residuals[-1] == residuals[-2] == residuals[-3]:
        return "stalled"
    return "iterate"
