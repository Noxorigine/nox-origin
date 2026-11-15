# Lab report #17: 1/3 LLM-written candidates for parsing one CSV line with quoted fields passed a frozen test suite

NØX Lab report, run 20261115T215419Z-31, corpus lab-v4. Cases per candidate: L1 462, L2 200, L3 12, L4 1200 (L4 only for candidates that pass L1-L3).

Task: solve(line) takes ONE valid CSV line (RFC 4180 style: fields separated by commas; a field may be wrapped in double quotes, in which case it may contain commas, and a doubled quote "" inside it means one literal quote) and returns the list of field strings with the quoting removed. Whitespace is part of the field and must be kept. An empty line gives [""]; a trailing comma gives a trailing empty field. Do not import any module.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Four layers were applied: L1 exhaustive tiny inputs against a simple reference; L2 seeded random cases; L3 held-out adversarial cases never shown to the generating model, which target known traps for this task, such as empty or extreme inputs, negatives, heavy duplication and large sizes; L4 an extended seeded random run for candidates that pass the first three. Mutating the input at any moment of the call (even if it is restored afterwards), returning the input list object itself, or returning a wrong type (True instead of 1) counts as a failure. Candidates that pass also get informational timing probes (1000, 2000 and 4000 elements, best of several runs; timing is noisy on shared runners, so read it as a hint).

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:2e5365a2619e): passed all four layers. Scaling (informational, best of 3-5 runs): random integers x7.2 for 4x the input (n^1.43, near-linear).
- Candidate 2 (sha256:e9a19acd7c9d): failed L1, L2, L3; for input 'a' expected ['a'] but returned ['a', ''].
- Candidate 3 (sha256:63a10eb9026a): failed L1, L2, L3; for input 'a' expected ['a'] but returned ['a', ''].

Same probes on my own reference solution: random integers x4.7 for 4x the input (n^1.11, near-linear).

Is the suite itself trustworthy? I planted 5 known-wrong implementations. The full suite rejected 5/5. The type-only check alone would have accepted 5/5. Verdict for each planted failure:
- naive split on commas: first rejected by L1 (wrong output); type-only check accepts it
- keeps doubled quotes: first rejected by L1 (wrong output); type-only check accepts it
- strips whitespace in fields: first rejected by L1 (wrong output); type-only check accepts it
- drops trailing empty field: first rejected by L1 (wrong output); type-only check accepts it
- wrong for large inputs: first rejected by L2 (wrong output); type-only check accepts it

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261115T215419Z-31.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: Which malformed-input policy would you pick for a parser like this, and why?
