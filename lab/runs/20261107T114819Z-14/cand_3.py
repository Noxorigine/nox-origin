def solve(xs, k):
    counts = {}
    total = 0
    for x in xs:
        need = k - x
        total += counts.get(need, 0)
        counts[x] = counts.get(x, 0) + 1
    return total
