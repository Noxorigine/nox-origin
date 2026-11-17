def solve(iv):
    # Work on a copy to avoid modifying the input
    intervals = list(iv)
    if not intervals:
        return []
    # Sort intervals by start point
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0][:]]
    for a, b in intervals[1:]:
        last = merged[-1]
        if a <= last[1] + 0:  # overlapping or touching (a <= last[1])
            # Merge by extending the end if needed
            if b > last[1]:
                last[1] = b
        else:
            merged.append([a, b])
    return merged
