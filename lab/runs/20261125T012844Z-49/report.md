# Lab report #26: 3/3 LLM-written candidates for counting index pairs that sum to a target passed a frozen test suite

NØX Lab report, run 20261125T012844Z-49, corpus lab-v4.2. Cases per candidate: L1 605, L2 200, L3 5, L4 1200 (L4 only for candidates that pass L1-L3).

Task: solve(xs, k) takes a list of integers xs and an integer k and returns the number of index pairs (i, j) with i < j and xs[i] + xs[j] == k. Duplicate values count separately by position. It must not modify xs.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O) and run in a sandbox (no network, unprivileged user, CPU and memory limits). Layers: L1 exhaustive tiny inputs against a simple reference; L2 seeded random cases; L3 held-out adversarial cases never shown to the generating model (traps such as empty or extreme inputs, negatives, duplication, large sizes); L4 an extended random run for candidates that pass L1-L3. Mutating the input at any moment (even if restored afterwards), returning the input object itself, or returning a wrong type (True for 1) is a failure. Passing candidates also get timing probes (1000, 2000, 4000 elements, best of several runs; noisy, read as a hint).

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:b1ec9e7c8a2e): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x4.1 for 4x the input (n^1.03, near-linear); hash-colliding integers x15.9 for 4x the input (n^2, near-quadratic).
- Candidate 2 (sha256:fae32e9730e8): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x4.5 for 4x the input (n^1.08, near-linear); hash-colliding integers x16.7 for 4x the input (n^2.03, near-quadratic).
- Candidate 3 (sha256:ee92366edf4f): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x4.1 for 4x the input (n^1.02, near-linear); hash-colliding integers x15.5 for 4x the input (n^1.98, near-quadratic).

Same probes on my own reference solution: random integers x4 for 4x the input (n^0.99, near-linear); hash-colliding integers x15.4 for 4x the input (n^1.97, near-quadratic). The reference degrades on colliding integers too, so that probe measures the hash container, not the candidate's own algorithm.

Hand-written expectations: 6 cases whose expected outputs I computed by hand, not with the reference. The reference agrees on 6/6; candidates matching all of them: 3/3.

Is the suite itself trustworthy? I planted 7 known-wrong implementations. The full suite rejected 7/7. The range-only check (called the weak check below) alone would have accepted 4/7. Verdict for each planted failure (first layer that rejects it, first failing input, and whether the weak check accepts it):

- counts distinct values not positions: L1 on [0, 0], 0 (wrong output); weak check accepts it
- counts ordered pairs twice: L1 on [0, 0], 0 (wrong output); weak check rejects it
- pairs an element with itself: L1 on [0], 0 (wrong output); weak check rejects it
- ignores duplicate positions: L1 on [0, 0], 0 (wrong output); weak check accepts it
- skips negative values: L3 on [-2, 2, -2, 2, 0, 0], 0 (wrong output); weak check accepts it
- mutates then restores input: L1 on [], 0 (mutated input); weak check accepts it
- wrong for large inputs: L2 (wrong output); weak check rejects it

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261125T012844Z-49.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: Would you test this with a brute-force oracle or with algebraic properties, and why?
