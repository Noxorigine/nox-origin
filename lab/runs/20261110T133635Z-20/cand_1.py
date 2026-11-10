def solve(iv):
    # Create a sorted copy of the intervals by start point
    sorted_intervals = sorted(iv, key=lambda x: x[0])
    merged = []
    for a, b in sorted_intervals:
        if not merged:
            merged.append([a, b])
        else:
            last = merged[-1]
            # Check if current interval overlaps or touches the last merged interval
            if a <= last[1]:
                # Merge by extending the end if needed
                if b > last[1]:
                    last[1] = b
            else:
                merged.append([a, b])
    return merged
