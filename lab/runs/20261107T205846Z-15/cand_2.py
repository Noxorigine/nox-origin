def solve(xs):
    if len(xs) <= 1:
        return xs[:]  # return a shallow copy
    mid = len(xs) // 2
    left = solve(xs[:mid])
    right = solve(xs[mid:])
    # merge left and right
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    if i < len(left):
        result.extend(left[i:])
    if j < len(right):
        result.extend(right[j:])
    return result
