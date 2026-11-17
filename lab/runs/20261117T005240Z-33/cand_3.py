def solve(xs):
    n = len(xs)
    if n < 2:
        return xs[:]
    # Find the longest non-increasing suffix
    i = n - 2
    while i >= 0 and xs[i] >= xs[i + 1]:
        i -= 1
    if i == -1:
        # xs is the highest permutation
        return sorted(xs)
    # Find rightmost successor to pivot in the suffix
    j = n - 1
    while xs[j] <= xs[i]:
        j -= 1
    # Build the next permutation
    result = xs[:i] + [xs[j]]
    # Append the suffix sorted in ascending order
    suffix = xs[i + 1:j] + xs[j + 1:]
    result.extend(sorted(suffix))
    return result
