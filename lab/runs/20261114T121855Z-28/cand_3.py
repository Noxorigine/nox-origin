def solve(xs, k):
    count = 0
    seen = {}
    for x in xs:
        complement = k - x
        count += seen.get(complement, 0)
        seen[x] = seen.get(x, 0) + 1
    return count
