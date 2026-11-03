import numpy as np

from tumataiti_ml.detectors.openai_privacy_filter import allowed_transitions, tags_to_spans, viterbi
from tumataiti_ml.metrics import score
from tumataiti_ml.spans import Doc, Span


def doc(text, *spans):
    return Doc("d", text, [Span(a, b, "x", c) for a, b, c in spans])


def test_perfect_prediction():
    g = doc("Call Aroha on 021 123 4567", (5, 10, "PERSON"), (14, 26, "PHONE"))
    r = score([g], {"d": g}).as_dict()
    assert r["doc_leak_rate"] == 0
    assert r["char_any"]["f1"] == 1
    assert r["exact_all"]["f1"] == 1


def test_partial_name_coverage_leaks():
    g = doc("Aroha Ngata", (0, 11, "PERSON"))
    p = doc("Aroha Ngata", (0, 5, "PERSON"))
    r = score([g], {"d": p}).as_dict()
    assert r["doc_leak_rate"] == 1
    assert r["char_any"]["recall"] == 5 / 10  # the space is not alphanumeric


def test_wrong_category_still_prevents_leak():
    g = doc("IRD 49-091-850", (4, 14, "ID"))
    p = doc("IRD 49-091-850", (4, 14, "PHONE"))
    r = score([g], {"d": p}).as_dict()
    assert r["doc_leak_rate"] == 0
    assert r["char"]["ID"]["recall"] == 0
    assert r["char"]["PHONE"]["precision"] == 0


def test_ignored_regions_are_not_false_positives():
    g = doc("Meeting at 10:20am", (11, 18, None))
    p = doc("Meeting at 10:20am", (11, 18, "DATE"))
    r = score([g], {"d": p}).as_dict()
    assert r["char_any"]["fp"] == 0
    assert r["exact_all"]["fp"] == 0
    assert r["docs_with_pii"] == 0


def test_false_positive_counted():
    g = doc("Order 12345678")
    p = doc("Order 12345678", (6, 14, "ID"))
    r = score([g], {"d": p}).as_dict()
    assert r["char_any"]["fp"] == 8


def test_viterbi_never_emits_invalid_bioes():
    labels = ["O", "B-x", "I-x", "E-x", "S-x"]
    start, trans, end = allowed_transitions(labels)
    rng = np.random.default_rng(0)
    for _ in range(50):
        logp = np.log(rng.dirichlet(np.ones(5), size=12))
        path = [labels[i] for i in viterbi(logp, start, trans, end)]
        assert path[0][0] in "OBS" and path[-1][0] in "OES"
        for a, b in zip(path, path[1:]):
            assert (a[0] in "BI") == (b[0] in "IE")


def test_tags_to_spans_trims_whitespace():
    text = "Hi Aroha Ngata!"
    tags = ["O", "B-private_person", "E-private_person", "O"]
    offsets = [(0, 2), (2, 8), (8, 14), (14, 15)]
    assert tags_to_spans(text, tags, offsets) == [(3, 14, "private_person")]


def test_name_group_handles_macrons_and_two_word_names():
    from tumataiti_ml.analysis import name_group

    assert name_group("Hēmi Walker") == "Māori"
    assert name_group("Hemi") == "Māori"
    assert name_group("Te Ao Smith") == "Māori"
    assert name_group("Smith") == "Pākehā"
    assert name_group("Zebedee") is None


def test_combine_prefers_primary_on_overlap():
    from tumataiti_ml.analysis import combine

    rules = Doc("d", "", [Span(4, 14, "nz_ird", "ID")])
    model = Doc("d", "", [Span(0, 12, "private_phone", "PHONE"), Span(20, 25, "private_person", "PERSON")])
    spans = combine(rules, model).spans
    assert [s.label for s in spans] == ["nz_ird", "private_person"]
    # The rule's label wins, stretched over the model span's extra characters.
    assert (spans[0].start, spans[0].end) == (0, 14)
