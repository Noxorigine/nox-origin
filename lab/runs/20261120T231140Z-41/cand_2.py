def solve(iv):
    # Make a shallow copy to avoid modifying the input list
    intervals = [(a, b) for a, b in iv]
    if not intervals:
        return []
    # Sort intervals by start (and by end to stabilize)
    intervals.sort(key=lambda x: (x[0], x[1]))
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
