// All preset content is synthetic. Identifiers are published test values or
// made up; IP addresses are from the documentation range 203.0.113.0/24.

export interface Preset {
  id: string;
  title: string;
  shows: string;
  text: string;
}

export const PRESETS: Preset[] = [
  {
    id: "hui",
    title: "Hui notes",
    shows: "te reo text, a birth date in a Māori month, and a hui date left alone",
    text: `Hui ā-whānau: notes
Present: Hōhepa, Mere, Tama (Tama joined online from 203.0.113.42)

Hōhepa (DOB 14/03/1987) will collect the kai. Contact him on 022 012 3456 or hōhepa.k@example.nz.
I whānau mai a Nanny Rīpeka i te 12 o Hōngongoi 1948.

Next hui: 14/03/2027 at the marae.`,
  },
  {
    id: "pepeha",
    title: "Pepeha",
    shows:
      "a pepeha, long and short: with the name model on, the maunga, awa, waka, iwi, hapū, marae and tupuna are each marked as an affiliation, and the speaker's name as a name",
    text: `Tēnā koutou katoa.

Ko Hikurangi te maunga
Ko Waiapu te awa
Ko Horouta te waka
Ko Ngāti Porou te iwi
Ko Te Whānau-a-Ruataupare te hapū
Ko Ōwae te marae
Ko Porourangi te tupuna
Ko Mereana Tāwhiri tōku ingoa.

Kia ora, I'm Mereana. I'm Ngāti Porou on Mum's side and Ngāi Tahu on Dad's.
Get in touch on 027 012 3456 or mereana.t@example.nz.`,
  },
  {
    id: "checksums",
    title: "Checksums",
    shows: "IRD and NHI check digits: a labelled number that fails is still redacted in case it is a typo. The rules ignore unlabelled look-alikes such as the order reference; the name model sometimes redacts one as another kind of ID, in case it is one",
    text: `Kia ora, I've updated the whānau records.

Koro's IRD number: 49-091-850
Nan's IRD number: 49-091-851 (one digit off)
NHI, old format: ZZZ0016
NHI, new format: ZZZ00AC
NHI, mistyped: ZZZ0017
Order reference: 49-091-857`,
  },
  {
    id: "signature",
    title: "Email signature",
    shows: "phone, email and web link; names wait for the model",
    text: `Ngā mihi,
Aroha Ngata
Kaiwhakahaere Rangahau | Research Manager
P: 04 123 4567 | M: 021 123 4567
E: aroha.ngata@example.ac.nz
W: https://example.ac.nz/people/aroha-ngata`,
  },
  {
    id: "payment",
    title: "Payment details",
    shows: "bank account format and Luhn-checked card numbers",
    text: `Koha for the wānanga can be paid into 12-3140-0123456-00.
Or by card: 4111 1111 1111 1111, expiry 08/28.
Card on file: 4111 1111 1111 1112`,
  },
  {
    id: "travel",
    title: "Travel booking",
    shows: "passport and licence numbers told apart by their labels",
    text: `Booking for the conference in Rarotonga:
Passport: LA123456
Driver licence (for the rental car): DL AB654321
Booking code: XY998877`,
  },
  {
    id: "secret",
    title: "Leaked API key",
    shows: "a secret blocks the whole request",
    text: `Can you help me debug this? My config is:

ANTHROPIC_API_KEY=sk-ant-api03-Xq7vR2mN8pL4tK9wB3cF6hJ1dS5gY0aZ-EXAMPLEONLY
db_password: kumara-hangi-2024`,
  },
];
