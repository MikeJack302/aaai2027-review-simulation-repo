---
name: aaai2027-review-simulation-repo
version: 1.0.0
description: Simulate an AAAI-27-style multi-reviewer process for anonymized AI papers, producing evidence-grounded reviews, a meta-review, a decision matrix, and a prioritized revision plan.
compatibility: Agent Skills / Claude Code / Cursor / Codex-style local agents
license: MIT
---

# AAAI-27 Review Simulation

Use this skill when the user asks to review, red-team, score, simulate peer review, predict AAAI-27 reception, prepare rebuttals, or plan revisions for an AI conference manuscript.

This is a **simulation**, not an official AAAI review and not a prediction of acceptance. Never present the scoring scale, reviewer names, or venue policies as official unless they are verified from the current official AAAI author instructions.

## Inputs

Required: a manuscript in PDF, LaTeX, DOCX, Markdown, or plain text.

Optional: supplementary material, experiment logs, a response-to-review draft, target track, a preferred review mode, and an output directory.

Infer defaults when omitted:

- `mode=full`
- `num_reviewers=5`
- `language=English outputs, Chinese executive summary when the user writes Chinese`
- `output_dir=./reviews/<paper-stem>/`

Supported modes:

- `fast`: one evidence audit, three reviewers, short meta-review.
- `full`: evidence audit, five independent reviewers, meta-review, matrix, revision plan.
- `rebuttal`: identify defensible responses and experiments needed for likely critiques.
- `revision`: convert existing reviews into a ranked, executable revision plan.
- `camera-ready`: focus on clarity, reproducibility, claims, figures, tables, and anonymity.

## Non-negotiable review rules

1. **Read before judging.** Extract a paper map: task, contribution claims, method, assumptions, datasets, splits, baselines, metrics, costs, statistical tests, and stated limitations.
2. **Anchor findings in evidence.** Every major concern must cite a concrete anchor such as a section, equation, figure, table, page, or quoted manuscript claim. If an anchor is unavailable, label it `uncertain` rather than asserting it.
3. **Do not invent missing facts.** Do not say a baseline, seed, dataset, test, theorem, or result is absent unless the manuscript has been searched for it.
4. **Separate three statements.** Clearly distinguish: (a) what the manuscript reports, (b) what a reviewer may infer, and (c) what additional evidence is needed.
5. **Preserve scope.** Do not punish a paper merely for not solving every adjacent problem. Evaluate whether the title, abstract, and conclusions claim more than the evidence supports.
6. **Treat leakage and cost claims seriously.** For ML, RAG, agents, and transfer learning, audit train/dev/test separation, memory provenance, tuning boundaries, oracle inputs, compute, calls, tokens, and fairness of budgets.
7. **Do not optimize for negativity.** Findings must be decision-relevant. Include genuine strengths and the smallest repair that would resolve each major concern.
8. **Protect anonymity.** Flag author-identifying names, affiliations, acknowledgments, local file paths, self-referential language, repository links that identify authors, and metadata risks. Do not attempt to deanonymize authors.

## Workflow

### Phase 0 — Intake and preflight

1. Identify the manuscript and optional supplement.
2. Run `python3 scripts/preflight.py <manuscript> --out <output_dir>/00_preflight.md` when local execution is available.
3. Inspect all figures, tables, and appendices needed to understand experimental claims. For PDFs, do not rely only on extracted text when a table, chart, or diagram matters.
4. State any constraints: unreadable pages, missing supplement, absent code, unavailable references, or incomplete result tables.
5. For questions about AAAI-27 policy, search the official AAAI website at runtime. Do not assume deadlines, page limits, tracks, templates, or scoring conventions.

### Phase 1 — Evidence map

Create `01_evidence_map.md` using `prompts/evidence_map.md`.

The map must include:

- one-sentence problem statement;
- 3–5 claimed contributions, each paired with an evidence anchor;
- method inputs, outputs, trainable components, and inference-time steps;
- evaluation protocol: datasets, data splits, target leakage protections, baselines, metrics, seeds, statistics, and compute/cost accounting;
- scope boundaries and negative results;
- an `evidence gaps` section that lists missing information without assuming misconduct.

### Phase 2 — Select reviewers

Use the five default personas below. Each reviewer works independently from the same evidence map and manuscript; reviewers do not see each other’s reviews.

1. **R1 — Novelty and positioning.** Tests whether the contribution is distinct from adjacent work and whether the paper states a falsifiable, appropriately narrow claim.
2. **R2 — Technical correctness and reproducibility.** Audits definitions, algorithms, equations, objectives, assumptions, implementation closure, and whether the method can be reproduced.
3. **R3 — Experimental rigor and causality.** Audits split design, leakage, baselines, ablations, seed variance, significance, oracle boundaries, cost fairness, and threats to validity.
4. **R4 — Domain specialist.** Select the most relevant checklist from `references/domain_checks.md` after identifying the paper’s field.
5. **R5 — AAAI generalist / senior PC.** Evaluates importance, clarity, balanced presentation, likely reviewer disagreement, and whether the result would matter to a broad AI audience.

In `fast` mode, run R1, R2, and R3 only. In `full` mode, use all five. Do not fabricate reviewer diversity from real people or institutions; these are role-based simulated perspectives.

### Phase 3 — Independent structured reviews

For each reviewer, use `prompts/reviewer_review.md`. Save outputs as:

- `review_r1_novelty.md`
- `review_r2_technical.md`
- `review_r3_experiments.md`
- `review_r4_domain.md`
- `review_r5_generalist.md`

Use this **synthetic calibration scale** only:

- `8–10`: strong accept leaning; evidence is compelling and concerns are limited.
- `6–7`: accept leaning; contributions are credible with reparable limitations.
- `5`: borderline; outcome depends on clarification, reviewer pool, and confidence in evidence.
- `3–4`: reject leaning; one or more central validity, novelty, or evidence issues remain.
- `1–2`: strong reject leaning; central claims are unsupported, invalid, or irreproducible.

Ask every reviewer to provide:

- summary;
- strengths;
- major concerns, each with `severity`, `confidence`, `evidence anchor`, `why it matters`, and `minimum repair`;
- minor concerns;
- score and confidence;
- the single fact or experiment most likely to change their score.

### Phase 4 — Meta-review and decision matrix

Create `meta_review.md` using `prompts/meta_review.md`.

The meta-review must:

1. Separate consensus concerns from reviewer-specific concerns.
2. Reconcile disagreements rather than averaging them away.
3. State a simulated verdict distribution, not an acceptance probability.
4. Identify exactly three decision drivers, ranked by severity.
5. Mark whether each driver is addressable by writing, analysis, rerunning experiments, or redesign.
6. Include a `claim calibration` table: keep / narrow / remove / support with new evidence.

Create `concerns_matrix.csv` with columns:

`id, concern, severity, reviewer_ids, anchors, evidence_status, repair_type, estimated_effort, priority`

Create `revision_plan.md` with P0 / P1 / P2 priorities:

- **P0:** likely decision-changing before submission.
- **P1:** materially improves confidence, clarity, or competitiveness.
- **P2:** polish, positioning, and presentation improvements.

Create `results.json` using `references/results_schema.json`. It must contain only the artifact paths, synthetic scores, reviewer confidence, verdict inclinations, and IDs of consensus decision drivers; it must not contain hidden reasoning.

### Phase 5 — Quality gate

Before delivering, verify:

- every major concern has an evidence anchor or is explicitly marked uncertain;
- no reviewer asserts an official AAAI policy without an official live citation;
- score matches written critique;
- proposed fixes are feasible and specific;
- no claim is strengthened beyond what the manuscript shows;
- all output paths and output files are listed.

## Special audits

Always load the relevant subsection of `references/domain_checks.md`.

For RAG / LLM / agent papers, additionally check:

- target-label, test-query, test-document, test-entity, prompt, memory, and retrieval index leakage;
- whether an oracle uses gold labels, gold evidence, future information, or privileged metadata;
- whether calls, tokens, latency, batching, model costs, and retry budgets are counted consistently;
- whether all baselines share comparable model backbones, decoding, context budgets, data access, and test constraints;
- whether external transfer results use frozen hyperparameters and no target-task tuning;
- whether a claimed causal result identifies an intervention, estimand, assumptions, and alternative explanations.

For time-series transfer / causal mechanism papers, additionally check representation leakage, cross-domain split integrity, causal terminology, intervention validity, and interpretation of learned graphs.

For embodied AI papers, additionally check simulator dependencies, train/test scenes, domain gap, action budget, safety, benchmark realism, and whether gains arise from memory/retrieval rather than extra privileged observations.

## Output style

- Be concise but specific; avoid generic “add more experiments” comments.
- Default to a professional, constructive reviewer tone.
- Use English for review artifacts unless asked otherwise. When the user writes Chinese, include a short Chinese executive summary.
- For user-facing responses, begin with the simulated verdict and three P0 issues. Then link or list the artifacts.
- Do not reveal hidden reasoning. Present only the evidence-based review.
