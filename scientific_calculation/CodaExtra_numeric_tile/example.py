def tile_bin(value, bins):
    if not bins:
        raise ValueError("empty bins")
    if any(bins[i] >= bins[i + 1] for i in range(len(bins) - 1)):
        raise ValueError("bins must be increasing")
    if value < bins[0]:
        return -1
    for index in range(len(bins) - 1):
        if bins[index] <= value < bins[index + 1]:
            return index
    return len(bins) - 1
