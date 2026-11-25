def solve(xs, k):
    count = 0
    freq = {}
    for x in xs:
        complement = k - x
        count += freq.get(complement, 0)
        freq[x] = freq.get(x, 0) + 1
    return count
