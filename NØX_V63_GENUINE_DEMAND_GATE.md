NØX Origin — V63 Genuine Demand Gate

Version: V63
Generated: 2026-09-02
Mode: "genuine_demand_gate"

Objective

V63 improves V62 by detecting genuine, actionable work opportunities instead of simply detecting task-related keywords.

The priority is precision over volume.

A capability match alone is never sufficient to classify a post as a genuine demand.

---

1. Demand evidence

Strong demand indicators include:

- "I need someone to"
- "we need someone to"
- "looking for someone to"
- "looking for an agent to"
- "can someone"
- "who can"
- "help needed"
- "task available"
- "hiring"
- "seeking help"
- "commission"
- "bounty"
- "paid task"

These indicators must be evaluated in context.

A phrase such as "we need" inside an analysis, finding or technical explanation must not automatically create a buyer request.

---

2. Weak demand signals

The following words are insufficient on their own:

- "need"
- "require"
- "looking"
- "want"
- "help"
- "task"

Weak signals may contribute to scoring but can never independently produce:

"genuine_demand: true"

---

3. Actionable task requirement

A genuine demand must contain a concrete task that another agent could perform.

Examples:

- research
- writing
- coding
- debugging
- testing
- verification
- data processing
- API integration
- workflow automation
- analysis
- documentation

Capability matching is evaluated only after credible demand evidence exists.

---

4. Compensation detection

A reward signal is valid only when compensation is directly associated with an available task.

Valid

- "paid task"
- "$20 for someone who can..."
- "reward for completing..."
- "bounty"
- "commission"
- "tip for..."

Invalid

- discussion of API prices;
- discussion of model costs;
- "paying" used in an analysis;
- completed payment;
- payment receipt;
- already settled hire.

A completed payment must never be classified as an open opportunity.

---

5. Post-type protection

Posts classified as:

- "finding"
- "analysis"
- "discussion"

receive a strong negative demand prior unless they contain explicit evidence of an actual actionable request.

Typical non-demand content includes:

- research summaries;
- scientific findings;
- technical discoveries;
- opinions;
- project retrospectives;
- tutorials;
- announcements;
- completed work;
- philosophical discussions.

Examples such as:

"I built..."

"I tested..."

"I wrote..."

describe completed work and are not automatically opportunities.

---

6. Service-offer protection

The phrase:

"I will"

must not automatically produce:

"SERVICE_OFFER"

A service offer requires commercial intent such as:

- available for work;
- accepting commissions;
- offering services;
- hire me;
- pricing;
- rates;
- paid service;
- commission;
- available to build/fix/test for others.

---

7. Completed work

Detect and separate completed work from open work.

Signals include:

- "shipped"
- "built"
- "completed"
- "finished"
- "I solved"
- "I received"
- "payment received"
- "hire settled"
- "completed task"

Possible classifications:

"COMPLETED_WORK"

or

"PAYMENT_RECEIPT"

Neither classification represents an open buyer request.

---

8. Rhetorical protection

Questions and statements must be interpreted in context.

For example:

"Who can really verify this?"

does not automatically mean that the author is hiring someone.

Likewise:

"We need better testing."

does not automatically mean that an actionable job is available.

---

9. Classification model

V63 may use these classifications:

"OPEN_PAID_TASK"

A concrete task is requested and compensation is explicitly associated with it.

"BUYER_REQUEST"

A concrete actionable task is genuinely requested, but compensation is not confirmed.

"OPEN_UNPAID_TASK"

A genuine actionable request exists without identified compensation.

"SERVICE_OFFER"

The author is genuinely offering a service to others.

"COMPLETED_WORK"

The author describes work already completed.

"PAYMENT_RECEIPT"

The author documents a completed payment or completed hire.

"PROMOTIONAL"

The post primarily promotes a product, service, tool or project.

"DISCUSSION"

Discussion, analysis, opinion or rhetorical content without an actionable work request.

"UNCLEAR"

Evidence is insufficient.

---

10. Genuine demand gate

The following conditions are required before:

"genuine_demand = true"

1. credible request intent;
2. concrete actionable task;
3. work is not already completed;
4. request is not merely analytical, rhetorical or promotional;
5. sufficient confidence exists in the context.

The following can never independently create a genuine demand:

- capability match;
- task keyword;
- reward keyword;
- "we need";
- "I will";
- "I can".

---

11. Scoring

Demand evidence must dominate capability matching.

Recommended scoring structure:

- demand evidence: "0–70"
- task specificity: "0–15"
- compensation evidence: "0–10"
- NØX capability match: "0–10"
- freshness/availability: "0–5"

Apply penalties for:

- analysis;
- findings;
- discussion;
- completed work;
- payment receipts;
- promotional content;
- rhetorical language;
- isolated keywords.

A high capability score must never transform a non-demand post into a genuine opportunity.

---

12. Manual review only

V63 must not contact requesters automatically.

Disabled actions:

- comments;
- DM;
- marketplace actions;
- automatic acceptance;
- payments;
- automatic contact.

When a credible opportunity is detected:

"action = MANUAL_REVIEW_REQUIRED"

NØX must provide the original post information for human verification.

---

13. Rejected item integrity

Rejected items must retain their original metadata.

Never output empty placeholder records.

Each rejected item must preserve:

- "id"
- "title"
- "requester"
- "post_type"
- "classification"
- "genuine_demand"
- "score"
- "confidence"
- "signals"
- "evidence"
- "rejection_reason"

Example:

{
  "id": "original-id",
  "title": "original title",
  "requester": "original requester",
  "post_type": "finding",
  "classification": "DISCUSSION",
  "genuine_demand": false,
  "rejection_reason": [
    "no_actionable_request",
    "analysis_content"
  ]
}

---

14. Priority rule

V63 must prefer:

1 highly credible opportunity

over:

30 speculative opportunities.

The goal is not maximum detection volume.

The goal is maximum probability that a detected opportunity is real and actionable.

---

15. Gemini and cost constraint

Gemini remains disabled in V63.

V63 must use deterministic analysis only.

No paid API, paid model, paid service or paid dependency may be introduced.

The NØX project must remain at:

€0 cost to the user.

---

16. Success criteria

V63 succeeds if it:

- removes narrative "we need" false positives;
- removes reward/payment discussion false positives;
- separates completed work from available work;
- reduces capability-driven false positives;
- correctly preserves rejected-item metadata;
- produces fewer but more credible opportunities;
- keeps all requester contact disabled.

---

NØX Origin — V63 Genuine Demand Gate
