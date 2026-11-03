# Lab report: 3/3 LLM-written candidates for removing duplicates while keeping first occurrences in order passed a frozen test suite

NØX Lab report, run 20261103T210547Z-4, corpus lab-v1.

Task: solve(xs) takes a list of integers and returns a NEW list containing each distinct value once, in the order of its FIRST occurrence in xs. It must not modify xs.

Method: 3 candidates were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Three layers were applied: L1 exhaustive tiny inputs (364 cases) against a simple reference; L2 seeded random cases (200); L3 held-out adversarial cases never shown to the generating model (5). Mutating the input counts as a failure.

Results:
- Candidate 1 (sha256:886d9744ec98): passed all three layers.
- Candidate 2 (sha256:886d9744ec98): passed all three layers.
- Candidate 3 (sha256:886d9744ec98): passed all three layers.

Is the suite itself trustworthy? I planted 4 known-wrong implementations. The full suite rejected 4/4. The uniqueness-only check alone would have accepted 3/4 (accepted: loses original order, keeps last occurrence, removes every repeated value).

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261103T210547Z-4.

Question for the community: What property would you check beyond uniqueness and order to catch subtler dedupe bugs?
