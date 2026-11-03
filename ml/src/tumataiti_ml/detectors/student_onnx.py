"""A student exported to ONNX (fp32 or int8), run with ONNX Runtime on CPU.

The same runtime family runs in the browser (ONNX Runtime Web), so this is the
closest laptop-side check of what the demo will ship.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from ..spans import Span
from ..student.encode import decode, union, windows

EVAL_CATEGORY = {"AFFILIATION": None}


def make(model: str, threshold: float = 0.5, **_):
    import onnxruntime as ort
    from transformers import AutoTokenizer

    path = Path(model)
    tokenizer = AutoTokenizer.from_pretrained(path.parent)
    opts = ort.SessionOptions()
    opts.intra_op_num_threads = 4
    session = ort.InferenceSession(str(path), opts, providers=["CPUExecutionProvider"])

    def predict(text: str) -> list[Span]:
        enc = windows(tokenizer, text, 512, 128)
        found = []
        for w in range(len(enc["input_ids"])):
            feed = {
                "input_ids": np.array([enc["input_ids"][w]], dtype=np.int64),
                "attention_mask": np.array([enc["attention_mask"][w]], dtype=np.int64),
            }
            logits = session.run(["logits"], feed)[0][0]
            probs = np.exp(logits - logits.max(-1, keepdims=True))
            probs /= probs.sum(-1, keepdims=True)
            offsets = [(a, b) if not sp else (0, 0) for (a, b), sp in zip(enc["offset_mapping"][w], enc["special_tokens_mask"][w])]
            found += decode(text, offsets, probs, threshold)
        return [Span(a, b, label, EVAL_CATEGORY.get(label, label), conf) for a, b, label, conf in union(found)]

    return predict
