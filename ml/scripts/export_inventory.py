"""Export what the paper says about the data and the shipped models, counted
from the files rather than typed, to the taura result ledger/results/inventory.json:

    taura run -- ml/.venv/bin/python ml/scripts/export_inventory.py

- docs/<set>: documents in each data file (ml/data/);
- templates/<split>: generator templates per split (synth.generate);
- names/<community>/<part>/<train|held_out>: name-list lengths (synth.lexicon);
- mb/<run>: ONNX file sizes in MB (10^6 bytes) of the exported students (ml/runs/);
- params/<run>: parameters of each fp32 ONNX export, in millions.

Cite as \\res{inventory/docs/nz_train} and so on.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ML = Path(__file__).resolve().parents[1]
ROOT = ML.parent
sys.path.insert(0, str(ML / "src"))

from tumataiti_ml.synth import generate as g  # noqa: E402
from tumataiti_ml.synth import lexicon as lx  # noqa: E402

DATA = {
    # data set: file under ml/data/
    "nz_train": "v1/nz_train.jsonl",  # v2 has the same size (make_data_v2.sh)
    "nz_dev": "v1/nz_dev.jsonl",
    "nz_test_names": "v1/nz_test_names.jsonl",
    "nz_test_full": "v1/nz_test_full.jsonl",
    "nz_cf_maori": "v1/nz_cf_maori.jsonl",
    "nz_test_false_alarm": "v1/nz_test_false_alarm.jsonl",
    "nemotron_train": "open/nemotron_train.jsonl",
    "gretel_en_train": "open/gretel_en_train.jsonl",
    "gretel_en_train_all": "open/gretel-en_train_all.jsonl",
    "open_en_train": "open/open_en_train.jsonl",
    "nemotron_test": "open/nemotron_test.jsonl",
    "gretel_en_test": "open/gretel_en_test.jsonl",
    "open_en_test": "open/open_en_test.jsonl",
    "pii300k_en_train": "v1/pii300k_en_train.jsonl",
    "pii300k_en_val": "v1/pii300k_en_val.jsonl",
}
RAW = {"gretel_en_train_raw": "raw/open/gretel_en_train.parquet"}

TEMPLATES = {
    "train_v1": g.TRAIN_TEMPLATES,
    "v2_added": g.V2_TEMPLATES,
    "train_v2": {**g.TRAIN_TEMPLATES, **g.V2_TEMPLATES},
    "test_full": g.TEST_TEMPLATES,
    "false_alarm": g.FALSE_ALARM_TEMPLATES,
    "v3_added": g.V3_TEMPLATES,
}

ONNX = {
    # run: file under ml/runs/
    "deberta-v3-small-open-fp32": "m3-v2/deberta-v3-small-open/onnx/model.onnx",
    "deberta-v3-small-open-int4": "m3-v2/deberta-v3-small-open/onnx/model_int8_int4-block.onnx",
    "modernbert-base-open-fp32": "m3-v2/modernbert-base-open/onnx/model.onnx",
    "modernbert-base-open-int4": "m3-v2/modernbert-base-open/onnx/model_int8_int4-block.onnx",
    "mdeberta-v3-base-open-fp32": "m3-v2/mdeberta-v3-base-open/onnx/model.onnx",
    "mdeberta-v3-base-open-int4": "m3-v2/mdeberta-v3-base-open/onnx/model_int8_int4-block.onnx",
    "deberta-v3-small-fp32": "m3-v2/deberta-v3-small/onnx/model.onnx",
    "modernbert-base-fp32": "m3-v2/modernbert-base/onnx/model.onnx",
    "mdeberta-v3-base-fp32": "m3-v2/mdeberta-v3-base/onnx/model.onnx",
    "deberta-v3-small-int8": "m3-v2/deberta-v3-small/onnx/model_int8.onnx",
    "deberta-v3-small-fp16": "m3-v2/deberta-v3-small/onnx/model_int8_fp16.onnx",
    "modernbert-base-int8": "m3-v2/modernbert-base/onnx/model_int8.onnx",
    "modernbert-base-fp16": "m3-v2/modernbert-base/onnx/model_int8_fp16.onnx",
    "mdeberta-v3-base-int8": "m3-v2/mdeberta-v3-base/onnx/model_int8.onnx",
    "deberta-v3-small-int4": "m3-v2/deberta-v3-small/onnx/model_int8_int4-block.onnx",
    "modernbert-base-int4": "m3-v2/modernbert-base/onnx/model_int8_int4-block.onnx",
    "mdeberta-v3-base-int4": "m3-v2/mdeberta-v3-base/onnx/model_int8_int4-block.onnx",
    "mdeberta-v3-base-int8-gather": "m3-v2/mdeberta-v3-base/onnx/model_int8_gather.onnx",
    "mdeberta-v3-base-int8-matmul": "m3-v2/mdeberta-v3-base/onnx/model_int8_matmul.onnx",
    "mdeberta-v3-base-fp16": "m3-v2/mdeberta-v3-base/onnx/model_int8_fp16.onnx",
}


def lines(path: Path) -> int:
    with path.open() as f:
        return sum(1 for line in f if line.strip())


def params(path: Path) -> float:
    import onnx
    from onnx import numpy_helper

    model = onnx.load(str(path), load_external_data=True)
    return sum(numpy_helper.to_array(t).size for t in model.graph.initializer) / 1e6


def main() -> None:
    import pyarrow.parquet as pq

    docs = {k: lines(ML / "data" / v) for k, v in DATA.items()}
    docs |= {k: pq.read_metadata(ML / "data" / v).num_rows for k, v in RAW.items()}
    docs["gretel_en_dropped"] = docs["gretel_en_train_raw"] - docs["gretel_en_train_all"]

    names = {}
    for group, parts in lx.NAMES.items():
        key = {"Māori": "maori", "Pākehā": "pakeha", "Pasifika": "pasifika", "Asian NZ": "asian_nz"}[group]
        for part, (train, held_out) in parts.items():
            names[f"{key}.{part}.train"] = len(train)
            names[f"{key}.{part}.held_out"] = len(held_out)

    mb = {k: (ML / "runs" / v).stat().st_size / 1e6 for k, v in ONNX.items()}
    fp32 = {k: params(ML / "runs" / v) for k, v in ONNX.items() if k.endswith("-open-fp32")}

    result = {
        "name": "inventory",
        "metrics": {
            "docs": docs,
            "templates": {k: len(v) for k, v in TEMPLATES.items()},
            "names": names,
            "mb": mb,
            "params": fp32,
        },
        "source": {"path": "ml/scripts/export_inventory.py"},
        "produced_by": "ml/scripts/export_inventory.py",
    }
    out = ROOT / "ledger/results/inventory.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result["metrics"], indent=1))


if __name__ == "__main__":
    main()
