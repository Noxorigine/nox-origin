def solve(iv):
    # Create a copy to avoid modifying the input
    intervals = sorted(iv, key=lambda x: x[0])
    merged = []
    for a, b in intervals:
        if not merged or a > merged[-1][1] + 0:  # no overlap or touch
            merged.append([a, b])
        else:
            # Overlap or touch: extend the last interval
            merged[-1][1] = max(merged[-1][1], b)
    return merged
