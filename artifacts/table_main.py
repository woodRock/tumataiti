"""Table: document leak rate of every detector merged with the rules, on the three
test sets, with model size and median time per document.

Run by `taura build`; reads $TAURA_RESULTS and writes a taura table spec to $TAURA_OUTPUT.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

SETS = ["nz_test_full", "open_en_test", "pii300k_en_val"]
STUDENTS = [("DeBERTa-v3-small", "deberta-v3-small-open"),
            ("ModernBERT-base", "modernbert-base-open"),
            ("mDeBERTa-v3-base", "mdeberta-v3-base-open")]
INT4 = "-int8-int4-block"


def main() -> None:
    R = json.loads(Path(os.environ["TAURA_RESULTS"]).read_text())
    inv = R["inventory"]["metrics"]

    def leak(tag: str, det: str) -> list:
        return [R[f"{tag}_{s}"]["metrics"]["doc_leak"][det] for s in SETS]

    def ms(tag: str, det: str):
        return R[f"{tag}_nz_test_full"]["metrics"]["ms"][det]

    cols = [{"label": "Detector"},
            {"label": "NZ held-out", "metric": "doc_leak"},
            {"label": "Open English", "metric": "doc_leak"},
            {"label": "PII-300k", "metric": "doc_leak"},
            {"label": "MB", "metric": "mb", "bold": "none"},
            {"label": "ms", "metric": "ms", "bold": "none"}]
    rows: list = [
        ["Rules only", *leak("m3open", "rules"), None, None],
        ["Rules + teacher", *leak("m3open", "rules_openai-privacy-filter"), None,
         ms("m3open", "rules_openai-privacy-filter")],
        {"group": r"\textit{Rules + student, fp32 (GPU)}"},
    ]
    for label, det in STUDENTS:
        rows.append([label, *leak("m3open", f"rules_{det}"), inv["mb"][f"{det}-fp32"], ms("m3open", f"rules_{det}")])
    rows.append({"group": r"\textit{Rules + student, int4 encoder (laptop CPU)}"})
    for label, det in STUDENTS:
        rows.append([label, *leak("m3open_int4", f"rules_{det}{INT4}"), inv["mb"][f"{det}-int4"],
                     ms("m3open_int4", f"rules_{det}{INT4}")])
    Path(os.environ["TAURA_OUTPUT"]).write_text(json.dumps({"columns": cols, "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
