"""What check digits add: the shipped rules against a format-only variant that
also redacts every IRD- and NHI-shaped match, checksum or not (same patterns as
crates/tumataiti-rules/src/rules.rs). Scores false alarms on the false-alarm
set, and leakage and precision on the other test sets.

    taura run -- ml/.venv/bin/python ml/scripts/checksum_ablation.py

Writes ml/results/checksum_false_alarms.{json,md} and checksum_<set>.{json,md}.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ML = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ML / "src"))

from tumataiti_ml.spans import Doc, Span, read_jsonl, write_jsonl  # noqa: E402

IRD = re.compile(r"(?<![\w+])\d{2,3}[- ]?\d{3}[- ]?\d{3}(?!\w)", re.ASCII)
NHI = re.compile(r"\b(?:[A-HJ-NP-Z]{3}\d{4}|[A-HJ-NP-Z]{3}\d{2}[A-HJ-NP-Z]{2})\b")
SETS = {"nz_test_false_alarm": "data/v1", "nz_test_full": "data/v1", "open_en_test": "data/open",
        "pii300k_en_val": "data/v1"}
RUNS = Path("runs/checksum")
RULES = {"nz_test_false_alarm": "runs/m3-fa/rules"}


def cli(*args: str) -> None:
    env = {**os.environ, "PATH": f"{ML / '.venv/bin'}:{os.environ['PATH']}"}
    subprocess.run(["tumataiti-ml", *args], cwd=ML, env=env, check=True, stdout=subprocess.DEVNULL)


def main() -> None:
    for ds, folder in SETS.items():
        gold = f"{folder}/{ds}.jsonl"
        shipped = {d.id: d for d in read_jsonl(ML / RULES.get(ds, "runs/m3-v2/rules") / f"{ds}.jsonl")}
        kept, wide = [], []
        for g in read_jsonl(ML / gold):
            spans = shipped[g.id].spans if g.id in shipped else []
            extra = [Span(m.start(), m.end(), "format_only", "ID", 1.0)
                     for pattern in (IRD, NHI) for m in pattern.finditer(g.text)]
            kept.append(Doc(id=g.id, text="", spans=spans, meta={}))
            wide.append(Doc(id=g.id, text="", spans=sorted([*spans, *extra], key=lambda s: s.start), meta={}))
        write_jsonl(ML / RUNS / "rules" / f"{ds}.jsonl", kept)
        write_jsonl(ML / RUNS / "rules-format-only" / f"{ds}.jsonl", wide)
        preds = [str(RUNS / n / f"{ds}.jsonl") for n in ("rules", "rules-format-only")]
        cli("score", "--gold", gold, "--pred", *preds, "--title", f"Rules with and without check digits: {ds}",
            "--markdown", f"results/checksum_{ds}.md", "--json", f"results/checksum_{ds}.json")
        if ds == "nz_test_false_alarm":
            cli("false-alarms", "--gold", gold, "--pred", *preds, "--title", "Rules with and without check digits",
                "--markdown", "results/checksum_false_alarms.md", "--json", "results/checksum_false_alarms.json")


if __name__ == "__main__":
    main()
