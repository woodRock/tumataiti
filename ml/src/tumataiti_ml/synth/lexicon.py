"""Word lists for synthetic NZ documents.

Names are common given names and surnames drawn from Māori, Pākehā, Pasifika
and Asian New Zealand communities. Combinations are random, so no generated
person is meant to be real. Email domains use the reserved `example` names.
"""

# Each community's names are split into training and held-out lists, so test
# documents use names the student never saw (SPEC §9.1). Held-out Māori names
# include several that are also everyday words (Tūī, Whetū, Kōwhai, Nīkau).
NAMES = {
    "Māori": {
        "given": (
            ["Aroha", "Hēmi", "Mere", "Tama", "Rangi", "Wiremu", "Hōhepa", "Mereana", "Rāwiri", "Ngaio",
             "Tamati", "Kiri", "Manaia", "Anahera", "Hine", "Tāne", "Ihaia", "Moana", "Te Ao", "Ngāpaki",
             "Āperahama", "Rīpeka", "Pita", "Kahurangi", "Hōani", "Riria", "Ataahua", "Tamatea", "Paora",
             "Huia", "Mihi", "Rewi", "Hūhana", "Matiu", "Ngaire"],
            ["Tūī", "Whetū", "Kōwhai", "Nīkau", "Te Rina", "Wairere", "Mātai", "Rongo", "Āwhina", "Pōtiki",
             "Tūmanako", "Ngāhuia", "Te Waimarie"],
        ),
        "surname": (
            ["Ngata", "Parata", "Henare", "Tipene", "Te Whata", "Paewai", "Tāwhai", "Herewini", "Kereama",
             "Wihongi", "Rāwiri", "Te Rangi", "Kingi", "Mātene", "Pōmare"],
            ["Hōhaia", "Te Huia", "Waititi", "Whaanga", "Te Kanawa", "Tamihana", "Rangihuna", "Takerei"],
        ),
    },
    "Pākehā": {
        "given": (
            ["Sarah", "James", "Olivia", "Jack", "Charlotte", "Liam", "Emma", "Oliver", "Isla", "Noah",
             "Amelia", "Thomas", "William", "Sophie", "Henry", "Ella", "George", "Mia", "Jacob", "Zoe",
             "Ben", "Lucy", "Max", "Hannah", "Ethan", "Chloe", "Daniel", "Kate"],
            ["Grace", "Lucas", "Ruby", "Samuel", "Harper", "Hugo", "Georgia", "Finn"],
        ),
        "surname": (
            # v2 adds surnames that are also English words (Baker, Hunter, Young), the
            # case v1 students missed most.
            ["Smith", "Wilson", "Brown", "Taylor", "Williams", "Anderson", "Baker", "Fisher", "Hunter",
             "Wood", "Young", "King", "Bell", "Hill", "Green", "White", "Cook", "Mason", "Shepherd",
             "Marshall", "Stewart", "Hall", "Turner", "Wright", "Bishop", "Fox", "Stone", "Brooks"],
            ["Thompson", "Walker", "Campbell", "Robinson", "Clarke", "Mitchell"],
        ),
    },
    "Pasifika": {
        "given": (
            ["Sione", "Losa", "Mele", "Tavita", "Malia", "Ioane", "Salote", "Tevita", "Sina", "Paulo",
             "Iosefa", "Semisi", "Lavinia", "Siaosi", "Fetu"],
            ["Sefa", "Viliami", "Ana", "Lupe", "Seini", "Malakai"],
        ),
        "surname": (
            ["Fonoti", "Tuilagi", "Taufa", "Fifita", "Leota", "Aumua", "Seiuli", "Pouono", "Vea", "Kioa",
             "Lolohea", "Fa'alogo", "Lealaiauloto"],
            ["Faleolo", "Vaifale", "Mataele", "Havili", "Tupou"],
        ),
    },
    "Asian NZ": {
        "given": (
            ["Wei", "Priya", "Arjun", "Mei", "Hiroshi", "Jing", "Aditya", "Hana", "Sung-min", "Kavya", "Tao",
             "Rohan", "Kenji"],
            ["Ji-woo", "Anika", "Minh", "Ravi", "Yuki"],
        ),
        "surname": (
            ["Chen", "Patel", "Singh", "Kim", "Zhang", "Liu", "Wang", "Gupta", "Lee", "Park", "Yamamoto",
             "Tran", "Reddy", "Choi"],
            ["Nguyen", "Wong", "Tanaka", "Li", "Sharma"],
        ),
    },
}

# Share of synthetic people from each community. Held-out splits keep the v1
# mix so their files stay identical; v2 training data is balanced.
GROUP_WEIGHTS = {"Māori": 0.5, "Pākehā": 0.2, "Pasifika": 0.15, "Asian NZ": 0.15}
BALANCED_WEIGHTS = {g: 0.25 for g in GROUP_WEIGHTS}


def all_names(group: str, part: str) -> list[str]:
    train, test = NAMES[group][part]
    return train + test


# Te reo sentences in which name-like words are ordinary words (a bird, a tree,
# the sea, "sorry"). They are hard negatives: nothing in them is PII.
FILLERS = [
    "The tūī were singing in the kōwhai this morning.",
    "Kua puāwai ngā kōwhai.",
    "Aroha mai, I'm running a bit late.",
    "He moana pukepuke e ekengia e te waka.",
    "Kia kaha te aroha ki te whānau.",
    "The nīkau palms by the awa came through the storm.",
    "Ka kite au i ngā whetū i te pō.",
    "There's a kererū on the power line again.",
    "We planted harakeke and mānuka along the fence.",
    "Mā te huruhuru ka rere te manu.",
    "Ngā mihi o te rangi ki a koutou.",
    "The huia is extinct, but its feathers are still treasured.",
]

# Closings before a name on its own line. "Nāku noa," is left out: the held-out
# cover letter uses it.
SIGNOFFS = [
    "Ngā mihi,", "Ngā mihi nui,", "Nāku iti nei,", "Mauri ora,", "Noho ora mai,", "Kia pai tō rā,",
    "Kind regards,", "Regards,", "Cheers,", "Thanks,", "Many thanks,", "Best wishes,", "Yours sincerely,",
]

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
