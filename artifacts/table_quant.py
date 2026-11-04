"""Table: quantisation of the published (open-data) students. Held-out NZ document leak rate
(merged with the rules), file size and laptop-CPU time for dynamic int8, and for
int8 embeddings with an fp16 or block-wise int4 encoder.

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
    mb = R["inventory"]["metrics"]["mb"]
    i8 = f16 = i4 = R["m3open_quant_nz_test_full"]["metrics"]

    cols = [{"label": "Student"}, {"label": "fp32", "metric": "doc_leak", "bold": "none"}]
    for what in ("int8", "fp16 enc.", "int4 enc."):
        cols += [{"label": what, "metric": "doc_leak", "bold": "none"}, {"label": "MB", "metric": "mb", "bold": "none"}]
    cols.append({"label": "ms", "metric": "ms", "bold": "none"})
    rows: list = []
    for label, det in STUDENTS:
        rows.append([label, i8["doc_leak"][f"rules_{det}"],
                     i8["doc_leak"][f"rules_{det}-int8"], mb[f"{det}-int8"],
                     f16["doc_leak"][f"rules_{det}-int8-fp16"], mb[f"{det}-fp16"],
                     i4["doc_leak"][f"rules_{det}-int8-int4-block"], mb[f"{det}-int4"],
                     i4["ms"][f"rules_{det}-int8-int4-block"]])
    Path(os.environ["TAURA_OUTPUT"]).write_text(json.dumps({"columns": cols, "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
