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
    "OTHER_ID": "ID",
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


# Labels of the openly licensed sets (datasets/open_pii.py): Nemotron-PII and
# Gretel's two PII sets, which mostly share names. Mapped as for
# PII-Masking-300k: city, postcode and coordinates count as address; only
# birth dates count as DATE; identifiers that point at a person (customer and
# employee numbers, health and licence numbers, plates) count as ID; PINs,
# card security codes and cookies count as SECRET. Companies, jobs, places
# larger than a city, generic dates and times, usernames, and demographic or
# belief attributes are not scored (they train as background).
OPEN_PII = {
    **dict.fromkeys(["first_name", "last_name", "name"], "PERSON"),
    **dict.fromkeys(["street_address", "address", "city", "postcode", "coordinate", "local_latlng"], "ADDRESS"),
    "email": "EMAIL",
    **dict.fromkeys(["phone_number", "fax_number"], "PHONE"),
    "url": "URL",
    **dict.fromkeys(["ipv4", "ipv6"], "IP_ADDRESS"),
    "date_of_birth": "DATE",
    **dict.fromkeys(
        [
            "ssn", "national_id", "tax_id", "passport_number", "driver_license_number",
            "certificate_license_number", "medical_record_number", "health_plan_beneficiary_number",
            "credit_debit_card", "credit_card_number", "account_number", "bank_routing_number", "iban", "bban",
            "customer_id", "employee_id", "unique_id", "unique_identifier", "license_plate", "vehicle_identifier",
        ],
        "ID",
    ),
    **dict.fromkeys(
        ["password", "api_key", "pin", "account_pin", "cvv", "credit_card_security_code", "http_cookie"], "SECRET"
    ),
    **dict.fromkeys(
        [
            "company", "company_name", "occupation", "country", "state", "county", "date", "time", "date_time",
            "user_name", "swift_bic", "swift_bic_code", "mac_address", "device_identifier", "biometric_identifier",
            "education_level", "employment_status", "race_ethnicity", "religious_belief", "political_view",
            "sexuality", "gender", "age", "blood_type", "language",
        ],
        None,
    ),
}


def map_label(table: dict[str, str | None], label: str) -> str | None:
    """Look up a label, failing loudly on labels the table does not know."""
    if label not in table:
        raise KeyError(f"unmapped label {label!r}")
    return table[label]
