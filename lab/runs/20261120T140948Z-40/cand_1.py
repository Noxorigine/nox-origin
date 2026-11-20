def solve(xs):
    n = len(xs)
    # Find the first index i from the end where xs[i] < xs[i+1]
    i = n - 2
    while i >= 0 and xs[i] >= xs[i + 1]:
        i -= 1
    if i == -1:
        # xs is the last permutation
        return sorted(xs)
    # Find the smallest element greater than xs[i] to the right
    j = n - 1
    while xs[j] <= xs[i]:
        j -= 1
    # Create new list to avoid modifying xs
    res = xs[:]
    # Swap positions i and j
    res[i], res[j] = res[j], res[i]
    # Reverse the suffix starting at i+1
    res[i + 1:] = reversed(res[i + 1:])
    return res
