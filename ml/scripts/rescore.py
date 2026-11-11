"""Re-score result files from the predictions already on disk, into the same
files, so a `taura run` records them as outputs and links them to the ledger.

    taura run -- uv run python ml/scripts/rescore.py m3open_nz_test_full m3open_names_counterfactual ...

Each results/<name>.json names its gold file (or, for a counterfactual audit,
its runs) and its detectors; the predictions are found under runs/. Nothing is
re-predicted or re-combined, so a changed number means the predictions on disk
changed since the file was written.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ML = Path(__file__).resolve().parents[1]
# Where each family's predictions live. Several hold detectors of the same
# name (runs/m3/deberta-v3-small is the v1 student, runs/m3-v2/... the v2 one).
# From data v4 the current students are in runs/m3-v4 and score on data/v4;
# v2-era results (runs/m3-v2, data/v1) are reproducible from commit 3437c11.
RUN_DIRS = {"m1_": "runs", "m3_": "runs/m3", "m3v2": "runs/m3-v2", "m3open": "runs/m3-v4", "m3fa": "runs/m3-v4kin",
            "fa_baseline": "runs/m3-v4", "txn": "runs/m3-v4"}


def find_run_dir(stem: str, names: list[str], file: str) -> str:
    r = next(d for prefix, d in RUN_DIRS.items() if stem.startswith(prefix))
    missing = [n for n in names if not (ML / r / n / file).is_file()]
    if missing:
        raise SystemExit(f"{stem}: {r} has no {file} for {missing}")
    return r


def rescore(stem: str) -> None:
    data = json.loads((ML / "results" / f"{stem}.json").read_text())
    md, js = f"results/{stem}.md", f"results/{stem}.json"
    if "gold" not in data:  # counterfactual audit: {run: {community: leak}}
        names = list(data)
        r = find_run_dir(stem, names, "nz_cf_maori.jsonl")
        data_dir = "data/v4" if r.startswith("runs/m3-v4") else "data/v1"
        cmd = ["counterfactual", "--data", data_dir, "--runs", *[f"{r}/{n}" for n in names]]
    else:
        names = list(data["results"])
        ds = Path(data["gold"]).name
        r = find_run_dir(stem, names, ds)
        title = (ML / md).read_text().splitlines()[0].removeprefix("## ")
        cmd = ["score", "--gold", data["gold"], "--pred", *[f"{r}/{n}/{ds}" for n in names], "--title", title]
    subprocess.run(["uv", "run", "tumataiti-ml", *cmd, "--markdown", md, "--json", js],
                   cwd=ML, check=True, stdout=subprocess.DEVNULL)
    print(f"{stem}: rescored from {r}")


if __name__ == "__main__":
    for stem in sys.argv[1:]:
        rescore(stem)
