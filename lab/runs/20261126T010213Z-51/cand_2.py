def solve(xs):
    # Kadane's algorithm for maximum subarray sum
    max_ending = max_sofar = xs[0]
    min_ending = min_sofar = xs[0]
    total = xs[0]
    for v in xs[1:]:
        max_ending = v if max_ending + v < v else max_ending + v
        max_sofar = max(max_sofar, max_ending)
        min_ending = v if min_ending + v > v else min_ending + v
        min_sofar = min(min_sofar, min_ending)
        total += v
    # If all numbers are negative, total == min_sofar and max_sofar is the answer
    if total == min_sofar:
        return max_sofar
    return max(max_sofar, total - min_sofar)
