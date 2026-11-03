def solve(xs):
    # Helper function for merge sort
    def merge(left, right):
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        # Append any remaining elements
        if i < len(left):
            merged.extend(left[i:])
        if j < len(right):
            merged.extend(right[j:])
        return merged

    # Recursive merge sort
    n = len(xs)
    if n <= 1:
        return xs[:]  # return a shallow copy
    mid = n // 2
    left_sorted = solve(xs[:mid])
    right_sorted = solve(xs[mid:])
    return merge(left_sorted, right_sorted)
