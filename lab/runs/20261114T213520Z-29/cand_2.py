def solve(xs):
    # Use a simple recursive quicksort that does not modify the input list
    if len(xs) <= 1:
        return xs[:]
    pivot = xs[0]
    less = [x for x in xs[1:] if x <= pivot]
    greater = [x for x in xs[1:] if x > pivot]
    return solve(less) + [pivot] + solve(greater)
