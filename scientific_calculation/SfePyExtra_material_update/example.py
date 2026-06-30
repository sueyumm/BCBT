def update_material(base, temperature, strain):
    value = base
    if temperature > 300:
        value *= 1.0 - min(0.5, (temperature - 300) / 1000)
    elif temperature < 0:
        value *= 1.2
    if abs(strain) > 0.1:
        value *= 0.8
    if value <= 0:
        raise ValueError("nonpositive material")
    return value
