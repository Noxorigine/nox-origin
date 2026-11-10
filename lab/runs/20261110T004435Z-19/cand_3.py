def solve(xs):
    n = len(xs)
    if n < 2:
        return xs[:]  # return a shallow copy
    # Find the largest index i such that xs[i] < xs[i + 1]
    i = n - 2
    while i >= 0 and xs[i] >= xs[i + 1]:
        i -= 1
    if i == -1:
        # xs is the last permutation; return sorted ascending list
        return sorted(xs)
    # Find the largest index j > i such that xs[j] > xs[i]
    j = n - 1
    while xs[j] <= xs[i]:
        j -= 1
    # Build the new permutation
    # Prefix unchanged up to i-1, then swapped element, then reversed suffix
    new_perm = xs[:i] + [xs[j]] + xs[i+1:j] + [xs[i]] + xs[j+1:]
    # Reverse the suffix after position i
    new_perm[i+1:] = reversed(new_perm[i+1:])
    return new_perm
