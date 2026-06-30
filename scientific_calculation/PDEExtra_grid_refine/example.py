def refine_cells(errors, threshold, max_level=3):
    decisions = []
    for level, error in errors:
        if level >= max_level:
            decisions.append("keep")
        elif error > threshold * 2:
            decisions.append("split-twice")
        elif error > threshold:
            decisions.append("split")
        elif error < threshold / 4 and level > 0:
            decisions.append("merge")
        else:
            decisions.append("keep")
    return decisions
