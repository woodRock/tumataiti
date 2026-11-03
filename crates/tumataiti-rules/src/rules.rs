//! Deterministic detectors. Each one appends candidate spans; [`crate::merge`]
//! resolves overlaps afterwards.

use std::sync::LazyLock;

use regex::Regex;

use crate::checksum;
use crate::span::{Category, Checksum, Source, Span};

/// Confidence for an ID-shaped code with nothing nearby saying what it is.
/// Sits below the default policy threshold so these are flagged, not redacted.
const WEAK: f32 = 0.4;

/// Confidence for a number labelled as an ID ("IRD number: …") whose check
/// digit fails. Most likely a typo of a real ID, which still identifies the
/// person, so it sits above the default threshold and is redacted (recall first).
const LABELLED_INVALID: f32 = 0.7;

fn re(pattern: &str) -> Regex {
    Regex::new(pattern).expect("built-in pattern compiles")
}

fn floor_boundary(text: &str, mut i: usize) -> usize {
    while !text.is_char_boundary(i) {
        i -= 1;
    }
    i
}

/// True if `pattern` matches within `window` bytes before `start`, on the
/// same line, so a label on one line does not leak onto the next.
fn has_context(text: &str, start: usize, window: usize, pattern: &Regex) -> bool {
    let lo = floor_boundary(text, start.saturating_sub(window));
    let lo = text[lo..start].rfind('\n').map_or(lo, |i| lo + i + 1);
    pattern.is_match(&text[lo..start])
}

/// True if the match is not glued to surrounding letters or digits.
fn isolated(text: &str, start: usize, end: usize) -> bool {
    let before = text[..start].chars().next_back();
    let after = text[end..].chars().next();
    !before.is_some_and(|c| c.is_alphanumeric() || c == '+')
        && !after.is_some_and(|c| c.is_alphanumeric())
}

struct Out<'a> {
    text: &'a str,
    spans: Vec<Span>,
}

impl Out<'_> {
    #[allow(clippy::too_many_arguments)]
    fn push(
        &mut self,
        start: usize,
        end: usize,
        category: Category,
        confidence: f32,
        detector: &str,
        checksum: Checksum,
        note: Option<&str>,
    ) {
        self.spans.push(Span {
            start,
            end,
            text: self.text[start..end].to_string(),
            category,
            confidence,
            source: Source::Rule,
            detector: detector.to_string(),
            checksum,
            note: note.map(str::to_string),
        });
    }
}

/// Run every rule over `text`. Spans may overlap; call [`crate::merge`] next.
pub fn candidates(text: &str) -> Vec<Span> {
    let mut out = Out {
        text,
        spans: Vec::new(),
    };
    email(&mut out);
    url(&mut out);
    ip_address(&mut out);
    phone(&mut out);
    ird(&mut out);
    nhi(&mut out);
    passport_or_licence(&mut out);
    payment_card(&mut out);
    bank_account(&mut out);
    date_of_birth(&mut out);
    secrets(&mut out);
    out.spans
}

static EMAIL: LazyLock<Regex> =
    LazyLock::new(|| re(r"(?i)\b[\p{L}\p{N}._%+-]+@[a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z]{2,}\b"));

fn email(out: &mut Out) {
    for m in EMAIL.find_iter(out.text) {
        out.push(m.start(), m.end(), Category::Email, 0.97, "email", Checksum::None, None);
    }
}

static URL: LazyLock<Regex> =
    LazyLock::new(|| re(r#"(?i)\b(?:https?://|www\.)[^\s<>"'()\[\]{}]+"#));

fn url(out: &mut Out) {
    for m in URL.find_iter(out.text) {
        let trimmed = m.as_str().trim_end_matches(['.', ',', ';', ':', '!', '?']);
        let end = m.start() + trimmed.len();
        out.push(m.start(), end, Category::Url, 0.75, "url", Checksum::None, None);
    }
}

static IPV4: LazyLock<Regex> = LazyLock::new(|| re(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"));

fn ip_address(out: &mut Out) {
    for m in IPV4.find_iter(out.text) {
        let octets_ok = m.as_str().split('.').all(|o| o.parse::<u16>().is_ok_and(|n| n <= 255));
        // Skip longer dotted runs such as version numbers `1.2.3.4.5`.
        let rest = &out.text[m.end()..];
        let continues = rest.starts_with('.') && rest[1..].starts_with(|c: char| c.is_ascii_digit());
        if octets_ok && !continues {
            out.push(m.start(), m.end(), Category::IpAddress, 0.9, "ipv4", Checksum::None, None);
        }
    }
}

// Mobile: 02x then 6–8 digits. Landline: area code 3/4/6/7/9 then 7 digits.
// Either may start with +64 instead of the trunk 0, and the area code may be bracketed.
static PHONE: LazyLock<Regex> = LazyLock::new(|| {
    re(r"(?:\+64[ -]?(?:\(0\)[ -]?)?|\(?0)(?:2\d\)?[ -]?\d{3,4}[ -]?\d{3,4}|[34679]\)?[ -]?\d{3}[ -]?\d{4})")
});

fn phone(out: &mut Out) {
    for m in PHONE.find_iter(out.text) {
        if isolated(out.text, m.start(), m.end()) {
            out.push(m.start(), m.end(), Category::Phone, 0.9, "nz_phone", Checksum::None, None);
        }
    }
}

static IRD: LazyLock<Regex> = LazyLock::new(|| re(r"\b\d{2,3}[- ]?\d{3}[- ]?\d{3}\b"));
static IRD_CONTEXT: LazyLock<Regex> =
    LazyLock::new(|| re(r"(?i)\b(?:ird|tax\s*(?:file\s*)?(?:number|no\.?|#)|inland\s+revenue)"));

fn ird(out: &mut Out) {
    for m in IRD.find_iter(out.text) {
        if !isolated(out.text, m.start(), m.end()) {
            continue;
        }
        if checksum::ird(m.as_str()) {
            out.push(m.start(), m.end(), Category::NzGovId, 0.97, "nz_ird", Checksum::Valid, None);
        } else if has_context(out.text, m.start(), 40, &IRD_CONTEXT) {
            out.push(
                m.start(),
                m.end(),
                Category::NzGovId,
                LABELLED_INVALID,
                "nz_ird",
                Checksum::Invalid,
                Some("Labelled as an IRD number but the check digit fails; redacted in case it is a mistyped real number"),
            );
        }
    }
}

static NHI: LazyLock<Regex> = LazyLock::new(|| {
    re(r"\b(?:[A-HJ-NP-Z]{3}\d{4}|[A-HJ-NP-Z]{3}\d{2}[A-HJ-NP-Z]{2})\b")
});
static NHI_CONTEXT: LazyLock<Regex> =
    LazyLock::new(|| re(r"(?i)\bnhi\b|national\s+health\s+index"));

fn nhi(out: &mut Out) {
    for m in NHI.find_iter(out.text) {
        if checksum::nhi(m.as_str()) {
            out.push(m.start(), m.end(), Category::NzGovId, 0.95, "nz_nhi", Checksum::Valid, None);
        } else if has_context(out.text, m.start(), 40, &NHI_CONTEXT) {
            out.push(
                m.start(),
                m.end(),
                Category::NzGovId,
                LABELLED_INVALID,
                "nz_nhi",
                Checksum::Invalid,
                Some("Labelled as an NHI but the check character fails; redacted in case it is a mistyped real NHI"),
            );
        }
    }
}

// NZ passports and driver licences share the two-letters-six-digits shape,
// so context decides which one it is.
static TWO_LETTER_SIX_DIGIT: LazyLock<Regex> = LazyLock::new(|| re(r"\b[A-Z]{2}\d{6}\b"));
static PASSPORT_CONTEXT: LazyLock<Regex> = LazyLock::new(|| re(r"(?i)passport"));
static LICENCE_CONTEXT: LazyLock<Regex> =
    LazyLock::new(|| re(r"(?i)licen[cs]e|\bDL\b|driver"));

fn passport_or_licence(out: &mut Out) {
    for m in TWO_LETTER_SIX_DIGIT.find_iter(out.text) {
        let (s, e) = (m.start(), m.end());
        if has_context(out.text, s, 40, &PASSPORT_CONTEXT) {
            out.push(s, e, Category::NzGovId, 0.9, "nz_passport", Checksum::None, None);
        } else if has_context(out.text, s, 40, &LICENCE_CONTEXT) {
            out.push(s, e, Category::NzGovId, 0.9, "nz_driver_licence", Checksum::None, None);
        } else {
            out.push(
                s,
                e,
                Category::NzGovId,
                WEAK,
                "nz_id_format",
                Checksum::None,
                Some("Same shape as an NZ passport or driver licence number, but nothing nearby says which"),
            );
        }
    }
}

static CARD: LazyLock<Regex> = LazyLock::new(|| re(r"\b(?:\d[ -]?){12,18}\d\b"));
static CARD_CONTEXT: LazyLock<Regex> =
    LazyLock::new(|| re(r"(?i)\b(?:card|visa|mastercard|amex|credit|debit)\b"));

fn payment_card(out: &mut Out) {
    for m in CARD.find_iter(out.text) {
        let digits: String = m.as_str().chars().filter(char::is_ascii_digit).collect();
        let plausible_prefix = digits.starts_with(['2', '3', '4', '5', '6']);
        if !(13..=19).contains(&digits.len()) || !plausible_prefix {
            continue;
        }
        if checksum::luhn(&digits) {
            out.push(m.start(), m.end(), Category::Financial, 0.95, "payment_card", Checksum::Valid, None);
        } else if has_context(out.text, m.start(), 40, &CARD_CONTEXT) {
            out.push(
                m.start(),
                m.end(),
                Category::Financial,
                LABELLED_INVALID,
                "payment_card",
                Checksum::Invalid,
                Some("Labelled as a card number but fails the Luhn check; redacted in case it is a mistyped real card"),
            );
        }
    }
}

// BB-bbbb-AAAAAAA-SS(S): bank, branch, account, suffix. Separators required,
// otherwise any 15–16 digit run would match.
static BANK: LazyLock<Regex> = LazyLock::new(|| re(r"\b\d{2}[- ]\d{4}[- ]\d{7}[- ]\d{2,3}\b"));

fn bank_account(out: &mut Out) {
    for m in BANK.find_iter(out.text) {
        out.push(
            m.start(),
            m.end(),
            Category::Financial,
            0.85,
            "nz_bank_account",
            Checksum::None,
            Some("NZ bank account format; per-bank checksum not verified yet"),
        );
    }
}

static DATE: LazyLock<Regex> = LazyLock::new(|| {
    re(concat!(
        r"(?i)\b(?:",
        r"\d{1,2}[/.-]\d{1,2}[/.-](?:\d{4}|\d{2})",
        r"|\d{4}-\d{2}-\d{2}",
        r"|\d{1,2}(?:st|nd|rd|th)?\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?,?\s+\d{4}",
        r"|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}",
        // Māori month names, with or without macrons.
        r"|\d{1,2}\s+(?:o\s+)?(?:te\s+marama\s+)?(?:kohit[āa]tea|huitanguru|pout[ūu]terangi|paengawh[āa]wh[āa]|haratua|pipiri|h[ōo]ngongoi|here-turi-k[ōo]k[āa]|mahuru|whiringa-[āa]-nuku|whiringa-[āa]-rangi|hakihea)\s+\d{4}",
        r")\b"
    ))
});
static DOB_CONTEXT: LazyLock<Regex> = LazyLock::new(|| {
    re(r"(?i)\b(?:born|d\.?o\.?b\.?|date\s+of\s+birth|birth\s*date|birthday|died|passed\s+away|date\s+of\s+death|whānau\s+mai|i\s+whānau)")
});

/// Dates are only personal when tied to a person's birth or death, so this
/// rule needs context; the model will cover the rest.
fn date_of_birth(out: &mut Out) {
    for m in DATE.find_iter(out.text) {
        if has_context(out.text, m.start(), 48, &DOB_CONTEXT) {
            out.push(m.start(), m.end(), Category::Date, 0.85, "date_of_birth", Checksum::None, None);
        }
    }
}

static SECRET_TOKENS: LazyLock<Vec<(&'static str, Regex)>> = LazyLock::new(|| {
    vec![
        ("anthropic_api_key", re(r"\bsk-ant-[A-Za-z0-9_-]{20,}")),
        ("openai_api_key", re(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}")),
        ("github_token", re(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{22,})")),
        ("aws_access_key", re(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
        ("slack_token", re(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
        ("google_api_key", re(r"\bAIza[0-9A-Za-z_-]{35}")),
        (
            "private_key",
            re(r"-----BEGIN [A-Z ]*PRIVATE KEY-----(?s:.*?)(?:-----END [A-Z ]*PRIVATE KEY-----|\z)"),
        ),
    ]
});
static SECRET_ASSIGNMENT: LazyLock<Regex> = LazyLock::new(|| {
    re(r#"(?i)(?:password|passwd|pwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token)\s*[:=]\s*["']?([^\s"']{6,})"#)
});

fn secrets(out: &mut Out) {
    for (detector, pattern) in SECRET_TOKENS.iter() {
        for m in pattern.find_iter(out.text) {
            // The generic `sk-` pattern also matches Anthropic keys; let the specific one win.
            let confidence = if *detector == "openai_api_key" { 0.98 } else { 0.99 };
            out.push(m.start(), m.end(), Category::Secret, confidence, detector, Checksum::None, None);
        }
    }
    for caps in SECRET_ASSIGNMENT.captures_iter(out.text) {
        let v = caps.get(1).expect("group 1 always participates");
        out.push(v.start(), v.end(), Category::Secret, 0.9, "secret_assignment", Checksum::None, None);
    }
}
