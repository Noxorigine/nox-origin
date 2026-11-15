def solve(xs):
    total = 0
    max_ending = max_sofar = xs[0]
    min_ending = min_sofar = xs[0]
    for i, x in enumerate(xs):
        total += x
        if i:
            max_ending = x if max_ending < 0 else max_ending + x
            max_sofar = max(max_sofar, max_ending)
            min_ending = x if min_ending > 0 else min_ending + x
            min_sofar = min(min_sofar, min_ending)
    wrap = total - min_sofar
    return max_sofar if wrap == 0 else max(max_sofar, wrap)
