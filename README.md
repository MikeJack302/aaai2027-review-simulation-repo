# aaai2027-review-simulation-repo

A reusable **AAAI-27-style paper-review simulation skill** for agent environments that support `SKILL.md` files, including Claude Code, Cursor, Codex-style local agents, and compatible Agent Skills runtimes.

It produces a multi-reviewer simulation rather than an official AAAI review. The package emphasizes evidence anchors, reproducibility, leakage auditing, fair cost accounting, and actionable revision planning.

## What it generates

```text
reviews/<paper-stem>/
├── 00_preflight.md
├── 01_evidence_map.md
├── review_r1_novelty.md
├── review_r2_technical.md
├── review_r3_experiments.md
├── review_r4_domain.md
├── review_r5_generalist.md
├── meta_review.md
├── concerns_matrix.csv
├── revision_plan.md
└── results.json
```

## Install

Copy or symlink the folder into your agent’s skills directory. Typical locations are:

```bash
# Claude Code project scope
mkdir -p .claude/skills
cp -R aaai2027-review-simulation-repo .claude/skills/aaai2027-review-simulation-repo

# Cursor project scope
mkdir -p .cursor/skills
cp -R aaai2027-review-simulation-repo .cursor/skills/aaai2027-review-simulation-repo
```

Restart the agent session after installation when required by the host application.

## Typical requests

```text
Use aaai2027-review-simulation-repo to run a full AAAI-27 review simulation on paper/main.pdf.

Review main.tex and supplement.pdf in full mode. Focus on novelty, test leakage, baseline fairness, and experiment rigor.

Run rebuttal mode on this manuscript. Give me the strongest likely reviewer objections and the minimum experiments needed to answer them.

Use revision mode on the manuscript and these three external reviews.
```

## Optional local preflight scan

```bash
python3 scripts/preflight.py paper/main.pdf --out reviews/main/00_preflight.md
python3 scripts/preflight.py paper/main.tex --out reviews/main/00_preflight.md
```

The scanner is intentionally conservative. It flags likely issues for manual review; it does not certify anonymity, formatting, or AAAI compliance.

## Design principles

- **Evidence first:** concerns must point to manuscript evidence or be marked uncertain.
- **No fictional venue policy:** official AAAI-27 rules must be checked from official AAAI sources at review time.
- **Independent roles:** novelty, technical correctness, experimental rigor, domain expertise, and generalist impact are reviewed separately.
- **Decision-relevant findings:** every major concern includes a minimum repair.
- **Research integrity checks:** explicit audits for split leakage, oracle boundaries, compute/call fairness, and overclaiming.

## License

MIT. See `LICENSE`.
