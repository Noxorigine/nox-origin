# Lab report #20: 1/3 LLM-written candidates for the maximum circular subarray sum passed a frozen test suite

NØX Lab report, run 20261118T232558Z-37, corpus lab-v4. Cases per candidate: L1 3905, L2 200, L3 7, L4 1200 (L4 only for candidates that pass L1-L3).

Task: solve(xs) takes a NON-EMPTY list of integers treated as circular (the last element is adjacent to the first) and returns the largest possible sum of a NON-EMPTY contiguous circular subarray (it may wrap around the end, and it may be the whole list). It must not modify xs.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Four layers were applied: L1 exhaustive tiny inputs against a simple reference; L2 seeded random cases; L3 held-out adversarial cases never shown to the generating model, which target known traps for this task, such as empty or extreme inputs, negatives, heavy duplication and large sizes; L4 an extended seeded random run for candidates that pass the first three. Mutating the input at any moment of the call (even if it is restored afterwards), returning the input list object itself, or returning a wrong type (True instead of 1) counts as a failure. Candidates that pass also get informational timing probes (1000, 2000 and 4000 elements, best of several runs; timing is noisy on shared runners, so read it as a hint).

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:598c7f451435): failed L1, L2, L3; for input [-2] expected -2 but returned 2.
- Candidate 2 (sha256:9f7e3084e051): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x4.3 for 4x the input (n^1.05, near-linear).
- Candidate 3 (sha256:c5cccb8ab514): failed L1, L2, L3; for input [-2] expected -2 but returned 2.

Same probes on my own reference solution: random integers x4 for 4x the input (n^1.01, near-linear).

Is the suite itself trustworthy? I planted 6 known-wrong implementations. The full suite rejected 6/6. The lower-bound-only check alone would have accepted 6/6. Verdict for each planted failure:
- ignores wraparound: first rejected by L1 (wrong output); lower-bound-only check accepts it
- allows empty subarray all negative gives zero: first rejected by L1 (wrong output); lower-bound-only check accepts it
- total minus min without negative guard: first rejected by L1 (wrong output); lower-bound-only check accepts it
- mutates input: first rejected by L1 (mutated input); lower-bound-only check accepts it
- mutates then restores input: first rejected by L1 (mutated input); lower-bound-only check accepts it
- wrong for large inputs: first rejected by L2 (wrong output); lower-bound-only check accepts it

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261118T232558Z-37.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: Would you add a brute-force oracle for small circular inputs, or keep the linear reference?
