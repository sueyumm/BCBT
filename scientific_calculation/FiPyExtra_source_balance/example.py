def source_balance(transient, diffusion, source, volume):
    if volume <= 0:
        raise ValueError("volume must be positive")
    total = transient + diffusion + source * volume
    if abs(total) < 1e-12:
        return "balanced"
    if total > 0:
        return "accumulating" if source >= 0 else "diffusion-dominated"
    return "depleting" if source <= 0 else "transient-dominated"
