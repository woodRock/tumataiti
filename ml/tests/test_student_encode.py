import re

import numpy as np

from tumataiti_ml.spans import Doc, Span
from tumataiti_ml.student.encode import IGNORE_INDEX, TAGS, decode, encode_doc, union


class WordTokenizer:
    """Stand-in for a fast tokenizer: one token per word or punctuation mark."""

    def __call__(self, text, max_length, stride, **_):
        offsets = [m.span() for m in re.finditer(r"\w+|[^\w\s]", text)]
        body = max_length - 2
        out = {"input_ids": [], "attention_mask": [], "offset_mapping": [], "special_tokens_mask": []}
        start = 0
        while True:
            chunk = offsets[start : start + body]
            offs = [(0, 0), *chunk, (0, 0)]
            out["input_ids"].append(list(range(len(offs))))
            out["attention_mask"].append([1] * len(offs))
            out["offset_mapping"].append(offs)
            out["special_tokens_mask"].append([1] + [0] * len(chunk) + [1])
            if start + body >= len(offsets):
                return out
            start += body - stride


TEXT = "Ko Te Ao Ngata tōku ingoa, ring 021 123 4567 or Te Ao again."
GOLD = [Span(3, 14, "PERSON:p1.full", "PERSON"), Span(32, 44, "PHONE:p1.mobile", "PHONE"), Span(48, 53, "PERSON:p1.given", "PERSON")]


def one_hot(labels):
    probs = np.zeros((len(labels), len(TAGS)))
    for i, l in enumerate(labels):
        probs[i, 0 if l == IGNORE_INDEX else l] = 1
    return probs


def test_labels_round_trip_through_decode():
    doc = Doc("d", TEXT, GOLD)
    tok = WordTokenizer()
    (ex,) = encode_doc(tok, doc, max_length=64, stride=4)
    offsets = tok(TEXT, 64, 4)["offset_mapping"][0]
    spans = decode(TEXT, offsets, one_hot(ex["labels"]))
    assert [(a, b, l) for a, b, l, _ in spans] == [(3, 14, "PERSON"), (32, 44, "PHONE"), (48, 53, "PERSON")]


def test_adjacent_entities_stay_separate():
    tags = [TAGS.index("B-PERSON"), TAGS.index("B-PERSON")]
    spans = decode("Aroha Mere", [(0, 5), (6, 10)], one_hot(tags))
    assert [(a, b) for a, b, *_ in spans] == [(0, 5), (6, 10)]


def test_spans_widen_to_whole_words():
    # "I" alone inside "NHI", and "Nga" inside "Ngata's" (the Rust decoder has the same test).
    text = "NHI ZZZ0016, Ngata's"
    tags = [TAGS.index("B-ID"), 0, TAGS.index("B-PERSON"), 0]
    spans = decode(text, [(2, 3), (3, 4), (13, 16), (16, 18)], one_hot(tags))
    # "NHI" widens to a whole word, then is dropped as a field label.
    assert [(a, b) for a, b, *_ in spans] == [(13, 18)]


def test_windows_cover_long_documents_and_union_merges_overlaps():
    doc = Doc("d", TEXT, GOLD)
    tok = WordTokenizer()
    examples = encode_doc(tok, doc, max_length=8, stride=2)
    assert len(examples) > 1
    found = []
    enc = tok(TEXT, 8, 2)
    for ex, offs in zip(examples, enc["offset_mapping"]):
        found += decode(TEXT, offs, one_hot(ex["labels"]))
    assert [(a, b, l) for a, b, l, _ in union(found)] == [(3, 14, "PERSON"), (32, 44, "PHONE"), (48, 53, "PERSON")]


def test_lower_threshold_redacts_more():
    probs = np.zeros((1, len(TAGS)))
    probs[0, 0], probs[0, TAGS.index("B-PERSON")] = 0.8, 0.2
    assert decode("Tūī", [(0, 3)], probs, threshold=0.5) == []
    assert decode("Tūī", [(0, 3)], probs, threshold=0.15)[0][:3] == (0, 3, "PERSON")
