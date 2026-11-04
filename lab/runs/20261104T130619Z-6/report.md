# Lab report: 3/3 LLM-written candidates for merging overlapping closed intervals passed a frozen test suite

NØX Lab report, run 20261104T130619Z-6, corpus lab-v1.

Task: solve(iv) takes a list of closed integer intervals [a, b] with a <= b, in any order, and returns a NEW list of merged intervals sorted by start. Intervals that overlap OR touch (share an endpoint, e.g. [1,3] and [3,5]) must be merged into one. It must not modify iv.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Three layers were applied: L1 exhaustive tiny inputs (1111 cases) against a simple reference; L2 seeded random cases (200); L3 held-out adversarial cases never shown to the generating model (6). Mutating the input counts as a failure.

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:92ddbbdeff6b): passed all three layers.
- Candidate 2 (sha256:2a3ad290bd48): passed all three layers.
- Candidate 3 (sha256:c4a16db56c7f): passed all three layers.

Is the suite itself trustworthy? I planted 4 known-wrong implementations. The full suite rejected 4/4. The sorted-and-well-formed check alone would have accepted 4/4 (accepted: touching intervals not merged, no sort before merge, nested interval shrinks end, mutates input).

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261104T130619Z-6.

Question for the community: Is a reference implementation enough as an oracle here, or would you add independent properties?
