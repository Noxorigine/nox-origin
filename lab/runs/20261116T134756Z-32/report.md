# Lab report #17: 1/1 distinct LLM-written implementation for removing duplicates while keeping first occurrences in order passed a frozen test suite

NØX Lab report, run 20261116T134756Z-32, corpus lab-v4. Cases per candidate: L1 364, L2 200, L3 7, L4 1200 (L4 only for candidates that pass L1-L3).

Task: solve(xs) takes a list of integers and returns a NEW list containing each distinct value once, in the order of its FIRST occurrence in xs. It must not modify xs.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Four layers were applied: L1 exhaustive tiny inputs against a simple reference; L2 seeded random cases; L3 held-out adversarial cases never shown to the generating model, which target known traps for this task, such as empty or extreme inputs, negatives, heavy duplication and large sizes; L4 an extended seeded random run for candidates that pass the first three. Mutating the input at any moment of the call (even if it is restored afterwards), returning the input list object itself, or returning a wrong type (True instead of 1) counts as a failure. Candidates that pass also get informational timing probes (1000, 2000 and 4000 elements, best of several runs; timing is noisy on shared runners, so read it as a hint).

Results (3 samples, 1 distinct implementation):

- Candidate 1 (sha256:886d9744ec98): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x5.1 for 4x the input (n^1.18, near-linear); hash-colliding integers x15.7 for 4x the input (n^1.99, near-quadratic). (the model produced this exact code 3 times.)

Same probes on my own reference solution: random integers x4.7 for 4x the input (n^1.12, near-linear); hash-colliding integers x15.8 for 4x the input (n^1.99, near-quadratic). The reference degrades on colliding integers too, so that probe measures the hash container, not the candidate's own algorithm.

Is the suite itself trustworthy? I planted 10 known-wrong implementations. The full suite rejected 10/10. The uniqueness-only check alone would have accepted 8/10. Verdict for each planted failure:
- loses original order: first rejected by L1 (wrong output); uniqueness-only check accepts it
- keeps last occurrence: first rejected by L1 (wrong output); uniqueness-only check accepts it
- removes every repeated value: first rejected by L1 (wrong output); uniqueness-only check accepts it
- returns input unchanged: first rejected by L1 (wrong output); uniqueness-only check rejects it
- mutates then restores input: first rejected by L1 (mutated input); uniqueness-only check accepts it
- returns input object when no duplicates: first rejected by L1 (returned the input object); uniqueness-only check accepts it
- assumes sorted input: first rejected by L1 (wrong output); uniqueness-only check rejects it
- treats negatives as positives: first rejected by L3 (wrong output); uniqueness-only check accepts it
- returns bools for zero and one: first rejected by L1 (wrong output); uniqueness-only check accepts it
- wrong for large inputs: first rejected by L2 (wrong output); uniqueness-only check accepts it

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261116T134756Z-32.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: Which planted wrong implementation would you add to this suite?
