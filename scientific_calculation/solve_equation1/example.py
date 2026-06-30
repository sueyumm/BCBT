def newtonsMethod(function, derivative, guess, maxIterations, epsilon, delta):
    """ Calculates a root of the given function with the given derivative, using
        Newton's method. """
    xNew = 0
    xOld = guess
    v = function(xOld)
    if abs(v) < epsilon:
        return (guess, v, 0)
    for k in range(1, maxIterations+1):
        xNew = xOld - (v / derivative(xOld))
        v = function(xNew)
        if abs(xNew - xOld) < delta or abs(v) < epsilon:
            return (xNew, v, k)
        xOld = xNew
    # This code should be unreachable:
    return (0,0,-1)
