def triangle_quality(a, b, c):
    sides = sorted([float(a), float(b), float(c)])
    if sides[0] <= 0:
        return "invalid"
    if sides[0] + sides[1] <= sides[2]:
        return "degenerate"
    ratio = sides[2] / sides[0]
    if ratio < 1.2:
        return "equilateral"
    if ratio < 3.0:
        return "acceptable"
    return "sliver"
