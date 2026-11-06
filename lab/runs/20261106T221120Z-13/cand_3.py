def solve(iv):
    # Work on a copy to avoid modifying the input
    intervals = list(iv)
    if not intervals:
        return []
    # Sort intervals by start point
    intervals.sort(key=lambda x: x[0])
    merged = []
    cur_start, cur_end = intervals[0]
    for start, end in intervals[1:]:
        if start <= cur_end:  # overlap or touch
            if end > cur_end:
                cur_end = end
        else:
            merged.append([cur_start, cur_end])
            cur_start, cur_end = start, end
    merged.append([cur_start, cur_end])
    return merged
