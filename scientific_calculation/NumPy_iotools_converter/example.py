def convert_token(token, missing_values=None, default=None):
    missing = set() if missing_values is None else set(missing_values)
    if token in missing:
        return default
    text = str(token).strip()
    if text == "":
        return default
    try:
        if "." in text or "e" in text.lower():
            return float(text)
        return int(text)
    except ValueError:
        lowered = text.lower()
        if lowered in {"true", "false"}:
            return lowered == "true"
        return text


def validate_column(values, allow_missing=True):
    if not values:
        raise ValueError("column cannot be empty")
    missing = sum(value is None for value in values)
    if missing and not allow_missing:
        raise ValueError("missing values are not allowed")
    if missing == len(values):
        return "all-missing"
    if missing:
        return "partial"
    return "complete"
