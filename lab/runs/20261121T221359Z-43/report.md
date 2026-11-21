# Lab report #23: 3/3 LLM-written candidates for sorting a list of integers passed a frozen test suite

NØX Lab report, run 20261121T221359Z-43, corpus lab-v4.2. Cases per candidate: L1 341, L2 200, L3 8, L4 1200 (L4 only for candidates that pass L1-L3).

Task: solve(xs) takes a list of integers (possibly empty, negative, with duplicates) and returns a NEW list with the same elements in ascending order. It must not modify xs. Implement the sorting algorithm yourself: do not use sorted(), .sort(), or heapq.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O) and run in a sandbox (no network, unprivileged user, CPU and memory limits). Layers: L1 exhaustive tiny inputs against a simple reference; L2 seeded random cases; L3 held-out adversarial cases never shown to the generating model (traps such as empty or extreme inputs, negatives, duplication, large sizes); L4 an extended random run for candidates that pass L1-L3. Mutating the input at any moment (even if restored afterwards), returning the input object itself, or returning a wrong type (True for 1) is a failure. Passing candidates also get timing probes (1000, 2000, 4000 elements, best of several runs; noisy, read as a hint).

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:cc10bd1b042a): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x4.7 for 4x the input (n^1.11, near-linear).
- Candidate 2 (sha256:5fdaef240013): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x4.7 for 4x the input (n^1.12, near-linear).
- Candidate 3 (sha256:ce9dad6ee580): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x4.7 for 4x the input (n^1.11, near-linear).

Same probes on my own reference solution: random integers x6.1 for 4x the input (n^1.31, near-linear).

Hand-written expectations: 5 cases whose expected outputs I computed by hand, not with the reference. The reference agrees on 5/5; candidates matching all of them: 3/3.

Is the suite itself trustworthy? I planted 9 known-wrong implementations. The full suite rejected 9/9. The order-only check (called the weak check below) alone would have accepted 6/9. Verdict for each planted failure (first layer that rejects it, first failing input, and whether the weak check accepts it):

- drops duplicates: L1 on [-1, -1] (wrong output); weak check accepts it
- drops last element: L1 on [-1] (wrong output); weak check accepts it
- sorts descending: L1 on [-1, 0] (wrong output); weak check rejects it
- mutates input: L1 on [] (mutated input); weak check accepts it
- sorts by absolute value: L1 on [-1, 0] (wrong output); weak check rejects it
- mutates then restores input: L1 on [] (mutated input); weak check accepts it
- returns input object when already sorted: L1 on [] (returned the input object); weak check accepts it
- wrong for large inputs: L2 (wrong output); weak check accepts it
- mishandles values beyond 2 pow 40: L3 (wrong output); weak check rejects it

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261121T221359Z-43.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: Which planted wrong implementation would you add to make this suite harder to pass?
