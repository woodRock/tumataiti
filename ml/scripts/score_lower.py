"""The students retrained with some lowercased documents (ecs_student_lower.sh)
beside the deployed int4 students, merged with the rules, on ordinary text, with
macrons stripped and lowercased. The retrained students are not quantised yet, so
their predictions are from the full model on GPU.

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

RUNS = Path("runs/lowertrain")
V2 = Path("runs/m3-v2")
INT4 = "-int8-int4-block"


def cli(*args: str) -> None:
    env = {**os.environ, "PATH": f"{ML / '.venv/bin'}:{os.environ['PATH']}"}
    subprocess.run(["tumataiti-ml", *args], cwd=ML, env=env, check=True)


def score(typing: str) -> None:
    plain = typing == "plain"
    data = Path("data/v1") if plain else Path("data/robust") / typing
    rules = V2 / "rules" if plain else Path("runs/robust") / typing / "rules"
    deployed = [V2 / f"rules+{m}{INT4}" if plain else Path("runs/robust") / typing / f"rules+{m}" for m in STUDENTS]
    retrained = []
    for m in STUDENTS:
        pred = V2 / f"{m}-lower" / "pred" / ("" if plain else f"robust/{typing}")
        retrained.append(RUNS / typing / f"rules+{m}-lower")
        for ds in SETS:
            cli("combine", "--primary", str(rules / f"{ds}.jsonl"), "--secondary", str(pred / f"{ds}.jsonl"),
                "--out", str(retrained[-1] / f"{ds}.jsonl"))
    ds = "nz_test_full"
    runs = [*deployed, *retrained]
    cli("score", "--gold", str(data / f"{ds}.jsonl"), "--pred", *(str(r / f"{ds}.jsonl") for r in runs),
        "--title", f"Deployed and lowercase-trained students, {typing}: test_full",
        "--markdown", f"results/m3open_lowertrain_{typing}_{ds}.md", "--json", f"results/m3open_lowertrain_{typing}_{ds}.json")
    cli("counterfactual", "--data", str(data), "--runs", *map(str, runs),
        "--markdown", f"results/m3open_lowertrain_{typing}_names_counterfactual.md",
        "--json", f"results/m3open_lowertrain_{typing}_names_counterfactual.json")


def main() -> None:
    for typing in ["plain", *VARIANTS]:
        score(typing)


if __name__ == "__main__":
    main()
