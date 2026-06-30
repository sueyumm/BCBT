def normalize_slice(length, start=None, stop=None, step=None):
    if length < 0:
        raise ValueError("length must be non-negative")
    step = 1 if step is None else step
    if step == 0:
        raise ValueError("step cannot be zero")
    start, stop, step = slice(start, stop, step).indices(length)
    return start, stop, step


def slice_chunks(length, chunk):
    if chunk <= 0:
        raise ValueError("chunk size must be positive")
    chunks = []
    start = 0
    while start < length:
        stop = min(length, start + chunk)
        chunks.append((start, stop))
        start = stop
    if not chunks:
        return [(0, 0)]
    return chunks
