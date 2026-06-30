def condition_label(cond):
    if cond < 0:
        raise ValueError("negative condition")
    if cond == 0:
        return "singular"
    if cond < 10:
        return "well-conditioned"
    if cond < 1e6:
        return "ill-conditioned"
    return "unstable"
