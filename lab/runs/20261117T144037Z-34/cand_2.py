def solve(iv):
    # Create a sorted copy of the intervals by start, then by end
    intervals = sorted(iv, key=lambda x: (x[0], x[1]))
    merged = []
    for a, b in intervals:
        if not merged:
            merged.append([a, b])
        else:
            last_a, last_b = merged[-1]
            if a <= last_b:  # overlap or touch
                merged[-1][1] = max(last_b, b)
            else:
                merged.append([a, b])
    return merged
