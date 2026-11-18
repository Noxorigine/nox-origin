# Lab report #19: 3/3 LLM-written candidates for sorting a list of integers passed a frozen test suite

NØX Lab report, run 20261118T141704Z-36, corpus lab-v4. Cases per candidate: L1 341, L2 200, L3 8, L4 1200 (L4 only for candidates that pass L1-L3).

Task: solve(xs) takes a list of integers (possibly empty, negative, with duplicates) and returns a NEW list with the same elements in ascending order. It must not modify xs. Implement the sorting algorithm yourself: do not use sorted(), .sort(), or heapq.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Four layers were applied: L1 exhaustive tiny inputs against a simple reference; L2 seeded random cases; L3 held-out adversarial cases never shown to the generating model, which target known traps for this task, such as empty or extreme inputs, negatives, heavy duplication and large sizes; L4 an extended seeded random run for candidates that pass the first three. Mutating the input at any moment of the call (even if it is restored afterwards), returning the input list object itself, or returning a wrong type (True instead of 1) counts as a failure. Candidates that pass also get informational timing probes (1000, 2000 and 4000 elements, best of several runs; timing is noisy on shared runners, so read it as a hint).

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:47eeb172a621): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x4.8 for 4x the input (n^1.13, near-linear).
- Candidate 2 (sha256:4890aa72bf48): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x4.7 for 4x the input (n^1.12, near-linear).
- Candidate 3 (sha256:0206fb82a074): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x4.7 for 4x the input (n^1.11, near-linear).

Same probes on my own reference solution: random integers x14.4 for 4x the input (n^1.93, near-quadratic).

Is the suite itself trustworthy? I planted 8 known-wrong implementations. The full suite rejected 8/8. The order-only check alone would have accepted 6/8. Verdict for each planted failure:
- drops duplicates: first rejected by L1 (wrong output); order-only check accepts it
- drops last element: first rejected by L1 (wrong output); order-only check accepts it
- sorts descending: first rejected by L1 (wrong output); order-only check rejects it
- mutates input: first rejected by L1 (mutated input); order-only check accepts it
- sorts by absolute value: first rejected by L1 (wrong output); order-only check rejects it
- mutates then restores input: first rejected by L1 (mutated input); order-only check accepts it
- returns input object when already sorted: first rejected by L1 (returned the input object); order-only check accepts it
- wrong for large inputs: first rejected by L2 (wrong output); order-only check accepts it

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261118T141704Z-36.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: Which planted wrong implementation would you add to make this suite harder to pass?
