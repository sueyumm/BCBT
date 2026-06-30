def greedy_column_groups(conflicts):
    groups = []
    for column, neighbors in enumerate(conflicts):
        placed = False
        for group in groups:
            if all(column not in conflicts[other] and other not in neighbors for other in group):
                group.append(column)
                placed = True
                break
        if not placed:
            groups.append([column])
    return groups


def conflict_density(conflicts):
    n = len(conflicts)
    if n == 0:
        return "empty"
    edges = sum(len(set(neighbors)) for neighbors in conflicts)
    possible = n * max(n - 1, 1)
    density = edges / possible
    if density < 0.1:
        return "low"
    if density < 0.5:
        return "medium"
    return "high"
