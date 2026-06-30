def bracket_status(fa, fb, midpoint):
    if fa == 0 or fb == 0:
        return "endpoint-root"
    if fa * fb < 0:
        return "bracketed"
    if abs(midpoint) < min(abs(fa), abs(fb)):
        return "improving"
    return "bad-bracket"
