def solve(iv):
    # Work on a copy to avoid modifying the input
    intervals = [list(x) for x in iv]
    if not intervals:
        return []
    # Sort intervals by start point
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for cur in intervals[1:]:
        prev = merged[-1]
        if cur[0] <= prev[1]:  # overlap or touch
            # Merge by extending the end if needed
            if cur[1] > prev[1]:
                prev[1] = cur[1]
        else:
            merged.append(cur)
    return merged
