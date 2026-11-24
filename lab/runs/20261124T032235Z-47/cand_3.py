def solve(xs):
    n = len(xs)
    # Find the first index i from the right where xs[i] < xs[i+1]
    i = n - 2
    while i >= 0 and xs[i] >= xs[i + 1]:
        i -= 1
    if i == -1:
        # xs is the highest permutation
        return sorted(xs)
    # Find the smallest element greater than xs[i] to the right
    j = n - 1
    while xs[j] <= xs[i]:
        j -= 1
    # Build the next permutation without modifying xs
    prefix = xs[:i]               # elements before i
    pivot = xs[j]                 # element to swap with xs[i]
    # Elements after i, with xs[i] removed and xs[j] removed, then sorted
    suffix = xs[i+1:j] + xs[j+1:]
    suffix = sorted(suffix + [xs[i]])
    return prefix + [pivot] + suffix
