"""Export the score files in ml/results/ to taura results in ledger/results/,
so the paper can cite them as \\res{<result>/<measure>/<detector>}:

    taura run -- python3 ml/scripts/export_ledger.py

One result per score file, named after it (m3open_nz_test_full). Detector
names are as in the tables, with "+" written "_" (rules_deberta-v3-small-open).

- score files: docs (documents scored), and per detector doc_leak,
  span_leak, precision, recall, f1 (any-PII characters), exact_f1, ms
  (median per document) and leak_<category> (span leak rate);
- counterfactual audits: maori, pakeha, pasifika, asian_nz (name leak
  rate) and gap (Māori − Pākehā), per detector;
- false-alarm files: <slot>_redacted and <slot>_flagged for text that is
  not PII, and <slot>_leaked for the PII beside it, per detector;
- browser latency (browser_*.json, demo/src/bench.ts): docs, ms (median per
  document) and ms_p90, per detector (rules, the shipped student, both merged).

Rates are fractions; ledger/artifacts.toml formats them as percentages. Each
result names its source file, which taura links to the run that wrote it.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "ml/results"
OUT = ROOT / "ledger/results"
COMMUNITIES = {"Māori": "maori", "Pākehā": "pakeha", "Pasifika": "pasifika", "Asian NZ": "asian_nz"}


def key(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", name.replace("+", "_"))


def from_score(data: dict) -> dict:
    metrics: dict[str, dict] = {}

    def put(measure: str, detector: str, value) -> None:
        if value is not None:
            metrics.setdefault(measure, {})[key(detector)] = value

    for det, r in data["results"].items():
        put("doc_leak", det, r["doc_leak_rate"])
        put("span_leak", det, r["span_leak_rate"])
        for stat in ("precision", "recall", "f1"):
            put(stat, det, r["char_any"][stat])
        put("exact_f1", det, r["exact_all"]["f1"])
        for cat, rate in r["span_leak_rate_by_category"].items():
            put(f"leak_{cat.lower()}", det, rate)
        seconds = (data.get("timings", {}).get(det) or {}).get("seconds_median")
        put("ms", det, None if seconds is None else seconds * 1000)
    docs = {r["docs"] for r in data["results"].values()}
    if len(docs) == 1:
        metrics["docs"] = docs.pop()
    return metrics


def from_counterfactual(data: dict) -> dict:
    metrics: dict[str, dict] = {}
    for det, rates in data.items():
        for community, measure in COMMUNITIES.items():
            metrics.setdefault(measure, {})[key(det)] = rates[community]
        metrics.setdefault("gap", {})[key(det)] = rates["Māori"] - rates["Pākehā"]
    return metrics


def from_false_alarms(data: dict) -> dict:
    metrics: dict[str, dict] = {}
    for det, rows in data.items():
        for slot, r in rows.items():
            kind, name = slot.split(": ", 1)  # "not PII: kin", "PII: given"
            for stat in ("leaked",) if kind == "PII" else ("redacted", "flagged"):
                metrics.setdefault(f"{key(name)}_{stat}", {})[key(det)] = r[stat]
    return metrics


def from_browser(data: dict) -> dict:
    name = data["model"]["name"] + "-int4"
    dets = {"rules": "rules", "student": name, "rules_student": f"rules_{name}"}
    return {
        "docs": data["docs"],
        "ms": {dets[k]: v["median"] for k, v in data["ms"].items()},
        "ms_p90": {dets[k]: v["p90"] for k, v in data["ms"].items()},
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for path in sorted(SRC.glob("*.json")):
        data = json.loads(path.read_text())
        if "results" in data:
            metrics = from_score(data)
        elif path.stem.endswith("_false_alarms"):
            metrics = from_false_alarms(data)
        elif path.stem.endswith("_counterfactual"):
            metrics = from_counterfactual(data)
        elif path.stem.startswith("browser_"):
            metrics = from_browser(data)
        else:
            continue
        result = {
            "name": path.stem,
            "metrics": metrics,
            "source": {"path": str(path.relative_to(ROOT))},
            "produced_by": "ml/scripts/export_ledger.py",
        }
        (OUT / f"{path.stem}.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        print(f"ledger/results/{path.stem}.json: {sum(len(v) if isinstance(v, dict) else 1 for v in metrics.values())} values")


if __name__ == "__main__":
    main()
