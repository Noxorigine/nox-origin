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
    def merge_sort(arr):
        n = len(arr)
        if n <= 1:
            return arr[:]
        mid = n // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        return merge(left, right)

    # Ensure we do not modify the original list
    return merge_sort(xs)
