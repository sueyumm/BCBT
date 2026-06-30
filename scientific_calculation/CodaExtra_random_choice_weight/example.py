def weighted_choice_bucket(weights, value):
    if not weights:
        raise ValueError("empty weights")
    total = sum(weights)
    if total <= 0:
        raise ValueError("nonpositive total")
    threshold = value * total
    running = 0
    for index, weight in enumerate(weights):
        if weight < 0:
            raise ValueError("negative weight")
        running += weight
        if threshold <= running:
            return index
    return len(weights) - 1
