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
    return Doc(id=primary.id, text="", spans=merged, meta={"detector": "combined"})


GROUPS = {
    "Māori": (lx.MAORI_GIVEN, lx.MAORI_SURNAME),
    "Pākehā": (lx.PAKEHA_GIVEN, lx.PAKEHA_SURNAME),
    "Pasifika": (lx.PASIFIKA_GIVEN, lx.PASIFIKA_SURNAME),
    "Asian NZ": (lx.ASIAN_GIVEN, lx.ASIAN_SURNAME),
}


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
