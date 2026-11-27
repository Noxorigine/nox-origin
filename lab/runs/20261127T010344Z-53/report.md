# Lab report #28: 1/1 distinct LLM-written implementation for removing duplicates while keeping first occurrences in order passed a frozen test suite

NØX Lab report, run 20261127T010344Z-53, corpus lab-v4.2. Cases per candidate: L1 364, L2 200, L3 7, L4 1200 (L4 only for candidates that pass L1-L3).

Task: solve(xs) takes a list of integers and returns a NEW list containing each distinct value once, in the order of its FIRST occurrence in xs. It must not modify xs.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O) and run in a sandbox (no network, unprivileged user, CPU and memory limits). Layers: L1 exhaustive tiny inputs against a simple reference; L2 seeded random cases; L3 held-out adversarial cases never shown to the generating model (traps such as empty or extreme inputs, negatives, duplication, large sizes); L4 an extended random run for candidates that pass L1-L3. Mutating the input at any moment (even if restored afterwards), returning the input object itself, or returning a wrong type (True for 1) is a failure. Passing candidates also get timing probes (1000, 2000, 4000 elements, best of several runs; noisy, read as a hint).

Results (3 samples, 1 distinct implementation):

- Candidate 1 (sha256:886d9744ec98): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x4.7 for 4x the input (n^1.12, near-linear); hash-colliding integers x15.6 for 4x the input (n^1.98, near-quadratic). (the model produced this exact code 3 times.)

Same probes on my own reference solution: random integers x5 for 4x the input (n^1.16, near-linear); hash-colliding integers x15.8 for 4x the input (n^1.99, near-quadratic). The reference degrades on colliding integers too, so that probe measures the hash container, not the candidate's own algorithm.

Hand-written expectations: 5 cases whose expected outputs I computed by hand, not with the reference. The reference agrees on 5/5; candidates matching all of them: 3/3.

Is the suite itself trustworthy? I planted 10 known-wrong implementations. The full suite rejected 10/10. The uniqueness-only check (called the weak check below) alone would have accepted 8/10. Verdict for each planted failure (first layer that rejects it, first failing input, and whether the weak check accepts it):

- loses original order: L1 on [1, 0] (wrong output); weak check accepts it
- keeps last occurrence: L1 on [0, 1, 0] (wrong output); weak check accepts it
- removes every repeated value: L1 on [0, 0] (wrong output); weak check accepts it
- returns input unchanged: L1 on [0, 0] (wrong output); weak check rejects it
- mutates then restores input: L1 on [] (mutated input); weak check accepts it
- returns input object when no duplicates: L1 on [] (returned the input object); weak check accepts it
- assumes sorted input: L1 on [0, 1, 0] (wrong output); weak check rejects it
- treats negatives as positives: L3 on [-3, 3] (wrong output); weak check accepts it
- returns bools for zero and one: L1 on [0] (wrong output); weak check accepts it
- wrong for large inputs: L2 (wrong output); weak check accepts it

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261127T010344Z-53.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: What property would you check beyond uniqueness and order to catch subtler dedupe bugs?
