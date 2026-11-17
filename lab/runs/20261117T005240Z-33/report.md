# Lab report #18: 1/3 LLM-written candidates for computing the next lexicographic permutation passed a frozen test suite

NØX Lab report, run 20261117T005240Z-33, corpus lab-v4. Cases per candidate: L1 364, L2 200, L3 7, L4 1200 (L4 only for candidates that pass L1-L3).

Task: solve(xs) takes a list of integers (possibly empty, possibly with duplicates) and returns a NEW list: the next permutation of xs in lexicographic order, or the ascending sorted list if xs is already the last (largest) permutation. It must not modify xs.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Four layers were applied: L1 exhaustive tiny inputs against a simple reference; L2 seeded random cases; L3 held-out adversarial cases never shown to the generating model, which target known traps for this task, such as empty or extreme inputs, negatives, heavy duplication and large sizes; L4 an extended seeded random run for candidates that pass the first three. Mutating the input at any moment of the call (even if it is restored afterwards), returning the input list object itself, or returning a wrong type (True instead of 1) counts as a failure. Candidates that pass also get informational timing probes (1000, 2000 and 4000 elements, best of several runs; timing is noisy on shared runners, so read it as a hint).

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:e3d2f84e7a30): passed all four layers.
- Candidate 2 (sha256:841b0558429d): failed L1, L2, L3; for input [] it raised IndexError.
- Candidate 3 (sha256:ea9683cf3c42): failed L1, L2, L3; for input [0, 1] expected [1, 0] but returned [1].

Is the suite itself trustworthy? I planted 6 known-wrong implementations. The full suite rejected 6/6. The same-elements-only check alone would have accepted 4/6. Verdict for each planted failure:
- last permutation not wrapped: first rejected by L1 (wrong output); same-elements-only check accepts it
- suffix not reversed: first rejected by L1 (wrong output); same-elements-only check accepts it
- strict comparison breaks duplicates: first rejected by L1 (raised an exception); same-elements-only check rejects it
- mutates input: first rejected by L1 (mutated input); same-elements-only check accepts it
- mutates then restores input: first rejected by L1 (mutated input); same-elements-only check accepts it
- wrong for large inputs: first rejected by L3 (wrong output); same-elements-only check rejects it

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261117T005240Z-33.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: Which planted wrong implementation would you add to this suite?
