import re
from pathlib import Path

from tumataiti_ml.analysis import false_alarms
from tumataiti_ml.review import KINSHIP_WORDS, review
from tumataiti_ml.spans import Doc, Span
from tumataiti_ml.synth import lexicon as lx
from tumataiti_ml.synth.generate import FALSE_ALARM_TEMPLATES, V3_TEMPLATES, generate

RUST = Path(__file__).parents[2] / "crates/tumataiti-rules/src/review.rs"


def test_kinship_word_alone_is_flagged_and_names_are_kept():
    text = "Koro's IRD number. Nan Li and Nanny Rīpeka will help Tāua."
    spans = [Span(text.index(w), text.index(w) + len(w), "PERSON", "PERSON") for w in ("Koro", "Nan Li", "Nanny Rīpeka", "Tāua")]
    out = review(Doc("d", text, spans), text)
    assert [text[s.start : s.end] for s in out.spans] == ["Nan Li", "Nanny Rīpeka"]
    assert [text[a:b] for a, b, *_ in out.meta["flagged"]] == ["Koro", "Tāua"]


def test_only_person_spans_are_reviewed():
    text = "Nan"
    out = review(Doc("d", text, [Span(0, 3, "ADDRESS", "ADDRESS")]), text)
    assert len(out.spans) == 1 and not out.meta["flagged"]


def test_python_and_rust_kinship_lists_match():
    rust = set(re.findall(r'"([a-z]+)"', RUST.read_text().split("KINSHIP_WORDS")[1].split("];")[0]))
    assert rust == set(KINSHIP_WORDS)


def test_every_kinship_word_in_the_generator_is_reviewed():
    for words in lx.KINSHIP:
        assert {lx.strip_macrons(w).lower() for w in words} <= KINSHIP_WORDS


def test_false_alarm_set_records_negatives_and_holds_out_kinship_words():
    docs = generate(60, seed=6, split="test_false_alarm")
    assert {d.meta["template"] for d in docs} == set(FALSE_ALARM_TEMPLATES)
    train_kin, test_kin = set(lx.KINSHIP[0]), set(lx.KINSHIP[1])
    assert not train_kin & test_kin
    for d in docs:
        for a, b, slot in d.meta["negatives"]:
            assert not any(s.start < b and a < s.end for s in d.spans)
            if slot == "kin":
                assert d.text[a:b] in test_kin
    assert not set(FALSE_ALARM_TEMPLATES) & set(V3_TEMPLATES)


def test_false_alarms_counts_redacted_and_flagged():
    gold = Doc("d", "ask Koro about INV-1", [], {"negatives": [[4, 8, "kin"], [15, 20, "invoice"]]})
    pred = Doc("d", "", [Span(15, 20, "x", "ID")], {"flagged": [[4, 8, "PERSON", "note"]]})
    rows = false_alarms([gold], {"d": pred})
    assert rows["not PII: kin"] == {"n": 1, "redacted": 0.0, "flagged": 1.0}
    assert rows["not PII: invoice"]["redacted"] == 1.0
