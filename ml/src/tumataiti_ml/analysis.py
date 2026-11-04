"""Extra analyses: combining detectors, and name leakage by community (SPEC §9.3)."""

from __future__ import annotations

from collections import Counter

from .spans import Doc, Span
from .synth import lexicon as lx


def combine(primary: Doc, secondary: Doc) -> Doc:
    """Merge two detectors' spans the way the Rust merge does.

    Overlapping spans form one cluster, which becomes a single span covering
    all of them (so no overlapping text is left exposed), labelled by the best
    span: a primary (rules) span if there is one, otherwise the widest.
    """
    tagged = [(s, 1) for s in primary.spans] + [(s, 0) for s in secondary.spans]
    tagged.sort(key=lambda t: (t[0].start, -t[0].end))
    merged, cluster, end = [], [], 0

    def flush() -> None:
        best, _ = max(cluster, key=lambda t: (t[1], t[0].end - t[0].start))
        start = min(s.start for s, _ in cluster)
        stop = max(s.end for s, _ in cluster)
        merged.append(Span(start, stop, best.label, best.category, best.confidence))
        cluster.clear()

    for s, is_primary in tagged:
        if cluster and s.start >= end:
            flush()
        end = s.end if not cluster else max(end, s.end)
        cluster.append((s, is_primary))
    if cluster:
        flush()
    meta = {"detector": "combined"}
    if "flagged" in secondary.meta:  # spans the review layer held back (review.py)
        meta["flagged"] = secondary.meta["flagged"]
    return Doc(id=primary.id, text="", spans=merged, meta=meta)


GROUPS = {g: (lx.all_names(g, "given"), lx.all_names(g, "surname")) for g in lx.NAMES}


def name_group(text: str) -> str | None:
    """Community of the leading name in a synthetic PERSON span (given name first)."""
    folded = lx.strip_macrons(text)
    for which in (0, 1):  # given names, then surnames for surname-only spans
        best = None
        for group, lists in GROUPS.items():
            for name in lists[which]:
                n = lx.strip_macrons(name)
                if (folded == n or folded.startswith(n + " ")) and (best is None or len(n) > best[1]):
                    best = (group, len(n))
        if best:
            return best[0]
    return None


def person_leak_by_group(gold: list[Doc], preds: dict[str, Doc]) -> dict[str, tuple[int, int]]:
    """{group: (leaked, total)} over synthetic PERSON spans."""
    total, leaked = Counter(), Counter()
    for g in gold:
        p = preds.get(g.id)
        covered = set()
        for s in p.spans if p else []:
            covered.update(range(s.start, s.end))
        for s in g.spans:
            if s.category != "PERSON":
                continue
            group = name_group(g.text[s.start : s.end])
            if group is None:
                continue
            total[group] += 1
            if any(g.text[i].isalnum() and i not in covered for i in range(s.start, s.end)):
                leaked[group] += 1
    return {k: (leaked[k], total[k]) for k in GROUPS if total[k]}


def _covers(text: str, a: int, b: int, spans: list[tuple[int, int]]) -> bool:
    """True if any letter or digit in text[a:b] is inside one of `spans`."""
    return any(text[i].isalnum() and any(x <= i < y for x, y in spans) for i in range(a, b))


def false_alarms(gold: list[Doc], preds: dict[str, Doc]) -> dict[str, dict[str, float]]:
    """For the false-alarm set: per unlabelled slot type (meta["negatives"]),
    the share redacted and the share flagged for review instead; and per gold
    slot type the share leaked (no part left visible counts as caught).
    Flagged spans come from review.review (meta["flagged"])."""
    neg: dict[str, Counter] = {}
    pos: dict[str, Counter] = {}
    for g in gold:
        p = preds.get(g.id)
        spans = [(s.start, s.end) for s in p.spans] if p else []
        flagged = [(a, b) for a, b, *_ in p.meta.get("flagged", [])] if p else []
        for a, b, slot in g.meta.get("negatives", []):
            c = neg.setdefault(slot, Counter())
            c["n"] += 1
            if _covers(g.text, a, b, spans):
                c["redacted"] += 1
            elif _covers(g.text, a, b, flagged):
                c["flagged"] += 1
        for s in g.spans:
            slot = s.label.split(":", 1)[1].split(".")[-1]  # "PERSON:p1.given" → "given"
            c = pos.setdefault(slot, Counter())
            c["n"] += 1
            if any(g.text[i].isalnum() and not any(x <= i < y for x, y in spans) for i in range(s.start, s.end)):
                c["leaked"] += 1
    out = {f"not PII: {k}": {"n": c["n"], "redacted": c["redacted"] / c["n"], "flagged": c["flagged"] / c["n"]}
           for k, c in sorted(neg.items())}
    out |= {f"PII: {k}": {"n": c["n"], "leaked": c["leaked"] / c["n"]} for k, c in sorted(pos.items())}
    return out
