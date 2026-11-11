"""Score kinship-word false alarms per word (SPEC §9.8, finding 2) for the
data-v4 and v4kin DeBERTa-v3-small runs (runs/m3-v4fa, score_fa.sh): the share of standalone held-out kinship
words each model redacts, per word and per language group, with the same
definition as `tumataiti-ml false-alarms` (analysis.false_alarms). Run from the
repo root:

    taura run -- ml/.venv/bin/python ml/scripts/score_kinship_words.py

Writes ml/results/m3fa_kinwords_false_alarms.{json,md}; export_ledger.py turns
it into \\res{m3fa_kinwords_false_alarms/kin_<word>_redacted/<run>}.
"""

from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path

ML = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ML / "src"))

from tumataiti_ml.analysis import false_alarms  # noqa: E402
from tumataiti_ml.spans import Doc, read_jsonl  # noqa: E402
from tumataiti_ml.synth import lexicon as lx  # noqa: E402

GOLD = ML / "data/v4/nz_test_false_alarm.jsonl"
RUNS = ML / "runs/m3-v4fa"
MODELS = ["deberta-small-open-v4", "deberta-small-open-v4-1ep", "deberta-small-open-v4-1ep-s1",
          "deberta-small-open-v4kin", "deberta-small-open-v4kin-s1", "deberta-small-open-v4ids"]
# Held-out kinship words by language. Nana is used in both NZ English and te
# reo, so it is reported per word only.
TE_REO = {"Koroua", "Tāua", "Pōua", "Kaumātua"}
ENGLISH = {"Grandad", "Granny", "Auntie"}
OUT = ML / "results/m3fa_kinwords_false_alarms"


def slug(word: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", word) if c.isascii()).lower()


def relabel(doc: Doc) -> Doc:
    """Keep only the standalone kinship slots, labelled by word and by group."""
    negatives = []
    for a, b, slot in doc.meta.get("negatives", []):
        if slot != "kin":
            continue
        word = doc.text[a:b]
        negatives.append([a, b, f"kin_{slug(word)}"])
        if word in TE_REO:
            negatives.append([a, b, "kin_te_reo"])
        elif word in ENGLISH:
            negatives.append([a, b, "kin_english"])
    return Doc(id=doc.id, text=doc.text, spans=[], meta={**doc.meta, "negatives": negatives})


def main() -> None:
    held_out = set(lx.KINSHIP[1])
    assert TE_REO | ENGLISH <= held_out, "groups must be held-out kinship words"
    gold = [relabel(d) for d in read_jsonl(GOLD)]
    rows = {}
    for m in MODELS:
        preds = {d.id: d for d in read_jsonl(RUNS / m / "nz_test_false_alarm.jsonl")}
        rows[m] = {k: v for k, v in false_alarms(gold, preds).items() if k.startswith("not PII: ")}
    OUT.with_suffix(".json").write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")
    keys = list(next(iter(rows.values())))
    lines = ["| Slot | n | " + " | ".join(MODELS) + " |", "|---|---:|" + "---:|" * len(MODELS)]
    for k in keys:
        lines.append(f"| {k} | {rows[MODELS[0]][k]['n']} | "
                     + " | ".join(f"{rows[m][k]['redacted'] * 100:.1f}%" for m in MODELS) + " |")
    OUT.with_suffix(".md").write_text(
        "## Held-out kinship words redacted by the model alone (false-alarm set)\n\n"
        "Lower is better. te reo: " + ", ".join(sorted(TE_REO)) + "; English: " + ", ".join(sorted(ENGLISH))
        + ".\n\n" + "\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
