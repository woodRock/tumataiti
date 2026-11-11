"""Affiliation (iwi and marae): how often the int4 open students, merged with
the rules, leave it showing and how often they tag it as affiliation. The
students learn AFFILIATION but the main scoring ignores it (taxonomy.py), so it
is scored here, with nothing retrained.

The generator draws iwi and marae from closed lists (lexicon.IWI, lexicon.MARAE)
shared by every split, so the test sets only contain names the students saw in
training. heldout swaps each affiliation span of the test sets for a name that
is in neither list, shifting the other spans, and runs the students on it.

    taura run -- ml/.venv/bin/python ml/scripts/score_affiliation.py

or on the ECS Grid as jobs.py jobs affiliation/gold, affiliation/rules,
affiliation/<set>/<student> and report/affiliation.

Writes ml/results/m3open_<seen|heldout>_<set>_affiliation.{json,md}, per
detector: spans (gold affiliation spans), leaked (share with a character no
prediction covers), tagged (share fully covered by AFFILIATION predictions),
and precision (share of AFFILIATION predictions that overlap a gold
affiliation span).
"""

from __future__ import annotations

import json
import os
import random
import sys
from pathlib import Path

ML = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ML / "src"))
sys.path.insert(0, str(ML / "scripts"))

from robustness import STUDENTS, cli  # noqa: E402
from tumataiti_ml.spans import Doc, Span, read_jsonl, write_jsonl  # noqa: E402
from tumataiti_ml.synth import lexicon as lx  # noqa: E402

SETS = ["nz_test_full", "nz_test_names"]
VARIANT = "aff_heldout"
SEED = 0
# Real iwi and marae outside lexicon.IWI and lexicon.MARAE. To be checked by a
# Māori colleague, as the paper's other te reo material is.
HELDOUT_IWI = ["Te Arawa", "Ngāti Whātua", "Ngāti Maniapoto", "Te Rarawa", "Ngāti Awa", "Ngāti Tūwharetoa",
               "Whakatōhea", "Ngāti Ruanui", "Ngāti Toa Rangatira", "Rongowhakaata", "Ngāi Te Rangi", "Rangitāne"]
HELDOUT_MARAE = ["Tūrangawaewae Marae", "Ōrākei Marae", "Waiwhetū Marae", "Pipitea Marae", "Hoani Waititi Marae",
                 "Takahanga Marae", "Tuahiwi Marae", "Koriniti Marae"]
assert not set(HELDOUT_IWI) & set(lx.IWI) and not set(HELDOUT_MARAE) & set(lx.MARAE)


def is_aff(span: Span) -> bool:
    return span.label.startswith("AFFILIATION")


def swap(doc: Doc, rng: random.Random) -> Doc:
    """doc with every gold affiliation span replaced by a held-out name."""
    text, spans, shift, pos = [], [], 0, 0
    for s in sorted(doc.spans, key=lambda s: (s.start, s.end)):
        if s.start < pos:  # overlapping gold spans don't occur in the generator's output
            raise ValueError(f"{doc.id}: overlapping gold spans")
        value = doc.text[s.start:s.end]
        if is_aff(s):
            value = rng.choice(HELDOUT_MARAE if s.label.endswith(".marae") else HELDOUT_IWI)
        text.append(doc.text[pos:s.start])
        start = s.start + shift
        spans.append(Span(start, start + len(value), s.label, s.category, s.confidence))
        text.append(value)
        shift += len(value) - (s.end - s.start)
        pos = s.end
    text.append(doc.text[pos:])
    meta = dict(doc.meta)
    meta.pop("negatives", None)  # offsets moved; not used by this scoring
    return Doc(id=doc.id, text="".join(text), spans=spans, meta=meta)


def gold() -> None:
    rng = random.Random(SEED)
    for ds in SETS:
        docs = [swap(d, rng) for d in read_jsonl(ML / "data/v1" / f"{ds}.jsonl")]
        path = ML / "data/robust" / VARIANT / f"{ds}.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(f".{os.getpid()}.tmp")
        write_jsonl(tmp, docs)
        tmp.replace(path)


def rules() -> None:
    for ds in SETS:
        cli("predict", "--detector", "rules", "--gold", f"data/robust/{VARIANT}/{ds}.jsonl",
            "--out", f"runs/robust/{VARIANT}/rules/{ds}.jsonl")


def predict(ds: str, m: str) -> None:
    cli("predict", "--detector", "student-onnx", "--model", f"runs/m3-v2/{m}/onnx/model_int8_int4-block.onnx",
        "--gold", f"data/robust/{VARIANT}/{ds}.jsonl", "--out", f"runs/robust/{VARIANT}/{m}/{ds}.jsonl")


def measure(golds: list[Doc], preds: dict[str, Doc]) -> dict:
    spans = leaked = tagged = predicted = correct = 0
    for g in golds:
        p = preds[g.id].spans
        aff = [s for s in g.spans if is_aff(s)]
        covered = [False] * len(g.text)
        as_aff = [False] * len(g.text)
        for s in p:
            for i in range(s.start, min(s.end, len(g.text))):
                covered[i] = True
                as_aff[i] = as_aff[i] or is_aff(s)
        for s in aff:
            chars = [i for i in range(s.start, s.end) if g.text[i].isalnum()]
            spans += 1
            leaked += not all(covered[i] for i in chars)
            tagged += all(as_aff[i] for i in chars)
        for s in p:
            if is_aff(s):
                predicted += 1
                correct += any(s.start < a.end and a.start < s.end for a in aff)
    out = {"docs": len(golds), "spans": spans, "predicted": predicted,
           "precision": correct / predicted if predicted else None}
    if spans:
        out |= {"leaked": leaked / spans, "tagged": tagged / spans}
    return out


def write(name: str, title: str, rows: dict[str, dict]) -> None:
    metrics: dict[str, dict] = {}
    for det, r in rows.items():
        for stat, v in r.items():
            if v is not None:
                metrics.setdefault(stat, {})[det.replace("+", "_")] = v
    out = ML / "results" / name
    out.with_suffix(".json").write_text(json.dumps({"title": title, "metrics": metrics}, indent=2,
                                                   ensure_ascii=False) + "\n")
    pct = lambda v: "–" if v is None else f"{v * 100:.1f}%"  # noqa: E731
    lines = [f"## {title}", "", "| Detector | Spans | Leaked | Tagged | Precision |", "|---|---:|---:|---:|---:|"]
    lines += [f"| {d} | {r['spans']} | {pct(r.get('leaked'))} | {pct(r.get('tagged'))} | {pct(r['precision'])} |"
              for d, r in rows.items()]
    out.with_suffix(".md").write_text("\n".join(lines) + "\n")


def report() -> None:
    runs = Path("runs/robust") / VARIANT
    for ds in SETS:
        for m in STUDENTS:
            cli("combine", "--primary", str(runs / "rules" / f"{ds}.jsonl"), "--secondary", str(runs / m / f"{ds}.jsonl"),
                "--out", str(runs / f"rules+{m}" / f"{ds}.jsonl"))
    for ds in SETS:
        golds = list(read_jsonl(ML / "data/v1" / f"{ds}.jsonl"))
        seen = {f"rules+{m}": {d.id: d for d in read_jsonl(ML / "runs/m3-v2" / f"rules+{m}-int8-int4-block" / f"{ds}.jsonl")}
                for m in STUDENTS}
        write(f"m3open_seen_{ds}_affiliation", f"Affiliation, names seen in training: {ds}",
              {n: measure(golds, p) for n, p in seen.items()})
    for ds in SETS:
        golds = list(read_jsonl(ML / "data/robust" / VARIANT / f"{ds}.jsonl"))
        held = {f"rules+{m}": {d.id: d for d in read_jsonl(ML / runs / f"rules+{m}" / f"{ds}.jsonl")} for m in STUDENTS}
        write(f"m3open_heldout_{ds}_affiliation", f"Affiliation, held-out names: {ds}",
              {n: measure(golds, p) for n, p in held.items()})


def main() -> None:
    gold()
    rules()
    for ds in SETS:
        for m in STUDENTS:
            predict(ds, m)
    report()


if __name__ == "__main__":
    main()
