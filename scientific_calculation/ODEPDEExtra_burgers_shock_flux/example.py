def burgers_flux(left, right, viscosity=0.0):
    if viscosity < 0:
        raise ValueError("viscosity must be non-negative")
    f_left = 0.5 * left * left
    f_right = 0.5 * right * right
    if left > right:
        speed = 0.5 * (left + right)
        flux = f_left if speed >= 0 else f_right
    elif left < 0 < right:
        flux = 0.0
    else:
        flux = f_left if abs(left) >= abs(right) else f_right
    if viscosity > 0:
        flux -= viscosity * (right - left)
    return flux
def entropy_fix(left_states, right_states, epsilon=1e-3):
    import numpy as np

    left = np.asarray(left_states, dtype=float)
    right = np.asarray(right_states, dtype=float)
    if left.shape != right.shape or left.ndim != 1:
        raise ValueError("states must be matching one-dimensional arrays")
    transonic = (left < 0) & (right > 0)
    if np.any(np.abs(right - left) < epsilon):
        return "nearly-constant"
    if np.count_nonzero(transonic) >= max(1, left.size // 2):
        return "many-rarefactions"
    if np.any(left > right):
        return "shock-present"
    return "smooth"
