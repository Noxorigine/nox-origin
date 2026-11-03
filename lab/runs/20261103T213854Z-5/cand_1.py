def solve(xs):
    # Make a copy to avoid modifying the input
    a = xs[:]
    n = len(a)
    # Find the first index i from the end where a[i] < a[i+1]
    i = n - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i == -1:
        # xs is the highest permutation
        return sorted(a)
    # Find the smallest element greater than a[i] to the right
    j = n - 1
    while a[j] <= a[i]:
        j -= 1
    # Swap them
    a[i], a[j] = a[j], a[i]
    # Reverse the suffix starting at i+1
    a[i + 1:] = reversed(a[i + 1:])
    return a
