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
    weights: dict[str, float] = field(default_factory=lambda: lx.GROUP_WEIGHTS)
    # Data v4: draw affiliations from lexicon.PEPEHA (training or held-out
    # lists, as for names). False keeps the v1-v3 lists, so those splits are unchanged.
    pepeha: bool = False

    def affiliation(self, rng: random.Random, kind: str) -> str:
        if not self.pepeha:  # v1-v3: iwi and marae only, one list for every split
            return rng.choice({"iwi": lx.IWI, "marae": lx.MARAE}[kind])
        return rng.choice(lx.PEPEHA[kind][1 if self.held_out else 0])

    def draw(self, rng: random.Random, part: str) -> str:
        # Always draw the community, even when it is fixed, so counterfactual
        # files consume the random stream identically and differ only in names.
        groups = list(self.weights)
        drawn = rng.choices(groups, weights=[self.weights[g] for g in groups])[0]
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
            case "iwi" | "marae":
                return self.pool.affiliation(rng, attr)
            case "maunga" | "awa" | "moana" | "waka" | "hapu" | "wharenui" | "tupuna":
                if not self.pool.pepeha:
                    raise KeyError(f"{attr} needs a v4 split")
                return self.pool.affiliation(rng, attr)
        raise KeyError(attr)


PERSON_CATEGORY = {
    "given": "PERSON", "surname": "PERSON", "full": "PERSON", "plain": "PERSON",
    "email": "EMAIL", "phone": "PHONE", "mobile": "PHONE", "landline": "PHONE",
    "dob": "DATE", "ird": "NZ_GOV_ID", "nhi": "NZ_GOV_ID", "passport": "NZ_GOV_ID",
    "licence": "NZ_GOV_ID", "card": "FINANCIAL", "bank": "FINANCIAL", "address": "ADDRESS",
    "url": "URL", **{k: "AFFILIATION" for k in lx.PEPEHA},
}


def global_slot(rng: random.Random, name: str, pool: NamePool | None = None) -> tuple[str, str | None]:
    """Slots not tied to a person: (value, Tūmataiti category or None)."""
    match name:
        case "kin":  # a kinship word, from the held-out list in held-out splits
            return rng.choice(lx.KINSHIP[1 if pool and pool.held_out else 0]), None
        case "nan_full":  # a real person whose given name is also a kinship word
            return f"Nan {rng.choice(lx.NAN_SURNAMES)}", "PERSON"
        case "booking_code":  # NHI-shaped, failing the check character
            return nzids.gen_nhi(rng, valid=False), None
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
        case "signoff":
            return rng.choice(lx.SIGNOFFS), None
        case "time":
            return f"{rng.randint(6, 22)}:{rng.randrange(60):02d}", None
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

# Added in data v2 for the M3 failure modes on held-out text: a name alone on
# the last line after a closing, chat speakers and @-mentions, and names in
# formal prose with no field label (bare, or after Mr/Ms/Whaea). Phrasing
# differs from the held-out templates.
V2_TEMPLATES: dict[str, str] = {
    "email_reply": """Kia ora {p2.given},

Thanks for sending the minutes through. I'll bring the koha on the day and can help set up from {time}.

{signoff}
{p1.full}""",
    "short_reply": """Sounds good, see you at the hui on {hui_date}. {filler}

{signoff}
{p1.given}""",
    "chat_log": """{time} {p1.given}: anyone got a trailer for saturday?
{time} {p2.given}: {p3.given} has one I think
{time} {p3.given}: yep all good, @{p1.given} I'll drop it round to {p1.address}
{time} {p1.plain}: legend, cheers {p3.plain}""",
    "chat_export": """{p1.full}: Mōrena whānau! Rehearsal moved to {hui_date}.
{p2.full}: Kei te pai. Can {p3.given} still give us a ride?
{p1.full}: Ask {p3.given} {p3.surname} directly, their number is {p3.mobile}""",
    "hearing_notes": """Ms {p1.surname} told the panel she had lived at the property for four years. Her evidence was supported by {p2.full}, a neighbour. Mr {p3.surname} did not dispute the dates but said the agreement had been made with {p4.full} rather than with him.""",
    "board_minutes": """Minutes of the board meeting, {hui_date}
{p1.full} opened with a karakia. Apologies were received from {p2.given} {p2.surname}.
Moved by {p3.full}, seconded by Whaea {p4.given}, that the accounts be accepted. Carried.
The chair thanked {p2.surname} for the report on the {town} kaupapa.""",
}

# Data v3 (rejected, SPEC §9.8): templates for false alarms seen in the demo,
# kinship words on their own or before a name ("Koro's IRD number", "Nanny
# Rīpeka"), and real people whose given name is a kinship word. Training on
# them made the model skip held-out Māori names that are also words.
V3_TEMPLATES: dict[str, str] = {
    "kin_update": """Kia ora koutou, {kin} is home from the hospital and doing well. {kin} says thanks heaps for the kai. {p1.given} will pop round on {hui_date}. {filler}""",
    "kin_titles": """{kin} {p1.given} will open with a karakia, then {kin} {p2.full} will speak about the whenua. Ring {p3.given} on {p3.mobile} if you need a ride.""",
    "kin_tax": """Helping {kin} with the tax return this week. {kin}'s IRD number is {p1.ird}, and the NHI on the hospital letter is {p1.nhi}.""",
    "named_nan": """{nan_full} chaired the meeting. {kin} {p1.given} sent apologies. Action: {nan_full} to send the notes to {p2.email}.""",
}

# Data v3ids (rejected) adds order and booking codes shaped like IRD numbers and NHIs,
# unlabelled, beside labelled real ones. Kept separate because the open
# English data labels order numbers as customer IDs, and nine-digit routing
# numbers, SSNs and passports share the IRD shape (SPEC §9.8).
V3_ID_TEMPLATES: dict[str, str] = {
    "id_lookalikes": """Helping {kin} with the paperwork. The order reference {order_ref} and booking code {booking_code} are from the travel agent; the IRD number is {p1.ird}.""",
    "order_confirmation": """Order confirmation
Order number: {order_ref}
Booking code: {booking_code}
Customer: {p1.full}
Email: {p1.email}
NHI on the prescription: {p1.nhi}""",
}

# Data v4: pepeha, long and short, in te reo and English, and affiliation in
# the places it appears in everyday writing (signatures, introductions, notes).
# Every place a pepeha names is labelled AFFILIATION.
V4_TEMPLATES: dict[str, str] = {
    "pepeha_long": """Tēnā koutou katoa.
Ko {p1.maunga} te maunga
Ko {p1.awa} te awa
Ko {p1.waka} te waka
Ko {p1.iwi} te iwi
Ko {p1.hapu} te hapū
Ko {p1.marae} te marae
Ko {p1.wharenui} te whare tupuna
Ko {p1.full} tōku ingoa
Nō reira, tēnā koutou, tēnā koutou, tēnā tātou katoa.""",
    "pepeha_moana": """Ko {p1.maunga} te maunga, ko {p1.moana} te moana.
Ko {p1.waka} te waka. Ko {p1.iwi} te iwi. Ko {p1.marae} te marae.
Ko {p1.given} ahau. {filler}""",
    "pepeha_tupuna": """Ko {p1.tupuna} te tupuna.
Ko {p1.iwi} te iwi, ko {p1.hapu} te hapū.
Ko {p1.wharenui} te wharenui, kei {p1.marae}.
Ko {p1.given} {p1.surname} tōku ingoa.""",
    "pepeha_english": """My mountain is {p1.maunga} and my river is {p1.awa}. My waka is {p1.waka}.
I am {p1.iwi}, from the hapū {p1.hapu}, and my marae is {p1.marae}.
My name is {p1.full}, and you can reach me on {p1.mobile}.""",
    "intro_sides": """Kia ora, I'm {p1.given}. I'm {p1.iwi} on my dad's side and {p2.iwi} on my mum's side, and I grew up going back to {p1.marae} for tangihanga. {filler}""",
    "signature_iwi": """Ngā mihi,
{p1.full} ({p1.iwi}, {p1.hapu})
Kaiārahi | Navigator
M: {p1.mobile}""",
    "whakapapa_note": """Interview 7 notes: {p1.given} whakapapa to {p1.iwi} through {p1.hapu} and grew up near {p1.maunga}. Their whānau still gathers at {p1.marae}. Follow up by email: {p1.email}.""",
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


# Data v4 held-out pepeha: different wording, order and genres from V4_TEMPLATES.
V4_TEST_TEMPLATES: dict[str, str] = {
    "pepeha_formal": """Tihei mauri ora!
Ko {p1.maunga} te maunga e tū mai rā, ko {p1.awa} te awa e rere ana.
Ko {p1.waka} te waka, ko {p1.iwi} te iwi, ko {p1.hapu} te hapū.
He uri ahau nō {p1.tupuna}.
Ko {p1.marae} te marae, ko {p1.wharenui} te whare.
Ko {p1.full} ahau.""",
    "pepeha_brief": """Nō {p1.moana} ahau, nō {p1.iwi} hoki. Ko {p1.given} tōku ingoa, ā, kei {town} ahau e noho ana.""",
    "author_bio": """About the author: {p1.full} ({p1.iwi}, {p1.hapu}) grew up beneath {p1.maunga} and now lives in {town}. Contact: {p1.email}.""",
    "consent_form": """KAUPAPA MĀORI RESEARCH CONSENT
Participant: {p1.full}
Iwi affiliation(s): {p1.iwi}; {p2.iwi}
Hapū: {p1.hapu}
Marae: {p1.marae}
Waka: {p1.waka}
Date: {hui_date}""",
}

# Held-out false-alarm set: the same cases as V3_TEMPLATES with different
# wording and the held-out kinship list. Its unlabelled slots are recorded in
# meta["negatives"], so anything redacted there counts as a false alarm.
FALSE_ALARM_TEMPLATES: dict[str, str] = {
    "fa_text": """hey just letting u know {kin} is staying with us this week. {kin} wants to see the mokos before {hui_date}, {p1.plain} can pick them up""",
    "fa_birthday": """Pānui: {kin} {p1.given} turns 80 on {hui_date}! Whānau welcome at the {town} hall. RSVP to {p2.full} on {p2.mobile}.""",
    "fa_ids": """Could you double-check these for {kin}? NHI: {p1.nhi}. IRD number: {p1.ird}. The letter also lists claim number {order_ref} and reference {booking_code}, which I don't think are personal.""",
    "fa_receipt": """TAX INVOICE
Order no. {order_ref}
Ref: {booking_code}
{invoice}
Billed to: {p1.full}, {p1.address}
Thank you for your purchase.""",
    "fa_treasurer": """Welcome to our new treasurer, {nan_full}! The treasurer can be reached at {p1.email}. {kin} {p2.given} will hand over the books.""",
    "fa_appointment": """{kin}'s appointment is on {hui_date}. {kin} needs a ride, so {p1.given} {p1.surname} is driving. Call {p1.landline} to confirm.""",
}


def fill(
    template: str, rng: random.Random, pool: NamePool | None = None, negatives: list | None = None
) -> tuple[str, list[Span]]:
    """Fill a template. Unlabelled slots are appended to `negatives` as
    [start, end, slot] when it is given."""
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
            value, category = global_slot(rng, name, pool)
            label = name
        out.append(value)
        if category is not None:
            spans.append(Span(pos, pos + len(value), f"{category}:{label}", TUMATAITI[category]))
        elif negatives is not None:
            negatives.append([pos, pos + len(value), label])
        pos += len(value)
        cursor = m.end()
    out.append(template[cursor:])
    return "".join(out), spans


SPLITS = {
    # name: (templates, held-out names, community weights)
    # Training data is v2 (balanced names, v2 templates); the v1 training data
    # can be regenerated from commit 5f1b73f. Held-out splits are unchanged
    # from v1, so their files are identical and results stay comparable.
    "train": ({**TRAIN_TEMPLATES, **V2_TEMPLATES}, False, lx.BALANCED_WEIGHTS),
    "dev": ({**TRAIN_TEMPLATES, **V2_TEMPLATES}, False, lx.BALANCED_WEIGHTS),
    "test_names": (TRAIN_TEMPLATES, True, lx.GROUP_WEIGHTS),
    "test_full": (TEST_TEMPLATES, True, lx.GROUP_WEIGHTS),
    # v3 and v3ids were tried and rejected: they leak Māori names that are
    # also words (SPEC §9.8). Kept so the result can be reproduced.
    "train_v3": ({**TRAIN_TEMPLATES, **V2_TEMPLATES, **V3_TEMPLATES}, False, lx.BALANCED_WEIGHTS),
    "dev_v3": ({**TRAIN_TEMPLATES, **V2_TEMPLATES, **V3_TEMPLATES}, False, lx.BALANCED_WEIGHTS),
    "train_v3ids": ({**TRAIN_TEMPLATES, **V2_TEMPLATES, **V3_TEMPLATES, **V3_ID_TEMPLATES}, False, lx.BALANCED_WEIGHTS),
    "dev_v3ids": ({**TRAIN_TEMPLATES, **V2_TEMPLATES, **V3_TEMPLATES, **V3_ID_TEMPLATES}, False, lx.BALANCED_WEIGHTS),
    "test_false_alarm": (FALSE_ALARM_TEMPLATES, True, lx.GROUP_WEIGHTS),
    # v4: pepeha. Training lists for training splits, held-out lists (names and
    # every affiliation) for test splits. Affiliation is scored from v4 on.
    "train_v4": ({**TRAIN_TEMPLATES, **V2_TEMPLATES, **V4_TEMPLATES}, False, lx.BALANCED_WEIGHTS),
    "dev_v4": ({**TRAIN_TEMPLATES, **V2_TEMPLATES, **V4_TEMPLATES}, False, lx.BALANCED_WEIGHTS),
    "test_names_v4": ({**TRAIN_TEMPLATES, **V4_TEMPLATES}, True, lx.GROUP_WEIGHTS),
    "test_full_v4": ({**TEST_TEMPLATES, **V4_TEST_TEMPLATES}, True, lx.GROUP_WEIGHTS),
    # v4 ablations (SPEC §9.8 on v3): v4 plus the kinship and ID-lookalike templates.
    "train_v4kin": ({**TRAIN_TEMPLATES, **V2_TEMPLATES, **V4_TEMPLATES, **V3_TEMPLATES}, False, lx.BALANCED_WEIGHTS),
    "dev_v4kin": ({**TRAIN_TEMPLATES, **V2_TEMPLATES, **V4_TEMPLATES, **V3_TEMPLATES}, False, lx.BALANCED_WEIGHTS),
    "train_v4ids": ({**TRAIN_TEMPLATES, **V2_TEMPLATES, **V4_TEMPLATES, **V3_TEMPLATES, **V3_ID_TEMPLATES}, False,
                    lx.BALANCED_WEIGHTS),
    "dev_v4ids": ({**TRAIN_TEMPLATES, **V2_TEMPLATES, **V4_TEMPLATES, **V3_TEMPLATES, **V3_ID_TEMPLATES}, False,
                  lx.BALANCED_WEIGHTS),
}


def generate(n: int, seed: int = 0, split: str = "train", group: str | None = None) -> list[Doc]:
    """`n` documents cycling through the split's templates. With `group`, every
    person comes from that community (the counterfactual name audit)."""
    templates, held_out, weights = SPLITS[split]
    pool = NamePool(held_out=held_out, group=group, weights=weights, pepeha="v4" in split)
    rng = random.Random(seed)
    names = sorted(templates)
    prefix = f"nz-{split}" + (f"-{group}" if group else "")
    docs = []
    for i in range(n):
        name = names[i % len(names)]
        negatives = [] if split == "test_false_alarm" else None
        text, spans = fill(templates[name], rng, pool, negatives)
        meta = {"template": name, "split": split, "group": group}
        if negatives is not None:
            meta["negatives"] = negatives
        docs.append(Doc(id=f"{prefix}-{i:05d}", text=text, spans=spans, meta=meta))
    return docs
