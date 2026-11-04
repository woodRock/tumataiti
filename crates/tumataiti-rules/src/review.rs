//! Review layer for model spans (SPEC §6.1, §9.8).
//!
//! - A PERSON span that is only a kinship word ("Koro", "Nan") drops below the
//!   policy threshold, so a person decides rather than it being redacted: on
//!   its own it is usually not identifying, but it can be someone's name. A
//!   kinship word in front of a name stays in the span, so the "Nan" of
//!   "Nan Li" is never left exposed.
//! - A model ID is checked: a valid IRD number or NHI stays an NZ government
//!   ID, a valid card number becomes financial, and anything else becomes
//!   [`Category::OtherId`], still redacted but no longer called a government
//!   ID. The shape of a number is not evidence that it is not PII: routing
//!   numbers, SSNs and passports share the IRD shape.
//!
//! Python port (kinship only; its evaluation categories merge the IDs):
//! ml/src/tumataiti_ml/review.py. Keep the two in step.

use crate::checksum;
use crate::rules::WEAK;
use crate::span::{Category, Checksum, Source, Span};

/// Lowercase, without macrons.
const KINSHIP_WORDS: [&str; 24] = [
    "koro", "koroua", "kuia", "nan", "nana", "nanna", "nanny", "taua", "poua", "aunty", "auntie", "uncle",
    "matua", "whaea", "mama", "papa", "mum", "mom", "dad", "grandma", "grandpa", "grandad", "granny",
    "kaumatua",
];

const KINSHIP_NOTE: &str = "A family word like Koro or Nan; flagged in case it is someone's name";
const OTHER_ID_NOTE: &str =
    "Looks like an ID to the model, but not a valid IRD number, NHI or card number; redacted in case it is another kind of ID";

/// The category a model ID's check digits support, or None if none passes.
fn verified(text: &str) -> Option<Category> {
    let numeric = text.chars().all(|c| c.is_ascii_digit() || c == '-' || c == ' ');
    let digits = text.chars().filter(char::is_ascii_digit).count();
    if (numeric && checksum::ird(text)) || checksum::nhi(text) {
        Some(Category::NzGovId)
    } else if numeric && (13..=19).contains(&digits) && checksum::luhn(text) {
        Some(Category::Financial)
    } else {
        None
    }
}

fn fold(s: &str) -> String {
    s.chars()
        .map(|c| match c {
            'ā' | 'Ā' => 'a',
            'ē' | 'Ē' => 'e',
            'ī' | 'Ī' => 'i',
            'ō' | 'Ō' => 'o',
            'ū' | 'Ū' => 'u',
            c => c,
        })
        .flat_map(char::to_lowercase)
        .collect()
}

fn is_kinship(word: &str) -> bool {
    KINSHIP_WORDS.contains(&fold(word).as_str())
}

/// Review model spans: flag kinship words (confidence below the default
/// threshold, with a note) and label IDs by what their check digits support.
/// Rule spans are left alone.
pub fn review(spans: &mut [Span]) {
    for s in spans.iter_mut().filter(|s| s.source == Source::Model) {
        if s.category == Category::Person && is_kinship(&s.text) {
            s.confidence = s.confidence.min(WEAK);
            s.note = Some(KINSHIP_NOTE.to_string());
        } else if s.category == Category::NzGovId {
            match verified(&s.text) {
                Some(category) => {
                    s.category = category;
                    s.checksum = Checksum::Valid;
                }
                None => {
                    s.category = Category::OtherId;
                    s.note = Some(OTHER_ID_NOTE.to_string());
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::span::Checksum;

    fn model(text: &str, category: Category) -> Span {
        Span {
            start: 0,
            end: text.len(),
            text: text.to_string(),
            category,
            confidence: 0.99,
            source: Source::Model,
            detector: "student".into(),
            checksum: Checksum::None,
            note: None,
        }
    }

    #[test]
    fn kinship_word_alone_is_flagged() {
        for w in ["Koro", "Nan", "TĀUA", "Tāua", "Taua", "Kaumātua", "nanny"] {
            let mut spans = [model(w, Category::Person)];
            review(&mut spans);
            assert!(spans[0].confidence < 0.5, "{w}");
            assert!(spans[0].note.is_some());
        }
    }

    #[test]
    fn names_with_kinship_words_are_kept_whole() {
        for w in ["Nan Li", "Nanny Rīpeka", "Koro Hēmi", "Rangi"] {
            let mut spans = [model(w, Category::Person)];
            review(&mut spans);
            assert_eq!(spans[0].confidence, 0.99, "{w}");
            assert_eq!(spans[0].text, w);
        }
    }

    #[test]
    fn model_ids_are_labelled_by_their_check_digits() {
        for (text, category) in [
            ("49-091-850", Category::NzGovId),
            ("ZZZ0016", Category::NzGovId),
            ("4111 1111 1111 1111", Category::Financial),
            ("49-091-857", Category::OtherId),
            ("123456789", Category::OtherId),
            ("XWA6261", Category::OtherId),
            ("A49091850", Category::OtherId),
        ] {
            let mut spans = [model(text, Category::NzGovId)];
            review(&mut spans);
            assert_eq!(spans[0].category, category, "{text}");
            assert_eq!(spans[0].confidence, 0.99, "{text}: still redacted");
        }
    }

    #[test]
    fn only_model_person_spans_are_reviewed() {
        let mut spans = [model("Nan", Category::Address), model("Koro", Category::Person)];
        spans[1].source = Source::Rule;
        review(&mut spans);
        assert!(spans.iter().all(|s| s.confidence == 0.99));
    }
}
