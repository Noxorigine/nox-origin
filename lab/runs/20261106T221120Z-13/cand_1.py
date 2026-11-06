def solve(iv):
    # Create a sorted copy of the intervals by their start values
    intervals = sorted(iv, key=lambda x: x[0])
    merged = []
    for a, b in intervals:
        if not merged or merged[-1][1] < a - 0:  # no overlap or touch
            merged.append([a, b])
        else:
            # Merge with the last interval
            merged[-1][1] = max(merged[-1][1], b)
    return merged
