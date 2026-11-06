# Lab report: 0/3 LLM-written candidates for computing the next lexicographic permutation passed a frozen test suite

NØX Lab report, run 20261106T130224Z-12, corpus lab-v2.

Task: solve(xs) takes a list of integers (possibly empty, possibly with duplicates) and returns a NEW list: the next permutation of xs in lexicographic order, or the ascending sorted list if xs is already the last (largest) permutation. It must not modify xs.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Four layers were applied: L1 exhaustive tiny inputs (364 cases) against a simple reference; L2 seeded random cases (200); L3 held-out adversarial cases never shown to the generating model (7), which target known traps for this task, such as empty or extreme inputs, heavy duplication and large sizes; L4 an extended seeded random run (1000+ extra cases), reserved for candidates that pass the first three. Mutating the input, or returning the input list object itself instead of a new list, counts as a failure. Candidates that pass also get an informational scaling probe (inputs of 1000, 2000 and 4000 elements; timing is noisy on shared runners, so read it as a hint).

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:9e7b6125c8c8): failed L1, L2, L3; for input [] it raised IndexError.
- Candidate 2 (sha256:70992e472d2f): failed L1, L2, L3; for input [] it raised IndexError.
- Candidate 3 (sha256:7fe166022f70): failed L1, L2, L3; for input [] it raised IndexError.

Is the suite itself trustworthy? I planted 4 known-wrong implementations. The full suite rejected 4/4. The same-elements-only check alone would have accepted 3/4 (accepted: last permutation not wrapped, suffix not reversed, mutates input).

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261106T130224Z-12.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: Which planted wrong implementation would you add to this suite?
