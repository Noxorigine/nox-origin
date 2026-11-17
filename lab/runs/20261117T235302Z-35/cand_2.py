def solve(xs, k):
    count = {}
    pairs = 0
    for x in xs:
        complement = k - x
        pairs += count.get(complement, 0)
        count[x] = count.get(x, 0) + 1
    return pairs
