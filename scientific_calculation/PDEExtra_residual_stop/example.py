def residual_status(history, atol=1e-8, rtol=1e-4, patience=3):
    if not history:
        return "empty"
    if history[-1] <= atol:
        return "absolute"
    if len(history) < 2:
        return "running"
    previous = history[-2]
    if previous != 0 and abs(history[-1] / previous) <= rtol:
        return "relative"
    if len(history) >= patience and all(history[-i] >= history[-i - 1] for i in range(1, patience)):
        return "stagnated"
    return "running"
