"""Shared figure style: IEEE column sizes, serif text, and the reference
categorical palette (slots in fixed order; light mode, for print)."""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

COLUMN = 3.5   # inches, one IEEE column
PAGE = 7.16    # inches, full IEEE page width
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]  # blue, orange, aqua, yellow
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e4e3df"
LEAK = "#e34948"
METADATA = {"CreationDate": None, "ModDate": None}

plt.rcParams.update({
    "font.family": "serif", "font.size": 7, "pdf.fonttype": 42,
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "axes.linewidth": 0.5,
    "xtick.color": INK2, "ytick.color": INK2, "xtick.major.width": 0.5, "ytick.major.width": 0.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "axes.grid.axis": "y", "grid.color": GRID, "grid.linewidth": 0.5,
    "legend.frameon": False, "legend.fontsize": 6,
})
