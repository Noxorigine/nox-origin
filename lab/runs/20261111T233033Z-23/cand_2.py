def solve(xs):
    # Compute maximum subarray sum using Kadane's algorithm
    max_ending = max_sofar = xs[0]
    min_ending = min_sofar = xs[0]
    total = xs[0]
    for v in xs[1:]:
        total += v
        max_ending = v if max_ending < 0 else max_ending + v
        if max_ending > max_sofar:
            max_sofar = max_ending
        min_ending = v if min_ending > 0 else min_ending + v
        if min_ending < min_sofar:
            min_sofar = min_ending
    # If all numbers are negative, max_sofar is the answer
    if max_sofar < 0:
        return max_sofar
    # Otherwise, consider wrapping subarray
    return max(max_sofar, total - min_sofar)
