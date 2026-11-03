import json
import random

import pytest
import tumataiti_rules

from tumataiti_ml.analysis import name_group
from tumataiti_ml.synth import nzids
from tumataiti_ml.synth import lexicon as lx
from tumataiti_ml.synth.generate import TEST_TEMPLATES, TRAIN_TEMPLATES, V2_TEMPLATES, generate


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
    n_train = len(TRAIN_TEMPLATES) + len(V2_TEMPLATES)
    docs = generate(n_train * 3, seed=7) + generate(len(TEST_TEMPLATES) * 3, 7, "test_full")
    assert {d.meta["template"] for d in docs} == set(TRAIN_TEMPLATES) | set(V2_TEMPLATES) | set(TEST_TEMPLATES)
    for d in docs:
        assert d.spans, d.id
        for s in d.spans:
            assert 0 <= s.start < s.end <= len(d.text)
            assert d.text[s.start : s.end].strip() == d.text[s.start : s.end]
    again = generate(n_train * 3, seed=7)
    assert [d.text for d in docs[: len(again)]] == [d.text for d in again]


def test_hard_negatives_are_not_gold():
    docs = [d for d in generate(200, seed=3) if d.meta["template"] == "agenda"]
    for d in docs:
        assert all(s.category == "EMAIL" for s in d.spans)


def _person_names(docs):
    return {d.text[s.start : s.end] for d in docs for s in d.spans if s.label.split(".")[-1] in ("given", "surname")}


def test_held_out_splits_share_no_names_or_templates():
    assert not (set(TRAIN_TEMPLATES) | set(V2_TEMPLATES)) & set(TEST_TEMPLATES)
    for group, parts in lx.NAMES.items():
        for part, (train, test) in parts.items():
            assert not set(train) & set(test), (group, part)
    train_names = _person_names(generate(2000, 1, "train"))
    test_names = _person_names(generate(700, 2, "test_full"))
    assert train_names and test_names and not train_names & test_names


def test_counterfactual_files_differ_only_in_names():
    a = generate(70, 5, "test_full", group="Māori")
    b = generate(70, 5, "test_full", group="Pākehā")
    for x, y in zip(a, b):
        assert [s.label for s in x.spans] == [s.label for s in y.spans]
        assert x.meta["template"] == y.meta["template"]
        names = [x.text[s.start : s.end] for s in x.spans if s.category == "PERSON"]
        assert names and {name_group(n) for n in names} == {"Māori"}


def test_each_name_belongs_to_one_community():
    seen = {}
    for group in lx.NAMES:
        for part in ("given", "surname"):
            for name in lx.all_names(group, part):
                assert seen.setdefault(name, group) == group, name


def test_training_names_are_balanced():
    docs = generate(4000, 1, "train")
    groups = [name_group(d.text[s.start : s.end]) for d in docs for s in d.spans if s.label.endswith(".given")]
    for g in lx.NAMES:
        assert 0.2 < groups.count(g) / len(groups) < 0.3, g


def test_v2_closings_put_the_name_last():
    for d in generate(200, 0, "train"):
        if d.meta["template"] in ("email_reply", "short_reply"):
            last = d.spans[-1]
            assert last.category == "PERSON" and d.text[last.start :] == d.text[last.start : last.end]
