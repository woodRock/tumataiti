"""Figure: held-out NZ document leakage rate (test_full, merged with the rules)
by training data, per backbone: NZ data v1 or v2 with PII-Masking-300k, and v2
with the open English sets. The teacher is a reference line. Reads
$TAURA_RESULTS; writes a PDF to $TAURA_OUTPUT.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _style import COLUMN, INK2, METADATA, SERIES, plt  # noqa: E402

STUDENTS = [("DeBERTa-v3-small", "deberta-v3-small"), ("ModernBERT-base", "modernbert-base"),
            ("mDeBERTa-v3-base", "mdeberta-v3-base")]
VERSIONS = [("v1 + PII-Masking-300k", "m3v2_nz_test_full", "-v1"),
            ("v2 + PII-Masking-300k", "m3v2_nz_test_full", ""),
            ("v2 + open English", "m3open_nz_test_full", "-open")]


def main() -> None:
    R = json.loads(Path(os.environ["TAURA_RESULTS"]).read_text())
    fig, ax = plt.subplots(figsize=(COLUMN, 1.85))
    n = len(VERSIONS)
    width = 0.8 / n
    for j, (label, result, suffix) in enumerate(VERSIONS):
        m = R[result]["metrics"]["doc_leak"]
        xs = [i + (j - (n - 1) / 2) * width for i in range(len(STUDENTS))]
        ys = [100 * m[f"rules_{det}{suffix}"] for _, det in STUDENTS]
        ax.bar(xs, ys, width=width * 0.9, color=SERIES[j], label=label, linewidth=0, zorder=2)
        for x, y in zip(xs, ys):
            ax.text(x, y + 0.8, f"{y:.1f}", ha="center", va="bottom", fontsize=4.8, color=INK2)
    teacher = 100 * R["m3open_nz_test_full"]["metrics"]["doc_leak"]["rules_openai-privacy-filter"]
    ax.axhline(teacher, color=INK2, lw=0.7, ls="--", zorder=1)
    ax.text(len(STUDENTS) - 0.55, teacher - 1.2, f"rules + Privacy Filter ({teacher:.1f})", ha="right", va="top",
            fontsize=5.5, color=INK2)
    ax.set_xticks(range(len(STUDENTS)), [s for s, _ in STUDENTS])
    ax.tick_params(axis="x", labelsize=6)
    ax.set_ylabel("Document leakage rate (%)")
    ax.set_ylim(0, 50)
    ax.tick_params(axis="x", length=0)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, handlelength=1, columnspacing=0.8, fontsize=5.5)
    fig.tight_layout(pad=0.2)
    fig.savefig(os.environ["TAURA_OUTPUT"], metadata=METADATA)


if __name__ == "__main__":
    main()
