"""Turn character spans into BIO token labels and back (SPEC §10.0).

Long documents are split into overlapping windows. At inference, spans found
in any window are unioned, which errs towards redacting more (recall first).
"""

from __future__ import annotations

import numpy as np

from ..spans import Doc, Span
from ..taxonomy import EVAL_CATEGORIES

# AFFILIATION is last, as it was before it was scored, so older models' tag ids still match.
LABELS = EVAL_CATEGORIES
TAGS = ("O", *(f"{p}-{c}" for c in LABELS for p in ("B", "I")))
TAG_ID = {t: i for i, t in enumerate(TAGS)}
IGNORE_INDEX = -100

# Identifier field labels. They are never PII themselves, but after spans widen
# to whole words a stray tag on part of one (the "I" of "NHI") would redact the
# label, so a span that is exactly one of these is dropped. The Rust decoder
# (crates/tumataiti-student) has the same list.
FIELD_LABELS = frozenset(
    "NHI IRD GST DOB DL SSN PIN CVV CVC IBAN BSB TFN NZBN ACC NI ID SIN EIN ITIN MRN VIN".split()
)


def student_label(span: Span) -> str | None:
    """Training label for a gold span, or None to train it as background."""
    if span.label.startswith("AFFILIATION:"):
        return "AFFILIATION"
    return span.category


def windows(tokenizer, text: str, max_length: int, stride: int):
    """Tokenizer output for overlapping windows, with character offsets."""
    return tokenizer(
        text,
        max_length=max_length,
        stride=stride,
        truncation=True,
        return_overflowing_tokens=True,
        return_offsets_mapping=True,
        return_special_tokens_mask=True,
    )


def encode_doc(tokenizer, doc: Doc, max_length: int, stride: int) -> list[dict]:
    """One training example per window: input_ids, attention_mask, labels."""
    char_label: list[tuple[str, int] | None] = [None] * len(doc.text)
    for s in doc.spans:
        label = student_label(s)
        if label is None:
            continue
        # A few PII-Masking-300k spans run past the end of their text; clamp them.
        for i in range(max(0, s.start), min(len(doc.text), s.end)):
            char_label[i] = (label, s.start)
    enc = windows(tokenizer, doc.text, max_length, stride)
    examples = []
    for w in range(len(enc["input_ids"])):
        labels = []
        prev_span = None  # start offset of the span the previous token belonged to
        for (a, b), special in zip(enc["offset_mapping"][w], enc["special_tokens_mask"][w]):
            if special or a == b:
                labels.append(IGNORE_INDEX)
                continue
            # A token is inside a span if any of its non-space characters are.
            hit = next((char_label[i] for i in range(a, b) if char_label[i] and not doc.text[i].isspace()), None)
            if hit is None:
                labels.append(TAG_ID["O"])
                prev_span = None
            else:
                label, span_start = hit
                labels.append(TAG_ID[f"{'I' if span_start == prev_span else 'B'}-{label}"])
                prev_span = span_start
        examples.append(
            {"input_ids": enc["input_ids"][w], "attention_mask": enc["attention_mask"][w], "labels": labels}
        )
    return examples


def decode(
    text: str,
    offsets: list[tuple[int, int]],
    probs: np.ndarray,
    threshold: float = 0.5,
) -> list[tuple[int, int, str, float]]:
    """Spans from one window's per-token tag probabilities.

    A token is part of an entity when P(not O) >= threshold; its label is the
    most likely non-O tag. Lower thresholds redact more (an operating point).
    An I- tag that does not continue a span of the same label starts a new one.
    Spans are trimmed of whitespace, then widened to whole words: a span that
    starts or ends inside a run of letters and digits takes the whole run, so
    no part of a word is left exposed (M3: this cut held-out document leakage
    for DeBERTa-small from 4.9% to 3.0%; trimming to whole words instead raised it).
    """
    o = TAG_ID["O"]
    spans: list[list] = []
    prev_label = None
    for (a, b), p in zip(offsets, probs):
        if a == b:
            continue
        if 1 - p[o] < threshold:
            prev_label = None
            continue
        p_ent = p.copy()
        p_ent[o] = -1
        tag = TAGS[int(p_ent.argmax())]
        kind, label = tag.split("-", 1)
        conf = float(1 - p[o])
        if kind == "I" and prev_label == label and spans:
            spans[-1][1] = b
            spans[-1][3] = min(spans[-1][3], conf)
        else:
            spans.append([a, b, label, conf])
        prev_label = label
    out = []
    for a, b, label, conf in spans:
        while a < b and text[a].isspace():
            a += 1
        while b > a and text[b - 1].isspace():
            b -= 1
        if a < b:
            while a > 0 and text[a - 1].isalnum() and text[a].isalnum():
                a -= 1
            while b < len(text) and text[b].isalnum() and text[b - 1].isalnum():
                b += 1
            if text[a:b].upper() not in FIELD_LABELS:
                out.append((a, b, label, conf))
    return out


def union(spans: list[tuple[int, int, str, float]]) -> list[tuple[int, int, str, float]]:
    """Merge overlapping spans from different windows."""
    merged: list[list] = []
    for a, b, label, conf in sorted(spans):
        if merged and a < merged[-1][1]:
            last = merged[-1]
            if b - a > last[1] - last[0]:
                last[2] = label
            last[1] = max(last[1], b)
            last[3] = max(last[3], conf)
        else:
            merged.append([a, b, label, conf])
    return [tuple(m) for m in merged]
