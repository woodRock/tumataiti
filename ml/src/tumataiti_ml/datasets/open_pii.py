"""Openly licensed synthetic English PII data, used in place of PII-Masking-300k
for any model that will be published (its licence forbids distributing
derivative works such as trained weights).

- nvidia/Nemotron-PII (CC BY 4.0): character spans.
- gretelai/gretel-pii-masking-en-v1 (Apache-2.0): entity strings without
  offsets; spans are found by exact, word-bounded matching, and a document is
  dropped when any of its entities cannot be found (an unlabelled name would
  teach the model to skip it).
- gretelai/synthetic_pii_finance_multilingual (Apache-2.0), English: character
  spans, labelled after generation with GLiNER and an LLM judge, so noisier.

Files are downloaded on demand into data/raw/open/ and never committed.
Attribution for the paper and model card: see SPEC §9.1.
"""

from __future__ import annotations

import ast
import json
import random
import re
import urllib.request
from pathlib import Path

from ..spans import Doc, Span
from ..taxonomy import OPEN_PII, map_label

HF = "https://huggingface.co/datasets/"
SOURCES = {
    # name: {split: (repo file URL, local file)}
    "nemotron": {
        "train": (HF + "nvidia/Nemotron-PII/resolve/main/data/train-00000-of-00001.parquet", "nemotron_train.parquet"),
        "test": (HF + "nvidia/Nemotron-PII/resolve/main/data/test-00000-of-00001.parquet", "nemotron_test.parquet"),
    },
    "gretel-en": {
        "train": (
            HF + "gretelai/gretel-pii-masking-en-v1/resolve/main/data/train-00000-of-00001.parquet",
            "gretel_en_train.parquet",
        ),
        "test": (
            HF + "gretelai/gretel-pii-masking-en-v1/resolve/main/data/validation-00000-of-00001.parquet",
            "gretel_en_validation.parquet",
        ),
    },
    "gretel-finance": {
        "train": (
            HF + "gretelai/synthetic_pii_finance_multilingual/resolve/main/data/English_train-00000-of-00001.parquet",
            "gretel_fin_en_train.parquet",
        ),
        "test": (
            HF + "gretelai/synthetic_pii_finance_multilingual/resolve/main/data/English_test-00000-of-00001.parquet",
            "gretel_fin_en_test.parquet",
        ),
    },
}


def download(source: str, split: str, raw_dir: Path) -> Path:
    url, name = SOURCES[source][split]
    dest = raw_dir / name
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, dest)
    return dest


def _parse(value):
    """Span lists are stored as JSON (Gretel finance) or Python literals (the others)."""
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return ast.literal_eval(value)


def _span(start: int, end: int, label: str) -> Span:
    return Span(start, end, label, map_label(OPEN_PII, label))


def find_entities(text: str, entities: list[tuple[str, str]]) -> list[Span] | None:
    """Spans for every word-bounded occurrence of each `(value, label)`, or None
    if a value does not occur. Where matches overlap, the longer value wins."""
    found: list[Span] = []
    for value, label in sorted(entities, key=lambda e: -len(e[0])):
        value = value.strip()
        if not value:
            continue
        hits = [m.start() for m in re.finditer(r"(?<!\w)" + re.escape(value) + r"(?!\w)", text)]
        if not hits:
            return None
        for a in hits:
            b = a + len(value)
            if not any(s.start < b and a < s.end for s in found):
                found.append(_span(a, b, label))
    return sorted(found, key=lambda s: s.start)


def load(source: str, path: Path) -> tuple[list[Doc], int]:
    """Documents from one downloaded file, and how many were dropped."""
    import pyarrow.parquet as pq

    rows = pq.read_table(path).to_pylist()
    docs, dropped = [], 0
    for i, row in enumerate(rows):
        if source == "nemotron":
            # Offsets are exact; the copied span text sometimes differs in case only.
            text = row["text"]
            spans = [_span(s["start"], s["end"], s["label"]) for s in _parse(row["spans"])]
        elif source == "gretel-finance":
            text = row["generated_text"]
            spans = [_span(s["start"], s["end"], s["label"]) for s in _parse(row["pii_spans"])]
        else:
            text = row["text"]
            entities = [(e["entity"], t) for e in _parse(row["entities"]) for t in e["types"][:1]]
            spans = find_entities(text, entities)
        if spans is None or any(not (0 <= s.start < s.end <= len(text)) for s in spans):
            dropped += 1
            continue
        uid = row.get("uid") or row.get("index") or i
        docs.append(Doc(id=f"{source}-{uid}", text=text, spans=spans, meta={"source": source}))
    return docs, dropped


def sample(docs: list[Doc], n: int | None, seed: int) -> list[Doc]:
    if n is None or n >= len(docs):
        return docs
    return random.Random(seed).sample(docs, n)
