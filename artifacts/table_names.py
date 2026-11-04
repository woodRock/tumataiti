"""Table: counterfactual name audit (name span leak rate per community, and the
Māori − Pākehā gap), each detector merged with the rules.

Run by `taura build`; reads $TAURA_RESULTS and writes a taura table spec to $TAURA_OUTPUT.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

COMMUNITIES = [("M\\={a}ori", "maori"), ("P\\={a}keh\\={a}", "pakeha"), ("Pasifika", "pasifika"),
               ("Asian NZ", "asian_nz")]
STUDENTS = [("DeBERTa-v3-small", "deberta-v3-small-open"),
            ("ModernBERT-base", "modernbert-base-open"),
            ("mDeBERTa-v3-base", "mdeberta-v3-base-open")]


def main() -> None:
    R = json.loads(Path(os.environ["TAURA_RESULTS"]).read_text())

    def row(label: str, result: str, det: str) -> list:
        m = R[result]["metrics"]
        return [label, *(m[key][det] for _, key in COMMUNITIES), m["gap"][det]]

    cols = [{"label": "Detector"}, *({"label": lab, "metric": key, "bold": "none"} for lab, key in COMMUNITIES),
            {"label": "Gap", "metric": "gap", "bold": "none"}]
    rows: list = [row("Rules + teacher", "m3open_names_counterfactual", "rules_openai-privacy-filter"),
                  {"group": r"\textit{Rules + student, fp32}"}]
    rows += [row(lab, "m3open_names_counterfactual", f"rules_{det}") for lab, det in STUDENTS]
    rows.append({"group": r"\textit{Rules + student, int4 encoder}"})
    rows += [row(lab, "m3open_int4_names_counterfactual", f"rules_{det}-int8-int4-block") for lab, det in STUDENTS]
    Path(os.environ["TAURA_OUTPUT"]).write_text(json.dumps({"columns": cols, "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
