"""Scoring predictions against gold spans (SPEC §9.2).

Three views, all over the evaluation categories in taxonomy.py:

- Character level: precision, recall and F1 over alphanumeric characters, so
  boundary conventions (a trailing full stop, "Dr" in or out of a name) and
  name splitting (given and family name as one span or two) don't dominate.
- Exact spans: same start, end and category. Strict; useful to compare models
  trained on the same conventions.
- Leakage, the headline: a gold span leaks if any of its alphanumeric
  characters is left uncovered by every prediction, whatever its category.
  A document leaks if any of its gold spans leaks.

Gold spans whose category is None mark ignored regions: predictions there
are neither rewarded nor counted as false positives.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from .spans import Doc
from .taxonomy import EVAL_CATEGORIES

IGNORE = "~"


@dataclass
class PRF:
    tp: int = 0
    fp: int = 0
    fn: int = 0

    @property
    def precision(self) -> float:
        return self.tp / (self.tp + self.fp) if self.tp + self.fp else 0.0

    @property
    def recall(self) -> float:
        return self.tp / (self.tp + self.fn) if self.tp + self.fn else 0.0

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if p + r else 0.0

    def as_dict(self) -> dict:
        return {
            "precision": self.precision,
            "recall": self.recall,
            "f1": self.f1,
            "tp": self.tp,
            "fp": self.fp,
            "fn": self.fn,
        }


@dataclass
class Report:
    docs: int = 0
    docs_with_pii: int = 0
    docs_leaked: int = 0
    char_any: PRF = field(default_factory=PRF)
    char: dict[str, PRF] = field(default_factory=lambda: {c: PRF() for c in EVAL_CATEGORIES})
    exact: dict[str, PRF] = field(default_factory=lambda: {c: PRF() for c in EVAL_CATEGORIES})
    gold_spans: Counter = field(default_factory=Counter)
    leaked_spans: Counter = field(default_factory=Counter)

    @property
    def doc_leak_rate(self) -> float:
        return self.docs_leaked / self.docs_with_pii if self.docs_with_pii else 0.0

    def as_dict(self) -> dict:
        total_gold = sum(self.gold_spans.values())
        exact_all = PRF(
            sum(p.tp for p in self.exact.values()),
            sum(p.fp for p in self.exact.values()),
            sum(p.fn for p in self.exact.values()),
        )
        return {
            "docs": self.docs,
            "docs_with_pii": self.docs_with_pii,
            "doc_leak_rate": self.doc_leak_rate,
            "span_leak_rate": sum(self.leaked_spans.values()) / total_gold if total_gold else 0.0,
            "char_any": self.char_any.as_dict(),
            "char": {c: p.as_dict() for c, p in self.char.items() if p.tp + p.fn + p.fp},
            "exact_all": exact_all.as_dict(),
            "exact": {c: p.as_dict() for c, p in self.exact.items() if p.tp + p.fn + p.fp},
            "span_leak_rate_by_category": {
                c: self.leaked_spans[c] / n for c, n in sorted(self.gold_spans.items())
            },
            "gold_spans": dict(sorted(self.gold_spans.items())),
        }


def _char_labels(n: int, spans, gold: bool) -> list[str | None]:
    labels: list[str | None] = [None] * n
    # Scored categories overwrite ignored regions, so overlaps resolve to "scored".
    for s in sorted(spans, key=lambda s: s.category is not None):
        cat = s.category if s.category is not None else (IGNORE if gold else None)
        if cat is None:
            continue
        for i in range(max(0, s.start), min(n, s.end)):
            labels[i] = cat
    return labels


def score(gold_docs: list[Doc], pred_docs: dict[str, Doc]) -> Report:
    r = Report()
    for g in gold_docs:
        p = pred_docs.get(g.id)
        pred_spans = p.spans if p else []
        n = len(g.text)
        alnum = [c.isalnum() for c in g.text]
        gl = _char_labels(n, g.spans, gold=True)
        pl = _char_labels(n, pred_spans, gold=False)
        covered = [False] * n
        for s in pred_spans:
            for i in range(max(0, s.start), min(n, s.end)):
                covered[i] = True

        r.docs += 1
        for i in range(n):
            if not alnum[i] or gl[i] == IGNORE:
                continue
            g_cat, p_cat = gl[i], pl[i]
            if g_cat and covered[i]:
                r.char_any.tp += 1
            elif g_cat:
                r.char_any.fn += 1
            elif p_cat:
                r.char_any.fp += 1
            if g_cat and g_cat == p_cat:
                r.char[g_cat].tp += 1
            else:
                if g_cat:
                    r.char[g_cat].fn += 1
                if p_cat:
                    r.char[p_cat].fp += 1

        scored_gold = [s for s in g.spans if s.category is not None]
        gold_keys = {(s.start, s.end, s.category) for s in scored_gold}
        for s in pred_spans:
            if s.category is None:
                continue
            if (s.start, s.end, s.category) in gold_keys:
                r.exact[s.category].tp += 1
            elif not all(gl[i] == IGNORE or not alnum[i] for i in range(s.start, min(n, s.end))):
                r.exact[s.category].fp += 1
        pred_keys = {(s.start, s.end, s.category) for s in pred_spans}
        for s in scored_gold:
            if (s.start, s.end, s.category) not in pred_keys:
                r.exact[s.category].fn += 1

        leaked = False
        for s in scored_gold:
            r.gold_spans[s.category] += 1
            if any(alnum[i] and not covered[i] for i in range(s.start, s.end)):
                r.leaked_spans[s.category] += 1
                leaked = True
        if scored_gold:
            r.docs_with_pii += 1
            r.docs_leaked += leaked
    return r
