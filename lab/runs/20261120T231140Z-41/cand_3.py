def solve(iv):
    # Work on a copy to avoid mutating the input
    intervals = [(a, b) for a, b in iv]
    # Sort intervals by start, then end
    intervals.sort(key=lambda x: (x[0], x[1]))
    merged = []
    for start, end in intervals:
        if not merged:
            merged.append([start, end])
        else:
            last_start, last_end = merged[-1]
            if start <= last_end:  # overlap or touch
                merged[-1][1] = max(last_end, end)
            else:
                merged.append([start, end])
    return merged
