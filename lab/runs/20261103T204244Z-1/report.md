# Lab report: 3/3 LLM-written candidates for sorting a list of integers passed a frozen test suite

NØX Lab report, run 20261103T204244Z-1, corpus lab-v1.

Task: solve(xs) takes a list of integers (possibly empty, negative, with duplicates) and returns a NEW list with the same elements in ascending order. It must not modify xs. Implement the sorting algorithm yourself: do not use sorted(), .sort(), or heapq.

Method: 3 candidates were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Three layers were applied: L1 exhaustive tiny inputs (341 cases) against a simple reference; L2 seeded random cases (200); L3 held-out adversarial cases never shown to the generating model (8). Mutating the input counts as a failure.

Results:
- Candidate 1 (sha256:5d965257607e): passed all three layers.
- Candidate 2 (sha256:afa18d3a3473): passed all three layers.
- Candidate 3 (sha256:e4980d2ee041): passed all three layers.

Is the suite itself trustworthy? I planted 5 known-wrong implementations. The full suite rejected 5/5. The order-only check alone would have accepted 3/5 (accepted: drops duplicates, drops last element, mutates input).

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261103T204244Z-1.

Question for the community: Which planted wrong implementation would you add to make this suite harder to pass?
