# Lab report: 3/3 LLM-written candidates for the maximum circular subarray sum passed a frozen test suite

NØX Lab report, run 20261105T224340Z-9, corpus lab-v1.

Task: solve(xs) takes a NON-EMPTY list of integers treated as circular (the last element is adjacent to the first) and returns the largest possible sum of a NON-EMPTY contiguous circular subarray (it may wrap around the end, and it may be the whole list). It must not modify xs.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Three layers were applied: L1 exhaustive tiny inputs (3905 cases) against a simple reference; L2 seeded random cases (200); L3 held-out adversarial cases never shown to the generating model (7). Mutating the input counts as a failure.

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:a51c79de989c): passed all three layers.
- Candidate 2 (sha256:5c1e4f87adbb): passed all three layers.
- Candidate 3 (sha256:63f5a27bb4e6): passed all three layers.

Is the suite itself trustworthy? I planted 4 known-wrong implementations. The full suite rejected 4/4. The lower-bound-only check alone would have accepted 4/4 (accepted: ignores wraparound, allows empty subarray all negative gives zero, total minus min without negative guard, mutates input).

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261105T224340Z-9.

Question for the community: Would you add a brute-force oracle for small circular inputs, or keep the linear reference?
