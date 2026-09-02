# NØX V96 — Controlled Correction Deployment

Generated: 2026-09-02T21:02:10.893515+00:00

## Deployment

- Deployment ID: V96-20260902T210210Z
- Status: DEPLOYMENT_BLOCKED
- Gate open: False
- Authority: RETAIN_BASELINE

## Correction

- ID: CORR_C_ACCEPTANCE_PRIORITY
- Name: Increase acceptance evidence
- Change: Increase the importance of explicit acceptance criteria and verifiable completion conditions.

## Evidence chain

- V93: CORRECTION_REJECTED_REGRESSION_RISK
- V94: CORRECTION_LIVE_NEUTRAL
- V94 confidence: 0.6
- V95: CORRECTION_UNRESOLVED
- V95 score: 45.0/100
- V95 confidence: 0.45

## Deployment gate

- V95 did not grant clear controlled deployment candidate status.
- V95 arbitration score is below 80/100.
- V95 confidence is below 0.80.

## Reversibility

- Baseline preserved: true
- Rollback target: V90_BASELINE
- Permanent modification: false
- Production rule overwritten: false

## Next stage

V97 will measure the actual decision effects of the controlled correction.
The correction can then be retained, rolled back or refined from observed evidence.

## Safety

- Gemini: disabled
- External action: disabled
- Contact: disabled
- Bidding: disabled
- Payments: disabled
- Permanent self-modification: false
- Rollback available: true
- Project cost: €0
- Human override: enabled