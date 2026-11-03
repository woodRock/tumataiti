"""openai/privacy-filter, the teacher and baseline (SPEC §6.1).

Decoding follows the model card: a constrained Viterbi pass over per-token
log-probabilities that only allows valid BIOES transitions. The released
default operating point sets all six transition biases to zero, so plain
constrained Viterbi reproduces it.
"""

from __future__ import annotations

import numpy as np

from ..spans import Span
from ..taxonomy import OPENAI_PRIVACY_FILTER, map_label

MODEL_ID = "openai/privacy-filter"


def allowed_transitions(labels: list[str]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(start, transition, end) masks for BIOES: True where allowed."""
    n = len(labels)
    tag = [l.split("-", 1)[0] if l != "O" else "O" for l in labels]
    ent = [l.split("-", 1)[1] if l != "O" else None for l in labels]
    start = np.array([t in ("O", "B", "S") for t in tag])
    end = np.array([t in ("O", "E", "S") for t in tag])
    trans = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(n):
            if tag[i] in ("O", "E", "S"):
                trans[i, j] = tag[j] in ("O", "B", "S")
            else:  # inside an entity: continue or close the same one
                trans[i, j] = tag[j] in ("I", "E") and ent[j] == ent[i]
    return start, trans, end


def viterbi(logp: np.ndarray, start: np.ndarray, trans: np.ndarray, end: np.ndarray) -> list[int]:
    neg = -1e9
    t_score = np.where(trans, 0.0, neg)
    score = logp[0] + np.where(start, 0.0, neg)
    back = np.zeros(logp.shape, dtype=np.int64)
    for t in range(1, len(logp)):
        cand = score[:, None] + t_score
        back[t] = cand.argmax(axis=0)
        score = cand.max(axis=0) + logp[t]
    score = score + np.where(end, 0.0, neg)
    path = [int(score.argmax())]
    for t in range(len(logp) - 1, 0, -1):
        path.append(int(back[t, path[-1]]))
    return path[::-1]


def tags_to_spans(text: str, tags: list[str], offsets: list[tuple[int, int]]) -> list[tuple[int, int, str]]:
    spans, open_ = [], None
    for tag, (a, b) in zip(tags, offsets):
        if a == b:
            continue
        kind, _, ent = tag.partition("-")
        if kind == "S":
            spans.append((a, b, ent))
        elif kind == "B":
            open_ = (a, ent)
        elif kind == "E" and open_:
            spans.append((open_[0], b, open_[1]))
            open_ = None
    trimmed = []
    for a, b, ent in spans:
        while a < b and text[a].isspace():
            a += 1
        while b > a and text[b - 1].isspace():
            b -= 1
        if a < b:
            trimmed.append((a, b, ent))
    return trimmed


def make(device: str = "cuda", **_):
    import torch
    from transformers import AutoModelForTokenClassification, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForTokenClassification.from_pretrained(MODEL_ID, dtype=torch.bfloat16).to(device).eval()
    labels = [model.config.id2label[i] for i in range(model.config.num_labels)]
    start, trans, end = allowed_transitions(labels)

    @torch.inference_mode()
    def predict(text: str) -> list[Span]:
        enc = tokenizer(text, return_offsets_mapping=True, return_tensors="pt")
        offsets = [tuple(o) for o in enc.pop("offset_mapping")[0].tolist()]
        logits = model(**enc.to(device)).logits[0].float()
        logp = torch.log_softmax(logits, dim=-1).cpu().numpy()
        path = viterbi(logp, start, trans, end)
        return [
            Span(a, b, ent, map_label(OPENAI_PRIVACY_FILTER, ent))
            for a, b, ent in tags_to_spans(text, [labels[i] for i in path], offsets)
        ]

    return predict
