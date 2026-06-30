def normalize_color_value(value, vmin=0.0, vmax=1.0, clip=True):
    if vmax <= vmin:
        raise ValueError("invalid range")
    scaled = (value - vmin) / (vmax - vmin)
    if clip:
        if scaled < 0:
            return 0.0
        if scaled > 1:
            return 1.0
    return scaled
