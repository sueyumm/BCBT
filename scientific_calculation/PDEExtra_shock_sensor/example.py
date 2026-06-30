def shock_sensor(left, center, right, eps=1e-12):
    jump_left = abs(center - left)
    jump_right = abs(right - center)
    smooth = abs(right - 2 * center + left)
    scale = abs(left) + abs(center) + abs(right) + eps
    ratio = smooth / scale
    if ratio < 0.01:
        return "smooth"
    if jump_left > 3 * jump_right:
        return "left-shock"
    if jump_right > 3 * jump_left:
        return "right-shock"
    return "oscillatory"
