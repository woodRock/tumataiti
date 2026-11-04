//! Review layer for model spans (SPEC §6.1, §9.8). A PERSON span that is only
//! a kinship word ("Koro", "Nan") drops below the policy threshold, so a
//! person decides rather than it being redacted: on its own it is usually not
//! identifying, but it can be someone's name. A kinship word in front of a
//! name stays in the span, so the "Nan" of "Nan Li" is never left exposed.
//!
//! IDs are not reviewed: flagging unlabelled IRD-shaped numbers that fail the
//! check digit leaked routing numbers, SSNs and passports of the same shape.
//! Python port: ml/src/tumataiti_ml/review.py; keep the two in step.

use crate::rules::WEAK;
use crate::span::{Category, Source, Span};

/// Lowercase, without macrons.
const KINSHIP_WORDS: [&str; 24] = [
    "koro", "koroua", "kuia", "nan", "nana", "nanna", "nanny", "taua", "poua", "aunty", "auntie", "uncle",
    "matua", "whaea", "mama", "papa", "mum", "mom", "dad", "grandma", "grandpa", "grandad", "granny",
    "kaumatua",
];

const KINSHIP_NOTE: &str = "A family word like Koro or Nan; flagged in case it is someone's name";

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

/// Flag model spans that are probably not PII: lower their confidence below
/// the default threshold and say why. Rule spans are left alone.
pub fn review(spans: &mut [Span]) {
    for s in spans.iter_mut().filter(|s| s.source == Source::Model) {
        if s.category == Category::Person && is_kinship(&s.text) {
            s.confidence = s.confidence.min(WEAK);
            s.note = Some(KINSHIP_NOTE.to_string());
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
    fn only_model_person_spans_are_reviewed() {
        let mut spans = [model("Nan", Category::Address), model("Koro", Category::Person)];
        spans[1].source = Source::Rule;
        review(&mut spans);
        assert!(spans.iter().all(|s| s.confidence == 0.99));
    }
}
