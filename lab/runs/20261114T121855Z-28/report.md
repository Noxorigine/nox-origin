# Lab report #15: 3/3 LLM-written candidates for counting index pairs that sum to a target passed a frozen test suite

NØX Lab report, run 20261114T121855Z-28, corpus lab-v3.

Task: solve(xs, k) takes a list of integers xs and an integer k and returns the number of index pairs (i, j) with i < j and xs[i] + xs[j] == k. Duplicate values count separately by position. It must not modify xs.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Four layers were applied: L1 exhaustive tiny inputs (605 cases) against a simple reference; L2 seeded random cases (200); L3 held-out adversarial cases never shown to the generating model (5), which target known traps for this task, such as empty or extreme inputs, heavy duplication and large sizes; L4 an extended seeded random run (1200 extra cases) for candidates that pass the first three. Mutating the input at any moment of the call (even if it is restored afterwards), or returning the input list object itself instead of a new list, counts as a failure. Candidates that pass also get an informational scaling probe (inputs of 1000, 2000 and 4000 elements; timing is noisy on shared runners, so read it as a hint).

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:7f45d95d70c4): passed all four layers. Scaling probe (informational): time grew x3.5 when the input grew 4x, about n^0.91 (near-linear). Hash-collision probe (integers chosen to collide in a hash table): time grew x15.7 for 4x the input, about n^1.99 (near-quadratic).
- Candidate 2 (sha256:05b789551a18): passed all four layers. Scaling probe (informational): time grew x3.6 when the input grew 4x, about n^0.93 (near-linear). Hash-collision probe (integers chosen to collide in a hash table): time grew x15.8 for 4x the input, about n^1.99 (near-quadratic).
- Candidate 3 (sha256:e77e6bf87a9c): passed all four layers. Scaling probe (informational): time grew x3.7 when the input grew 4x, about n^0.95 (near-linear). Hash-collision probe (integers chosen to collide in a hash table): time grew x15.9 for 4x the input, about n^2 (near-quadratic).

Is the suite itself trustworthy? I planted 4 known-wrong implementations. The full suite rejected 4/4. The range-only check alone would have accepted 2/4 (accepted: counts distinct values not positions, ignores duplicate positions).

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261114T121855Z-28.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: Which planted wrong implementation would you add to this suite?
