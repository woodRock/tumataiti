"""Figure: counterfactual name audit. Person span leak rate per community on the
same test_full documents, for the rules merged with the teacher and with the
DeBERTa-v3-small student (fp32 and int4). Reads $TAURA_RESULTS; writes a PDF.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _style import COLUMN, INK2, METADATA, SERIES, plt  # noqa: E402

COMMUNITIES = [("Māori", "maori"), ("Pākehā", "pakeha"), ("Pasifika", "pasifika"), ("Asian NZ", "asian_nz")]
DETECTORS = [("Rules + Privacy Filter", "m3open_names_counterfactual", "rules_openai-privacy-filter"),
             ("Rules + student, fp32", "m3open_names_counterfactual", "rules_deberta-v3-small-open"),
             ("Rules + student, int4", "m3open_int4_names_counterfactual", "rules_deberta-v3-small-open-int8-int4-block")]


def main() -> None:
    R = json.loads(Path(os.environ["TAURA_RESULTS"]).read_text())
    fig, ax = plt.subplots(figsize=(COLUMN, 1.65))
    n = len(DETECTORS)
    width = 0.8 / n
    for j, (label, result, det) in enumerate(DETECTORS):
        m = R[result]["metrics"]
        xs = [i + (j - (n - 1) / 2) * width for i in range(len(COMMUNITIES))]
        ys = [100 * m[key][det] for _, key in COMMUNITIES]
        ax.bar(xs, ys, width=width * 0.9, color=SERIES[j], label=label, linewidth=0, zorder=2)
        for x, y in zip(xs, ys):
            ax.text(x, y + 1, f"{y:.1f}", ha="center", va="bottom", fontsize=4.8, color=INK2)
    ax.set_xticks(range(len(COMMUNITIES)), [c for c, _ in COMMUNITIES])
    ax.set_ylabel("Person span leak rate (%)")
    ax.set_ylim(0, 60)
    ax.tick_params(axis="x", length=0)
    ax.legend(loc="upper right", handlelength=1)
    fig.tight_layout(pad=0.2)
    fig.savefig(os.environ["TAURA_OUTPUT"], metadata=METADATA)


if __name__ == "__main__":
    main()
