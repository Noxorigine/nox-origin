# Lab report #27: 3/3 LLM-written candidates for the maximum circular subarray sum passed a frozen test suite

NØX Lab report, run 20261126T010213Z-51, corpus lab-v4.2. Cases per candidate: L1 3905, L2 200, L3 7, L4 1200 (L4 only for candidates that pass L1-L3).

Task: solve(xs) takes a NON-EMPTY list of integers treated as circular (the last element is adjacent to the first) and returns the largest possible sum of a NON-EMPTY contiguous circular subarray (it may wrap around the end, and it may be the whole list). It must not modify xs.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O) and run in a sandbox (no network, unprivileged user, CPU and memory limits). Layers: L1 exhaustive tiny inputs against a simple reference; L2 seeded random cases; L3 held-out adversarial cases never shown to the generating model (traps such as empty or extreme inputs, negatives, duplication, large sizes); L4 an extended random run for candidates that pass L1-L3. Mutating the input at any moment (even if restored afterwards), returning the input object itself, or returning a wrong type (True for 1) is a failure. Passing candidates also get timing probes (1000, 2000, 4000 elements, best of several runs; noisy, read as a hint).

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:40ee3245a37f): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x4.1 for 4x the input (n^1.02, near-linear).
- Candidate 2 (sha256:9a36f26de6ca): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x4.1 for 4x the input (n^1.02, near-linear).
- Candidate 3 (sha256:09a6b6a6b378): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x4.1 for 4x the input (n^1.02, near-linear).

Same probes on my own reference solution: random integers x4.1 for 4x the input (n^1.02, near-linear).

Hand-written expectations: 7 cases whose expected outputs I computed by hand, not with the reference. The reference agrees on 7/7; candidates matching all of them: 3/3.

Is the suite itself trustworthy? I planted 7 known-wrong implementations. The full suite rejected 7/7. The lower-bound-only check (called the weak check below) alone would have accepted 6/7. Verdict for each planted failure (first layer that rejects it, first failing input, and whether the weak check accepts it):

- ignores wraparound: L1 on [1, -2, 1] (wrong output); weak check accepts it
- allows empty subarray all negative gives zero: L1 on [-2] (wrong output); weak check accepts it
- total minus min without negative guard: L1 on [-2] (wrong output); weak check accepts it
- mutates input: L1 on [-2] (mutated input); weak check accepts it
- mutates then restores input: L1 on [-2] (mutated input); weak check accepts it
- wrong for large inputs: L2 (wrong output); weak check accepts it
- wrong for long all negative lists: L3 (wrong output); weak check rejects it

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261126T010213Z-51.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: Which input family do you expect LLM-written solutions to get wrong most often here?
