def solve(xs):
    # Kadane for maximum subarray sum
    max_ending = max_sofar = xs[0]
    for v in xs[1:]:
        max_ending = v if max_ending < 0 else max_ending + v
        if max_ending > max_sofar:
            max_sofar = max_ending

    # Kadane for minimum subarray sum
    min_ending = min_sofar = xs[0]
    for v in xs[1:]:
        min_ending = v if min_ending > 0 else min_ending + v
        if min_ending < min_sofar:
            min_sofar = min_ending

    total = sum(xs)
    # If all numbers are negative, max_sofar is the answer
    if min_sofar == total:
        return max_sofar
    # Otherwise consider wrap-around case
    return max(max_sofar, total - min_sofar)
