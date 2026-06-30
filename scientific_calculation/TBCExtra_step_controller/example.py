def adapt_step(error, step, tolerance):
    if step <= 0 or tolerance <= 0:
        raise ValueError("invalid step/tolerance")
    if error == 0:
        return step * 2
    ratio = tolerance / abs(error)
    if ratio > 4:
        return step * 1.5
    if ratio > 1:
        return step
    if ratio > 0.25:
        return step * 0.5
    return step * 0.25
