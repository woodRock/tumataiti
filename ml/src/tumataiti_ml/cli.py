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

    n = write_jsonl(a.out, generate(a.n, a.seed, a.split, a.group))
    print(f"wrote {n} documents to {a.out}")


def cmd_prepare_pii300k(a: argparse.Namespace) -> None:
    from .datasets import pii300k

    a.raw = a.raw or Path(f"data/raw/pii300k_en_{a.split}.jsonl")
    raw = pii300k.download(a.raw, a.split)
    n = write_jsonl(a.out, pii300k.load(raw, a.limit))
    print(f"wrote {n} documents to {a.out}")


def cmd_prepare_open(a: argparse.Namespace) -> None:
    from .datasets import open_pii

    raw = open_pii.download(a.source, a.split, a.raw_dir)
    docs, dropped = open_pii.load(a.source, raw)
    n = write_jsonl(a.out, open_pii.sample(docs, a.n, a.seed))
    print(f"wrote {n} of {len(docs)} documents to {a.out} ({dropped} dropped: entities not found in the text)")


def cmd_predict(a: argparse.Namespace) -> None:
    gold = list(read_jsonl(a.gold))[: a.limit]
    predict = detectors.load(a.detector, device=a.device, threshold=a.threshold, model=a.model)
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
        "threshold": a.threshold,
        "model": a.model,
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


def cmd_review(a: argparse.Namespace) -> None:
    from .review import review

    text = {d.id: d.text for d in read_jsonl(a.gold)}
    out = [review(d, text[d.id], a.transaction_labels) for d in read_jsonl(a.pred) if d.id in text]
    write_jsonl(a.out, out)
    meta = a.pred.with_suffix(".meta.json")
    if meta.exists():
        a.out.with_suffix(".meta.json").write_text(meta.read_text())
    n = sum(len(d.meta["flagged"]) for d in out)
    print(f"wrote {len(out)} reviewed predictions to {a.out} ({n} spans flagged for review)")


def cmd_false_alarms(a: argparse.Namespace) -> None:
    from .analysis import false_alarms

    gold = list(read_jsonl(a.gold))
    rows = {p.parent.name: false_alarms(gold, {d.id: d for d in read_jsonl(p)}) for p in a.pred}
    names = list(rows)
    keys = list(next(iter(rows.values())))
    lines = ["| Slot | n | " + " | ".join(names) + " |", "|---|---:|" + "---:|" * len(names)]
    def cell(r: dict) -> str:
        if "leaked" in r:
            return f"{r['leaked'] * 100:.1f}% leaked"
        return f"{r['redacted'] * 100:.1f}% redacted" + (f", {r['flagged'] * 100:.1f}% flagged" if r["flagged"] else "")

    for k in keys:
        lines.append(f"| {k} | {rows[names[0]][k]['n']} | " + " | ".join(cell(rows[n][k]) for n in names) + " |")
    md = (f"## {a.title or a.gold.stem}\n\nFalse alarms on text that is not PII (lower is better), "
          "and leaks of the PII beside it:\n\n" + "\n".join(lines) + "\n")
    if a.markdown:
        a.markdown.parent.mkdir(parents=True, exist_ok=True)
        a.markdown.write_text(md)
    if a.json:
        a.json.write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    print(md)


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


def cmd_train(a: argparse.Namespace) -> None:
    from .student.train import Config, train

    cfg = Config(
        backbone=a.backbone, train=[str(p) for p in a.train], dev=str(a.dev), out=str(a.out),
        epochs=a.epochs, lr=a.lr, batch_size=a.batch_size, seed=a.seed, max_steps=a.max_steps, dev_limit=a.dev_limit,
        bf16=not a.no_bf16, log_every=a.log_every, deterministic=not a.no_deterministic,
    )
    train(cfg, device=a.device)


def cmd_counterfactual(a: argparse.Namespace) -> None:
    """Name leak rate per community from counterfactual files (identical but for names)."""
    groups = {"maori": "Māori", "pakeha": "Pākehā", "pasifika": "Pasifika", "asian_nz": "Asian NZ"}
    rows: dict[str, dict[str, float]] = {}
    for run in a.runs:
        rows[run.name] = {}
        for slug, label in groups.items():
            gold = list(read_jsonl(a.data / f"nz_cf_{slug}.jsonl"))
            preds = {d.id: d for d in read_jsonl(run / f"nz_cf_{slug}.jsonl")}
            r = metrics.score([g for g in gold if g.id in preds], preds).as_dict()
            rows[run.name][label] = r["span_leak_rate_by_category"]["PERSON"]
    names = list(rows)
    lines = ["| Names (same documents, only names swapped) | " + " | ".join(names) + " |", "|---|" + "---:|" * len(names)]
    for label in groups.values():
        lines.append(f"| {label} | " + " | ".join(f"{rows[n][label] * 100:.1f}%" for n in names) + " |")
    gap = lambda n: (rows[n]["Māori"] - rows[n]["Pākehā"]) * 100  # noqa: E731
    lines.append("| **Māori − Pākehā gap (points)** | " + " | ".join(f"**{gap(n):+.1f}**" for n in names) + " |")
    md = "Name leak rate by community, counterfactual audit (lower is better):\n\n" + "\n".join(lines) + "\n"
    if a.markdown:
        a.markdown.parent.mkdir(parents=True, exist_ok=True)
        a.markdown.write_text(md)
    if a.json:
        a.json.write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    print(md)


def cmd_export(a: argparse.Namespace) -> None:
    from .student.export import export_onnx

    print(export_onnx(a.model, a.out))


def cmd_quantise(a: argparse.Namespace) -> None:
    from .student.export import quantise_int8

    name = "model_int8.onnx" if a.encoder == "dynamic" else f"model_int8_{a.encoder}.onnx"
    out = quantise_int8(a.onnx, a.onnx.with_name(name), a.encoder)
    print(f"{out}: {out.stat().st_size / 1e6:.1f} MB (fp32 {a.onnx.stat().st_size / 1e6:.1f} MB)")


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="tumataiti-ml")
    sub = ap.add_subparsers(required=True)

    g = sub.add_parser("generate", help="synthetic NZ documents with gold spans")
    g.add_argument("--n", type=int, default=1600)
    g.add_argument("--seed", type=int, default=0)
    g.add_argument("--split", default="train", choices=["train", "dev", "train_v3", "dev_v3", "train_v3ids", "dev_v3ids", "test_names", "test_full", "test_false_alarm"])
    g.add_argument("--group", help="counterfactual audit: every person from this community")
    g.add_argument("--out", type=Path, required=True)
    g.set_defaults(fn=cmd_generate)

    p3 = sub.add_parser("prepare-pii300k", help="download and convert PII-Masking-300k (English)")
    p3.add_argument("--split", default="validation", choices=["train", "validation"])
    p3.add_argument("--raw", type=Path, default=None, help="default: data/raw/pii300k_en_<split>.jsonl")
    p3.add_argument("--out", type=Path, required=True)
    p3.add_argument("--limit", type=int)
    p3.set_defaults(fn=cmd_prepare_pii300k)

    po = sub.add_parser("prepare-open", help="download and convert an openly licensed PII set (English)")
    po.add_argument("--source", required=True, choices=["nemotron", "gretel-en", "gretel-finance"])
    po.add_argument("--split", default="train", choices=["train", "test"])
    po.add_argument("--raw-dir", type=Path, default=Path("data/raw/open"))
    po.add_argument("--n", type=int, help="random sample of this many documents")
    po.add_argument("--seed", type=int, default=0)
    po.add_argument("--out", type=Path, required=True)
    po.set_defaults(fn=cmd_prepare_open)

    pr = sub.add_parser("predict", help="run a detector over a dataset")
    pr.add_argument("--detector", required=True, choices=["rules", "openai-privacy-filter", "student", "student-onnx"])
    pr.add_argument("--model", help="student model directory, or .onnx file for student-onnx")
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

    t = sub.add_parser("train", help="fine-tune a student encoder")
    t.add_argument("--backbone", required=True, help="Hugging Face model id")
    t.add_argument("--train", type=Path, nargs="+", required=True)
    t.add_argument("--dev", type=Path, required=True)
    t.add_argument("--out", type=Path, required=True)
    t.add_argument("--epochs", type=int, default=3)
    t.add_argument("--lr", type=float, default=5e-5)
    t.add_argument("--batch-size", type=int, default=16)
    t.add_argument("--seed", type=int, default=0)
    t.add_argument("--max-steps", type=int)
    t.add_argument("--dev-limit", type=int)
    t.add_argument("--no-bf16", action="store_true", help="train in fp32")
    t.add_argument("--no-deterministic", action="store_true", help="allow non-deterministic CUDA kernels")
    t.add_argument("--log-every", type=int, default=200)
    t.add_argument("--device", default="cuda")
    t.set_defaults(fn=cmd_train)

    c = sub.add_parser("combine", help="rules-first union of two prediction files")
    c.add_argument("--primary", type=Path, required=True)
    c.add_argument("--secondary", type=Path, required=True)
    c.add_argument("--out", type=Path, required=True)
    c.set_defaults(fn=cmd_combine)

    rv = sub.add_parser("review", help="flag model spans that are probably not PII (review.py)")
    rv.add_argument("--gold", type=Path, required=True, help="the documents the predictions are for")
    rv.add_argument("--pred", type=Path, required=True)
    rv.add_argument("--out", type=Path, required=True)
    rv.add_argument("--transaction-labels", action="store_true",
                    help="also flag unverified IDs labelled as order or booking codes (SPEC §9.8)")
    rv.set_defaults(fn=cmd_review)

    fa = sub.add_parser("false-alarms", help="false alarms and leaks on the false-alarm set")
    fa.add_argument("--gold", type=Path, required=True)
    fa.add_argument("--pred", type=Path, nargs="+", required=True)
    fa.add_argument("--title")
    fa.add_argument("--markdown", type=Path)
    fa.add_argument("--json", type=Path)
    fa.set_defaults(fn=cmd_false_alarms)

    nm = sub.add_parser("names", help="PERSON leak rate by community (synthetic NZ data only)")
    nm.add_argument("--gold", type=Path, required=True)
    nm.add_argument("--pred", type=Path, nargs="+", required=True)
    nm.add_argument("--markdown", type=Path)
    nm.set_defaults(fn=cmd_names)

    ex = sub.add_parser("export", help="export a student to ONNX (needs PyTorch)")
    ex.add_argument("--model", type=Path, required=True)
    ex.add_argument("--out", type=Path, required=True)
    ex.set_defaults(fn=cmd_export)

    qu = sub.add_parser("quantise", help="int8 quantisation of an exported student")
    qu.add_argument("--onnx", type=Path, required=True)
    qu.add_argument("--encoder", default="dynamic", choices=["dynamic", "fp16", "int8-block", "int4-block"],
                    help="encoder weights; the embedding table is always int8 (SPEC §9.6)")
    qu.set_defaults(fn=cmd_quantise)

    cf = sub.add_parser("counterfactual", help="name leak by community from the nz_cf_* files")
    cf.add_argument("--data", type=Path, required=True, help="directory with nz_cf_<group>.jsonl")
    cf.add_argument("--runs", type=Path, nargs="+", required=True, help="prediction directories")
    cf.add_argument("--markdown", type=Path)
    cf.add_argument("--json", type=Path)
    cf.set_defaults(fn=cmd_counterfactual)

    a = ap.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
