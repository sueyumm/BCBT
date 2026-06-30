def classify_cfl(dx, dt, velocity, diffusion=0.0):
    if dx <= 0 or dt <= 0:
        raise ValueError("dx and dt must be positive")
    advective = abs(velocity) * dt / dx
    diffusive = diffusion * dt / (dx * dx)
    if diffusion < 0:
        return "invalid-diffusion"
    if advective == 0 and diffusive == 0:
        return "static"
    if advective <= 0.5 and diffusive <= 0.25:
        return "safe"
    if advective <= 1.0 and diffusive <= 0.5:
        return "marginal"
    return "unstable"
