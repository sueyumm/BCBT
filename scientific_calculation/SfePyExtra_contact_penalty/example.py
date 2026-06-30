def contact_force(gap, normal_stiffness, friction=0.0):
    if normal_stiffness < 0 or friction < 0:
        raise ValueError("invalid stiffness")
    if gap > 0:
        return 0.0
    normal = -gap * normal_stiffness
    if friction == 0:
        return normal
    return normal * (1.0 + min(friction, 1.0))
