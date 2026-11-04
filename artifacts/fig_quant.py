"""Figure: quantisation trade-off for the data-v2 students. Held-out NZ document
leakage rate (merged with the rules) against ONNX file size, for fp32, dynamic
int8, and int8 embeddings with an fp16 or int4 encoder. Reads $TAURA_RESULTS;
writes a PDF to $TAURA_OUTPUT.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _style import COLUMN, INK2, METADATA, SERIES, plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

STUDENTS = [("DeBERTa-v3-small", "deberta-v3-small"), ("ModernBERT-base", "modernbert-base"),
            ("mDeBERTa-v3-base", "mdeberta-v3-base")]
# (label, marker, result, detector suffix, size suffix)
VARIANTS = [("fp32", "o", "m3v2_int8_nz_test_full", "", "fp32"),
            ("dynamic int8", "X", "m3v2_int8_nz_test_full", "-int8", "int8"),
            ("fp16 encoder", "s", "m3v2_fp16_nz_test_full", "-int8-fp16", "fp16"),
            ("int4 encoder", "^", "m3v2_int4_nz_test_full", "-int8-int4-block", "int4")]


def main() -> None:
    R = json.loads(Path(os.environ["TAURA_RESULTS"]).read_text())
    mb = R["inventory"]["metrics"]["mb"]
    fig, ax = plt.subplots(figsize=(COLUMN, 1.9))
    ax.grid(axis="x", color="#e4e3df", linewidth=0.5)
    for j, (label, det) in enumerate(STUDENTS):
        pts = []
        for vlabel, marker, result, suffix, size in VARIANTS:
            x = mb[f"{det}-{size}"]
            y = 100 * R[result]["metrics"]["doc_leak"][f"rules_{det}{suffix}"]
            pts.append((x, y))
            ax.scatter(x, y, s=22, marker=marker, color=SERIES[j], edgecolor="white", linewidth=0.6, zorder=3)
        # fp32 -> int4, the shipping path
        ax.plot([pts[0][0], pts[3][0]], [pts[0][1], pts[3][1]], color=SERIES[j], lw=0.8, ls=":", zorder=2)
    ax.set_xscale("log")
    ax.set_xticks([100, 200, 400, 800], ["100", "200", "400", "800"])
    ax.minorticks_off()
    ax.set_xlabel("ONNX file size (MB, log scale)")
    ax.set_ylabel("Document leakage rate (%)")
    ax.set_ylim(0, 70)
    colours = [Line2D([], [], color=SERIES[j], marker="o", ls="", markersize=4, label=s) for j, (s, _) in enumerate(STUDENTS)]
    shapes = [Line2D([], [], color=INK2, marker=m, ls="", markersize=4, label=v) for v, m, *_ in VARIANTS]
    first = ax.legend(handles=colours, loc="upper right", handletextpad=0.2)
    ax.add_artist(first)
    ax.legend(handles=shapes, loc="center right", bbox_to_anchor=(1.0, 0.42), handletextpad=0.2)
    fig.tight_layout(pad=0.2)
    fig.savefig(os.environ["TAURA_OUTPUT"], metadata=METADATA)


if __name__ == "__main__":
    main()
