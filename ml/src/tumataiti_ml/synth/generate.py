"""Synthetic NZ / te reo documents with gold PII spans (SPEC §9.1).

Templates contain slots such as `{p1.full}` (person 1's full name) or
`{hui_date}`. Each slot is filled with a generated value, and the gold label
comes from the slot itself, so labels are exact by construction. Slots whose
category is None are hard negatives: text that looks like PII but is not
(a hui date, an order reference shaped like an IRD number, a public website).
"""

from __future__ import annotations

import datetime as dt
import random
import re
from dataclasses import dataclass, field

from ..spans import Doc, Span
from ..taxonomy import TUMATAITI
from . import lexicon as lx
from . import nzids

SLOT = re.compile(r"\{([a-z0-9_]+)(?:\.([a-z_]+))?\}")


def _date(rng: random.Random, lo: int, hi: int) -> dt.date:
    start = dt.date(lo, 1, 1).toordinal()
    return dt.date.fromordinal(rng.randint(start, dt.date(hi, 12, 31).toordinal()))


def format_date(rng: random.Random, d: dt.date) -> str:
    style = rng.randrange(9)
    if style == 0:
        return f"{d.day:02d}/{d.month:02d}/{d.year}"
    if style == 1:
        return f"{d.day}/{d.month}/{d.year}"
    if style == 2:
        return f"{d.day:02d}-{d.month:02d}-{d.year}"
    if style == 3:
        return d.isoformat()
    if style == 4:
        return f"{d.day} {lx.MONTHS_EN[d.month - 1]} {d.year}"
    if style == 5:
        suffix = "th" if 11 <= d.day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(d.day % 10, "th")
        return f"{d.day}{suffix} {lx.MONTHS_EN[d.month - 1]} {d.year}"
    if style == 6:
        return f"{lx.MONTHS_EN[d.month - 1]} {d.day}, {d.year}"
    month = lx.MONTHS_MI[d.month - 1]
    if style == 8:
        month = lx.strip_macrons(month)
    return f"{d.day} o {month} {d.year}"


@dataclass
class NamePool:
    """Which names a split may use: training or held-out lists, optionally one community only."""

    held_out: bool = False
    group: str | None = None

    def draw(self, rng: random.Random, part: str) -> str:
        # Always draw the community, even when it is fixed, so counterfactual
        # files consume the random stream identically and differ only in names.
        groups = list(lx.GROUP_WEIGHTS)
        drawn = rng.choices(groups, weights=[lx.GROUP_WEIGHTS[g] for g in groups])[0]
        names = lx.NAMES[self.group or drawn][part][1 if self.held_out else 0]
        return names[rng.randrange(len(names))]


@dataclass
class Person:
    rng: random.Random
    pool: NamePool = field(default_factory=NamePool)
    values: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.given = self.pool.draw(self.rng, "given")
        self.surname = self.pool.draw(self.rng, "surname")

    def get(self, attr: str) -> str:
        if attr not in self.values:
            self.values[attr] = self._make(attr)
        return self.values[attr]

    def _make(self, attr: str) -> str:
        rng = self.rng
        local = lambda s: lx.strip_macrons(s).lower().replace(" ", "").replace("-", "")  # noqa: E731
        match attr:
            case "given":
                return self.given
            case "surname":
                return self.surname
            case "full":
                return f"{self.given} {self.surname}"
            case "plain":  # typed without macrons, as in a quick text message
                return lx.strip_macrons(self.given)
            case "email":
                style = rng.randrange(3)
                name = (
                    f"{local(self.given)}.{local(self.surname)}"
                    if style == 0
                    else f"{local(self.given)[0]}{local(self.surname)}"
                    if style == 1
                    else f"{local(self.given)}{rng.randint(1, 99)}"
                )
                return f"{name}@{rng.choice(lx.EMAIL_DOMAINS)}"
            case "phone":
                return nzids.gen_phone(rng)
            case "mobile":
                return nzids.gen_phone(rng, mobile=True)
            case "landline":
                return nzids.gen_phone(rng, mobile=False)
            case "dob":
                return format_date(rng, _date(rng, 1938, 2006))
            case "ird":
                return nzids.gen_ird(rng)
            case "nhi":
                return nzids.gen_nhi(rng, new_format=rng.random() < 0.3)
            case "passport":
                return nzids.gen_passport(rng)
            case "licence":
                return nzids.gen_licence(rng)
            case "card":
                return nzids.gen_card(rng)
            case "bank":
                return nzids.gen_bank(rng)
            case "address":
                town, postcode = rng.choice(lx.TOWNS)
                street = f"{rng.randint(1, 240)} {rng.choice(lx.STREET_NAMES)} {rng.choice(lx.STREET_TYPES)}"
                return f"{street}, {town} {postcode}" if rng.random() < 0.7 else f"{street}, {town}"
            case "url":
                return f"https://{rng.choice(lx.EMAIL_DOMAINS)}/people/{local(self.given)}-{local(self.surname)}"
            case "iwi":
                return rng.choice(lx.IWI)
            case "marae":
                return rng.choice(lx.MARAE)
        raise KeyError(attr)


PERSON_CATEGORY = {
    "given": "PERSON", "surname": "PERSON", "full": "PERSON", "plain": "PERSON",
    "email": "EMAIL", "phone": "PHONE", "mobile": "PHONE", "landline": "PHONE",
    "dob": "DATE", "ird": "NZ_GOV_ID", "nhi": "NZ_GOV_ID", "passport": "NZ_GOV_ID",
    "licence": "NZ_GOV_ID", "card": "FINANCIAL", "bank": "FINANCIAL", "address": "ADDRESS",
    "url": "URL", "iwi": "AFFILIATION", "marae": "AFFILIATION",
}


def global_slot(rng: random.Random, name: str) -> tuple[str, str | None]:
    """Slots not tied to a person: (value, Tūmataiti category or None)."""
    match name:
        case "hui_date":
            return format_date(rng, _date(rng, 2026, 2027)), None
        case "death_date":
            return format_date(rng, _date(rng, 2020, 2026)), "DATE"
        case "order_ref":
            return nzids.gen_ird(rng, valid=False), None
        case "invoice":
            return f"INV-{rng.randint(10000, 99999)}", None
        case "public_url":
            return rng.choice(lx.PUBLIC_URLS), None
        case "ip":
            return nzids.gen_ipv4(rng), "IP_ADDRESS"
        case "secret":
            return nzids.gen_secret(rng)[0], "SECRET"
        case "bad_ird":
            return nzids.gen_ird(rng, valid=False), "NZ_GOV_ID"
        case "bad_nhi":
            return nzids.gen_nhi(rng, valid=False), "NZ_GOV_ID"
        case "bad_card":
            return nzids.gen_card(rng, valid=False), "FINANCIAL"
        case "town":
            return rng.choice(lx.TOWNS)[0], None
        case "filler":
            return rng.choice(lx.FILLERS), None
    raise KeyError(name)


# Training templates. Held-out templates (different genres and phrasing) follow.
TRAIN_TEMPLATES: dict[str, str] = {
    "hui_notes": """Hui ā-whānau: notes
Present: {p1.given}, {p2.given}, {p3.given} ({p3.given} joined online from {ip})

{p1.given} (DOB {p1.dob}) will collect the kai. Contact {p1.given} on {p1.mobile} or {p1.email}.
Next hui: {hui_date} at {p2.marae}. {filler}""",
    "signature": """Ngā mihi,
{p1.full}
Kaiwhakahaere Rangahau | Research Manager
P: {p1.landline} | M: {p1.mobile}
E: {p1.email}
W: {p1.url}""",
    "referral": """Tēnā koe Dr {p2.surname},

Referral for {p1.full}, date of birth {p1.dob}, NHI {p1.nhi}.
Address: {p1.address}
Phone: {p1.phone}
Whānau contact: {p3.full} ({p3.mobile}).

More information: {public_url}""",
    "form": """Ingoa / Name: {p1.full}
Rā whānau / Date of birth: {p1.dob}
Wāhi noho / Address: {p1.address}
IRD number: {p1.ird}
Bank account: {p1.bank}
Īmēra / Email: {p1.email}""",
    "interview": """Interviewer: Kia ora, can you tell me a bit about yourself?
Participant ({p1.given}): Ko {p1.iwi} te iwi. I grew up with my nan, {p2.full}, at {p2.address}.
Interviewer: And can we follow up later?
Participant ({p1.given}): Yeah, text me on {p1.mobile}. My email's {p1.email}. {filler}""",
    "contact_list": """Whānau contact list (updated {hui_date})
- {p1.full}: {p1.phone}, {p1.email}
- {p2.full}: {p2.phone}
- {p3.full}: {p3.email}, {p3.address}""",
    "payment": """Koha for the wānanga can be paid into {p1.bank} (account name {p1.full}).
Or by card: {p1.card}. Please quote {invoice}.
Card on file for {p2.given}: {bad_card}""",
    "travel": """Booking for the conference:
Traveller: {p1.full}
Passport: {p1.passport}
Driver licence (for the rental car): {p1.licence}
Booking code: {order_ref}""",
    "it_support": """Hi, the portal keeps logging me out. I'm {p1.full}, connecting from {ip}.
Here's my config in case it helps:
API_KEY={secret}
Reply to {p1.email}. Ticket {invoice}.""",
    "scholarship": """Scholarship application: {p1.full}
Born: {p1.dob}
Iwi: {p1.iwi}
Postal address: {p1.address}
Referee: {p2.full}, {p2.email}, {p2.phone}
See {public_url} for the criteria.""",
    "agenda": """Rārangi take / Agenda
Date: {hui_date}
Venue: {town} Community Hall
1. Karakia
2. Apologies
3. Budget (order {order_ref}, invoice {invoice})
Organiser: {p1.email}
Details: {public_url}""",
    "tangihanga": """With great sadness we announce that {p1.full} passed away on {death_date}.
I whānau mai ia i te {p1.dob}. Lying at {p1.marae}.
Please contact {p2.full} on {p2.phone} for details.""",
    "text_message": """kia ora its {p1.plain} lol, txt me on {p1.mobile} when ur at {p2.plain}'s place. {p2.address} {filler}""",
    "tax_query": """Kia ora, I'm helping {p1.full} with a tax return.
Their IRD number is {p1.ird}. My own IRD number is {bad_ird} (I might have typed it wrong).
Order reference from the IRD letter: {order_ref}.""",
    "clinic_note": """Patient {p1.given} {p1.surname} seen today. NHI: {p1.nhi}.
NHI recorded on the old form: {bad_nhi}.
Next appointment {hui_date}. Contact via {p1.email}.""",
    "te_reo_para": """Ko {p1.full} tōku ingoa. Nō {p1.iwi} ahau. E noho ana au ki {p1.address}.
Ko {p1.mobile} taku waea pūkoro, ko {p1.email} taku īmēra. {filler}""",
}

TEST_TEMPLATES: dict[str, str] = {
    "group_chat": """[{hui_date}] {p1.plain}: kia ora whānau, who's bringing the hāngī stones?
[{hui_date}] {p2.given}: me and {p3.given}. {p3.given} can you flick me ur number again
[{hui_date}] {p3.given}: {p3.mobile} bro
{filler}""",
    "discharge_summary": """DISCHARGE SUMMARY
Patient: {p1.surname}, {p1.given}
NHI: {p1.nhi}    DOB: {p1.dob}
Residential address: {p1.address}
Next of kin: {p2.full} (tamāhine), ph {p2.phone}
GP to follow up. Clinic letter copied to {p3.email}.""",
    "tenancy": """RESIDENTIAL TENANCY AGREEMENT
Landlord: {p1.full}, of {p1.address}
Tenant: {p2.full}
Tenant's contact: {p2.email} / {p2.mobile}
Bond paid from account {p2.bank}. Rent due from {hui_date}.""",
    "cover_letter": """Tēnā koe,

I am writing to apply for the kaiāwhina role advertised on {public_url}. I whakapapa to {p1.iwi} and have worked at {p1.marae} for six years.

You can reach me at {p1.email} or {p1.phone}. My referee is {p2.full}.

Nāku noa,
{p1.full}""",
    "school_newsletter": """Pānui o te Kura
Ka mau te wehi to {p1.full} and {p2.given} {p2.surname} for their kapa haka performance! {filler}
Questions about the trip? Contact Whaea {p3.given} on {p3.landline}.
Permission slips are due {hui_date}.""",
    "tribunal_summary": """The applicant, {p1.full} (born {p1.dob}), resides at {p1.address}. The applicant's IRD number is recorded as {p1.ird}. Evidence was given by {p2.full} and by Ms {p3.surname}. The hearing resumed on {hui_date}.""",
    "voice_transcript": """um yeah so this is {p1.plain} calling about my nan {p2.plain} she lives at {p2.address} you can call me back on {p1.mobile} thanks""",
}


def fill(template: str, rng: random.Random, pool: NamePool | None = None) -> tuple[str, list[Span]]:
    pool = pool or NamePool()
    people: dict[str, Person] = {}
    out: list[str] = []
    spans: list[Span] = []
    pos = 0
    cursor = 0
    for m in SLOT.finditer(template):
        literal = template[cursor : m.start()]
        out.append(literal)
        pos += len(literal)
        name, attr = m.group(1), m.group(2)
        if attr is not None:
            if name not in people:
                people[name] = Person(rng, pool)
            person = people[name]
            value, category = person.get(attr), PERSON_CATEGORY[attr]
            label = f"{name}.{attr}"
        else:
            value, category = global_slot(rng, name)
            label = name
        out.append(value)
        if category is not None:
            spans.append(Span(pos, pos + len(value), f"{category}:{label}", TUMATAITI[category]))
        pos += len(value)
        cursor = m.end()
    out.append(template[cursor:])
    return "".join(out), spans


SPLITS = {
    # name: (templates, held-out names)
    "train": (TRAIN_TEMPLATES, False),
    "dev": (TRAIN_TEMPLATES, False),
    "test_names": (TRAIN_TEMPLATES, True),
    "test_full": (TEST_TEMPLATES, True),
}


def generate(n: int, seed: int = 0, split: str = "train", group: str | None = None) -> list[Doc]:
    """`n` documents cycling through the split's templates. With `group`, every
    person comes from that community (the counterfactual name audit)."""
    templates, held_out = SPLITS[split]
    pool = NamePool(held_out=held_out, group=group)
    rng = random.Random(seed)
    names = sorted(templates)
    prefix = f"nz-{split}" + (f"-{group}" if group else "")
    docs = []
    for i in range(n):
        name = names[i % len(names)]
        text, spans = fill(templates[name], rng, pool)
        meta = {"template": name, "split": split, "group": group}
        docs.append(Doc(id=f"{prefix}-{i:05d}", text=text, spans=spans, meta=meta))
    return docs
