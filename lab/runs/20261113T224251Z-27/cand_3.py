def solve(iv):
    intervals = sorted(iv, key=lambda x: x[0])
    merged = []
    for a, b in intervals:
        if not merged or a > merged[-1][1] + 0:
            merged.append([a, b])
        else:
            merged[-1][1] = max(merged[-1][1], b)
    return merged
