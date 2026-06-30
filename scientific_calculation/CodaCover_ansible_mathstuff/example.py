import math


def safe_logarithm(value, base=math.e):
    if value <= 0:
        raise ValueError("logarithm input must be positive")
    if base <= 0 or base == 1:
        raise ValueError("invalid logarithm base")
    if base == math.e:
        return math.log(value)
    return math.log(value, base)


def human_to_bytes(text):
    units = {"b": 1, "kb": 1024, "mb": 1024 ** 2, "gb": 1024 ** 3, "tb": 1024 ** 4}
    raw = str(text).strip().lower().replace(" ", "")
    if not raw:
        raise ValueError("empty size")
    number = ""
    suffix = ""
    for char in raw:
        if char.isdigit() or char == ".":
            number += char
        else:
            suffix += char
    if number == "":
        raise ValueError("missing numeric size")
    suffix = suffix or "b"
    if suffix not in units:
        raise ValueError("unknown size unit")
    return int(float(number) * units[suffix])


def set_relationship(left, right):
    a, b = set(left), set(right)
    if a == b:
        return "equal"
    if a < b:
        return "proper-subset"
    if a > b:
        return "proper-superset"
    if a & b:
        return "overlap"
    return "disjoint"
