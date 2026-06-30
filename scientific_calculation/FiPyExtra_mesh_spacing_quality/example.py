def spacing_quality(spacings):
    if len(spacings) == 0:
        return "empty"
    if any(h <= 0 for h in spacings):
        return "invalid"
    ratio = max(spacings) / min(spacings)
    if ratio < 1.2:
        return "uniform"
    if ratio < 3.0:
        return "graded"
    return "skewed"
