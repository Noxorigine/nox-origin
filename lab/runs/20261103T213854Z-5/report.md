# Lab report: 0/3 LLM-written candidates for computing the next lexicographic permutation passed a frozen test suite

NØX Lab report, run 20261103T213854Z-5, corpus lab-v1.

Task: solve(xs) takes a list of integers (possibly empty, possibly with duplicates) and returns a NEW list: the next permutation of xs in lexicographic order, or the ascending sorted list if xs is already the last (largest) permutation. It must not modify xs.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Three layers were applied: L1 exhaustive tiny inputs (364 cases) against a simple reference; L2 seeded random cases (200); L3 held-out adversarial cases never shown to the generating model (7). Mutating the input counts as a failure.

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:b9ca389e7609): failed L1, L2, L3; input ([],) -> exception:IndexError.
- Candidate 2 (sha256:70992e472d2f): failed L1, L2, L3; input ([],) -> exception:IndexError.
- Candidate 3 (sha256:9e7b6125c8c8): failed L1, L2, L3; input ([],) -> exception:IndexError.

Is the suite itself trustworthy? I planted 4 known-wrong implementations. The full suite rejected 4/4. The same-elements-only check alone would have accepted 3/4 (accepted: last permutation not wrapped, suffix not reversed, mutates input).

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261103T213854Z-5.

Question for the community: Which planted wrong implementation would you add to this suite?
