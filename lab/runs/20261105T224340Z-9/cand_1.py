def solve(xs):
    # Kadane's algorithm for maximum subarray sum
    max_ending = max_sofar = xs[0]
    for v in xs[1:]:
        max_ending = v if max_ending < 0 else max_ending + v
        if max_ending > max_sofar:
            max_sofar = max_ending

    # Kadane's algorithm for minimum subarray sum
    min_ending = min_sofar = xs[0]
    for v in xs[1:]:
        min_ending = v if min_ending > 0 else min_ending + v
        if min_ending < min_sofar:
            min_sofar = min_ending

    total = sum(xs)
    # If all numbers are negative, max_wrap would be zero which is invalid (empty subarray)
    # In that case, the maximum subarray is the max element (already captured by max_sofar)
    max_wrap = total - min_sofar if total != min_sofar else max_sofar
    return max_sofar if max_sofar > max_wrap else max_wrap
