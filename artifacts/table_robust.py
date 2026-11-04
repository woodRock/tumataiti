"""Table: typing variation. test_full document leak rate and the Māori − Pākehā
name gap for the int4 open students, merged with the rules, on the original
text, with macrons stripped, and lowercased.

Run by `taura build`; reads $TAURA_RESULTS and writes a taura table spec to $TAURA_OUTPUT.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

STUDENTS = [("DeBERTa-v3-small", "deberta-v3-small-open"),
            ("ModernBERT-base", "modernbert-base-open"),
            ("mDeBERTa-v3-base", "mdeberta-v3-base-open")]


def main() -> None:
    R = json.loads(Path(os.environ["TAURA_RESULTS"]).read_text())
    m = {k: v["metrics"] for k, v in R.items()}
    cols = [{"label": "Student"}]
    for label in ("Orig.", "No macrons", "Lower"):
        cols.append({"label": f"Doc., {label.lower()}", "metric": "doc_leak", "bold": "none"})
    for label in ("Orig.", "No macrons", "Lower"):
        cols.append({"label": f"Gap, {label.lower()}", "metric": "gap", "bold": "none"})
    rows = []
    for label, det in STUDENTS:
        rows.append([label,
                     m["m3open_int4_nz_test_full"]["doc_leak"][f"rules_{det}-int8-int4-block"],
                     m["m3open_robust_nomacron_nz_test_full"]["doc_leak"][f"rules_{det}"],
                     m["m3open_robust_lower_nz_test_full"]["doc_leak"][f"rules_{det}"],
                     m["m3open_int4_names_counterfactual"]["gap"][f"rules_{det}-int8-int4-block"],
                     m["m3open_robust_nomacron_names_counterfactual"]["gap"][f"rules_{det}"],
                     m["m3open_robust_lower_names_counterfactual"]["gap"][f"rules_{det}"]])
    Path(os.environ["TAURA_OUTPUT"]).write_text(json.dumps({"columns": cols, "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
