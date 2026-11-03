"""ai4privacy/pii-masking-300k, English validation split (public benchmark).

The licence allows academic use with citation; the data is downloaded on
demand and never committed.
"""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

from ..spans import Doc, Span
from ..taxonomy import PII_MASKING_300K, map_label

URL = (
    "https://huggingface.co/datasets/ai4privacy/pii-masking-300k/resolve/main/"
    "data/validation/1english_openpii_8k.jsonl"
)


def download(dest: Path) -> Path:
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(URL, dest)
    return dest


def load(raw: Path, limit: int | None = None) -> list[Doc]:
    docs = []
    with raw.open(encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            spans = [
                Span(m["start"], m["end"], m["label"], map_label(PII_MASKING_300K, m["label"]))
                for m in row["privacy_mask"]
            ]
            docs.append(Doc(id=f"pii300k-{row['id']}", text=row["source_text"], spans=spans))
            if limit and len(docs) >= limit:
                break
    return docs
