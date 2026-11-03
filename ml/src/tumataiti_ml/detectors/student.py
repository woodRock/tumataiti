"""A fine-tuned student encoder (SPEC §10.0)."""

from __future__ import annotations

from ..spans import Span


def make(model: str, device: str = "cuda", threshold: float = 0.5, **_):
    from ..student.infer import load, spans_for

    net, tokenizer = load(model, device)

    def predict(text: str) -> list[Span]:
        return spans_for(net, tokenizer, text, threshold=threshold, device=device)

    return predict
