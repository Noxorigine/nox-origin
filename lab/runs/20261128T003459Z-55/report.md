# Lab report #29: 3/3 LLM-written candidates for merging overlapping closed intervals passed a frozen test suite

NØX Lab report, run 20261128T003459Z-55, corpus lab-v4.2. Cases per candidate: L1 1111, L2 200, L3 6, L4 1200 (L4 only for candidates that pass L1-L3).

Task: solve(iv) takes a list of closed integer intervals [a, b] with a <= b, in any order, and returns a NEW list of merged intervals sorted by start. Intervals that overlap OR touch (share an endpoint, e.g. [1,3] and [3,5]) must be merged into one. It must not modify iv.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O) and run in a sandbox (no network, unprivileged user, CPU and memory limits). Layers: L1 exhaustive tiny inputs against a simple reference; L2 seeded random cases; L3 held-out adversarial cases never shown to the generating model (traps such as empty or extreme inputs, negatives, duplication, large sizes); L4 an extended random run for candidates that pass L1-L3. Mutating the input at any moment (even if restored afterwards), returning the input object itself, or returning a wrong type (True for 1) is a failure. Passing candidates also get timing probes (1000, 2000, 4000 elements, best of several runs; noisy, read as a hint).

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:5eeea8fdc951): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x5.1 for 4x the input (n^1.18, near-linear).
- Candidate 2 (sha256:2658493554aa): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x5.9 for 4x the input (n^1.28, near-linear).
- Candidate 3 (sha256:c7923e640a3c): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x5.1 for 4x the input (n^1.17, near-linear).

Same probes on my own reference solution: random integers x4.9 for 4x the input (n^1.15, near-linear).

Hand-written expectations: 7 cases whose expected outputs I computed by hand, not with the reference. The reference agrees on 7/7; candidates matching all of them: 3/3.

Is the suite itself trustworthy? I planted 8 known-wrong implementations. The full suite rejected 8/8. The sorted-and-well-formed check (called the weak check below) alone would have accepted 8/8. Verdict for each planted failure (first layer that rejects it, first failing input, and whether the weak check accepts it):

- touching intervals not merged: L1 on [[0, 0], [0, 0]] (wrong output); weak check accepts it
- no sort before merge: L1 on [[1, 1], [0, 0]] (wrong output); weak check accepts it
- nested interval shrinks end: L1 on [[0, 2], [1, 1]] (wrong output); weak check accepts it
- mutates input: L1 on [] (mutated input); weak check accepts it
- returns input object when already merged: L1 on [] (returned the input object); weak check accepts it
- mutates then restores input: L1 on [] (mutated input); weak check accepts it
- wrong for large inputs: L2 (wrong output); weak check accepts it
- fails on ten or more identical intervals: L3 (wrong output); weak check accepts it

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261128T003459Z-55.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: Which edge case would you add to the held-out set for interval merging?
