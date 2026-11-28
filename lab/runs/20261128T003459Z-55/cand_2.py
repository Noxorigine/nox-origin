def solve(iv):
    # Create a copy to avoid modifying the original list
    intervals = [(a, b) for a, b in iv]
    # Sort intervals by start point
    intervals.sort(key=lambda x: x[0])
    merged = []
    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            # Overlap or touch: extend the previous interval
            merged[-1][1] = max(merged[-1][1], end)
    return merged
