def solve(xs):
    # Create a copy to avoid modifying the original list
    a = xs[:]
    n = len(a)
    # Find the longest non-increasing suffix
    i = n - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i == -1:
        # xs is the highest permutation; return sorted ascending
        return sorted(a)
    # Find rightmost successor to pivot in the suffix
    j = n - 1
    while a[j] <= a[i]:
        j -= 1
    # Swap pivot with successor
    a[i], a[j] = a[j], a[i]
    # Reverse the suffix
    a[i + 1:] = reversed(a[i + 1:])
    return a
