"""NØX Lab - task specifications, reference solutions, test corpora, planted failures.
Corpus version: lab-v2 (v2 adds the aliasing check and the scaling probe). Everything here is deterministic (seeded)."""
import itertools
import random
from collections import Counter

VERSION = "lab-v2"


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
    "returns_input_object_when_already_sorted": "def solve(xs):\n    if all(xs[i] <= xs[i + 1] for i in range(len(xs) - 1)):\n        return xs\n    return sorted(xs)\n",
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
    "returns_input_object_when_no_duplicates": "def solve(xs):\n    if len(set(xs)) == len(xs):\n        return xs\n    out = []\n    seen = set()\n    for x in xs:\n        if x not in seen:\n            seen.add(x)\n            out.append(x)\n    return out\n",
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
    "returns_input_object_when_already_merged": "def solve(iv):\n    rows = [list(x) for x in iv]\n    if all(rows[i][1] < rows[i + 1][0] for i in range(len(rows) - 1)) and rows == sorted(rows):\n        return iv\n    out = []\n    for a, b in sorted(rows):\n        if out and a <= out[-1][1]:\n            out[-1][1] = max(out[-1][1], b)\n        else:\n            out.append([a, b])\n    return out\n",
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

# ------------------------------------------------------- max_circular_subarray
def ref_circ(xs):
    best = cur = xs[0]
    worst = cur_min = xs[0]
    for x in xs[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
        cur_min = min(x, cur_min + x)
        worst = min(worst, cur_min)
    total = sum(xs)
    if best < 0:
        return best
    return max(best, total - worst)

def tiny_circ():
    for n in range(1, 6):
        for combo in itertools.product([-2, -1, 0, 1, 2], repeat=n):
            yield (list(combo),)

def rand_circ(rng):
    for _ in range(200):
        yield ([rng.randint(-20, 20) for _ in range(rng.randint(1, 30))],)

def held_circ(rng):
    yield ([-5],)
    yield ([-3, -1, -2],)
    yield ([5, -3, 5],)
    yield ([8, -8, 9, -9, 10, -11, 12],)
    yield ([0, 0, 0],)
    yield ([rng.randint(-1000, 1000) for _ in range(2500)],)
    yield ([-1] * 1000,)

def weak_circ(args, out):
    return isinstance(out, int) and not isinstance(out, bool) and out >= max(args[0])

MUT_CIRC = {
    "ignores_wraparound": "def solve(xs):\n    best = cur = xs[0]\n    for x in xs[1:]:\n        cur = max(x, cur + x)\n        best = max(best, cur)\n    return best\n",
    "allows_empty_subarray_all_negative_gives_zero": "def solve(xs):\n    best = cur = 0\n    worst = cur_min = 0\n    for x in xs:\n        cur = max(0, cur + x)\n        best = max(best, cur)\n        cur_min = min(0, cur_min + x)\n        worst = min(worst, cur_min)\n    return max(best, sum(xs) - worst)\n",
    "total_minus_min_without_negative_guard": "def solve(xs):\n    best = cur = xs[0]\n    worst = cur_min = xs[0]\n    for x in xs[1:]:\n        cur = max(x, cur + x)\n        best = max(best, cur)\n        cur_min = min(x, cur_min + x)\n        worst = min(worst, cur_min)\n    return max(best, sum(xs) - worst)\n",
    "mutates_input": "def solve(xs):\n    xs.sort()\n    return sum(x for x in xs if x > 0) if xs[-1] > 0 else xs[-1]\n",
}

# ------------------------------------------------------------- split_csv_line
def ref_csv(line):
    fields, cur, i, quoted = [], [], 0, False
    n = len(line)
    while i < n:
        ch = line[i]
        if quoted:
            if ch == '"':
                if i + 1 < n and line[i + 1] == '"':
                    cur.append('"')
                    i += 1
                else:
                    quoted = False
            else:
                cur.append(ch)
        elif ch == '"':
            quoted = True
        elif ch == ",":
            fields.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
        i += 1
    fields.append("".join(cur))
    return fields

def _serialize(fields):
    parts = []
    for f in fields:
        if any(c in f for c in ',"'):
            parts.append('"' + f.replace('"', '""') + '"')
        else:
            parts.append(f)
    return ",".join(parts)

def tiny_csv():
    alphabet = ["a", ",", '"', " "]
    pool = [""] + [a + b for a in alphabet for b in [""] + alphabet]
    pool = list(dict.fromkeys(pool))
    for n in range(1, 3):
        for combo in itertools.product(pool, repeat=n):
            yield (_serialize(list(combo)),)

def rand_csv(rng):
    alphabet = ["a", "b", ",", '"', " ", "x"]
    for _ in range(200):
        fields = ["".join(rng.choice(alphabet) for _ in range(rng.randint(0, 6))) for _ in range(rng.randint(1, 5))]
        yield (_serialize(fields),)

def held_csv(rng):
    yield ("",)
    yield (",",)
    yield (",,,",)
    yield ('"",""',)
    yield ('"a,b","c""d",e',)
    yield ('" leading and trailing ", x ',)
    yield (",".join(["f%d" % i for i in range(2000)]),)
    yield ('"""",""""""',)

def weak_csv(args, out):
    return isinstance(out, list) and all(isinstance(x, str) for x in out) and len(out) >= 1

MUT_CSV = {
    "naive_split_on_commas": "def solve(line):\n    return line.split(',')\n",
    "keeps_doubled_quotes": "def solve(line):\n    out, cur, q = [], '', False\n    for ch in line:\n        if ch == '\"':\n            q = not q\n            cur += ch if False else ''\n        elif ch == ',' and not q:\n            out.append(cur)\n            cur = ''\n        else:\n            cur += ch\n    out.append(cur)\n    return out\n",
    "strips_whitespace_in_fields": "def solve(line):\n    out, cur, q, i = [], '', False, 0\n    while i < len(line):\n        ch = line[i]\n        if q:\n            if ch == '\"':\n                if i + 1 < len(line) and line[i + 1] == '\"':\n                    cur += '\"'\n                    i += 1\n                else:\n                    q = False\n            else:\n                cur += ch\n        elif ch == '\"':\n            q = True\n        elif ch == ',':\n            out.append(cur.strip())\n            cur = ''\n        else:\n            cur += ch\n        i += 1\n    out.append(cur.strip())\n    return out\n",
    "drops_trailing_empty_field": "def solve(line):\n    out, cur, q, i = [], '', False, 0\n    while i < len(line):\n        ch = line[i]\n        if q:\n            if ch == '\"':\n                if i + 1 < len(line) and line[i + 1] == '\"':\n                    cur += '\"'\n                    i += 1\n                else:\n                    q = False\n            else:\n                cur += ch\n        elif ch == '\"':\n            q = True\n        elif ch == ',':\n            out.append(cur)\n            cur = ''\n        else:\n            cur += ch\n        i += 1\n    if cur != '':\n        out.append(cur)\n    return out or ['']\n",
}

# ------------------------------------------------------------- next_permutation
def ref_nextperm(xs):
    a = list(xs)
    i = len(a) - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i < 0:
        return sorted(a)
    j = len(a) - 1
    while a[j] <= a[i]:
        j -= 1
    a[i], a[j] = a[j], a[i]
    a[i + 1:] = reversed(a[i + 1:])
    return a

def tiny_nextperm():
    for xs in _tiny_lists(5, [0, 1, 2]):
        yield (xs,)

def rand_nextperm(rng):
    for _ in range(200):
        yield ([rng.randint(0, 6) for _ in range(rng.randint(0, 12))],)

def held_nextperm(rng):
    yield ([],)
    yield ([3, 2, 1],)
    yield ([1, 1, 1],)
    yield ([1, 5, 1],)
    yield ([2, 3, 1, 3, 3],)
    yield (list(range(2000, 0, -1)),)
    yield ([1] + list(range(1000, 1, -1)),)

def weak_nextperm(args, out):
    return isinstance(out, list) and Counter(out) == Counter(args[0])

MUT_NEXTPERM = {
    "last_permutation_not_wrapped": "def solve(xs):\n    a = list(xs)\n    i = len(a) - 2\n    while i >= 0 and a[i] >= a[i + 1]:\n        i -= 1\n    if i < 0:\n        return a\n    j = len(a) - 1\n    while a[j] <= a[i]:\n        j -= 1\n    a[i], a[j] = a[j], a[i]\n    a[i + 1:] = reversed(a[i + 1:])\n    return a\n",
    "suffix_not_reversed": "def solve(xs):\n    a = list(xs)\n    i = len(a) - 2\n    while i >= 0 and a[i] >= a[i + 1]:\n        i -= 1\n    if i < 0:\n        return sorted(a)\n    j = len(a) - 1\n    while a[j] <= a[i]:\n        j -= 1\n    a[i], a[j] = a[j], a[i]\n    return a\n",
    "strict_comparison_breaks_duplicates": "def solve(xs):\n    a = list(xs)\n    i = len(a) - 2\n    while i >= 0 and a[i] > a[i + 1]:\n        i -= 1\n    if i < 0:\n        return sorted(a)\n    j = len(a) - 1\n    while a[j] <= a[i]:\n        j -= 1\n    a[i], a[j] = a[j], a[i]\n    a[i + 1:] = reversed(a[i + 1:])\n    return a\n",
    "mutates_input": "def solve(xs):\n    i = len(xs) - 2\n    while i >= 0 and xs[i] >= xs[i + 1]:\n        i -= 1\n    if i < 0:\n        xs.sort()\n        return xs\n    j = len(xs) - 1\n    while xs[j] <= xs[i]:\n        j -= 1\n    xs[i], xs[j] = xs[j], xs[i]\n    xs[i + 1:] = reversed(xs[i + 1:])\n    return xs\n",
}


# ---------------------------------------------------------------- scaling probe inputs
def scale_sort(n, rng):
    return ([rng.randint(-10**6, 10**6) for _ in range(n)],)

def scale_dedupe(n, rng):
    return ([rng.randint(0, n) for _ in range(n)],)

def scale_merge(n, rng):
    items = []
    for _ in range(n):
        a = rng.randint(0, 50 * n)
        items.append([a, a + rng.randint(0, 20)])
    return (items,)

def scale_pairs(n, rng):
    return ([rng.randint(0, n) for _ in range(n)], n)

def scale_circ(n, rng):
    return ([rng.randint(-100, 100) for _ in range(n)],)

def scale_csv(n, rng):
    fields = ["a,b" if i % 7 == 0 else "x%d" % i for i in range(n)]
    return (_serialize(fields),)

def scale_nextperm(n, rng):
    return ([rng.randint(0, 5) for _ in range(n)],)

SPECS = {
    "max_circular_subarray": {
        "scale": scale_circ,
        "title": "the maximum circular subarray sum",
        "signature": "solve(xs)",
        "description": "solve(xs) takes a NON-EMPTY list of integers treated as circular (the last element is adjacent to the first) and returns the largest possible sum of a NON-EMPTY contiguous circular subarray (it may wrap around the end, and it may be the whole list). It must not modify xs.",
        "forbidden": [],
        "ref": ref_circ, "tiny": tiny_circ, "rand": rand_circ, "held": held_circ, "weak": weak_circ,
        "mutants": MUT_CIRC, "weak_name": "lower-bound-only check",
        "questions": ["Which input family do you expect LLM-written solutions to get wrong most often here?",
                      "Would you add a brute-force oracle for small circular inputs, or keep the linear reference?"],
    },
    "split_csv_line": {
        "scale": scale_csv,
        "title": "parsing one CSV line with quoted fields",
        "signature": "solve(line)",
        "description": "solve(line) takes ONE valid CSV line (RFC 4180 style: fields separated by commas; a field may be wrapped in double quotes, in which case it may contain commas, and a doubled quote \"\" inside it means one literal quote) and returns the list of field strings with the quoting removed. Whitespace is part of the field and must be kept. An empty line gives [\"\"]; a trailing comma gives a trailing empty field. Do not import any module.",
        "forbidden": [],
        "ref": ref_csv, "tiny": tiny_csv, "rand": rand_csv, "held": held_csv, "weak": weak_csv,
        "mutants": MUT_CSV, "weak_name": "type-only check",
        "questions": ["Which malformed-input policy would you pick for a parser like this, and why?",
                      "What edge case would you add to the held-out set for quoted fields?"],
    },
    "next_permutation": {
        "scale": scale_nextperm,
        "title": "computing the next lexicographic permutation",
        "signature": "solve(xs)",
        "description": "solve(xs) takes a list of integers (possibly empty, possibly with duplicates) and returns a NEW list: the next permutation of xs in lexicographic order, or the ascending sorted list if xs is already the last (largest) permutation. It must not modify xs.",
        "forbidden": [],
        "ref": ref_nextperm, "tiny": tiny_nextperm, "rand": rand_nextperm, "held": held_nextperm, "weak": weak_nextperm,
        "mutants": MUT_NEXTPERM, "weak_name": "same-elements-only check",
        "questions": ["Would you test this against a brute-force enumeration of permutations, and up to what size?",
                      "Which planted wrong implementation would you add to this suite?"],
    },
    "sort_ints": {
        "scale": scale_sort,
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
        "scale": scale_dedupe,
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
        "scale": scale_merge,
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
        "scale": scale_pairs,
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
SPEC_ORDER = ["sort_ints", "max_circular_subarray", "split_csv_line", "dedupe_keep_first", "next_permutation", "merge_intervals", "count_pairs_sum"]
