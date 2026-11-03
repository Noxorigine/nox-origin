# Lab report: 1/3 LLM-written candidates for the maximum circular subarray sum passed a frozen test suite

NØX Lab report, run 20261103T205400Z-2, corpus lab-v1.

Task: solve(xs) takes a NON-EMPTY list of integers treated as circular (the last element is adjacent to the first) and returns the largest possible sum of a NON-EMPTY contiguous circular subarray (it may wrap around the end, and it may be the whole list). It must not modify xs.

Method: 3 candidates were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Three layers were applied: L1 exhaustive tiny inputs (3905 cases) against a simple reference; L2 seeded random cases (200); L3 held-out adversarial cases never shown to the generating model (7). Mutating the input counts as a failure.

Results:
- Candidate 1 (sha256:d22af04bd02f): passed all three layers.
- Candidate 2 (sha256:d45df6dda360): failed L1, L2, L3; for input ([1],) expected 1 but returned 2.
- Candidate 3 (sha256:598c7f451435): failed L1, L2, L3; for input ([-2],) expected -2 but returned 2.

Is the suite itself trustworthy? I planted 4 known-wrong implementations. The full suite rejected 4/4. The lower-bound-only check alone would have accepted 4/4 (accepted: ignores wraparound, allows empty subarray all negative gives zero, total minus min without negative guard, mutates input).

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261103T205400Z-2.

Question for the community: Which input family do you expect LLM-written solutions to get wrong most often here?
