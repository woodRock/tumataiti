"""Figure: the false-alarm trade-off. For each DeBERTa-v3-small (open data)
training run, the share of standalone kinship words the model redacts (false
alarms) against held-out NZ document leakage (test_full, merged with the rules).
Reads $TAURA_RESULTS; writes a PDF to $TAURA_OUTPUT.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _style import COLUMN, INK, METADATA, SERIES, plt  # noqa: E402

# (label, detector, series slot); v2 runs share slot 1, v3 runs slot 2.
RUNS = [("v2 (shipped)", "deberta-small-open-v2", 0, (-5, -5)),
        ("v2 control A", "deberta-small-open-v2-1ep", 0, (-5, 6)),
        ("v2 control B", "deberta-small-open-v2-1ep-s1", 0, (5, 6)),
        ("v3 A", "deberta-small-open-v3", 1, (4, 2)),
        ("v3 B", "deberta-small-open-v3-s1", 1, (4, -6)),
        ("v3ids", "deberta-small-open-v3ids", 1, (-4, 3))]


def main() -> None:
    R = json.loads(Path(os.environ["TAURA_RESULTS"]).read_text())
    kin = R["m3fa_false_alarms"]["metrics"]["kin_redacted"]
    leak = R["m3fa_nz_test_full"]["metrics"]["doc_leak"]
    fig, ax = plt.subplots(figsize=(COLUMN, 1.7))
    ax.grid(axis="x", color="#e4e3df", linewidth=0.5)
    for label, det, slot, (dx, dy) in RUNS:
        x, y = 100 * kin[det], 100 * leak[f"rules_{det}"]
        ax.scatter(x, y, s=26, color=SERIES[slot], edgecolor="white", linewidth=0.6, zorder=3)
        ax.annotate(label, (x, y), xytext=(dx, dy), textcoords="offset points", fontsize=5.5, color=INK,
                    ha="left" if dx > 0 else "right", va="center")
    ax.set_xlabel("Standalone kinship words redacted by the model (%)")
    ax.set_ylabel("Held-out doc. leak (%)")
    ax.set_xlim(55, 100)
    ax.set_ylim(-0.25, 2.0)
    handles = [plt.Line2D([], [], color=SERIES[0], marker="o", ls="", markersize=4, label="v2 data"),
               plt.Line2D([], [], color=SERIES[1], marker="o", ls="", markersize=4, label="v3 data (kinship negatives)")]
    ax.legend(handles=handles, loc="upper right", bbox_to_anchor=(1.0, 0.95), handletextpad=0.2)
    fig.tight_layout(pad=0.2)
    fig.savefig(os.environ["TAURA_OUTPUT"], metadata=METADATA)


if __name__ == "__main__":
    main()
