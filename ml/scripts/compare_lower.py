"""Decide whether the lowercase-retrained DeBERTa-v3-small should replace the
deployed one: both int4, merged with the rules, on every evaluation the deployed
student has. test_full on each typing comes from score_lower.py; this adds the
other sets, the review layer on the false-alarm set, the decoding thresholds,
the kinship words and bootstrap intervals, and counts who wins:

    taura run -- ml/.venv/bin/python ml/scripts/compare_lower.py

Writes ml/results/m3open_lowercmp_* . The scoreboard's rows are fixed here before
the results are seen. A row is tied if both models print the same value.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ML = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ML / "scripts"))
sys.path.insert(0, str(ML / "src"))

from score_kinship_words import ENGLISH, TE_REO, relabel  # noqa: E402
from score_lower import ONNX, RUNS, TYPINGS, V2, cli, gold, prediction  # noqa: E402
from score_uncertainty import BOOTSTRAPS, CONFIDENCE, SEED, interval, leaks  # noqa: E402
from thresholds import THRESHOLDS  # noqa: E402
from thresholds import RUNS as THRESHOLD_RUNS  # noqa: E402

from tumataiti_ml.analysis import false_alarms  # noqa: E402
from tumataiti_ml.spans import read_jsonl  # noqa: E402

SETS = {"nz_test_names": "data/v4", "open_en_test": "data/open", "pii300k_en_val": "data/v1",
        "nz_test_false_alarm": "data/v4"}
FA = "nz_test_false_alarm"
FULL = "nz_test_full"
DEPLOYED = "deberta-v3-small-open"
OURS = Path("runs/lowercmp-v4")
SLOTS = ["booking_code", "hui_date", "invoice", "kin", "order_ref", "town"]


def student(model: str, ds: str) -> Path:
    if model == "deployed":
        return V2 / f"{DEPLOYED}-int8-int4-block" / f"{ds}.jsonl"
    return prediction("plain", ds)


def threshold_prediction(t: float | str) -> Path:
    return RUNS / "thresholds" / f"t{t}" / f"{FULL}.jsonl"


def predict(ds: str) -> None:
    cli("predict", "--detector", "student-onnx", "--model", str(ONNX / "model_int8_int4-block.onnx"),
        "--gold", f"{SETS[ds]}/{ds}.jsonl", "--out", str(prediction("plain", ds)))


def predict_threshold(t: float | str) -> None:
    cli("predict", "--detector", "student-onnx", "--model", str(ONNX / "model_int8_int4-block.onnx"),
        "--threshold", str(t), "--gold", f"data/v4/{FULL}.jsonl", "--out", str(threshold_prediction(t)))


def merged(name: str, ds: str) -> Path:
    return OURS / f"rules+{name}" / f"{ds}.jsonl"


def merge(secondary: Path, name: str, ds: str) -> Path:
    cli("combine", "--primary", str(V2 / "rules" / f"{ds}.jsonl"), "--secondary", str(secondary),
        "--out", str(merged(name, ds)))
    return merged(name, ds)


def score_sets() -> None:
    for ds, folder in SETS.items():
        runs = [merge(student(m, ds), m, ds) for m in ("deployed", "retrained")]
        cli("score", "--gold", f"{folder}/{ds}.jsonl", "--pred", *map(str, runs), "--title", f"Deployed and retrained, int4: {ds}",
            "--markdown", f"results/m3open_lowercmp_{ds}.md", "--json", f"results/m3open_lowercmp_{ds}.json")


def score_false_alarms() -> None:
    gold_file = f"data/v4/{FA}.jsonl"
    runs = []
    for m in ("deployed", "retrained"):
        runs.append(merged(m, FA))
        for tag, flags in (("review", []), ("txn", ["--transaction-labels"])):
            out = OURS / f"{m}+{tag}" / f"{FA}.jsonl"
            cli("review", "--gold", gold_file, "--pred", str(student(m, FA)), "--out", str(out), *flags)
            runs.append(merge(out, f"{m}+{tag}", FA))
    cli("false-alarms", "--gold", gold_file, "--pred", *map(str, runs), "--title", "Deployed and retrained, int4: false-alarm set",
        "--markdown", "results/m3open_lowercmp_false_alarms.md", "--json", "results/m3open_lowercmp_false_alarms.json")


def score_thresholds() -> None:
    runs = []
    for t in THRESHOLDS:
        runs.append(THRESHOLD_RUNS / f"rules+{DEPLOYED}-t{t}" / f"{FULL}.jsonl")
        runs.append(merge(threshold_prediction(t), f"retrained-t{t}", FULL))
    cli("score", "--gold", f"data/v4/{FULL}.jsonl", "--pred", *map(str, runs), "--title", "Deployed and retrained, int4, across decoding thresholds",
        "--markdown", "results/m3open_lowercmp_thresholds_nz_test_full.md",
        "--json", "results/m3open_lowercmp_thresholds_nz_test_full.json")


def score_kinship() -> None:
    docs = [relabel(d) for d in read_jsonl(ML / "data/v4" / f"{FA}.jsonl")]
    rows = {}
    for m in ("deployed", "retrained"):
        preds = {d.id: d for d in read_jsonl(ML / student(m, FA))}
        rows[m] = {k: v for k, v in false_alarms(docs, preds).items() if k.startswith("not PII: ")}
    out = ML / "results/m3open_lowercmp_kinwords_false_alarms"
    out.with_suffix(".json").write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")
    lines = ["| Slot | n | deployed | retrained |", "|---|---:|---:|---:|"]
    lines += [f"| {k} | {rows['deployed'][k]['n']} | {rows['deployed'][k]['redacted'] * 100:.1f}% | "
              f"{rows['retrained'][k]['redacted'] * 100:.1f}% |" for k in rows["deployed"]]
    out.with_suffix(".md").write_text(
        "## Held-out kinship words redacted by the model alone, int4 (false-alarm set)\n\nLower is better. te reo: "
        + ", ".join(sorted(TE_REO)) + "; English: " + ", ".join(sorted(ENGLISH)) + ".\n\n" + "\n".join(lines) + "\n")


def doc_flags(docs: list, path: Path) -> np.ndarray:
    preds = {d.id: d for d in read_jsonl(ML / path)}
    leaked, *_ = leaks(docs, preds)
    return leaked > 0


def views() -> dict[str, tuple[Path, Path, Path]]:
    """Name: gold file and the deployed and retrained runs, all merged with the rules."""
    out = {}
    for t in TYPINGS:
        deployed = V2 / f"rules+{DEPLOYED}-int8-int4-block" if t == "plain" else Path("runs/robust-v4") / t / f"rules+{DEPLOYED}"
        out[f"{FULL}/{t}"] = (gold(t, FULL), deployed / f"{FULL}.jsonl", RUNS / t / "rules+deberta-v3-small-open-lower-int4" / f"{FULL}.jsonl")
    for ds, folder in SETS.items():
        out[ds] = (Path(folder) / f"{ds}.jsonl", merged("deployed", ds), merged("retrained", ds))
    return out


def score_intervals() -> None:
    rng = np.random.default_rng(SEED)
    runs = views()
    out = {"bootstraps": BOOTSTRAPS, "confidence": CONFIDENCE, "doc_leak": {}, "gap": {}, "templates": {}}
    for view, (gold_file, deployed, retrained) in runs.items():
        docs = list(read_jsonl(ML / gold_file))
        keep = np.array([any(s.category is not None for s in d.spans) for d in docs])
        a, b = doc_flags(docs, deployed), doc_flags(docs, retrained)
        index = rng.integers(0, len(docs), size=(BOOTSTRAPS, len(docs)), dtype=np.int32)
        kept = keep[index].sum(1)
        diff = ((a[index] & keep[index]).sum(1) - (b[index] & keep[index]).sum(1)) / kept
        lo, hi = interval(diff)
        out["doc_leak"][view] = {"deployed": float(a[keep].mean()), "retrained": float(b[keep].mean()),
                                 "deployed_minus_retrained_lo": lo, "deployed_minus_retrained_hi": hi}
        if view.startswith(FULL):
            templates = np.array([d.meta["template"] for d in docs])
            out["templates"][view] = {str(t): {"deployed": float(a[(templates == t) & keep].mean()),
                                               "retrained": float(b[(templates == t) & keep].mean())}
                                      for t in sorted(set(templates))}
    for t in TYPINGS:
        data = ML / gold(t, "x").parent
        cf = {g: list(read_jsonl(data / f"nz_cf_{g}.jsonl")) for g in ("maori", "pakeha")}
        n = len(cf["maori"])
        index = rng.integers(0, n, size=(BOOTSTRAPS, n), dtype=np.int32)
        out["gap"][t] = {}
        for name, run in zip(("deployed", "retrained"), (p.parent for p in runs[f"{FULL}/{t}"][1:])):
            rates, points = {}, {}
            for g in cf:
                preds = {d.id: d for d in read_jsonl(ML / run / f"nz_cf_{g}.jsonl")}
                _, _, leaked, total = leaks(cf[g], preds)
                rates[g] = leaked[index].sum(1) / total[index].sum(1)
                points[g] = leaked.sum() / total.sum()
            lo, hi = interval(rates["maori"] - rates["pakeha"])
            out["gap"][t][name] = {"gap": float(points["maori"] - points["pakeha"]), "lo": lo, "hi": hi}
    (ML / "results/m3open_lowercmp_intervals.json").write_text(json.dumps(out, indent=2) + "\n")


def scoreboard() -> None:
    """One row per comparison. Lower is better unless the row is an F1."""
    rows = []

    def row(name: str, deployed: float, retrained: float, higher_better: bool = False) -> None:
        a, b = round(deployed * 100, 1), round(retrained * 100, 1)
        winner = "tie" if a == b else ("retrained" if (b > a) == higher_better else "deployed")
        rows.append({"row": name, "deployed": a, "retrained": b, "winner": winner})

    tables = {}
    for t in TYPINGS:
        data = json.loads((ML / f"results/m3open_lowertrain_{t}_{FULL}.json").read_text())["results"]
        names = list(data)
        tables[f"{FULL}/{t}"] = (data[names[0]], data[names[-1]])
    for ds in SETS:
        data = json.loads((ML / f"results/m3open_lowercmp_{ds}.json").read_text())["results"]
        tables[ds] = (data["rules+deployed"], data["rules+retrained"])
    for view, (a, b) in tables.items():
        row(f"{view}: document leak", a["doc_leak_rate"], b["doc_leak_rate"])
        row(f"{view}: span leak", a["span_leak_rate"], b["span_leak_rate"])
        row(f"{view}: char F1", a["char_any"]["f1"], b["char_any"]["f1"], True)
        row(f"{view}: exact-span F1", a["exact_all"]["f1"], b["exact_all"]["f1"], True)
    intervals = json.loads((ML / "results/m3open_lowercmp_intervals.json").read_text())
    for t in TYPINGS:
        gap = intervals["gap"][t]
        row(f"{t}: size of the Māori − Pākehā gap", abs(gap["deployed"]["gap"]), abs(gap["retrained"]["gap"]))
    alarms = json.loads((ML / "results/m3open_lowercmp_false_alarms.json").read_text())
    a, b = (alarms[f"rules+{m}+review"] for m in ("deployed", "retrained"))
    for slot in SLOTS:
        row(f"false alarm after review: {slot}", a[f"not PII: {slot}"]["redacted"], b[f"not PII: {slot}"]["redacted"])
    wins = {w: sum(r["winner"] == w for r in rows) for w in ("retrained", "deployed", "tie")}
    out = ML / "results/m3open_lowercmp_scoreboard"
    out.with_suffix(".json").write_text(json.dumps({"wins": wins, "rows": rows}, indent=2, ensure_ascii=False) + "\n")
    lines = ["| Row | Deployed | Retrained | Better |", "|---|---:|---:|---|"]
    lines += [f"| {r['row']} | {r['deployed']} | {r['retrained']} | {r['winner']} |" for r in rows]
    out.with_suffix(".md").write_text(f"## Deployed and retrained, int4\n\n{wins}\n\n" + "\n".join(lines) + "\n")
    print(wins)


def report() -> None:
    score_sets()
    score_false_alarms()
    score_thresholds()
    score_kinship()
    score_intervals()
    scoreboard()


def main() -> None:
    for ds in SETS:
        if not (ML / prediction("plain", ds).with_suffix(".meta.json")).exists():
            predict(ds)
    for t in THRESHOLDS:
        if not (ML / threshold_prediction(t).with_suffix(".meta.json")).exists():
            predict_threshold(t)
    report()


if __name__ == "__main__":
    main()
