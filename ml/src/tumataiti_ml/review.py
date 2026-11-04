"""Review layer for model spans: flag, rather than redact, model spans that
are probably not PII, so a person decides (SPEC §6.1, §9.8).

- A PERSON span that is only a kinship word ("Koro", "Nan") is flagged: on
  its own it is usually not identifying, but it can be someone's name. This
  is a lexicon rather than training data because training the model on
  kinship negatives made it skip Māori names that are also words (SPEC §9.8). A
  kinship word in front of a name stays in the span: trimming it would leave
  the "Nan" of "Nan Li" visible (the false-alarm set caught this).

IDs are not reviewed. Flagging unlabelled IRD- and NHI-shaped numbers that
fail the check digit was tried and rejected: nine-digit routing numbers,
SSNs and passports have the same shape, so it raised document leakage on the
open English test from 3.3% to 15.2% and on PII-Masking-300k from 34% to 51%
(SPEC §9.8). ID-shaped order and booking codes stay redacted: over-redaction,
the safe direction.

Flagged spans are moved out of `spans` (they are not redacted unless a person
says so), so leak metrics count them as leaks: the conservative reading. The
Rust port is crates/tumataiti-rules/src/review.rs; keep the two in step.
"""

from __future__ import annotations

from .spans import Doc, Span
from .synth.lexicon import strip_macrons

KINSHIP_WORDS = frozenset(
    strip_macrons(w).lower()
    for w in """Koro Koroua Kuia Nan Nana Nanna Nanny Tāua Pōua Aunty Auntie Uncle Matua Whaea Māmā Pāpā
    Mum Mom Dad Grandma Grandpa Grandad Granny Kaumātua""".split()
)

KINSHIP_NOTE = "A family word like Koro or Nan; flagged in case it is someone's name"


def _is_kin(word: str) -> bool:
    return strip_macrons(word).lower() in KINSHIP_WORDS


def review_span(text: str, s: Span) -> str | None:
    """A reason to flag the span, or None to keep it."""
    if s.category == "PERSON" and _is_kin(text[s.start : s.end]):
        return KINSHIP_NOTE
    return None


def review(doc: Doc, text: str) -> Doc:
    """Predictions with flagged spans moved to meta["flagged"] as [start, end, category, note]."""
    kept, flagged = [], []
    for s in doc.spans:
        note = review_span(text, s)
        if note:
            flagged.append([s.start, s.end, s.category, note])
        else:
            kept.append(s)
    return Doc(id=doc.id, text=doc.text, spans=kept, meta={**doc.meta, "flagged": flagged})
