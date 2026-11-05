"""One ECS Grid job per slow CPU prediction, for thresholds.py and robustness.py.
Rules, merging and scoring stay on the laptop, which has the rules binding, so
this only writes the student predictions those scripts then reuse:

    python scripts/grid_job.py list [PREFIX]   # job names, for grid_submit.sh
    python scripts/grid_job.py run JOB         # one job, on a grid machine

Jobs: gold/<variant>, threshold/<student>/<t> and robust/<variant>/<set>/<student>.

The int4 models are copied from the laptop to the shared disk, not re-quantised
here: quantising on another machine gives a different file, and these results
describe the deployed models. Check their hashes against demo/model.lock.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ML = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ML / "scripts"))

from robustness import SETS, STUDENTS, VARIANTS, write_variant  # noqa: E402
from thresholds import DS, RUNS, THRESHOLDS  # noqa: E402

MODEL = "runs/m3-v2/{}/onnx/model_int8_int4-block.onnx"


def jobs() -> list[str]:
    out = [f"gold/{v}" for v in VARIANTS]
    out += [f"threshold/{m}/{t}" for m in STUDENTS for t in THRESHOLDS]
    out += [f"robust/{v}/{ds}/{m}" for v in VARIANTS for ds in SETS for m in STUDENTS]
    return out


def cli(*args: str) -> None:
    subprocess.run(["tumataiti-ml", *args], cwd=ML, check=True)


def run(job: str) -> None:
    kind, *rest = job.split("/")
    if kind == "gold":
        for ds in SETS:
            write_variant(rest[0], ds)
    elif kind == "threshold":
        m, t = rest
        cli("predict", "--detector", "student-onnx", "--model", MODEL.format(m), "--threshold", t,
            "--gold", f"data/v1/{DS}.jsonl", "--out", str(RUNS / f"{m}-t{t}" / f"{DS}.jsonl"))
    elif kind == "robust":
        variant, ds, m = rest
        cli("predict", "--detector", "student-onnx", "--model", MODEL.format(m),
            "--gold", f"data/robust/{variant}/{ds}.jsonl", "--out", f"runs/robust/{variant}/{m}/{ds}.jsonl")
    else:
        raise SystemExit(f"unknown job {job!r}")


def main() -> None:
    if sys.argv[1] == "list":
        prefix = sys.argv[2] if len(sys.argv) > 2 else ""
        print("\n".join(j for j in jobs() if j.startswith(prefix)))
    else:
        run(sys.argv[2])


if __name__ == "__main__":
    main()
