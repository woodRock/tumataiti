"""The Rust rules (crates/tumataiti-rules) through their Python bindings."""

from __future__ import annotations

import json

import tumataiti_rules

from ..spans import Span
from ..taxonomy import TUMATAITI, map_label


def make(threshold: float = 0.5, **_):
    """Spans below `threshold` would be flagged, not redacted, so they don't count."""

    def predict(text: str) -> list[Span]:
        return [
            Span(s["start"], s["end"], s["detector"], map_label(TUMATAITI, s["category"]), s["confidence"])
            for s in json.loads(tumataiti_rules.scan_json(text))
            if s["confidence"] >= threshold
        ]

    return predict
