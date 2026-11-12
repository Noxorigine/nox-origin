# Lab report #14: 1/1 distinct LLM-written implementation for removing duplicates while keeping first occurrences in order passed a frozen test suite

NØX Lab report, run 20261112T224611Z-25, corpus lab-v3.

Task: solve(xs) takes a list of integers and returns a NEW list containing each distinct value once, in the order of its FIRST occurrence in xs. It must not modify xs.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Four layers were applied: L1 exhaustive tiny inputs (364 cases) against a simple reference; L2 seeded random cases (200); L3 held-out adversarial cases never shown to the generating model (5), which target known traps for this task, such as empty or extreme inputs, heavy duplication and large sizes; L4 an extended seeded random run (1200 extra cases) for candidates that pass the first three. Mutating the input at any moment of the call (even if it is restored afterwards), or returning the input list object itself instead of a new list, counts as a failure. Candidates that pass also get an informational scaling probe (inputs of 1000, 2000 and 4000 elements; timing is noisy on shared runners, so read it as a hint).

Results (3 samples, 1 distinct implementation):

- Candidate 1 (sha256:886d9744ec98): passed all four layers. Scaling probe (informational): time grew x4.8 when the input grew 4x, about n^1.14 (near-linear). Hash-collision probe (integers chosen to collide in a hash table): time grew x15.8 for 4x the input, about n^1.99 (near-quadratic). (the model produced this exact code 3 times.)

Is the suite itself trustworthy? I planted 6 known-wrong implementations. The full suite rejected 6/6. The uniqueness-only check alone would have accepted 5/6 (accepted: loses original order, keeps last occurrence, removes every repeated value, mutates then restores input, returns input object when no duplicates).

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261112T224611Z-25.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: Which planted wrong implementation would you add to this suite?
