def boundary_mask_index(index, nx, ny):
    if nx <= 0 or ny <= 0:
        raise ValueError("invalid grid")
    row, col = divmod(index, nx)
    if row < 0 or row >= ny:
        return "outside"
    if row == 0 or row == ny - 1:
        return "horizontal"
    if col == 0 or col == nx - 1:
        return "vertical"
    return "interior"
