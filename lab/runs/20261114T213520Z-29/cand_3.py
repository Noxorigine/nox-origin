def solve(xs):
    # Helper function for merging two sorted lists
    def merge(a, b):
        i = j = 0
        merged = []
        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                merged.append(a[i])
                i += 1
            else:
                merged.append(b[j])
                j += 1
        if i < len(a):
            merged.extend(a[i:])
        if j < len(b):
            merged.extend(b[j:])
        return merged

    # Recursive mergesort implementation
    def mergesort(lst):
        n = len(lst)
        if n <= 1:
            return lst[:]
        mid = n // 2
        left = mergesort(lst[:mid])
        right = mergesort(lst[mid:])
        return merge(left, right)

    return mergesort(xs)
