def dof_category(node, component, constrained):
    key = (node, component)
    if node < 0 or component < 0:
        raise ValueError("negative index")
    if key in constrained:
        return "fixed"
    if component == 0:
        return "x-free"
    if component == 1:
        return "y-free"
    return "extra"
