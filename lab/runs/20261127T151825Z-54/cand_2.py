def solve(xs):
    n = len(xs)
    # Find the first index i from the end where xs[i] < xs[i+1]
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
    # Build the new list without modifying xs
    prefix = xs[:i] + [xs[j]]
    # Take the suffix after i, remove the element at j, and sort it
    suffix = xs[i + 1:j] + xs[j + 1:]
    suffix.sort()
    return prefix + suffix
