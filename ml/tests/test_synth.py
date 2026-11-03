import json
import random

import pytest
import tumataiti_rules

from tumataiti_ml.synth import nzids
from tumataiti_ml.synth.generate import TEMPLATES, generate


def rule_hits(text: str) -> list[dict]:
    return json.loads(tumataiti_rules.scan_json(text))


@pytest.mark.parametrize("seed", range(5))
def test_ird_generator_agrees_with_rust(seed):
    rng = random.Random(seed)
    for _ in range(200):
        good, bad = nzids.gen_ird(rng), nzids.gen_ird(rng, valid=False)
        assert [h["checksum"] for h in rule_hits(f"IRD {good}")] == ["valid"], good
        assert [h["checksum"] for h in rule_hits(f"IRD {bad}")] == ["invalid"], bad


@pytest.mark.parametrize("new_format", [False, True])
def test_nhi_generator_agrees_with_rust(new_format):
    rng = random.Random(1)
    for _ in range(300):
        good = nzids.gen_nhi(rng, new_format=new_format)
        bad = nzids.gen_nhi(rng, valid=False, new_format=new_format)
        assert [h["checksum"] for h in rule_hits(f"NHI {good}")] == ["valid"], good
        assert [h["checksum"] for h in rule_hits(f"NHI {bad}")] == ["invalid"], bad


def test_card_generator_agrees_with_rust():
    rng = random.Random(2)
    for _ in range(300):
        good, bad = nzids.gen_card(rng), nzids.gen_card(rng, valid=False)
        assert [h["checksum"] for h in rule_hits(f"card {good}")] == ["valid"], good
        assert [h["checksum"] for h in rule_hits(f"card {bad}")] == ["invalid"], bad


def test_gold_spans_match_text_and_are_deterministic():
    docs = generate(len(TEMPLATES) * 3, seed=7)
    assert {d.meta["template"] for d in docs} == set(TEMPLATES)
    for d in docs:
        assert d.spans, d.id
        for s in d.spans:
            assert 0 <= s.start < s.end <= len(d.text)
            assert d.text[s.start : s.end].strip() == d.text[s.start : s.end]
    again = generate(len(TEMPLATES) * 3, seed=7)
    assert [d.text for d in docs] == [d.text for d in again]


def test_hard_negatives_are_not_gold():
    docs = [d for d in generate(200, seed=3) if d.meta["template"] == "agenda"]
    for d in docs:
        assert all(s.category == "EMAIL" for s in d.spans)
