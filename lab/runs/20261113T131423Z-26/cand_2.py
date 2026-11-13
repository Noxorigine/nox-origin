def solve(xs):
    n = len(xs)
    # Find the first index i from the right where xs[i] < xs[i+1]
    i = n - 2
    while i >= 0 and xs[i] >= xs[i + 1]:
        i -= 1
    if i == -1:
        # xs is the highest permutation; return sorted ascending copy
        return sorted(xs)
    # Find the smallest element greater than xs[i] to the right
    j = n - 1
    while xs[j] <= xs[i]:
        j -= 1
    # Create a new list to avoid modifying xs
    result = xs[:]
    # Swap xs[i] and xs[j]
    result[i], result[j] = result[j], result[i]
    # Reverse the suffix after i
    result[i + 1:] = reversed(result[i + 1:])
    return result
