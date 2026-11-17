def solve(xs):
    n = len(xs)
    if n < 2:
        return xs[:]
    # Find the longest non-increasing suffix
    i = n - 2
    while i >= 0 and xs[i] >= xs[i + 1]:
        i -= 1
    if i == -1:
        # xs is the last permutation
        return sorted(xs)
    # Find rightmost successor to pivot in suffix
    j = n - 1
    while xs[j] <= xs[i]:
        j -= 1
    # Create new list with swapped pivot and successor
    result = xs[:]
    result[i], result[j] = result[j], result[i]
    # Reverse the suffix
    result[i + 1:] = reversed(result[i + 1:])
    return result
