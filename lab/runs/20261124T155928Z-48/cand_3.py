def solve(iv):
    # Create a sorted copy of the intervals based on start then end
    sorted_intervals = sorted(iv, key=lambda x: (x[0], x[1]))
    merged = []
    for a, b in sorted_intervals:
        if not merged:
            merged.append([a, b])
        else:
            last = merged[-1]
            if a <= last[1] + 1:  # overlap or touch
                last[1] = max(last[1], b)
            else:
                merged.append([a, b])
    return merged
