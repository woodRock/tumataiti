"""Typing variation: the int4 open students on test_full and the name audit
with macrons stripped and with all text lowercased, merged with the rules.
Offsets are unchanged, so gold spans carry over. Student predictions already
present (from jobs.py) are reused.

The casing variants separate what the students read from capitals, on test_full
only: case_names lowercases the names and nothing else, case_words capitalises
every word that is not PII, case_upper uppercases everything.

    taura run -- ml/.venv/bin/python ml/scripts/robustness.py

Writes ml/results/m3open_robust_<variant>_nz_test_full.{json,md} and
m3open_robust_<variant>_names_counterfactual.{json,md}, or for a casing variant
m3open_robust_<variant>_false_alarms.{json,md}, the share of non-PII words redacted.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ML = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ML / "src"))

from tumataiti_ml.analysis import false_alarms  # noqa: E402
from tumataiti_ml.spans import Doc, read_jsonl, write_jsonl  # noqa: E402
from tumataiti_ml.synth import lexicon as lx  # noqa: E402

STUDENTS = ["deberta-v3-small-open", "modernbert-base-open", "mdeberta-v3-base-open"]
SETS = ["nz_test_full", "nz_cf_maori", "nz_cf_pakeha", "nz_cf_pasifika", "nz_cf_asian_nz"]
VARIANTS = {"nomacron": lx.strip_macrons, "lower": str.lower}
WORD = re.compile(r"[^\W\d_]{2,}")


def other_words(doc: Doc) -> list[tuple[int, int]]:
    """Words outside every gold span, and outside any e-mail address or URL."""
    gold = [(s.start, s.end) for s in doc.spans]
    words = []
    for chunk in re.finditer(r"\S+", doc.text):
        if "@" in chunk[0] or "://" in chunk[0] or "www." in chunk[0]:
            continue
        for w in WORD.finditer(chunk[0]):
            a, b = chunk.start() + w.start(), chunk.start() + w.end()
            if not any(a < y and x < b for x, y in gold):
                words.append((a, b))
    return words


def recase(text: str, ranges: list[tuple[int, int]], change) -> str:
    chars = list(text)
    for a, b in ranges:
        chars[a:b] = change(text[a:b])
    return "".join(chars)


CASINGS = {
    "case_names": lambda d: recase(d.text, [(s.start, s.end) for s in d.spans if s.category == "PERSON"], str.lower),
    "case_words": lambda d: recase(d.text, other_words(d), lambda w: w[0].upper() + w[1:]),
    "case_upper": lambda d: d.text.upper(),
}


def sets(variant: str) -> list[str]:
    return SETS if variant in VARIANTS else SETS[:1]


def cli(*args: str) -> None:
    env = {**os.environ, "PATH": f"{ML / '.venv/bin'}:{os.environ['PATH']}"}
    subprocess.run(["tumataiti-ml", *args], cwd=ML, env=env, check=True)


def write_variant(variant: str, ds: str) -> Path:
    """data/robust-v4/<variant>/<ds>.jsonl, written atomically because grid jobs
    for the same set may run at once. Returns its path under ml/."""
    docs = []
    for d in read_jsonl(ML / "data/v4" / f"{ds}.jsonl"):
        text = VARIANTS[variant](d.text) if variant in VARIANTS else CASINGS[variant](d)
        assert len(text) == len(d.text), d.id
        meta = d.meta if variant in VARIANTS else {**d.meta, "negatives": [[a, b, "word"] for a, b in other_words(d)]}
        docs.append(Doc(id=d.id, text=text, spans=d.spans, meta=meta))
    path = Path("data/robust-v4") / variant / f"{ds}.jsonl"
    (ML / path.parent).mkdir(parents=True, exist_ok=True)
    tmp = ML / path.with_suffix(f".{os.getpid()}.tmp")
    write_jsonl(tmp, docs)
    tmp.replace(ML / path)
    return path


def gold(variant: str) -> None:
    for ds in sets(variant):
        write_variant(variant, ds)


def rules(variant: str) -> None:
    for ds in sets(variant):
        cli("predict", "--detector", "rules", "--gold", f"data/robust-v4/{variant}/{ds}.jsonl",
            "--out", f"runs/robust-v4/{variant}/rules/{ds}.jsonl")


def predict(variant: str, ds: str, m: str) -> None:
    cli("predict", "--detector", "student-onnx", "--model", f"runs/m3-v4/{m}/onnx/model_int8_int4-block.onnx",
        "--gold", f"data/robust-v4/{variant}/{ds}.jsonl", "--out", f"runs/robust-v4/{variant}/{m}/{ds}.jsonl")


def report(variant: str) -> None:
    data = Path("data/robust-v4") / variant
    runs = Path("runs/robust-v4") / variant
    for ds in sets(variant):
        for m in STUDENTS:
            cli("combine", "--primary", str(runs / "rules" / f"{ds}.jsonl"), "--secondary", str(runs / m / f"{ds}.jsonl"),
                "--out", str(runs / f"rules+{m}" / f"{ds}.jsonl"))
    ds = "nz_test_full"
    names = ["rules", *(f"rules+{m}" for m in STUDENTS)]
    cli("score", "--gold", str(data / f"{ds}.jsonl"), "--pred", *(str(runs / n / f"{ds}.jsonl") for n in names),
        "--title", f"int4 open students, {variant}: test_full",
        "--markdown", f"results/m3open_robust_{variant}_{ds}.md", "--json", f"results/m3open_robust_{variant}_{ds}.json")
    if variant in VARIANTS:
        cli("counterfactual", "--data", str(data), "--runs", *(str(runs / n) for n in names[1:]),
            "--markdown", f"results/m3open_robust_{variant}_names_counterfactual.md",
            "--json", f"results/m3open_robust_{variant}_names_counterfactual.json")
        return
    golds = list(read_jsonl(ML / data / f"{ds}.jsonl"))
    rows = {n: false_alarms(golds, {d.id: d for d in read_jsonl(ML / runs / n / f"{ds}.jsonl")}) for n in names}
    rows = {n: {k: v for k, v in r.items() if k.startswith("not PII: ")} for n, r in rows.items()}
    out = ML / f"results/m3open_robust_{variant}_false_alarms"
    out.with_suffix(".json").write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")
    table = "\n".join(f"| {n} | {r['not PII: word']['n']} | {r['not PII: word']['redacted'] * 100:.1f}% |" for n, r in rows.items())
    out.with_suffix(".md").write_text(f"## Non-PII words redacted, {variant}\n\n| Detector | n | Redacted |\n|---|---:|---:|\n{table}\n")


def main() -> None:
    for variant in [*VARIANTS, *CASINGS]:
        gold(variant)
        rules(variant)
        for ds in sets(variant):
            for m in STUDENTS:
                if not (ML / "runs/robust-v4" / variant / m / f"{ds}.meta.json").exists():
                    predict(variant, ds, m)
        report(variant)


if __name__ == "__main__":
    main()
