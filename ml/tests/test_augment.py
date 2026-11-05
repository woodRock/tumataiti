from tumataiti_ml.spans import Doc, Span
from tumataiti_ml.student.augment import lowercase_some


def docs(n=10):
    return [Doc(f"d{i}", f"Kia ora Hēmi {i}", [Span(8, 12, "PERSON", "PERSON")]) for i in range(n)]


def test_fraction_is_replaced_and_spans_survive():
    out = lowercase_some(docs(), 0.3, seed=0)
    assert len(out) == 10
    assert sum(d.text == d.text.lower() for d in out) == 3
    assert all(d.text[8:12].lower() == "hēmi" and d.spans[0].start == 8 for d in out)


def test_zero_fraction_changes_nothing():
    original = docs()
    assert lowercase_some(original, 0.0, seed=0) == original


def test_same_seed_chooses_the_same_documents():
    assert lowercase_some(docs(), 0.5, seed=1) == lowercase_some(docs(), 0.5, seed=1)


def test_a_length_changing_lowercase_is_skipped():
    text = "İstanbul"  # lowercases to one character more
    d = Doc("d", text, [Span(0, 8, "ADDRESS", "ADDRESS")])
    assert lowercase_some([d], 1.0, seed=0)[0].text == text
