def solve(xs, k):
    count = {}
    pairs = 0
    for x in xs:
        need = k - x
        pairs += count.get(need, 0)
        count[x] = count.get(x, 0) + 1
    return pairs
