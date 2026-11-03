"""Documents, spans and JSONL I/O shared by datasets, detectors and metrics.

Offsets are Python string indices (code points), end exclusive.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Iterator
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class Span:
    start: int
    end: int
    # Label in the source taxonomy (dataset or detector), e.g. "nz_ird" or "GIVENNAME1".
    label: str
    # Evaluation category (see taxonomy.py), or None to ignore this span when scoring.
    category: str | None
    confidence: float = 1.0


@dataclass
class Doc:
    id: str
    text: str
    spans: list[Span] = field(default_factory=list)
    meta: dict = field(default_factory=dict)


def write_jsonl(path: Path, docs: Iterable[Doc]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8") as f:
        for d in docs:
            f.write(json.dumps(asdict(d), ensure_ascii=False) + "\n")
            n += 1
    return n


def read_jsonl(path: Path) -> Iterator[Doc]:
    with path.open(encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            spans = [Span(**s) for s in row.pop("spans")]
            yield Doc(spans=spans, **row)
