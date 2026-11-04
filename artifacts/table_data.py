"""Table: the data sets, with document and template counts from the inventory.

Run by `taura build`; reads $TAURA_RESULTS and writes a taura table spec to $TAURA_OUTPUT.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

# (set, role, inventory docs key, inventory templates key or None)
ROWS = [
    ("NZ synthetic, train", "Train", "nz_train", "train_v2"),
    ("NZ synthetic, dev", "Dev", "nz_dev", "train_v2"),
    ("Nemotron-PII, train sample", "Train", "nemotron_train", None),
    ("Gretel-en, train sample", "Train", "gretel_en_train", None),
    None,
    ("NZ held-out names", "Test", "nz_test_names", "train_v1"),
    ("NZ held-out templates, names", "Test", "nz_test_full", "test_full"),
    ("NZ name audit, per community", "Test", "nz_cf_maori", "test_full"),
    ("NZ false alarms", "Test", "nz_test_false_alarm", "false_alarm"),
    ("Open English test", "Test", "open_en_test", None),
    ("PII-Masking-300k, validation", "Test", "pii300k_en_val", None),
]


def main() -> None:
    m = json.loads(Path(os.environ["TAURA_RESULTS"]).read_text())["inventory"]["metrics"]
    cols = [{"label": "Set"}, {"label": "Role"},
            {"label": "Docs", "metric": "docs", "bold": "none"},
            {"label": "Templates", "metric": "templates", "bold": "none"}]
    rows: list = []
    for r in ROWS:
        if r is None:
            rows.append({"rule": True})
            continue
        name, role, docs, templates = r
        rows.append([name, role, m["docs"][docs], m["templates"][templates] if templates else ""])
    Path(os.environ["TAURA_OUTPUT"]).write_text(json.dumps({"columns": cols, "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
