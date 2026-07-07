# Evidence Map Prompt

Read the manuscript and optional supplement before judging it. Build an evidence map; do not write a review yet.

Use this structure:

```markdown
# Evidence Map

## Paper identity
- Title:
- Claimed problem:
- Claimed setting / task:
- Stated scope:

## Contribution ledger
| ID | Claim | Evidence anchor | Evidence reported | Scope / caveat |
|---|---|---|---|---|

## Method closure
- Inputs:
- Outputs:
- Trainable modules:
- Offline data / memory / cache construction:
- Inference-time steps:
- Losses / objective:
- Hyperparameters and tuning split:
- Unspecified or ambiguous components:

## Evaluation ledger
| Topic | What is reported | Evidence anchor | Missing / unclear |
|---|---|---|---|
| Data and splits | | | |
| Baselines | | | |
| Metrics | | | |
| Seeds / variance / tests | | | |
| Computational cost | | | |
| Oracle inputs | | | |
| Leakage safeguards | | | |
| External transfer | | | |
| Limitations / negative results | | | |

## Figure and table audit
- Essential figures / tables:
- Claims visually supported:
- Figures or tables requiring visual inspection:

## Evidence gaps
List only gaps that are actually unreported or ambiguous after searching the paper. Use neutral wording.
```

Rules:

1. Cite a page, section, equation, figure, table, or appendix anchor for every ledger entry.
2. Do not infer an implementation detail just because it is conventional.
3. If the supplement is unavailable, say so and mark relevant gaps as `supplement unavailable`.
4. Identify claims that are broader than the evaluation but do not yet recommend a verdict.
