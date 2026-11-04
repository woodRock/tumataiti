"""Uncertainty of the headline numbers (nothing is re-predicted). Bootstrap
over documents for the test_full document leak rate, the Māori − Pākehā name
gap, and DeBERTa-v3-small's difference from the other students; and leak rates
per held-out template, because a document bootstrap treats documents from the
same few templates as independent:

    taura run -- ml/.venv/bin/python ml/scripts/score_uncertainty.py

Writes ml/results/uncertainty_nz_test_full.json; export_ledger.py exports it.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ML = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ML / "src"))

from tumataiti_ml.spans import read_jsonl  # noqa: E402

BOOTSTRAPS = 10000
CONFIDENCE = 0.95
SEED = 0
RUNS = ML / "runs/m3-v2"
DATA = ML / "data/v1"
INT4 = "-open-int8-int4-block"
DETECTORS = {
    "rules_openai-privacy-filter": "rules+openai-privacy-filter",
    "rules_deberta-v3-small-open-int8-int4-block": f"rules+deberta-v3-small{INT4}",
    "rules_modernbert-base-open-int8-int4-block": f"rules+modernbert-base{INT4}",
    "rules_mdeberta-v3-base-open-int8-int4-block": f"rules+mdeberta-v3-base{INT4}",
}
DEPLOYED = "rules_deberta-v3-small-open-int8-int4-block"


def leaks(gold, preds):
    """Per document: leaked and total scored spans, as score() counts them."""
    leaked, total, person_leaked, person_total = [], [], [], []
    for g in gold:
        p = preds.get(g.id)
        covered = set()
        for s in p.spans if p else []:
            covered.update(range(s.start, s.end))
        spans = [s for s in g.spans if s.category is not None]
        hit = [any(g.text[i].isalnum() and i not in covered for i in range(s.start, s.end)) for s in spans]
        leaked.append(sum(hit))
        total.append(len(spans))
        person = [h for s, h in zip(spans, hit) if s.category == "PERSON"]
        person_leaked.append(sum(person))
        person_total.append(len(person))
    return map(np.array, (leaked, total, person_leaked, person_total))


def interval(samples: np.ndarray) -> tuple[float, float]:
    tail = 100 * (1 - CONFIDENCE) / 2
    lo, hi = np.percentile(samples, [tail, 100 - tail])
    return float(lo), float(hi)


def main() -> None:
    rng = np.random.default_rng(SEED)
    gold = list(read_jsonl(DATA / "nz_test_full.jsonl"))
    keep = np.array([any(s.category is not None for s in g.spans) for g in gold])
    templates = np.array([g.meta["template"] for g in gold])
    n = len(gold)
    index = rng.integers(0, n, size=(BOOTSTRAPS, n))

    def load(run, ds):
        return {d.id: d for d in read_jsonl(RUNS / run / f"{ds}.jsonl")}

    doc_leaked = {}
    out = defaultdict(dict)
    for det, run in DETECTORS.items():
        leaked, *_ = leaks(gold, load(run, "nz_test_full"))
        flags = (leaked > 0).astype(float)
        doc_leaked[det] = flags
        samples = (flags[index] * keep[index]).sum(1) / keep[index].sum(1)
        out["doc_leak"][det] = float(flags[keep].mean())
        out["doc_leak_lo"][det], out["doc_leak_hi"][det] = interval(samples)
        for t in sorted(set(templates)):
            mask = (templates == t) & keep
            out[f"tmpl_{t}"][det] = float(flags[mask].mean())
    for det in DETECTORS:
        if det == DEPLOYED or "openai" in det:
            continue
        diff = doc_leaked[DEPLOYED] - doc_leaked[det]
        samples = (diff[index] * keep[index]).sum(1) / keep[index].sum(1)
        out["diff_lo"][det], out["diff_hi"][det] = interval(samples)

    # The name gap: the audit documents are the same documents, so resample indices jointly.
    cf = {g: list(read_jsonl(DATA / f"nz_cf_{g}.jsonl")) for g in ("maori", "pakeha")}
    m = len(cf["maori"])
    index = rng.integers(0, m, size=(BOOTSTRAPS, m))
    for det, run in DETECTORS.items():
        rates = {}
        points = {}
        for g in cf:
            _, _, leaked, total = leaks(cf[g], load(run, f"nz_cf_{g}"))
            rates[g] = leaked[index].sum(1) / total[index].sum(1)
            points[g] = leaked.sum() / total.sum()
        out["gap"][det] = float(points["maori"] - points["pakeha"])
        out["gap_lo"][det], out["gap_hi"][det] = interval(rates["maori"] - rates["pakeha"])

    path = ML / "results/uncertainty_nz_test_full.json"
    path.write_text(json.dumps({"bootstraps": BOOTSTRAPS, "confidence": CONFIDENCE, "metrics": out}, indent=2) + "\n")
    for k in ("doc_leak", "doc_leak_lo", "doc_leak_hi", "diff_lo", "diff_hi", "gap", "gap_lo", "gap_hi"):
        print(k, {a.split("_")[1][:12]: round(100 * b, 2) for a, b in out[k].items()})
    for k, v in out.items():
        if k.startswith("tmpl_"):
            print(k, {a.split("_")[1][:12]: round(100 * b, 1) for a, b in v.items()})


if __name__ == "__main__":
    main()
