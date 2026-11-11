"""The students retrained with some lowercased documents (ecs_student_lower.sh)
beside the deployed int4 students, merged with the rules, on ordinary text, with
macrons stripped and lowercased. Their predictions are from the full model on GPU,
and the int4 DeBERTa-v3-small is scored beside them. Needs its ONNX export
(ecs_export.sh); a missing int4 model or prediction is made here:

    taura run -- ml/.venv/bin/python ml/scripts/score_lower.py

Writes ml/results/m3open_lowertrain_<typing>_nz_test_full.{json,md} and
m3open_lowertrain_<typing>_names_counterfactual.{json,md}.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ML = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ML / "scripts"))

from robustness import SETS, STUDENTS, VARIANTS  # noqa: E402

RUNS = Path("runs/lowertrain-v4")
V2 = Path("runs/m3-v4")
INT4 = "-int8-int4-block"
QUANTISED = "deberta-v3-small-open-lower"
ONNX = V2 / QUANTISED / "onnx"
TYPINGS = ["plain", *VARIANTS]


def cli(*args: str) -> None:
    env = {**os.environ, "PATH": f"{ML / '.venv/bin'}:{os.environ['PATH']}"}
    subprocess.run(["tumataiti-ml", *args], cwd=ML, env=env, check=True)


def gold(typing: str, ds: str) -> Path:
    return Path("data/v4" if typing == "plain" else f"data/robust-v4/{typing}") / f"{ds}.jsonl"


def prediction(typing: str, ds: str) -> Path:
    return RUNS / typing / f"{QUANTISED}-int4" / f"{ds}.jsonl"


def quantise() -> None:
    cli("quantise", "--onnx", str(ONNX / "model.onnx"), "--encoder", "int4-block")


def predict(typing: str, ds: str) -> None:
    cli("predict", "--detector", "student-onnx", "--model", str(ONNX / "model_int8_int4-block.onnx"),
        "--gold", str(gold(typing, ds)), "--out", str(prediction(typing, ds)))


def score(typing: str) -> None:
    plain = typing == "plain"
    data = gold(typing, "x").parent
    rules = V2 / "rules" if plain else Path("runs/robust-v4") / typing / "rules"
    deployed = [V2 / f"rules+{m}{INT4}" if plain else Path("runs/robust-v4") / typing / f"rules+{m}" for m in STUDENTS]
    retrained = []
    for m in STUDENTS:
        pred = V2 / f"{m}-lower" / "pred" / ("" if plain else f"robust/{typing}")
        retrained.append(RUNS / typing / f"rules+{m}-lower")
        for ds in SETS:
            cli("combine", "--primary", str(rules / f"{ds}.jsonl"), "--secondary", str(pred / f"{ds}.jsonl"),
                "--out", str(retrained[-1] / f"{ds}.jsonl"))
    quantised = RUNS / typing / f"rules+{QUANTISED}-int4"
    for ds in SETS:
        cli("combine", "--primary", str(rules / f"{ds}.jsonl"), "--secondary", str(prediction(typing, ds)),
            "--out", str(quantised / f"{ds}.jsonl"))
    ds = "nz_test_full"
    runs = [*deployed, *retrained, quantised]
    cli("score", "--gold", str(data / f"{ds}.jsonl"), "--pred", *(str(r / f"{ds}.jsonl") for r in runs),
        "--title", f"Deployed and lowercase-trained students, {typing}: test_full",
        "--markdown", f"results/m3open_lowertrain_{typing}_{ds}.md", "--json", f"results/m3open_lowertrain_{typing}_{ds}.json")
    cli("counterfactual", "--data", str(data), "--runs", *map(str, runs),
        "--markdown", f"results/m3open_lowertrain_{typing}_names_counterfactual.md",
        "--json", f"results/m3open_lowertrain_{typing}_names_counterfactual.json")


def report() -> None:
    for typing in TYPINGS:
        score(typing)


def main() -> None:
    if not (ML / ONNX / "model_int8_int4-block.onnx").exists():
        quantise()
    for typing in TYPINGS:
        for ds in SETS:
            if not (ML / prediction(typing, ds).with_suffix(".meta.json")).exists():
                predict(typing, ds)
    report()


if __name__ == "__main__":
    main()
