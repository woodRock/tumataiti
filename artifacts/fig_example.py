"""Figure: one held-out NZ document as the input (gold spans), and as the cloud
would receive it after the rules merged with the teacher and after the rules
merged with the int4 student. Leaked characters are red.

Reads artifacts/data/example_redaction.json (ml/scripts/export_example.py);
writes a PDF to $TAURA_OUTPUT.
"""
from __future__ import annotations

import json
import os
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _style import INK, INK2, LEAK, METADATA, PAGE, SERIES, plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

DATA = Path(__file__).parent / "data/example_redaction.json"
WRAP = 44          # characters per line in each panel
FS = 5.6           # font size, pt
CW = FS * 0.602 / 72  # monospace advance, inches
LH = FS * 1.45 / 72   # line height, inches


def segments(text: str, gold: list, pred: list | None) -> list[tuple[str, str]]:
    """(text, kind) runs. kind: plain, gold, placeholder, leak."""
    if pred is None:
        inside = [None] * len(text)
        for g in gold:
            for i in range(g["start"], g["end"]):
                inside[i] = "gold"
        out, i = [], 0
        while i < len(text):
            j = i
            while j < len(text) and inside[j] == inside[i]:
                j += 1
            out.append((text[i:j], inside[i] or "plain"))
            i = j
        return out
    gold_chars = set(i for g in gold for i in range(g["start"], g["end"]))
    spans = sorted(pred, key=lambda p: p["start"])
    ids: dict[tuple[str, str], int] = {}
    count: dict[str, int] = {}
    out, i = [], 0
    for p in spans:
        if p["start"] < i:
            continue
        for k in range(i, p["start"]):
            out.append((text[k], "leak" if k in gold_chars and text[k].isalnum() else "plain"))
        key = (p["category"], text[p["start"]:p["end"]].lower())
        if key not in ids:
            count[p["category"]] = count.get(p["category"], 0) + 1
            ids[key] = count[p["category"]]
        out.append((f"[{p['category']}_{ids[key]}]", "placeholder"))
        i = p["end"]
    for k in range(i, len(text)):
        out.append((text[k], "leak" if k in gold_chars and text[k].isalnum() else "plain"))
    return out


def lines(segs: list[tuple[str, str]]) -> list[list[tuple[str, str]]]:
    """Wrap runs into display lines, breaking at newlines and spaces."""
    chars = [(c, kind) for s, kind in segs for c in (s if kind != "placeholder" else [s])]
    out, cur, width = [], [], 0
    for c, kind in chars:
        if c == "\n":
            out.append(cur)
            cur, width = [], 0
            continue
        w = len(c)
        if width + w > WRAP:
            # break at the last space in the line
            cut = max((k for k, (x, _) in enumerate(cur) if x == " "), default=None)
            if cut is None:
                out.append(cur)
                cur, width = [], 0
            else:
                out.append(cur[:cut])
                cur = cur[cut + 1:]
                width = sum(len(x) for x, _ in cur)
        cur.append((c, kind))
        width += w
    out.append(cur)
    return out


def draw(ax, x0, y0, rows) -> None:
    style = {"gold": ("#d6e6f8", INK), "placeholder": ("#ecebe7", INK2), "leak": ("#f8d4d3", LEAK), "plain": (None, INK)}
    for r, row in enumerate(rows):
        y = y0 - r * LH
        x = x0
        for c, kind in row:
            face, color = style[kind]
            w = len(c) * CW
            if face:
                ax.add_patch(Rectangle((x, y - LH * 0.28), w, LH * 0.92, fc=face, ec="none", lw=0))
            ax.text(x, y, c, family="DejaVu Sans Mono", fontsize=FS, color=color, va="baseline",
                    fontweight="bold" if kind == "leak" else "normal")
            if kind == "leak":
                ax.plot([x, x + w], [y - LH * 0.22] * 2, color=LEAK, lw=0.6)
            x += w


def main() -> None:
    d = json.loads(DATA.read_text())
    panels = [("Input (gold PII shaded)", segments(d["text"], d["gold"], None)),
              ("Sent with rules + Privacy Filter", segments(d["text"], d["gold"], d["teacher"])),
              ("Sent with rules + student (int4)", segments(d["text"], d["gold"], d["student"]))]
    wrapped = [lines(s) for _, s in panels]
    nrows = max(len(w) for w in wrapped)
    pw = WRAP * CW
    gap = (PAGE - 3 * pw) / 4
    height = 0.30 + nrows * LH + 0.12
    fig = plt.figure(figsize=(PAGE, height))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, PAGE)
    ax.set_ylim(0, height)
    ax.axis("off")
    for k, ((title, _), rows) in enumerate(zip(panels, wrapped)):
        x0 = gap + k * (pw + gap)
        ax.text(x0, height - 0.10, title, fontsize=6.5, fontweight="bold", color=INK, va="top")
        ax.plot([x0, x0 + pw], [height - 0.22] * 2, color=SERIES[0] if k == 0 else INK2, lw=0.5)
        draw(ax, x0, height - 0.22 - LH, rows)
    fig.savefig(os.environ["TAURA_OUTPUT"], metadata=METADATA)


if __name__ == "__main__":
    main()
