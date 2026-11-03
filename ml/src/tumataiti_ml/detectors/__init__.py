"""Detectors turn documents into predicted spans (with eval categories set)."""

from __future__ import annotations

import time
from collections.abc import Callable

from ..spans import Doc, Span

Predict = Callable[[str], list[Span]]


def run(predict: Predict, docs: list[Doc], name: str) -> list[Doc]:
    """Apply `predict` to each document, recording per-document latency."""
    out = []
    for d in docs:
        t0 = time.perf_counter()
        spans = predict(d.text)
        out.append(Doc(id=d.id, text="", spans=spans, meta={"detector": name, "seconds": time.perf_counter() - t0}))
    return out


def load(name: str, **kwargs) -> Predict:
    if name == "rules":
        from .rules import make
    elif name == "openai-privacy-filter":
        from .openai_privacy_filter import make
    elif name == "student":
        from .student import make
    elif name == "student-onnx":
        from .student_onnx import make
    else:
        raise ValueError(f"unknown detector {name!r}")
    return make(**kwargs)
