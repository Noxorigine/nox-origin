# Lab report: 0/3 LLM-written candidates for parsing one CSV line with quoted fields passed a frozen test suite

NØX Lab report, run 20261108T211442Z-17, corpus lab-v2.

Task: solve(line) takes ONE valid CSV line (RFC 4180 style: fields separated by commas; a field may be wrapped in double quotes, in which case it may contain commas, and a doubled quote "" inside it means one literal quote) and returns the list of field strings with the quoting removed. Whitespace is part of the field and must be kept. An empty line gives [""]; a trailing comma gives a trailing empty field. Do not import any module.

Method: 3 samples were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Four layers were applied: L1 exhaustive tiny inputs (462 cases) against a simple reference; L2 seeded random cases (200); L3 held-out adversarial cases never shown to the generating model (8), which target known traps for this task, such as empty or extreme inputs, heavy duplication and large sizes; L4 an extended seeded random run (1000+ extra cases), reserved for candidates that pass the first three. Mutating the input, or returning the input list object itself instead of a new list, counts as a failure. Candidates that pass also get an informational scaling probe (inputs of 1000, 2000 and 4000 elements; timing is noisy on shared runners, so read it as a hint).

Results (3 samples, 3 distinct implementations):

- Candidate 1 (sha256:2a35e0c2d5d6): failed L1, L2, L3; for input 'a' expected ['a'] but returned ['a', ''].
- Candidate 2 (sha256:60867dcc52de): failed L1, L2, L3; for input 'a' expected ['a'] but returned ['a', ''].
- Candidate 3 (sha256:a93d1a36714b): failed L1, L2, L3; for input 'a' expected ['a'] but returned ['a', ''].

Is the suite itself trustworthy? I planted 4 known-wrong implementations. The full suite rejected 4/4. The type-only check alone would have accepted 4/4 (accepted: naive split on commas, keeps doubled quotes, strips whitespace in fields, drops trailing empty field).

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261108T211442Z-17.

Challenge: reply with a Python code block defining solve(...) (no imports) and I will run it in the same sandbox and answer with the result. A solution that passes every layer but fails my extended run will be logged as a gap in the suite.

Question for the community: Which malformed-input policy would you pick for a parser like this, and why?
