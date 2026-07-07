# Meta-Review Prompt

Synthesize independent simulated reviews without erasing disagreement. The meta-review is a decision-oriented summary, not a restatement of every comment.

## Required format

```markdown
# Simulated Meta-Review

## Simulated verdict distribution
- Accept leaning:
- Borderline:
- Reject leaning:
- Interpretation: [This is a simulated distribution, not an acceptance probability.]

## Consensus strengths
1. ...

## Consensus concerns
### D1 — [decision driver]
- **Raised by:**
- **Evidence status:** supported / partly supported / uncertain
- **Anchors:**
- **Why this changes the decision:**
- **Minimum resolution:**
- **Repair type:** writing / analysis / rerun / redesign

[Exactly three ranked decision drivers.]

## Reviewer disagreement
| Topic | Positions | Why they differ | What would resolve it |
|---|---|---|---|

## Claim calibration
| Claim | Current evidence | Action: keep / narrow / remove / support | Required change |
|---|---|---|---|

## Prioritized revision plan
### P0 — decision-changing
1. ...
### P1 — competitiveness
1. ...
### P2 — polish
1. ...

## Bottom line
[2–4 sentences, calibrated to evidence.]
```

Rules:

- Do not average scores mechanically.
- Do not turn a reviewer’s speculative worry into consensus fact.
- Preserve meaningful strengths.
- Never present this as an official AAAI committee decision.
