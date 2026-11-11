# Lab report #12: 3/3 LLM-written candidates for sorting a list of integers passed a frozen test suite

NØX Lab report, run 20261111T124934Z-22, corpus lab-v3.

Task: solve(xs) takes a list of integers (possibly empty, negative, with duplicates) and returns a NEW list with the same elements in ascending order. It must not modify xs. Implement the sorting algorithm yourself: do not use sorted(), .sort(), or heapq.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Four layers were applied: L1 exhaustive tiny inputs (341 cases) against a simple reference; L2 seeded random cases (200); L3 held-out adversarial cases never shown to the generating model (8), which target known traps for this task, such as empty or extreme inputs, heavy duplication and large sizes; L4 an extended seeded random run (1200 extra cases) for candidates that pass the first three. Mutating the input at any moment of the call (even if it is restored afterwards), or returning the input list object itself instead of a new list, counts as a failure. Candidates that pass also get an informational scaling probe (inputs of 1000, 2000 and 4000 elements; timing is noisy on shared runners, so read it as a hint).

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:b98d221fe3bb): passed all four layers. Scaling probe (informational): time grew x4.6 when the input grew 4x, about n^1.11 (near-linear).
- Candidate 2 (sha256:ce9dad6ee580): passed all four layers. Scaling probe (informational): time grew x4.6 when the input grew 4x, about n^1.11 (near-linear).
- Candidate 3 (sha256:472d5a187ebe): passed all four layers. Scaling probe (informational): time grew x4.5 when the input grew 4x, about n^1.09 (near-linear).

Is the suite itself trustworthy? I planted 7 known-wrong implementations. The full suite rejected 7/7. The order-only check alone would have accepted 5/7 (accepted: drops duplicates, drops last element, mutates input, mutates then restores input, returns input object when already sorted).

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261111T124934Z-22.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: Which planted wrong implementation would you add to make this suite harder to pass?
