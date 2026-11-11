def solve(xs):
    def merge(a, b):
        i = j = 0
        res = []
        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                res.append(a[i]); i += 1
            else:
                res.append(b[j]); j += 1
        if i < len(a):
            res.extend(a[i:])
        if j < len(b):
            res.extend(b[j:])
        return res

    def mergesort(arr):
        n = len(arr)
        if n <= 1:
            return arr[:]
        mid = n // 2
        left = mergesort(arr[:mid])
        right = mergesort(arr[mid:])
        return merge(left, right)

    return mergesort(xs)
