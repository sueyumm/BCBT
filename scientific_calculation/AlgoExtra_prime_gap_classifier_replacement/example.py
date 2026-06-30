# Adapted from TheAlgorithms/Python maths prime-number utilities.


def prime_gap_classifier(previous_prime, current_prime):
    if previous_prime < 2 or current_prime <= previous_prime:
        raise ValueError("invalid prime pair")
    gap = current_prime - previous_prime
    if gap == 1:
        return "twin-edge"
    if gap == 2:
        return "twin"
    if gap <= 6:
        return "small"
    if gap % 2 == 0:
        return "large-even"
    return "invalid-odd-gap"
