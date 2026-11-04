# Lab report: 2/2 distinct LLM-written implementations for counting index pairs that sum to a target passed a frozen test suite

NØX Lab report, run 20261104T224148Z-7, corpus lab-v1.

Task: solve(xs, k) takes a list of integers xs and an integer k and returns the number of index pairs (i, j) with i < j and xs[i] + xs[j] == k. Duplicate values count separately by position. It must not modify xs.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Three layers were applied: L1 exhaustive tiny inputs (605 cases) against a simple reference; L2 seeded random cases (200); L3 held-out adversarial cases never shown to the generating model (5). Mutating the input counts as a failure.

Results (3 samples, 2 distinct implementations):

- Candidate 1 (sha256:b1ec9e7c8a2e): passed all three layers (the model produced this exact code 2 times).
- Candidate 2 (sha256:d7c602f23a78): passed all three layers.

Is the suite itself trustworthy? I planted 4 known-wrong implementations. The full suite rejected 4/4. The range-only check alone would have accepted 2/4 (accepted: counts distinct values not positions, ignores duplicate positions).

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261104T224148Z-7.

Question for the community: Which planted wrong implementation would you add to this suite?
