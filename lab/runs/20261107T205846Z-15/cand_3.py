def solve(xs):
    # Mergesort implementation that returns a new sorted list without modifying xs
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
        if i < len(left):
            merged.extend(left[i:])
        if j < len(right):
            merged.extend(right[j:])
        return merged

    def mergesort(arr):
        n = len(arr)
        if n <= 1:
            return arr[:]
        mid = n // 2
        left = mergesort(arr[:mid])
        right = mergesort(arr[mid:])
        return merge(left, right)

    return mergesort(xs)
