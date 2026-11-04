"""Table: what the training data does. Held-out NZ document and name span leak
rates, merged with the rules, for students trained on NZ data v1 or v2 with
PII-Masking-300k, and on v2 with the openly licensed English sets.

Run by `taura build`; reads $TAURA_RESULTS and writes a taura table spec to $TAURA_OUTPUT.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

STUDENTS = [("DeBERTa-v3-small", "deberta-v3-small"),
            ("ModernBERT-base", "modernbert-base"),
            ("mDeBERTa-v3-base", "mdeberta-v3-base")]


def main() -> None:
    R = json.loads(Path(os.environ["TAURA_RESULTS"]).read_text())
    v2 = R["m3v2_nz_test_full"]["metrics"]
    op = R["m3open_nz_test_full"]["metrics"]

    def cells(measure: str, det: str) -> list:
        return [v2[measure][f"rules_{det}-v1"], v2[measure][f"rules_{det}"], op[measure][f"rules_{det}-open"]]

    cols = [{"label": "Detector"}]
    for what, metric in (("Doc.", "doc_leak"), ("Name", "span_leak")):
        cols += [{"label": f"{what} v1", "metric": metric}, {"label": f"{what} v2", "metric": metric},
                 {"label": f"{what} open", "metric": metric}]
    teacher = "rules_openai-privacy-filter"
    rows: list = [["Rules + teacher", v2["doc_leak"][teacher], "", "", v2["leak_person"][teacher], "", ""]]
    for label, det in STUDENTS:
        rows.append([label, *cells("doc_leak", det), *cells("leak_person", det)])
    Path(os.environ["TAURA_OUTPUT"]).write_text(json.dumps({"columns": cols, "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
