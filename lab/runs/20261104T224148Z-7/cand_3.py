def solve(xs, k):
    count = {}
    result = 0
    for x in xs:
        complement = k - x
        result += count.get(complement, 0)
        count[x] = count.get(x, 0) + 1
    return result
