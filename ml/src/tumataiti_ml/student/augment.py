"""Training-data augmentation that keeps gold offsets valid."""

from __future__ import annotations

import random

from ..spans import Doc


def lowercase_some(docs: list[Doc], fraction: float, seed: int) -> list[Doc]:
    """Replace a random `fraction` of documents with lowercased copies, so the
    training set keeps its size. A document whose length would change is left
    as it is, because its gold offsets would no longer hold."""
    chosen = set(random.Random(seed).sample(range(len(docs)), int(fraction * len(docs))))
    out = []
    for i, d in enumerate(docs):
        text = d.text.lower()
        same_length = len(text) == len(d.text)
        out.append(Doc(id=d.id, text=text, spans=d.spans, meta=d.meta) if i in chosen and same_length else d)
    return out
