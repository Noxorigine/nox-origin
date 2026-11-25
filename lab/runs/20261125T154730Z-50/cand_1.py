def solve(xs):
    # Helper function for merging two sorted lists
    def merge(left, right):
        i = j = 0
        merged = []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        if i < len(left):
            merged.extend(left[i:])
        if j < len(right):
            merged.extend(right[j:])
        return merged

    # Recursive mergesort
    def mergesort(arr):
        n = len(arr)
        if n <= 1:
            return arr[:]
        mid = n // 2
        left = mergesort(arr[:mid])
        right = mergesort(arr[mid:])
        return merge(left, right)

    # Work on a copy to avoid modifying the original list
    return mergesort(xs[:])
