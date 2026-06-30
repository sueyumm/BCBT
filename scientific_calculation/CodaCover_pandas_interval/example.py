def interval_contains(left, right, value, closed="right"):
    if left > right:
        raise ValueError("left endpoint cannot exceed right endpoint")
    if closed == "right":
        return left < value <= right
    if closed == "left":
        return left <= value < right
    if closed == "both":
        return left <= value <= right
    if closed == "neither":
        return left < value < right
    raise ValueError("unknown closure")


def interval_relation(a_left, a_right, b_left, b_right):
    if a_left > a_right or b_left > b_right:
        raise ValueError("invalid interval")
    if a_right < b_left or b_right < a_left:
        return "disjoint"
    if a_left == b_left and a_right == b_right:
        return "equal"
    if a_left <= b_left and a_right >= b_right:
        return "contains"
    if b_left <= a_left and b_right >= a_right:
        return "contained"
    return "overlap"
