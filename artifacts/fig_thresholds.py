"""Figure: operating points. test_full document leak rate against character
precision for the int4 open students, merged with the rules, across decoding
thresholds. Reads $TAURA_RESULTS; writes a PDF to $TAURA_OUTPUT.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _style import COLUMN, INK2, METADATA, SERIES, plt  # noqa: E402

STUDENTS = [("DeBERTa-v3-small", "deberta-v3-small-open"), ("ModernBERT-base", "modernbert-base-open"),
            ("mDeBERTa-v3-base", "mdeberta-v3-base-open")]


def main() -> None:
    m = json.loads(Path(os.environ["TAURA_RESULTS"]).read_text())["m3open_thresholds_nz_test_full"]["metrics"]
    fig, ax = plt.subplots(figsize=(COLUMN, 1.75))
    ax.grid(axis="x", color="#e4e3df", linewidth=0.5)
    for j, (label, det) in enumerate(STUDENTS):
        keys = sorted((k for k in m["doc_leak"] if k.startswith(f"rules_{det}-t")),
                      key=lambda k: float(k.rsplit("-t", 1)[1]))
        xs = [100 * m["precision"][k] for k in keys]
        ys = [100 * m["doc_leak"][k] for k in keys]
        ax.plot(xs, ys, color=SERIES[j], lw=1, marker="o", markersize=3.5, markeredgecolor="white",
                markeredgewidth=0.4, label=label, zorder=3)
        ax.annotate(f"t={keys[-1].rsplit('-t', 1)[1]}", (xs[-1], ys[-1]), xytext=(3, 3), textcoords="offset points",
                    fontsize=5, color=INK2)
    ax.set_xlabel("Character precision (%)")
    ax.set_ylabel("Document leakage rate (%)")
    ax.legend(loc="upper left", handlelength=1.2)
    fig.tight_layout(pad=0.2)
    fig.savefig(os.environ["TAURA_OUTPUT"], metadata=METADATA)


if __name__ == "__main__":
    main()
