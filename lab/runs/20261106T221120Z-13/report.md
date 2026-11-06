# Lab report: 3/3 LLM-written candidates for merging overlapping closed intervals passed a frozen test suite

NØX Lab report, run 20261106T221120Z-13, corpus lab-v2.

Task: solve(iv) takes a list of closed integer intervals [a, b] with a <= b, in any order, and returns a NEW list of merged intervals sorted by start. Intervals that overlap OR touch (share an endpoint, e.g. [1,3] and [3,5]) must be merged into one. It must not modify iv.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Four layers were applied: L1 exhaustive tiny inputs (1111 cases) against a simple reference; L2 seeded random cases (200); L3 held-out adversarial cases never shown to the generating model (6), which target known traps for this task, such as empty or extreme inputs, heavy duplication and large sizes; L4 an extended seeded random run (1200 extra cases) for candidates that pass the first three. Mutating the input, or returning the input list object itself instead of a new list, counts as a failure. Candidates that pass also get an informational scaling probe (inputs of 1000, 2000 and 4000 elements; timing is noisy on shared runners, so read it as a hint).

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:5b9a29ebab8d): passed all four layers. Scaling probe (informational): time grew x4.7 when the input grew 4x, about n^1.12 (near-linear).
- Candidate 2 (sha256:3baa94036e83): passed all four layers. Scaling probe (informational): time grew x4.9 when the input grew 4x, about n^1.14 (near-linear).
- Candidate 3 (sha256:cd6fc45c7d02): passed all four layers. Scaling probe (informational): time grew x5 when the input grew 4x, about n^1.17 (near-linear).

Is the suite itself trustworthy? I planted 5 known-wrong implementations. The full suite rejected 5/5. The sorted-and-well-formed check alone would have accepted 5/5 (accepted: touching intervals not merged, no sort before merge, nested interval shrinks end, mutates input, returns input object when already merged).

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261106T221120Z-13.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: Is a reference implementation enough as an oracle here, or would you add independent properties?
