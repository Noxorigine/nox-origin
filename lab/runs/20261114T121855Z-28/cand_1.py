def solve(xs, k):
    count = {}
    total = 0
    for x in xs:
        complement = k - x
        total += count.get(complement, 0)
        count[x] = count.get(x, 0) + 1
    return total
