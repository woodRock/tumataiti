"""Leakage across operating points (SPEC §9.2): predict test_full with each
int4 open student at each decoding threshold, merge with the rules and score.

    taura run -- ml/.venv/bin/python ml/scripts/thresholds.py

Predictions already present (from jobs.py) are reused. Writes
ml/results/m3open_thresholds_nz_test_full.{json,md}.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

ML = Path(__file__).resolve().parents[1]
THRESHOLDS = [0.1, 0.3, 0.5, 0.7, 0.9]
STUDENTS = ["deberta-v3-small-open", "modernbert-base-open", "mdeberta-v3-base-open"]
DS = "nz_test_full"
RUNS = Path("runs/thresholds")


def cli(*args: str) -> None:
    env = {**os.environ, "PATH": f"{ML / '.venv/bin'}:{os.environ['PATH']}"}
    subprocess.run(["tumataiti-ml", *args], cwd=ML, env=env, check=True)


def prediction(m: str, t: float | str) -> Path:
    return RUNS / f"{m}-t{t}" / f"{DS}.jsonl"


def predict(m: str, t: float | str) -> None:
    cli("predict", "--detector", "student-onnx", "--model", f"runs/m3-v2/{m}/onnx/model_int8_int4-block.onnx",
        "--threshold", str(t), "--gold", f"data/v1/{DS}.jsonl", "--out", str(prediction(m, t)))


def report() -> None:
    merged = []
    for m in STUDENTS:
        for t in THRESHOLDS:
            merged.append(str(RUNS / f"rules+{m}-t{t}" / f"{DS}.jsonl"))
            cli("combine", "--primary", f"runs/m3-v2/rules/{DS}.jsonl", "--secondary", str(prediction(m, t)),
                "--out", merged[-1])
    cli("score", "--gold", f"data/v1/{DS}.jsonl", "--pred", *merged, "--title", "int4 open students across decoding thresholds",
        "--markdown", f"results/m3open_thresholds_{DS}.md", "--json", f"results/m3open_thresholds_{DS}.json")


def main() -> None:
    for m in STUDENTS:
        for t in THRESHOLDS:
            if not (ML / prediction(m, t).with_suffix(".meta.json")).exists():
                predict(m, t)
    report()


if __name__ == "__main__":
    main()
