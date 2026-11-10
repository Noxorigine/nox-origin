def solve(xs, k):
    counts = {}
    result = 0
    for x in xs:
        complement = k - x
        result += counts.get(complement, 0)
        counts[x] = counts.get(x, 0) + 1
    return result
