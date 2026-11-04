"""Leakage across operating points (SPEC §9.2): predict test_full with each
int4 open student at each decoding threshold, merge with the rules and score.

    taura run -- ml/.venv/bin/python ml/scripts/thresholds.py

Writes ml/results/m3open_thresholds_nz_test_full.{json,md}.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

ML = Path(__file__).resolve().parents[1]
THRESHOLDS = [0.1, 0.3, 0.5, 0.7, 0.9]
STUDENTS = ["deberta-v3-small-open", "modernbert-base-open", "mdeberta-v3-base-open"]
DS = "nz_test_full"
RUNS = Path("runs/thresholds")


def cli(*args: str) -> None:
    env = {**os.environ, "PATH": f"{ML / '.venv/bin'}:{os.environ['PATH']}"}
    subprocess.run(["tumataiti-ml", *args], cwd=ML, env=env, check=True, stdout=subprocess.DEVNULL)


def main() -> None:
    gold = f"data/v1/{DS}.jsonl"
    rules = f"runs/m3-v2/rules/{DS}.jsonl"
    preds = []
    for m in STUDENTS:
        model = f"runs/m3-v2/{m}/onnx/model_int8_int4-block.onnx"
        for t in THRESHOLDS:
            name = f"{m}-t{t}"
            out = RUNS / name / f"{DS}.jsonl"
            if t == 0.5:  # already predicted at the default threshold
                (ML / out.parent).mkdir(parents=True, exist_ok=True)
                shutil.copy(ML / f"runs/m3-v2/{m}-int8-int4-block/{DS}.jsonl", ML / out)
                shutil.copy(ML / f"runs/m3-v2/{m}-int8-int4-block/{DS}.meta.json", ML / out.with_suffix(".meta.json"))
            elif not (ML / out.with_suffix(".meta.json")).exists():
                cli("predict", "--detector", "student-onnx", "--model", model, "--threshold", str(t),
                    "--gold", gold, "--out", str(out))
            merged = RUNS / f"rules+{name}" / f"{DS}.jsonl"
            cli("combine", "--primary", rules, "--secondary", str(out), "--out", str(merged))
            preds.append(str(merged))
    cli("score", "--gold", gold, "--pred", *preds, "--title", "int4 open students across decoding thresholds",
        "--markdown", f"results/m3open_thresholds_{DS}.md", "--json", f"results/m3open_thresholds_{DS}.json")


if __name__ == "__main__":
    main()
