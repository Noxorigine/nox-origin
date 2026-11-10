def solve(xs):
    a = xs[:]  # make a copy to avoid modifying the input
    n = len(a)
    # Step 1: find the longest non-increasing suffix
    i = n - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i == -1:
        # xs is the last permutation
        a.sort()
        return a
    # Step 2: find rightmost successor to pivot in the suffix
    j = n - 1
    while a[j] <= a[i]:
        j -= 1
    # Step 3: swap pivot with successor
    a[i], a[j] = a[j], a[i]
    # Step 4: reverse the suffix
    a[i + 1:] = reversed(a[i + 1:])
    return a
