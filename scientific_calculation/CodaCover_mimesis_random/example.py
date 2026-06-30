def weighted_choice_index(weights, value):
    if not weights:
        raise ValueError("weights cannot be empty")
    if value < 0:
        raise ValueError("value must be non-negative")
    total = sum(weights)
    if total <= 0:
        raise ValueError("total weight must be positive")
    threshold = value * total
    cumulative = 0.0
    for index, weight in enumerate(weights):
        if weight < 0:
            raise ValueError("weights must be non-negative")
        cumulative += weight
        if threshold < cumulative:
            return index
    return len(weights) - 1


def random_range_mode(start, stop, step=1):
    if step == 0:
        raise ValueError("step cannot be zero")
    if start == stop:
        return "empty"
    if (stop - start) * step < 0:
        return "descending-empty"
    if abs(stop - start) <= abs(step):
        return "single"
    return "multi"
