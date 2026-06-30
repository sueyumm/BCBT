import re


def parse_version(version):
    parts = re.split(r"[.\-]", str(version))
    parsed = []
    for part in parts:
        if part.isdigit():
            parsed.append(int(part))
        elif part:
            parsed.append(part)
    return parsed


def compare_version(left, right):
    a = parse_version(left)
    b = parse_version(right)
    for x, y in zip(a, b):
        if type(x) is type(y):
            if x < y:
                return -1
            if x > y:
                return 1
        elif isinstance(x, int):
            return 1
        else:
            return -1
    if len(a) == len(b):
        return 0
    return 1 if len(a) > len(b) else -1
