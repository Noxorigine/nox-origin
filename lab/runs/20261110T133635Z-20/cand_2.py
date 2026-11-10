def solve(iv):
    merged = []
    # Create a sorted copy of intervals by start then end
    sorted_intervals = sorted(iv, key=lambda x: (x[0], x[1]))
    for a, b in sorted_intervals:
        if not merged:
            merged.append([a, b])
        else:
            last = merged[-1]
            # If current interval overlaps or touches the last merged interval
            if a <= last[1]:
                # Extend the last interval's end if needed
                if b > last[1]:
                    last[1] = b
            else:
                merged.append([a, b])
    return merged
