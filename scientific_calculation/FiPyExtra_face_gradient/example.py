def choose_face_gradient(left, right, distance, scheme="central"):
    if distance <= 0:
        raise ValueError("distance must be positive")
    if scheme == "central":
        return (right - left) / distance
    if scheme == "upwind":
        return 0.0 if left * right < 0 else (right - left) / distance
    if scheme == "limited":
        raw = (right - left) / distance
        return max(-1.0, min(1.0, raw))
    raise ValueError("unknown scheme")
