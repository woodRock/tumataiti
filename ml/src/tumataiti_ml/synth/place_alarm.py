"""Place-name false-alarm set: the names a pepeha uses (maunga, awa, moana,
waka, iwi, marae, tupuna) in everyday writing that is not about anyone's
affiliation: weather, tramping, the environment, history, news, sport and
events. A pepeha names them as a person's affiliation, so training labels
every one; here they are unlabelled and recorded in meta["negatives"], so
anything redacted counts as a false alarm (`tumataiti-ml false-alarms`).

Names come from both the training and held-out lists of lexicon.PEPEHA. Some
templates include a person, so leaks are checked too. Kept apart from
generate.py so the v1-v4 splits and the runs that used them are untouched.

    python -m tumataiti_ml.synth.place_alarm --n 1000 --seed 7 --out data/v4/nz_test_place_alarm.jsonl
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from ..spans import Doc, Span, write_jsonl
from ..taxonomy import TUMATAITI
from . import lexicon as lx
from .generate import PERSON_CATEGORY, SLOT, NamePool, Person, global_slot

# The slot is the kind; the negatives record it, so results come per kind.
PLACES = {kind: train + held for kind, (train, held) in lx.PEPEHA.items()
          if kind in ("maunga", "awa", "moana", "waka", "iwi", "marae", "tupuna")}

TEMPLATES: dict[str, str] = {
    "weather": """MetService has issued a heavy rain warning for the ranges around {maunga}. The {awa} River is expected to rise overnight, so check road closures before you travel.""",
    "tramping": """Trip report: we tramped up {maunga} on Saturday, with great views out over {moana}. Next trip is led by {p1.full} ({p1.mobile}).""",
    "environment": """The regional council will test water quality in the {awa} and in {moana} over summer. Results will be posted on the council website.""",
    "history": """According to tradition, the {waka} waka made landfall on the coast after a long voyage. The museum's new exhibition tells the story.""",
    "iwi_news": """{iwi} has signed an agreement with the council to co-manage the {awa}. The agreement will be reviewed in five years.""",
    "school_trip": """Room 12 will visit {marae} on {hui_date} to learn about tikanga. Please return permission slips to {p1.given} {p1.surname} by Friday.""",
    "walk": """{maunga} is a popular day walk. Parking fills up early on weekends, so arrive before 8 am.""",
    "ancestor": """{tupuna} is remembered in many stories as a navigator and leader, and several places carry the name.""",
    "sport": """The {awa} Rowing Club won three medals at the national championships this weekend.""",
    "event": """The regional kapa haka competition will be held at {marae} this year. Tickets are on sale now; contact {p1.email} for group bookings.""",
}

def fill(template: str, rng: random.Random, pool: NamePool, negatives: list) -> tuple[str, list[Span]]:
    """generate.fill, plus unlabelled place slots ({maunga}, {awa}, ...)."""
    people: dict[str, Person] = {}
    out: list[str] = []
    spans: list[Span] = []
    pos = cursor = 0
    for m in SLOT.finditer(template):
        out.append(template[cursor : m.start()])
        pos += m.start() - cursor
        name, attr = m.group(1), m.group(2)
        if attr is not None:
            person = people.setdefault(name, Person(rng, pool))
            value, category, label = person.get(attr), PERSON_CATEGORY[attr], f"{name}.{attr}"
        elif name in PLACES:
            value, category, label = rng.choice(PLACES[name]), None, name
        else:
            (value, category), label = global_slot(rng, name, pool), name
        out.append(value)
        if category is not None:
            spans.append(Span(pos, pos + len(value), f"{category}:{label}", TUMATAITI[category]))
        else:
            negatives.append([pos, pos + len(value), label])
        pos += len(value)
        cursor = m.end()
    out.append(template[cursor:])
    return "".join(out), spans

def generate(n: int, seed: int = 7) -> list[Doc]:
    """`n` documents cycling through the templates, with held-out people."""
    pool = NamePool(held_out=True, weights=lx.GROUP_WEIGHTS, pepeha=True)
    rng = random.Random(seed)
    names = sorted(TEMPLATES)
    docs = []
    for i in range(n):
        name = names[i % len(names)]
        negatives: list = []
        text, spans = fill(TEMPLATES[name], rng, pool, negatives)
        meta = {"template": name, "split": "test_place_alarm", "group": None, "negatives": negatives}
        docs.append(Doc(id=f"nz-test_place_alarm-{i:05d}", text=text, spans=spans, meta=meta))
    return docs

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    print(f"wrote {write_jsonl(a.out, generate(a.n, a.seed))} documents to {a.out}")

if __name__ == "__main__":
    main()
