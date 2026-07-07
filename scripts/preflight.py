#!/usr/bin/env python3
"""Conservative manuscript preflight scanner for the AAAI-27 review simulation skill.

The script creates a text-based checklist, not a compliance certificate. It supports
PDF (via pdftotext if installed) and text-like formats. It does not upload files.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable

KEYWORDS = {
    "anonymity": [
        r"\bauthor(s)?\b",
        r"\baffiliation(s)?\b",
        r"\backnowledg(e)?ments?\b",
        r"github\.com/",
        r"gitlab\.com/",
        r"drive\.google\.com/",
        r"our (previous|prior) work",
        r"at (our|the) university",
    ],
    "experimental_rigor": [
        r"seed",
        r"standard deviation|std\.?|variance",
        r"confidence interval|bootstrap|p[- ]?value|significance",
        r"ablation",
        r"validation|development set|dev set|held[- ]out",
    ],
    "leakage_or_oracle": [
        r"oracle",
        r"test label|test set|test data|test entity|test document",
        r"leakage|leak",
        r"memory bank|cache|historical failure",
        r"frozen",
    ],
    "cost_accounting": [
        r"token",
        r"latency",
        r"call(s)?",
        r"cost",
        r"gpu|compute|flop",
    ],
}


def read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        tool = shutil.which("pdftotext")
        if not tool:
            raise RuntimeError("PDF input needs `pdftotext` on PATH; alternatively provide extracted text or LaTeX.")
        result = subprocess.run([tool, "-layout", str(path), "-"], text=True, capture_output=True, check=False)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "pdftotext failed")
        return result.stdout
    return path.read_text(encoding="utf-8", errors="replace")


def find_hits(text: str, patterns: Iterable[str]) -> list[str]:
    hits: list[str] = []
    for pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            hits.append(pattern)
    return hits


def line_count(text: str) -> int:
    return len(text.splitlines())


def create_report(path: Path, text: str) -> str:
    total_words = len(re.findall(r"\b\w+\b", text))
    category_hits = {category: find_hits(text, patterns) for category, patterns in KEYWORDS.items()}
    headings = re.findall(r"(?m)^\s*(?:\d+(?:\.\d+)*\s+)?([A-Z][A-Za-z][^\n]{2,90})$", text)
    title = next((line.strip() for line in text.splitlines() if len(line.strip()) > 12), path.stem)
    lines = [
        "# Preflight Scan",
        "",
        f"- **Input:** `{path}`",
        f"- **Approximate extracted words:** {total_words}",
        f"- **Extracted lines:** {line_count(text)}",
        f"- **Likely title line:** {title}",
        "- **Important:** This scan flags strings for manual inspection. It does not certify anonymity, formatting, novelty, reproducibility, or AAAI compliance.",
        "",
        "## Keyword audit",
    ]
    for category, hits in category_hits.items():
        formatted = ", ".join(f"`{h}`" for h in hits) if hits else "none found"
        lines.append(f"- **{category.replace('_', ' ').title()}:** {formatted}")
    lines += ["", "## Likely headings", ""]
    if headings:
        lines.extend(f"- {heading}" for heading in headings[:40])
    else:
        lines.append("- No reliable headings extracted; inspect the source manually.")
    lines += [
        "",
        "## Manual review checklist",
        "",
        "- Confirm that anonymized PDF metadata, acknowledgments, project URLs, and self-references do not identify authors.",
        "- Confirm that the paper defines every score, loss, module, oracle input, and tuning split used in central results.",
        "- Inspect figures/tables visually; PDF extraction can miss labels, legends, and image-only text.",
        "- Verify experiment splits, leakage safeguards, baselines, seeds, variance, and fair resource accounting.",
        "- Check current official AAAI author guidance separately; this tool intentionally does not encode venue rules.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a conservative preflight scan for an academic manuscript.")
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--json", type=Path, default=None, help="Optional machine-readable summary.")
    args = parser.parse_args()

    if not args.manuscript.exists():
        print(f"Input not found: {args.manuscript}", file=sys.stderr)
        return 2
    try:
        text = read_text(args.manuscript)
    except Exception as exc:  # pragma: no cover - CLI reporting
        print(f"Could not extract manuscript text: {exc}", file=sys.stderr)
        return 3

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(create_report(args.manuscript, text), encoding="utf-8")
    if args.json:
        payload = {
            "input": str(args.manuscript),
            "approximate_words": len(re.findall(r"\b\w+\b", text)),
            "keyword_hits": {category: find_hits(text, patterns) for category, patterns in KEYWORDS.items()},
        }
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
