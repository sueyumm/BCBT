def rk4_event_step(y, t, dt, rhs, threshold=None):
    if dt <= 0:
        raise ValueError("dt must be positive")
    k1 = rhs(t, y)
    k2 = rhs(t + 0.5 * dt, y + 0.5 * dt * k1)
    k3 = rhs(t + 0.5 * dt, y + 0.5 * dt * k2)
    k4 = rhs(t + dt, y + dt * k3)
    next_y = y + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
    if threshold is None:
        return next_y, "accepted"
    if y < threshold <= next_y:
        return threshold, "event-up"
    if y > threshold >= next_y:
        return threshold, "event-down"
    return next_y, "accepted"
