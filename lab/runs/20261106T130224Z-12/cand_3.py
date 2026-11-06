def solve(xs):
    a = xs[:]  # make a copy
    n = len(a)
    # Find the largest index i such that a[i] < a[i+1]
    i = n - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i == -1:
        # xs is the last permutation
        return sorted(a)
    # Find the largest index j > i such that a[j] > a[i]
    j = n - 1
    while a[j] <= a[i]:
        j -= 1
    # Swap a[i] and a[j]
    a[i], a[j] = a[j], a[i]
    # Reverse the suffix starting at i+1
    a[i + 1:] = reversed(a[i + 1:])
    return a
