def solve(xs):
    # Standard Kadane's algorithm for max subarray sum
    max_ending = max_sofar = xs[0]
    min_ending = min_sofar = xs[0]
    total = xs[0]
    for x in xs[1:]:
        max_ending = x if max_ending + x < x else max_ending + x
        max_sofar = max_sofar if max_sofar > max_ending else max_ending

        min_ending = x if min_ending + x > x else min_ending + x
        min_sofar = min_sofar if min_sofar < min_ending else min_ending

        total += x

    # If all numbers are negative, max_sofar is the answer
    if max_sofar < 0:
        return max_sofar

    circular_max = total - min_sofar
    return max_sofar if circular_max < max_sofar else circular_max
