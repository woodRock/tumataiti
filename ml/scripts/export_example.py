"""Pick one held-out NZ document for the paper's example-redaction figure and
write it, with gold spans and both detectors' merged predictions, to
artifacts/data/example_redaction.json (synthetic text, safe to commit):

    taura run -- ml/.venv/bin/python ml/scripts/export_example.py

The document is the first in test_full (by id) where the rules merged with the
teacher leak a Māori person name, the rules merged with the int4 student leak
nothing, every gold span is an evaluated category, and the text fits the figure.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ML = Path(__file__).resolve().parents[1]
ROOT = ML.parent
sys.path.insert(0, str(ML / "src"))

from tumataiti_ml.synth import lexicon as lx  # noqa: E402

GOLD = ML / "data/v4/nz_test_full.jsonl"
PRED = {
    "teacher": ML / "runs/m3-v4/rules+openai-privacy-filter/nz_test_full.jsonl",
    "student": ML / "runs/m3-v4/rules+deberta-v3-small-open-int8-int4-block/nz_test_full.jsonl",
}
OUT = ROOT / "artifacts/data/example_redaction.json"
MAX_CHARS = 420
MIN_CHARS = 200


def load(path: Path) -> dict:
    return {d["id"]: d for d in map(json.loads, path.open())}


def leaked(text: str, gold: dict, pred: list[dict]) -> bool:
    covered = [False] * len(text)
    for p in pred:
        for i in range(p["start"], p["end"]):
            covered[i] = True
    return any(text[i].isalnum() and not covered[i] for i in range(gold["start"], gold["end"]))


def main() -> None:
    maori = {n for part in lx.NAMES["Māori"].values() for names in part for n in names}
    gold = load(GOLD)
    preds = {k: load(v) for k, v in PRED.items()}
    for doc_id in sorted(gold):
        g = gold[doc_id]
        text, spans = g["text"], g["spans"]
        if not (MIN_CHARS <= len(text) <= MAX_CHARS) or any(s["category"] is None for s in spans):
            continue
        t, s = preds["teacher"][doc_id]["spans"], preds["student"][doc_id]["spans"]
        teacher_leaks = [x for x in spans if leaked(text, x, t)]
        if any(leaked(text, x, s) for x in spans):
            continue
        if not any(x["category"] == "PERSON" and any(w in maori for w in text[x["start"]:x["end"]].split())
                   for x in teacher_leaks):
            continue
        keep = ("start", "end", "category")
        out = {"id": doc_id, "text": text, "gold": [{k: x[k] for k in keep} for x in spans],
               "teacher": [{k: x[k] for k in keep} for x in t], "student": [{k: x[k] for k in keep} for x in s],
               "source": {k: str(v.relative_to(ROOT)) for k, v in {"gold": GOLD, **PRED}.items()}}
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
        print(doc_id, len(text), "chars;", len(teacher_leaks), "teacher leaks")
        print(text)
        return
    sys.exit("no document matches")


if __name__ == "__main__":
    main()
