def solve(xs, k):
    freq = {}
    count = 0
    for x in xs:
        complement = k - x
        count += freq.get(complement, 0)
        freq[x] = freq.get(x, 0) + 1
    return count
