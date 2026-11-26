def solve(xs):
    # Compute maximum subarray sum (non-circular) using Kadane's algorithm
    max_ending = max_sofar = xs[0]
    # Compute minimum subarray sum (non-circular) using Kadane's algorithm on negated values
    min_ending = min_sofar = xs[0]
    total = xs[0]
    for x in xs[1:]:
        total += x
        max_ending = x if max_ending < 0 else max_ending + x
        max_sofar = max(max_sofar, max_ending)
        min_ending = x if min_ending > 0 else min_ending + x
        min_sofar = min(min_sofar, min_ending)
    # If all numbers are negative, max_sofar is the answer
    if total == min_sofar:
        return max_sofar
    # Otherwise, consider wrapping subarray
    return max(max_sofar, total - min_sofar)
