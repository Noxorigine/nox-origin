def solve(xs):
    # Helper function for merging two sorted lists
    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    # Recursive mergesort
    n = len(xs)
    if n <= 1:
        return xs[:]  # return a shallow copy
    mid = n // 2
    left_sorted = solve(xs[:mid])
    right_sorted = solve(xs[mid:])
    return merge(left_sorted, right_sorted)
