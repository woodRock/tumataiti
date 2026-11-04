"""Table: test_full document leak rate per held-out template, merged with the
rules, because the headline rate pools a few templates.

Run by `taura build`; reads $TAURA_RESULTS and writes a taura table spec to $TAURA_OUTPUT.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

DETECTORS = [("Teacher", "rules_openai-privacy-filter"),
             ("DeBERTa", "rules_deberta-v3-small-open-int8-int4-block"),
             ("ModernBERT", "rules_modernbert-base-open-int8-int4-block"),
             ("mDeBERTa", "rules_mdeberta-v3-base-open-int8-int4-block")]


def main() -> None:
    m = json.loads(Path(os.environ["TAURA_RESULTS"]).read_text())["uncertainty_nz_test_full"]["metrics"]
    keys = sorted(k for k in m if k.startswith("tmpl_"))
    cols = [{"label": "Template"}, *({"label": label, "metric": "tmpl"} for label, _ in DETECTORS)]
    rows = [[k[len("tmpl_"):].replace("_", " ").capitalize(), *(m[k][det] for _, det in DETECTORS)] for k in keys]
    Path(os.environ["TAURA_OUTPUT"]).write_text(json.dumps({"columns": cols, "rows": rows, "bold_by": "row"}, indent=2))


if __name__ == "__main__":
    main()
