# Lab report #25: 1/3 LLM-written candidates for computing the next lexicographic permutation passed a frozen test suite

NØX Lab report, run 20261124T032235Z-47, corpus lab-v4.2. Cases per candidate: L1 364, L2 200, L3 7, L4 1200 (L4 only for candidates that pass L1-L3).

Task: solve(xs) takes a list of integers (possibly empty, possibly with duplicates) and returns a NEW list: the next permutation of xs in lexicographic order, or the ascending sorted list if xs is already the last (largest) permutation. It must not modify xs.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O) and run in a sandbox (no network, unprivileged user, CPU and memory limits). Layers: L1 exhaustive tiny inputs against a simple reference; L2 seeded random cases; L3 held-out adversarial cases never shown to the generating model (traps such as empty or extreme inputs, negatives, duplication, large sizes); L4 an extended random run for candidates that pass L1-L3. Mutating the input at any moment (even if restored afterwards), returning the input object itself, or returning a wrong type (True for 1) is a failure. Passing candidates also get timing probes (1000, 2000, 4000 elements, best of several runs; noisy, read as a hint).

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:610bd284c965): passed all four layers.
- Candidate 2 (sha256:841b0558429d): failed L1, L2, L3; for input [] it raised IndexError.
- Candidate 3 (sha256:777ca9160524): failed L1, L2, L3; for input [] it raised IndexError.

Failure grouping (ShatteredWorlds): 2 samples (candidates 2, 3) fail the same way, first failing input [], it raised IndexError. Different code with the same first failure usually means one bug written several times, not independent mistakes.

Hand-written expectations: 6 cases whose expected outputs I computed by hand, not with the reference. The reference agrees on 6/6; candidates matching all of them: 1/3.

Is the suite itself trustworthy? I planted 6 known-wrong implementations. The full suite rejected 6/6. The same-elements-only check (called the weak check below) alone would have accepted 4/6. Verdict for each planted failure (first layer that rejects it, first failing input, and whether the weak check accepts it):

- last permutation not wrapped: L1 on [1, 0] (wrong output); weak check accepts it
- suffix not reversed: L1 on [0, 1, 1] (wrong output); weak check accepts it
- strict comparison breaks duplicates: L1 on [0, 0] (raised an exception); weak check rejects it
- mutates input: L1 on [] (mutated input); weak check accepts it
- mutates then restores input: L1 on [] (mutated input); weak check accepts it
- wrong for large inputs: L3 (wrong output); weak check rejects it

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261124T032235Z-47.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: Which planted wrong implementation would you add to this suite?
