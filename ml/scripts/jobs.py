"""The slow experiments, split into jobs that run anywhere. Nothing here depends
on a scheduler: run them all on this machine, or one at a time from any other.

    taura run -- ml/.venv/bin/python ml/scripts/jobs.py all [PREFIX ...]
    python scripts/jobs.py run JOB
    python scripts/jobs.py list [PREFIX]

In stage order, each stage needing the one before:
- gold/<variant>, rules/<variant>: the typing variants of the evaluation sets, and
  the rules on them;
- threshold/<student>/<t>, robust/<variant>/<set>/<student>: student predictions;
- report/threshold, report/robust/<variant>: merge with the rules and score;
- checksum, uncertainty: score existing predictions. uncertainty stays one job,
  because splitting its seeded bootstrap would change the numbers.

thresholds.py, robustness.py, checksum_ablation.py and score_uncertainty.py also
run on their own. For the ECS Grid, see grid_push.sh, grid_submit.sh and grid_run.sh.

The int4 models must be the deployed files, not re-quantised ones: quantising on
another machine gives a different file. Check their hashes against demo/model.lock.
"""

from __future__ import annotations

import sys
from pathlib import Path

ML = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ML / "scripts"))

import checksum_ablation  # noqa: E402
import robustness  # noqa: E402
import score_uncertainty  # noqa: E402
import thresholds  # noqa: E402
from robustness import SETS, STUDENTS, VARIANTS  # noqa: E402
from thresholds import THRESHOLDS  # noqa: E402


def jobs() -> list[str]:
    out = [f"gold/{v}" for v in VARIANTS]
    out += [f"rules/{v}" for v in VARIANTS]
    out += [f"threshold/{m}/{t}" for m in STUDENTS for t in THRESHOLDS]
    out += [f"robust/{v}/{ds}/{m}" for v in VARIANTS for ds in SETS for m in STUDENTS]
    out += ["report/threshold", *(f"report/robust/{v}" for v in VARIANTS)]
    return [*out, "checksum", "uncertainty"]


def select(prefixes: list[str]) -> list[str]:
    return [j for j in jobs() if not prefixes or j.startswith(tuple(prefixes))]


def run(job: str) -> None:
    kind, *rest = job.split("/")
    if kind == "gold":
        robustness.gold(rest[0])
    elif kind == "rules":
        robustness.rules(rest[0])
    elif kind == "threshold":
        thresholds.predict(*rest)
    elif kind == "robust":
        robustness.predict(*rest)
    elif job == "report/threshold":
        thresholds.report()
    elif kind == "report":
        robustness.report(rest[1])
    elif job == "checksum":
        checksum_ablation.main()
    elif job == "uncertainty":
        score_uncertainty.main()
    else:
        raise SystemExit(f"unknown job {job!r}")


def main() -> None:
    command, *args = sys.argv[1:]
    if command == "list":
        print("\n".join(select(args)))
    elif command == "run":
        run(args[0])
    elif command == "all":
        for job in select(args):
            print(job, flush=True)
            run(job)
    else:
        raise SystemExit(f"unknown command {command!r}")


if __name__ == "__main__":
    main()
