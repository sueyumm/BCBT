def validate_sparse_shape(shape, nnz):
    if len(shape) != 2:
        raise ValueError("sparse shape must be two-dimensional")
    rows, cols = shape
    if rows < 0 or cols < 0:
        raise ValueError("dimensions must be non-negative")
    if nnz < 0:
        raise ValueError("number of nonzeros must be non-negative")
    if nnz > rows * cols:
        raise ValueError("too many nonzero entries")
    if rows == 0 or cols == 0:
        return "empty"
    density = nnz / (rows * cols)
    if density < 0.1:
        return "sparse"
    if density < 0.5:
        return "medium"
    return "dense"


def compressed_index_bounds(indptr, indices):
    if len(indptr) == 0:
        raise ValueError("indptr cannot be empty")
    if indptr[0] != 0:
        raise ValueError("indptr must start at zero")
    if any(indptr[i] > indptr[i + 1] for i in range(len(indptr) - 1)):
        raise ValueError("indptr must be nondecreasing")
    if indptr[-1] != len(indices):
        raise ValueError("indptr does not match indices")
    return (min(indices), max(indices)) if indices else None
