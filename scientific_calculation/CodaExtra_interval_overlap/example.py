def interval_relation(a_left, a_right, b_left, b_right, closed=True):
    if a_left > a_right or b_left > b_right:
        raise ValueError("invalid interval")
    if closed:
        if a_right < b_left or b_right < a_left:
            return "disjoint"
    else:
        if a_right <= b_left or b_right <= a_left:
            return "disjoint"
    if a_left == b_left and a_right == b_right:
        return "equal"
    if a_left <= b_left and b_right <= a_right:
        return "contains"
    if b_left <= a_left and a_right <= b_right:
        return "inside"
    return "overlap"
