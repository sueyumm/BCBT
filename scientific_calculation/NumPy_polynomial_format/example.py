def format_term(coefficient, power, variable="x"):
    if coefficient == 0:
        return ""
    sign = "-" if coefficient < 0 else "+"
    magnitude = abs(coefficient)
    if power == 0:
        body = f"{magnitude:g}"
    elif power == 1:
        body = variable if magnitude == 1 else f"{magnitude:g}{variable}"
    else:
        body = f"{variable}^{power}" if magnitude == 1 else f"{magnitude:g}{variable}^{power}"
    return sign + body


def polynomial_string(coefficients, variable="x"):
    terms = []
    degree = len(coefficients) - 1
    for index, coefficient in enumerate(coefficients):
        power = degree - index
        term = format_term(coefficient, power, variable)
        if term:
            terms.append(term)
    if not terms:
        return "0"
    result = "".join(terms)
    return result[1:] if result.startswith("+") else result
