"""Table: retraining against false alarms. DeBERTa-v3-small as deployed, controls
on the shortened schedule (seeds A and B), with kinship negatives added (seeds A
and B), and with ID look-alikes also added: leak rates merged with the rules, and
the share of standalone kinship words (model alone) and ID-shaped codes redacted.

Run by `taura build`; reads $TAURA_RESULTS and writes a taura table spec to $TAURA_OUTPUT.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

RUNS = [("Deployed", "deberta-small-open-v4"),
        ("Control A", "deberta-small-open-v4-1ep"),
        ("Control B", "deberta-small-open-v4-1ep-s1"),
        ("Kinship negatives A", "deberta-small-open-v4kin"),
        ("Kinship negatives B", "deberta-small-open-v4kin-s1"),
        ("Kinship and ID negatives", "deberta-small-open-v4ids")]


def main() -> None:
    R = json.loads(Path(os.environ["TAURA_RESULTS"]).read_text())
    m = {k: v["metrics"] for k, v in R.items()}
    fa = m["m3fa_false_alarms"]
    cols = [{"label": "Training data"},
            {"label": "NZ held-out", "metric": "doc_leak", "bold": "min"},
            {"label": "Gap", "metric": "gap", "bold": "none"},
            {"label": "Open English", "metric": "doc_leak", "bold": "min"},
            {"label": "PII-300k", "metric": "doc_leak", "bold": "none"},
            {"label": "Kin words", "metric": "kin_redacted", "bold": "min"},
            {"label": "Order codes", "metric": "order_ref_redacted", "bold": "min"}]
    rows = [[label,
             m["m3fa_nz_test_full"]["doc_leak"][f"rules_{det}"],
             m["m3fa_names_counterfactual"]["gap"][f"rules_{det}"],
             m["m3fa_open_en_test"]["doc_leak"][f"rules_{det}"],
             m["m3fa_pii300k_en_val"]["doc_leak"][f"rules_{det}"],
             fa["kin_redacted"][det],
             fa["order_ref_redacted"][f"rules_{det}"]] for label, det in RUNS]
    Path(os.environ["TAURA_OUTPUT"]).write_text(json.dumps({"columns": cols, "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
