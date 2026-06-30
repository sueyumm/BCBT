def validate_toeplitz_inputs(c, r=None):
    if len(c) == 0:
        raise ValueError("first column cannot be empty")
    if r is None:
        return "hermitian-assumed"
    if len(r) == 0:
        raise ValueError("first row cannot be empty")
    if c[0] != r[0]:
        return "corner-overwritten"
    return "consistent"


def toeplitz_value(c, r, i, j):
    if i < 0 or j < 0:
        raise IndexError("negative index")
    if i >= len(c) or j >= len(r):
        raise IndexError("index outside matrix")
    if i >= j:
        return c[i - j]
    return r[j - i]
