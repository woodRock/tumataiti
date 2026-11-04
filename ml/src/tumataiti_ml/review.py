"""Review layer for model spans: flag, rather than redact, model spans that
are probably not PII, so a person decides (SPEC §6.1, §9.8).

- A PERSON span that is only a kinship word ("Koro", "Nan") is flagged: on
  its own it is usually not identifying, but it can be someone's name. This
  is a lexicon rather than training data because training the model on
  kinship negatives made it skip Māori names that are also words (SPEC §9.8). A
  kinship word in front of a name stays in the span: trimming it would leave
  the "Nan" of "Nan Li" visible (the false-alarm set caught this).

- Optional (`transaction_labels`, off by default and not in the Rust port):
  an ID span that is not a valid IRD number, NHI or card number, and whose
  own label on the same line says it is a transaction code ("Order no.",
  "Booking code", "Invoice", "Tracking number"), is flagged. The open English
  test labels such order IDs as customer IDs, so it counts these as leaks
  (SPEC §9.8). The Rust port also relabels unverified model IDs as "other
  ID"; that changes no evaluation category, so it is not mirrored here.

The shape of a number is not evidence on its own: flagging every unlabelled
IRD- or NHI-shaped number that fails the check digit leaked routing numbers,
SSNs and passports of the same shape (open English test 3.3% → 15.2%
document leakage, SPEC §9.8), so unlabelled ID look-alikes stay redacted.

Flagged spans are moved out of `spans` (they are not redacted unless a person
says so), so leak metrics count them as leaks: the conservative reading. The
Rust port is crates/tumataiti-rules/src/review.rs; keep the two in step.
"""

from __future__ import annotations

import re

from .spans import Doc, Span
from .synth.lexicon import strip_macrons
from .synth.nzids import ird_is_valid, luhn_ok, nhi_is_valid

KINSHIP_WORDS = frozenset(
    strip_macrons(w).lower()
    for w in """Koro Koroua Kuia Nan Nana Nanna Nanny Tāua Pōua Aunty Auntie Uncle Matua Whaea Māmā Pāpā
    Mum Mom Dad Grandma Grandpa Grandad Granny Kaumātua""".split()
)

KINSHIP_NOTE = "A family word like Koro or Nan; flagged in case it is someone's name"
TRANSACTION_NOTE = "Labelled as an order or booking code, not a personal ID; flagged for review"

# A transaction label ending just before the span, on the same line.
TRANSACTION_LABEL = re.compile(
    r"(?i)\b(?:order|booking|invoice|tracking|receipt|reservation|confirmation)"
    r"\s*(?:no\.?|number|num|#|code|ref(?:erence)?|id)?\s*[:#.]?\s*$"
)

CODE_TAIL = re.compile(r"(?:[0-9A-Z]+[- ]?)*$")


def _verified_id(t: str) -> bool:
    digits = "".join(c for c in t if c.isdigit())
    return ird_is_valid(t) or nhi_is_valid(t) or (13 <= len(digits) <= 19 and luhn_ok(digits))


def _is_kin(word: str) -> bool:
    return strip_macrons(word).lower() in KINSHIP_WORDS


def review_span(text: str, s: Span, transaction_labels: bool = False) -> str | None:
    """A reason to flag the span, or None to keep it."""
    t = text[s.start : s.end]
    if s.category == "PERSON" and _is_kin(t):
        return KINSHIP_NOTE
    if transaction_labels and s.category == "ID" and not _verified_id(t):
        before = text[max(0, s.start - 40) : s.start].rsplit("\n", 1)[-1]
        # The model sometimes tags a piece of a code ("283-" of "61-283-509"):
        # skip the rest of the code back to its label.
        before = CODE_TAIL.sub("", before)
        if TRANSACTION_LABEL.search(before):
            return TRANSACTION_NOTE
    return None


def review(doc: Doc, text: str, transaction_labels: bool = False) -> Doc:
    """Predictions with flagged spans moved to meta["flagged"] as [start, end, category, note]."""
    kept, flagged = [], []
    for s in doc.spans:
        note = review_span(text, s, transaction_labels)
        if note:
            flagged.append([s.start, s.end, s.category, note])
        else:
            kept.append(s)
    return Doc(id=doc.id, text=doc.text, spans=kept, meta={**doc.meta, "flagged": flagged})
