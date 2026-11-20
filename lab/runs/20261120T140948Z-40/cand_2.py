def solve(xs):
    n = len(xs)
    if n < 2:
        return xs[:]  # copy of original (or empty)
    # Find the largest index i such that xs[i] < xs[i+1]
    i = n - 2
    while i >= 0 and xs[i] >= xs[i + 1]:
        i -= 1
    if i < 0:
        # xs is the highest permutation
        return sorted(xs)
    # Find the largest index j > i such that xs[j] > xs[i]
    j = n - 1
    while xs[j] <= xs[i]:
        j -= 1
    # Build the result without modifying xs
    result = xs[:]
    result[i], result[j] = result[j], result[i]
    # Reverse the suffix starting at i+1
    result[i + 1:] = reversed(result[i + 1:])
    return result
