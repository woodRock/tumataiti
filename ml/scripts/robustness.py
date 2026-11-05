"""Typing variation: the int4 open students on test_full and the name audit
with macrons stripped and with all text lowercased, merged with the rules.
Offsets are unchanged, so gold spans carry over. Student predictions already
present (from jobs.py) are reused.

    taura run -- ml/.venv/bin/python ml/scripts/robustness.py

Writes ml/results/m3open_robust_<variant>_nz_test_full.{json,md} and
m3open_robust_<variant>_names_counterfactual.{json,md}.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ML = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ML / "src"))

from tumataiti_ml.spans import Doc, read_jsonl, write_jsonl  # noqa: E402
from tumataiti_ml.synth import lexicon as lx  # noqa: E402

STUDENTS = ["deberta-v3-small-open", "modernbert-base-open", "mdeberta-v3-base-open"]
SETS = ["nz_test_full", "nz_cf_maori", "nz_cf_pakeha", "nz_cf_pasifika", "nz_cf_asian_nz"]
VARIANTS = {"nomacron": lx.strip_macrons, "lower": str.lower}


def cli(*args: str) -> None:
    env = {**os.environ, "PATH": f"{ML / '.venv/bin'}:{os.environ['PATH']}"}
    subprocess.run(["tumataiti-ml", *args], cwd=ML, env=env, check=True)


def write_variant(variant: str, ds: str) -> Path:
    """data/robust/<variant>/<ds>.jsonl, written atomically because grid jobs
    for the same set may run at once. Returns its path under ml/."""
    change = VARIANTS[variant]
    docs = []
    for d in read_jsonl(ML / "data/v1" / f"{ds}.jsonl"):
        text = change(d.text)
        assert len(text) == len(d.text), d.id
        docs.append(Doc(id=d.id, text=text, spans=d.spans, meta=d.meta))
    path = Path("data/robust") / variant / f"{ds}.jsonl"
    (ML / path.parent).mkdir(parents=True, exist_ok=True)
    tmp = ML / path.with_suffix(f".{os.getpid()}.tmp")
    write_jsonl(tmp, docs)
    tmp.replace(ML / path)
    return path


def gold(variant: str) -> None:
    for ds in SETS:
        write_variant(variant, ds)


def rules(variant: str) -> None:
    for ds in SETS:
        cli("predict", "--detector", "rules", "--gold", f"data/robust/{variant}/{ds}.jsonl",
            "--out", f"runs/robust/{variant}/rules/{ds}.jsonl")


def predict(variant: str, ds: str, m: str) -> None:
    cli("predict", "--detector", "student-onnx", "--model", f"runs/m3-v2/{m}/onnx/model_int8_int4-block.onnx",
        "--gold", f"data/robust/{variant}/{ds}.jsonl", "--out", f"runs/robust/{variant}/{m}/{ds}.jsonl")


def report(variant: str) -> None:
    data = Path("data/robust") / variant
    runs = Path("runs/robust") / variant
    for ds in SETS:
        for m in STUDENTS:
            cli("combine", "--primary", str(runs / "rules" / f"{ds}.jsonl"), "--secondary", str(runs / m / f"{ds}.jsonl"),
                "--out", str(runs / f"rules+{m}" / f"{ds}.jsonl"))
    ds = "nz_test_full"
    names = ["rules", *(f"rules+{m}" for m in STUDENTS)]
    cli("score", "--gold", str(data / f"{ds}.jsonl"), "--pred", *(str(runs / n / f"{ds}.jsonl") for n in names),
        "--title", f"int4 open students, {variant}: test_full",
        "--markdown", f"results/m3open_robust_{variant}_{ds}.md", "--json", f"results/m3open_robust_{variant}_{ds}.json")
    cli("counterfactual", "--data", str(data), "--runs", *(str(runs / n) for n in names[1:]),
        "--markdown", f"results/m3open_robust_{variant}_names_counterfactual.md",
        "--json", f"results/m3open_robust_{variant}_names_counterfactual.json")


def main() -> None:
    for variant in VARIANTS:
        gold(variant)
        rules(variant)
        for ds in SETS:
            for m in STUDENTS:
                if not (ML / "runs/robust" / variant / m / f"{ds}.meta.json").exists():
                    predict(variant, ds, m)
        report(variant)


if __name__ == "__main__":
    main()
