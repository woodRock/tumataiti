"""Command line: generate data, run detectors, score them.

    tumataiti-ml generate --n 1600 --out data/nz_synth_v0.jsonl
    tumataiti-ml prepare-pii300k --out data/pii300k_en_val.jsonl
    tumataiti-ml predict --detector rules --gold data/nz_synth_v0.jsonl --out runs/rules/nz_synth_v0.jsonl
    tumataiti-ml score --gold data/nz_synth_v0.jsonl --pred runs/*/nz_synth_v0.jsonl --markdown results/nz.md
"""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import sys
from pathlib import Path

from . import detectors, metrics
from .spans import Doc, read_jsonl, write_jsonl
from .taxonomy import EVAL_CATEGORIES


def cmd_generate(a: argparse.Namespace) -> None:
    from .synth.generate import generate

    n = write_jsonl(a.out, generate(a.n, a.seed))
    print(f"wrote {n} documents to {a.out}")


def cmd_prepare_pii300k(a: argparse.Namespace) -> None:
    from .datasets import pii300k

    raw = pii300k.download(a.raw)
    n = write_jsonl(a.out, pii300k.load(raw, a.limit))
    print(f"wrote {n} documents to {a.out}")


def cmd_predict(a: argparse.Namespace) -> None:
    gold = list(read_jsonl(a.gold))[: a.limit]
    predict = detectors.load(a.detector, device=a.device, threshold=a.threshold)
    preds = detectors.run(predict, gold, a.detector)
    write_jsonl(a.out, preds)
    secs = [d.meta["seconds"] for d in preds]
    meta = {
        "detector": a.detector,
        "gold": str(a.gold),
        "docs": len(preds),
        "seconds_total": sum(secs),
        "seconds_median": statistics.median(secs) if secs else 0.0,
        "device": a.device,
        "host": platform.node(),
    }
    a.out.with_suffix(".meta.json").write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta, indent=2))


def _fmt(x: float) -> str:
    return f"{x * 100:.1f}"


def to_markdown(title: str, results: dict[str, dict], timings: dict[str, dict]) -> str:
    names = list(results)
    lines = [f"## {title}", ""]
    header = "| Metric | " + " | ".join(names) + " |"
    lines += [header, "|---|" + "---:|" * len(names)]

    def row(label: str, get) -> None:
        cells = []
        for n in names:
            try:
                cells.append(get(results[n]))
            except KeyError:
                cells.append("–")
        lines.append(f"| {label} | " + " | ".join(cells) + " |")

    row("**Document leak rate** (lower is better)", lambda r: f"**{_fmt(r['doc_leak_rate'])}%**")
    row("Span leak rate", lambda r: f"{_fmt(r['span_leak_rate'])}%")
    row("Any-PII char precision", lambda r: _fmt(r["char_any"]["precision"]))
    row("Any-PII char recall", lambda r: _fmt(r["char_any"]["recall"]))
    row("Any-PII char F1", lambda r: _fmt(r["char_any"]["f1"]))
    row("Exact-span F1 (all categories)", lambda r: _fmt(r["exact_all"]["f1"]))
    row("Median ms per document", lambda r: f"{timings[r['_name']]['seconds_median'] * 1000:.2f}")
    lines += ["", "Span leak rate by category (lower is better):", ""]
    lines += [header, "|---|" + "---:|" * len(names)]
    first = results[names[0]]
    for c in EVAL_CATEGORIES:
        if c in first["gold_spans"]:
            row(f"{c} ({first['gold_spans'][c]} spans)", lambda r, c=c: f"{_fmt(r['span_leak_rate_by_category'][c])}%")
    lines += ["", "Character-level F1 by category (category must match):", ""]
    lines += [header, "|---|" + "---:|" * len(names)]
    for c in EVAL_CATEGORIES:
        if c in first["gold_spans"]:
            row(c, lambda r, c=c: _fmt(r["char"][c]["f1"]) if c in r["char"] else "0.0")
    return "\n".join(lines) + "\n"


def cmd_score(a: argparse.Namespace) -> None:
    gold = list(read_jsonl(a.gold))
    results, timings = {}, {}
    for p in a.pred:
        preds: dict[str, Doc] = {d.id: d for d in read_jsonl(p)}
        gold_subset = [g for g in gold if g.id in preds]
        name = p.parent.name
        res = metrics.score(gold_subset, preds).as_dict()
        res["_name"] = name
        results[name] = res
        meta = p.with_suffix(".meta.json")
        timings[name] = json.loads(meta.read_text()) if meta.exists() else {}
    if a.json:
        a.json.parent.mkdir(parents=True, exist_ok=True)
        a.json.write_text(json.dumps({"gold": str(a.gold), "results": results, "timings": timings}, indent=2))
    md = to_markdown(a.title or a.gold.stem, results, timings)
    if a.markdown:
        a.markdown.parent.mkdir(parents=True, exist_ok=True)
        a.markdown.write_text(md)
    print(md)


def cmd_combine(a: argparse.Namespace) -> None:
    from .analysis import combine

    primary = {d.id: d for d in read_jsonl(a.primary)}
    secondary = {d.id: d for d in read_jsonl(a.secondary)}
    out = [combine(primary[i], secondary[i]) for i in primary if i in secondary]
    write_jsonl(a.out, out)
    metas = [json.loads(p.with_suffix(".meta.json").read_text()) for p in (a.primary, a.secondary)]
    # Both detectors run on every document, so their latencies add.
    meta = {"detector": "combined", "parts": metas, "seconds_median": sum(m["seconds_median"] for m in metas)}
    a.out.with_suffix(".meta.json").write_text(json.dumps(meta, indent=2))
    print(f"wrote {len(out)} combined predictions to {a.out}")


def cmd_names(a: argparse.Namespace) -> None:
    from .analysis import person_leak_by_group

    gold = list(read_jsonl(a.gold))
    rows = {p.parent.name: person_leak_by_group(gold, {d.id: d for d in read_jsonl(p)}) for p in a.pred}
    groups = list(next(iter(rows.values())))
    lines = ["| Names | " + " | ".join(rows) + " |", "|---|" + "---:|" * len(rows)]
    for g in groups:
        n = next(iter(rows.values()))[g][1]
        cells = [f"{rows[r][g][0] / rows[r][g][1] * 100:.1f}%" for r in rows]
        lines.append(f"| {g} ({n} spans) | " + " | ".join(cells) + " |")
    md = "Name leak rate by community (lower is better):\n\n" + "\n".join(lines) + "\n"
    if a.markdown:
        a.markdown.write_text(md)
    print(md)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="tumataiti-ml")
    sub = ap.add_subparsers(required=True)

    g = sub.add_parser("generate", help="synthetic NZ documents with gold spans")
    g.add_argument("--n", type=int, default=1600)
    g.add_argument("--seed", type=int, default=0)
    g.add_argument("--out", type=Path, required=True)
    g.set_defaults(fn=cmd_generate)

    p3 = sub.add_parser("prepare-pii300k", help="download and convert PII-Masking-300k (English validation)")
    p3.add_argument("--raw", type=Path, default=Path("data/raw/pii300k_en_validation.jsonl"))
    p3.add_argument("--out", type=Path, required=True)
    p3.add_argument("--limit", type=int)
    p3.set_defaults(fn=cmd_prepare_pii300k)

    pr = sub.add_parser("predict", help="run a detector over a dataset")
    pr.add_argument("--detector", required=True, choices=["rules", "openai-privacy-filter"])
    pr.add_argument("--gold", type=Path, required=True)
    pr.add_argument("--out", type=Path, required=True)
    pr.add_argument("--limit", type=int)
    pr.add_argument("--device", default="cpu")
    pr.add_argument("--threshold", type=float, default=0.5)
    pr.set_defaults(fn=cmd_predict)

    s = sub.add_parser("score", help="score one or more prediction files against gold")
    s.add_argument("--gold", type=Path, required=True)
    s.add_argument("--pred", type=Path, nargs="+", required=True, help="named after their parent directory")
    s.add_argument("--title")
    s.add_argument("--markdown", type=Path)
    s.add_argument("--json", type=Path)
    s.set_defaults(fn=cmd_score)

    c = sub.add_parser("combine", help="rules-first union of two prediction files")
    c.add_argument("--primary", type=Path, required=True)
    c.add_argument("--secondary", type=Path, required=True)
    c.add_argument("--out", type=Path, required=True)
    c.set_defaults(fn=cmd_combine)

    nm = sub.add_parser("names", help="PERSON leak rate by community (synthetic NZ data only)")
    nm.add_argument("--gold", type=Path, required=True)
    nm.add_argument("--pred", type=Path, nargs="+", required=True)
    nm.add_argument("--markdown", type=Path)
    nm.set_defaults(fn=cmd_names)

    a = ap.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
