def solve(xs):
    n = len(xs)
    if n < 2:
        return xs[:]  # copy of the list (or empty)
    a = xs[:]  # work on a copy
    # Find the longest non-increasing suffix
    i = n - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i < 0:
        # xs is the highest permutation
        a.sort()
        return a
    # Find rightmost element greater than a[i]
    j = n - 1
    while a[j] <= a[i]:
        j -= 1
    # Swap pivot with that element
    a[i], a[j] = a[j], a[i]
    # Reverse the suffix
    a[i + 1:] = reversed(a[i + 1:])
    return a
