"""NØX Lab - task specifications, reference solutions, test corpora, planted failures.
Corpus version: lab-v1. Everything here is deterministic (seeded)."""
import itertools
import random
from collections import Counter

VERSION = "lab-v1"


def _tiny_lists(length, alphabet):
    for n in range(length + 1):
        for combo in itertools.product(alphabet, repeat=n):
            yield list(combo)


# ---------------------------------------------------------------- sort_ints
def ref_sort(xs):
    return sorted(xs)

def tiny_sort():
    for xs in _tiny_lists(4, [-1, 0, 1, 2]):
        yield (xs,)

def rand_sort(rng):
    for _ in range(200):
        yield ([rng.randint(-50, 50) for _ in range(rng.randint(0, 40))],)

def held_sort(rng):
    yield ([],)
    yield ([5],)
    yield ([1000] * 50,)
    yield (list(range(300, 0, -1)),)
    yield ([2**62, -2**62, 0, 2**62, -1],)
    yield ([rng.randint(-10**9, 10**9) for _ in range(3000)],)
    yield ([0, 1] * 500,)
    yield ([-3, -3, -1, -2, -2, -2],)

def weak_sort(args, out):
    return isinstance(out, list) and all(out[i] <= out[i + 1] for i in range(len(out) - 1))

MUT_SORT = {
    "drops_duplicates": "def solve(xs):\n    return sorted(set(xs))\n",
    "drops_last_element": "def solve(xs):\n    return sorted(xs)[:-1]\n",
    "sorts_descending": "def solve(xs):\n    return sorted(xs, reverse=True)\n",
    "mutates_input": "def solve(xs):\n    xs.sort()\n    return xs\n",
    "sorts_by_absolute_value": "def solve(xs):\n    return sorted(xs, key=abs)\n",
}

# ----------------------------------------------------------- dedupe_keep_first
def ref_dedupe(xs):
    seen = set()
    out = []
    for x in xs:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def tiny_dedupe():
    for xs in _tiny_lists(5, [0, 1, 2]):
        yield (xs,)

def rand_dedupe(rng):
    for _ in range(200):
        yield ([rng.randint(0, 10) for _ in range(rng.randint(0, 40))],)

def held_dedupe(rng):
    yield ([],)
    yield ([7] * 100,)
    yield ([rng.randint(0, 50) for _ in range(3000)],)
    yield ([2**61, -5, 2**61, -5, 0],)
    yield (list(range(500)) + list(range(500)),)

def weak_dedupe(args, out):
    return isinstance(out, list) and len(out) == len(set(out)) and set(out) <= set(args[0])

MUT_DEDUPE = {
    "loses_original_order": "def solve(xs):\n    return sorted(set(xs))\n",
    "keeps_last_occurrence": "def solve(xs):\n    out = []\n    for i, x in enumerate(xs):\n        if x not in xs[i + 1:]:\n            out.append(x)\n    return out\n",
    "removes_every_repeated_value": "def solve(xs):\n    return [x for x in xs if xs.count(x) == 1]\n",
    "returns_input_unchanged": "def solve(xs):\n    return list(xs)\n",
}

# -------------------------------------------------------------- merge_intervals
def ref_merge(iv):
    out = []
    for a, b in sorted([list(x) for x in iv]):
        if out and a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out

def tiny_merge():
    pool = [[a, b] for a in range(4) for b in range(a, 4)]
    for n in range(4):
        for combo in itertools.product(pool, repeat=n):
            yield ([list(x) for x in combo],)

def rand_merge(rng):
    for _ in range(200):
        items = []
        for _ in range(rng.randint(0, 30)):
            a = rng.randint(0, 100)
            items.append([a, a + rng.randint(0, 15)])
        yield (items,)

def held_merge(rng):
    yield ([],)
    yield ([[1, 1]],)
    yield ([[1, 10], [2, 3], [4, 5]],)
    yield ([[2, 2]] * 20,)
    yield ([[-5, -1], [-2, 4], [4, 9]],)
    items = []
    for _ in range(1500):
        a = rng.randint(0, 100000)
        items.append([a, a + rng.randint(0, 30)])
    yield (items,)

def weak_merge(args, out):
    try:
        rows = [list(x) for x in out]
    except TypeError:
        return False
    return all(len(r) == 2 and r[0] <= r[1] for r in rows) and all(rows[i][0] <= rows[i + 1][0] for i in range(len(rows) - 1))

MUT_MERGE = {
    "touching_intervals_not_merged": "def solve(iv):\n    out = []\n    for a, b in sorted([list(x) for x in iv]):\n        if out and a < out[-1][1]:\n            out[-1][1] = max(out[-1][1], b)\n        else:\n            out.append([a, b])\n    return out\n",
    "no_sort_before_merge": "def solve(iv):\n    out = []\n    for a, b in [list(x) for x in iv]:\n        if out and a <= out[-1][1]:\n            out[-1][1] = max(out[-1][1], b)\n        else:\n            out.append([a, b])\n    return out\n",
    "nested_interval_shrinks_end": "def solve(iv):\n    out = []\n    for a, b in sorted([list(x) for x in iv]):\n        if out and a <= out[-1][1]:\n            out[-1][1] = b\n        else:\n            out.append([a, b])\n    return out\n",
    "mutates_input": "def solve(iv):\n    iv.sort()\n    out = []\n    for a, b in iv:\n        if out and a <= out[-1][1]:\n            out[-1][1] = max(out[-1][1], b)\n        else:\n            out.append([a, b])\n    return out\n",
}

# ------------------------------------------------------------- count_pairs_sum
def ref_pairs(xs, k):
    seen = Counter()
    total = 0
    for x in xs:
        total += seen[k - x]
        seen[x] += 1
    return total

def tiny_pairs():
    for xs in _tiny_lists(4, [0, 1, 2]):
        for k in range(5):
            yield (xs, k)

def rand_pairs(rng):
    for _ in range(200):
        yield ([rng.randint(0, 15) for _ in range(rng.randint(0, 40))], rng.randint(0, 30))

def held_pairs(rng):
    yield ([], 0)
    yield ([0] * 3000, 0)
    yield ([5], 10)
    yield ([-2, 2, -2, 2, 0, 0], 0)
    yield ([rng.randint(0, 100) for _ in range(3000)], 100)

def weak_pairs(args, out):
    n = len(args[0])
    return isinstance(out, int) and not isinstance(out, bool) and 0 <= out <= n * (n - 1) // 2

MUT_PAIRS = {
    "counts_distinct_values_not_positions": "def solve(xs, k):\n    s = set(xs)\n    return sum(1 for x in s if k - x in s and x < k - x)\n",
    "counts_ordered_pairs_twice": "def solve(xs, k):\n    return 2 * sum(1 for i in range(len(xs)) for j in range(i + 1, len(xs)) if xs[i] + xs[j] == k)\n",
    "pairs_an_element_with_itself": "def solve(xs, k):\n    return sum(1 for i in range(len(xs)) for j in range(i, len(xs)) if xs[i] + xs[j] == k)\n",
    "ignores_duplicate_positions": "def solve(xs, k):\n    s = set(xs)\n    return sum(1 for x in s for y in s if x < y and x + y == k)\n",
}

SPECS = {
    "sort_ints": {
        "title": "sorting a list of integers",
        "signature": "solve(xs)",
        "description": "solve(xs) takes a list of integers (possibly empty, negative, with duplicates) and returns a NEW list with the same elements in ascending order. It must not modify xs. Implement the sorting algorithm yourself: do not use sorted(), .sort(), or heapq.",
        "forbidden": ["sorted", "sort"],
        "ref": ref_sort, "tiny": tiny_sort, "rand": rand_sort, "held": held_sort, "weak": weak_sort,
        "mutants": MUT_SORT, "weak_name": "order-only check",
        "questions": ["Which planted wrong implementation would you add to make this suite harder to pass?",
                      "For sorting, is the multiset-preservation check enough, or would you also test stability on keyed records?"],
    },
    "dedupe_keep_first": {
        "title": "removing duplicates while keeping first occurrences in order",
        "signature": "solve(xs)",
        "description": "solve(xs) takes a list of integers and returns a NEW list containing each distinct value once, in the order of its FIRST occurrence in xs. It must not modify xs.",
        "forbidden": [],
        "ref": ref_dedupe, "tiny": tiny_dedupe, "rand": rand_dedupe, "held": held_dedupe, "weak": weak_dedupe,
        "mutants": MUT_DEDUPE, "weak_name": "uniqueness-only check",
        "questions": ["What property would you check beyond uniqueness and order to catch subtler dedupe bugs?",
                      "Which planted wrong implementation would you add to this suite?"],
    },
    "merge_intervals": {
        "title": "merging overlapping closed intervals",
        "signature": "solve(iv)",
        "description": "solve(iv) takes a list of closed integer intervals [a, b] with a <= b, in any order, and returns a NEW list of merged intervals sorted by start. Intervals that overlap OR touch (share an endpoint, e.g. [1,3] and [3,5]) must be merged into one. It must not modify iv.",
        "forbidden": [],
        "ref": ref_merge, "tiny": tiny_merge, "rand": rand_merge, "held": held_merge, "weak": weak_merge,
        "mutants": MUT_MERGE, "weak_name": "sorted-and-well-formed check",
        "questions": ["Which edge case would you add to the held-out set for interval merging?",
                      "Is a reference implementation enough as an oracle here, or would you add independent properties?"],
    },
    "count_pairs_sum": {
        "title": "counting index pairs that sum to a target",
        "signature": "solve(xs, k)",
        "description": "solve(xs, k) takes a list of integers xs and an integer k and returns the number of index pairs (i, j) with i < j and xs[i] + xs[j] == k. Duplicate values count separately by position. It must not modify xs.",
        "forbidden": [],
        "ref": ref_pairs, "tiny": tiny_pairs, "rand": rand_pairs, "held": held_pairs, "weak": weak_pairs,
        "mutants": MUT_PAIRS, "weak_name": "range-only check",
        "questions": ["Would you test this with a brute-force oracle or with algebraic properties, and why?",
                      "Which planted wrong implementation would you add to this suite?"],
    },
}
SPEC_ORDER = ["sort_ints", "dedupe_keep_first", "merge_intervals", "count_pairs_sum"]
