def select_region(x, y, radius=1.0):
    r2 = x * x + y * y
    if radius <= 0:
        raise ValueError("radius must be positive")
    if abs(x) < 1e-12 and abs(y) < 1e-12:
        return "center"
    if r2 < radius * radius:
        return "inside"
    if abs(r2 - radius * radius) < 1e-9:
        return "boundary"
    return "outside"
