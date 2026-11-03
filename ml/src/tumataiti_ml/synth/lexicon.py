"""Word lists for synthetic NZ documents.

Names are common given names and surnames drawn from Māori, Pākehā, Pasifika
and Asian New Zealand communities. Combinations are random, so no generated
person is meant to be real. Email domains use the reserved `example` names.
"""

MAORI_GIVEN = [
    "Aroha", "Hēmi", "Mere", "Tama", "Rangi", "Wiremu", "Hōhepa", "Mereana", "Rāwiri",
    "Ngaio", "Tamati", "Kiri", "Manaia", "Nīkau", "Anahera", "Hine", "Tāne", "Ihaia",
    "Moana", "Te Ao", "Ngāpaki", "Whetū", "Āperahama", "Rīpeka", "Pita", "Mānaia",
    "Kahurangi", "Tūī", "Hōani", "Riria", "Kōwhai", "Ataahua", "Tamatea", "Paora",
]
PAKEHA_GIVEN = [
    "Sarah", "James", "Olivia", "Jack", "Charlotte", "Liam", "Emma", "Oliver",
    "Isla", "Noah", "Amelia", "Thomas", "Grace", "Lucas", "Ruby", "Samuel",
]
PASIFIKA_GIVEN = ["Sione", "Losa", "Mele", "Tavita", "Malia", "Ioane", "Salote", "Sefa", "Viliami", "Ana"]
ASIAN_GIVEN = ["Wei", "Priya", "Arjun", "Mei", "Hiroshi", "Ji-woo", "Anika", "Minh"]

MAORI_SURNAME = [
    "Ngata", "Parata", "Henare", "Tipene", "Te Whata", "Paewai", "Tāwhai", "Herewini",
    "Kereama", "Wihongi", "Rāwiri", "Te Rangi", "Kingi", "Mātene", "Pōmare", "Hōhaia",
    "Te Huia", "Waititi", "Whaanga",
]
PAKEHA_SURNAME = ["Smith", "Wilson", "Brown", "Taylor", "Williams", "Anderson", "Thompson", "Walker", "Campbell"]
PASIFIKA_SURNAME = ["Fonoti", "Tuilagi", "Taufa", "Fifita", "Leota", "Faleolo", "Vaifale", "Mataele"]
ASIAN_SURNAME = ["Chen", "Patel", "Singh", "Kim", "Nguyen", "Wong", "Tanaka"]

GIVEN = MAORI_GIVEN * 2 + PAKEHA_GIVEN + PASIFIKA_GIVEN + ASIAN_GIVEN
SURNAME = MAORI_SURNAME * 2 + PAKEHA_SURNAME + PASIFIKA_SURNAME + ASIAN_SURNAME

STREET_NAMES = [
    "Kōwhai", "Rimu", "Pōhutukawa", "Tōtara", "Mānuka", "Kauri", "Tūī", "Kererū",
    "Harakeke", "Whero", "Te Rauparaha", "Matai", "Ngaio", "Karaka", "Puriri", "Hinau",
]
STREET_TYPES = ["Street", "St", "Road", "Rd", "Avenue", "Ave", "Crescent", "Place", "Terrace", "Lane"]

# (town, postcode) pairs; postcodes are plausible, not authoritative.
TOWNS = [
    ("Ōtaki", "5512"), ("Whanganui", "4500"), ("Porirua", "5022"), ("Rotorua", "3010"),
    ("Ngāruawāhia", "3720"), ("Te Awamutu", "3800"), ("Whangārei", "0110"), ("Taupō", "3330"),
    ("Kaikōura", "7300"), ("Ōpōtiki", "3122"), ("Gisborne", "4010"), ("Kaitāia", "0410"),
    ("Hamilton", "3204"), ("Lower Hutt", "5010"), ("Ōtautahi Christchurch", "8011"),
    ("Tauranga", "3110"), ("Napier", "4110"), ("Wellington", "6011"), ("Auckland", "1010"),
]

EMAIL_DOMAINS = ["example.co.nz", "example.nz", "example.org.nz", "example.ac.nz", "example.com", "example.net"]

IWI = ["Ngāti Porou", "Ngāpuhi", "Ngāi Tahu", "Tūhoe", "Ngāti Raukawa", "Te Āti Awa", "Waikato-Tainui", "Ngāti Kahungunu"]
MARAE = ["Rāukawa Marae", "Te Pou o Tainui Marae", "Hīona Marae", "Tukorehe Marae", "Ngātokowaru Marae"]

MONTHS_EN = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
MONTHS_MI = [
    "Kohitātea", "Huitanguru", "Poutūterangi", "Paengawhāwhā", "Haratua", "Pipiri",
    "Hōngongoi", "Here-turi-kōkā", "Mahuru", "Whiringa-ā-nuku", "Whiringa-ā-rangi", "Hakihea",
]

PUBLIC_URLS = [
    "https://www.health.govt.nz",
    "https://www.ird.govt.nz/income-tax",
    "https://www.wgtn.ac.nz",
    "https://www.tpk.govt.nz/mi",
    "https://www.legislation.govt.nz",
]

MACRONS = str.maketrans("āēīōūĀĒĪŌŪ", "aeiouAEIOU")


def strip_macrons(s: str) -> str:
    return s.translate(MACRONS)
