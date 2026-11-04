from tumataiti_ml.datasets.open_pii import find_entities
from tumataiti_ml.taxonomy import OPEN_PII


def test_entities_found_at_word_boundaries_longest_first():
    text = "Ann Lee (ann@example.com) met Lee Ann. Plan: Annual."
    spans = find_entities(text, [("Ann", "first_name"), ("Ann Lee", "name"), ("ann@example.com", "email")])
    assert [(text[s.start : s.end], s.category) for s in spans] == [
        ("Ann Lee", "PERSON"),
        ("ann@example.com", "EMAIL"),
        ("Ann", "PERSON"),  # "Lee Ann": the second "Ann"; "Annual" is not a match
    ]


def test_missing_entity_drops_the_document():
    assert find_entities("Hello there.", [("Mere Ngata", "name")]) is None


def test_scored_labels_map_to_eval_categories():
    assert {v for v in OPEN_PII.values() if v} <= {
        "PERSON", "ADDRESS", "EMAIL", "PHONE", "URL", "IP_ADDRESS", "DATE", "ID", "SECRET",
    }
