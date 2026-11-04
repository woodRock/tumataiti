"""Figure: the Tūmataiti pipeline (detect → policy → pseudonymise → rehydrate).

Run by `taura build`; writes a PDF to $TAURA_OUTPUT. No data: a diagram of SPEC §5.
"""
from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

plt.rcParams.update({"font.family": "serif", "font.size": 6, "pdf.fonttype": 42})

W, H = 3.5, 1.9  # inches: one IEEE column
DEVICE = "#e8eef6"
CLOUD = "#f4ebe1"
EDGE = "#33415c"


def box(ax, x, y, w, h, text, face="white", bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.025",
                                fc=face, ec=EDGE, lw=0.6))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", linespacing=1.15,
            fontweight="bold" if bold else "normal")


def arrow(ax, a, b, text=None, dy=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=6, lw=0.6, color=EDGE,
                                 shrinkA=0, shrinkB=0))
    if text:
        ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + dy, text, ha="center", va="bottom",
                fontsize=5.5, style="italic")


def main() -> None:
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    # Device boundary (everything inside stays local) and the cloud.
    ax.add_patch(FancyBboxPatch((0.04, 0.05), 2.66, 1.80, boxstyle="round,pad=0,rounding_size=0.05",
                                fc=DEVICE, ec=EDGE, lw=0.6, ls=(0, (3, 2))))
    ax.text(2.64, 1.76, "user's device", ha="right", va="center", fontsize=6, style="italic")
    box(ax, 2.86, 0.18, 0.58, 1.46, "", face=CLOUD)
    ax.text(3.15, 1.02, "Cloud\nLLM", ha="center", va="center", fontweight="bold", fontsize=7)
    ax.text(3.15, 0.70, "sees only\nsanitised\ntext", ha="center", va="center", fontsize=5.5, style="italic")

    bw, bh = 0.58, 0.40
    xs = [0.10, 0.76, 1.42, 2.08]
    y1 = 1.18
    for x, t in zip(xs, ["Detect:\nrules, model", "Merge,\nreview", "Policy", "Pseudo-\nnymise"]):
        box(ax, x, y1, bw, bh, t)
    for a_, b_ in zip(xs, xs[1:]):
        arrow(ax, (a_ + bw, y1 + bh / 2), (b_, y1 + bh / 2))
    # Input.
    ax.text(xs[0], 1.72, "prompt, retrieved text", ha="left", va="center", fontsize=5.5, style="italic")
    arrow(ax, (xs[0] + bw / 2, 1.65), (xs[0] + bw / 2, y1 + bh))

    # Vault and rehydration under the pseudonymiser.
    x = xs[3]
    box(ax, x, 0.70, bw, 0.30, "Vault")
    box(ax, x, 0.16, bw, bh, "Rehydrate")
    arrow(ax, (x + bw / 2, y1), (x + bw / 2, 1.00))
    arrow(ax, (x + bw / 2, 0.70), (x + bw / 2, 0.16 + bh))

    # Only sanitised text crosses the boundary; the response comes back with placeholders.
    arrow(ax, (x + bw, y1 + bh / 2), (2.86, y1 + bh / 2))
    arrow(ax, (2.86, 0.36), (x + bw, 0.36))

    # Output to the user.
    arrow(ax, (x, 0.36), (1.30, 0.36))
    ax.text(0.70, 0.36, "response with\nplaceholders restored\n(display only)", ha="center", va="center", fontsize=5.5,
            style="italic")

    fig.savefig(os.environ["TAURA_OUTPUT"], metadata={"CreationDate": None, "ModDate": None})


if __name__ == "__main__":
    main()
