# Lab report #18: 3/3 LLM-written candidates for merging overlapping closed intervals passed a frozen test suite

NØX Lab report, run 20261117T144037Z-34, corpus lab-v4. Cases per candidate: L1 1111, L2 200, L3 6, L4 1200 (L4 only for candidates that pass L1-L3).

Task: solve(iv) takes a list of closed integer intervals [a, b] with a <= b, in any order, and returns a NEW list of merged intervals sorted by start. Intervals that overlap OR touch (share an endpoint, e.g. [1,3] and [3,5]) must be merged into one. It must not modify iv.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Four layers were applied: L1 exhaustive tiny inputs against a simple reference; L2 seeded random cases; L3 held-out adversarial cases never shown to the generating model, which target known traps for this task, such as empty or extreme inputs, negatives, heavy duplication and large sizes; L4 an extended seeded random run for candidates that pass the first three. Mutating the input at any moment of the call (even if it is restored afterwards), returning the input list object itself, or returning a wrong type (True instead of 1) counts as a failure. Candidates that pass also get informational timing probes (1000, 2000 and 4000 elements, best of several runs; timing is noisy on shared runners, so read it as a hint).

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:64005a7831c6): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x4.2 for 4x the input (n^1.03, near-linear).
- Candidate 2 (sha256:67b0b7257e0a): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x4.9 for 4x the input (n^1.14, near-linear).
- Candidate 3 (sha256:5832daa0c7b2): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x5.3 for 4x the input (n^1.2, near-linear).

Same probes on my own reference solution: random integers x4.2 for 4x the input (n^1.04, near-linear).

Is the suite itself trustworthy? I planted 7 known-wrong implementations. The full suite rejected 7/7. The sorted-and-well-formed check alone would have accepted 7/7. Verdict for each planted failure:
- touching intervals not merged: first rejected by L1 (wrong output); sorted-and-well-formed check accepts it
- no sort before merge: first rejected by L1 (wrong output); sorted-and-well-formed check accepts it
- nested interval shrinks end: first rejected by L1 (wrong output); sorted-and-well-formed check accepts it
- mutates input: first rejected by L1 (mutated input); sorted-and-well-formed check accepts it
- returns input object when already merged: first rejected by L1 (returned the input object); sorted-and-well-formed check accepts it
- mutates then restores input: first rejected by L1 (mutated input); sorted-and-well-formed check accepts it
- wrong for large inputs: first rejected by L2 (wrong output); sorted-and-well-formed check accepts it

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261117T144037Z-34.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: Which edge case would you add to the held-out set for interval merging?
