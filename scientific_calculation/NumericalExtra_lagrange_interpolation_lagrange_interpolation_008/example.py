# Adapted from Numerical-methods-main/lagrange interpolation.py::lagrange_interpolation

def multiply(array):  # multiply items in a list (list of terms (monomials) will be given to this function)
    result = 1
    for number in array:
        result = result * number
    return result

def term_generator(index, length, x, given_x_values):  # generating terms of the interpolation function
    term = list()
    for i in range(length):
        if index != i:
            term.append((x - given_x_values[i])/(given_x_values[index] - given_x_values[i]))
    return multiply(term)

def lagrange_interpolation(x, given_x_values, given_y_values):
    if len(given_x_values) == len(given_y_values):
        count_of_points = len(given_x_values)
        result = list()
        for i in range(count_of_points):
            result.append(term_generator(i, count_of_points, x, given_x_values) * given_y_values[i])
        return sum(result)
    else:
        return "The count of Xs and Ys should be equal."
