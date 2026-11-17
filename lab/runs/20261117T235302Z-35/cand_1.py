def solve(xs, k):
    count = 0
    n = len(xs)
    for i in range(n):
        xi = xs[i]
        for j in range(i + 1, n):
            if xi + xs[j] == k:
                count += 1
    return count
