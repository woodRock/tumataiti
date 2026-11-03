"""Mapping every source taxonomy onto one set of evaluation categories.

Detectors and datasets label things differently: the rules split government
IDs from financial numbers, the OpenAI teacher has a single `account_number`,
and PII-Masking-300k splits names into given and family names. Scoring happens
on the coarse categories below. A source label mapped to None is ignored: it
is neither a miss when undetected nor a false positive when detected.
"""

from __future__ import annotations

EVAL_CATEGORIES = (
    "PERSON",
    "ADDRESS",
    "EMAIL",
    "PHONE",
    "URL",
    "IP_ADDRESS",
    "DATE",
    "ID",
    "SECRET",
)

# Tūmataiti categories (SPEC §6.2), used by the rules and the synthetic NZ data.
TUMATAITI = {
    "PERSON": "PERSON",
    "ADDRESS": "ADDRESS",
    "EMAIL": "EMAIL",
    "PHONE": "PHONE",
    "URL": "URL",
    "IP_ADDRESS": "IP_ADDRESS",
    "DATE": "DATE",
    "NZ_GOV_ID": "ID",
    "FINANCIAL": "ID",
    "SECRET": "SECRET",
    # Not yet scored: no detector covers these, so they are reported separately.
    "AFFILIATION": None,
    "HEALTH": None,
    "CULTURAL_RESTRICTED": None,
}

# openai/privacy-filter span labels (BIOES prefix stripped).
OPENAI_PRIVACY_FILTER = {
    "private_person": "PERSON",
    "private_address": "ADDRESS",
    "private_email": "EMAIL",
    "private_phone": "PHONE",
    "private_url": "URL",
    "private_date": "DATE",
    "account_number": "ID",
    "secret": "SECRET",
}

# ai4privacy/pii-masking-300k labels. Generic dates and times, titles, sex,
# country and state are not personal on their own, so they are ignored.
PII_MASKING_300K = {
    "GIVENNAME1": "PERSON",
    "GIVENNAME2": "PERSON",
    "LASTNAME1": "PERSON",
    "LASTNAME2": "PERSON",
    "LASTNAME3": "PERSON",
    "STREET": "ADDRESS",
    "BUILDING": "ADDRESS",
    "SECADDRESS": "ADDRESS",
    "CITY": "ADDRESS",
    "POSTCODE": "ADDRESS",
    "GEOCOORD": "ADDRESS",
    "EMAIL": "EMAIL",
    "TEL": "PHONE",
    "IP": "IP_ADDRESS",
    "BOD": "DATE",
    "IDCARD": "ID",
    "SOCIALNUMBER": "ID",
    "PASSPORT": "ID",
    "DRIVERLICENSE": "ID",
    "PASS": "SECRET",
    "USERNAME": None,
    "DATE": None,
    "TIME": None,
    "TITLE": None,
    "SEX": None,
    "STATE": None,
    "COUNTRY": None,
    "CARDISSUER": None,
}


def map_label(table: dict[str, str | None], label: str) -> str | None:
    """Look up a label, failing loudly on labels the table does not know."""
    if label not in table:
        raise KeyError(f"unmapped label {label!r}")
    return table[label]
