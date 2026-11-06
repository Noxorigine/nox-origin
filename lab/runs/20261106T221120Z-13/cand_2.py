def solve(iv):
    # Create a sorted copy of the intervals by their start values
    intervals = sorted(iv, key=lambda x: x[0])
    merged = []
    for a, b in intervals:
        if not merged or a > merged[-1][1]:
            # No overlap or touching; start a new interval
            merged.append([a, b])
        else:
            # Overlap or touching; extend the previous interval's end if needed
            merged[-1][1] = max(merged[-1][1], b)
    return merged
