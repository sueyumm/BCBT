def bezier_flatness(p0, p1, p2, p3, tol=1e-3):
    chord = abs(p3 - p0)
    control = abs(p1 - p0) + abs(p2 - p1) + abs(p3 - p2)
    if tol <= 0:
        raise ValueError("tol must be positive")
    excess = control - chord
    if excess <= tol:
        return "flat"
    if excess <= 10 * tol:
        return "subdivide-once"
    return "subdivide-many"
