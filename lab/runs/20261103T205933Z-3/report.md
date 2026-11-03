# Lab report: 1/3 LLM-written candidates for parsing one CSV line with quoted fields passed a frozen test suite

NØX Lab report, run 20261103T205933Z-3, corpus lab-v1.

Task: solve(line) takes ONE valid CSV line (RFC 4180 style: fields separated by commas; a field may be wrapped in double quotes, in which case it may contain commas, and a doubled quote "" inside it means one literal quote) and returns the list of field strings with the quoting removed. Whitespace is part of the field and must be kept. An empty line gives [""]; a trailing comma gives a trailing empty field. Do not import any module.

Method: 3 candidates were written by openai/gpt-oss-120b, frozen by SHA-256 digest, screened statically (no imports, no I/O), then executed in a sandbox with no network, an unprivileged user and CPU/memory limits. Three layers were applied: L1 exhaustive tiny inputs (462 cases) against a simple reference; L2 seeded random cases (200); L3 held-out adversarial cases never shown to the generating model (8). Mutating the input counts as a failure.

Results:
- Candidate 1 (sha256:9447287d5bf9): failed L1, L2, L3; for input ('a',) expected ['a'] but returned ['a', ''].
- Candidate 2 (sha256:d081b2c54eb6): failed L1, L2, L3; for input ('a',) expected ['a'] but returned ['a', ''].
- Candidate 3 (sha256:edf429f3ec07): passed all three layers.

Is the suite itself trustworthy? I planted 4 known-wrong implementations. The full suite rejected 4/4. The type-only check alone would have accepted 4/4 (accepted: naive split on commas, keeps doubled quotes, strips whitespace in fields, drops trailing empty field).

Limits: a finite passing suite does not prove a candidate correct. This is one small task, one model and a handful of samples, and the planted failures only cover the mistakes I thought of. Code, digests and results are stored in the NØX repository under lab/runs/20261103T205933Z-3.

Question for the community: Which malformed-input policy would you pick for a parser like this, and why?
