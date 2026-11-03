use std::cmp::Ordering;

use crate::span::{Checksum, Span};

/// Ranking for overlapping spans: a verified checksum beats everything, then
/// category priority, then the wider span, then confidence.
fn rank(a: &Span, b: &Span) -> Ordering {
    let verified = |s: &Span| s.checksum == Checksum::Valid;
    verified(a)
        .cmp(&verified(b))
        .then(a.category.priority().cmp(&b.category.priority()))
        .then(a.len().cmp(&b.len()))
        .then(a.confidence.total_cmp(&b.confidence))
}

/// Resolve overlapping candidates from rules, model and gazetteers into a
/// non-overlapping list sorted by position. Best-ranked spans are kept first;
/// any span overlapping one already kept is dropped.
pub fn merge(mut candidates: Vec<Span>) -> Vec<Span> {
    candidates.retain(|s| !s.is_empty());
    candidates.sort_by(|a, b| rank(b, a).then(a.start.cmp(&b.start)));

    let mut kept: Vec<Span> = Vec::with_capacity(candidates.len());
    for span in candidates {
        if !kept.iter().any(|k| k.overlaps(&span)) {
            kept.push(span);
        }
    }
    kept.sort_by_key(|s| s.start);
    kept
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::span::{Category, Source};

    fn span(start: usize, end: usize, category: Category, checksum: Checksum) -> Span {
        Span {
            start,
            end,
            text: String::new(),
            category,
            confidence: 0.9,
            source: Source::Rule,
            detector: "test".into(),
            checksum,
            note: None,
        }
    }

    #[test]
    fn verified_checksum_beats_higher_priority() {
        let merged = merge(vec![
            span(0, 10, Category::Secret, Checksum::None),
            span(2, 8, Category::Financial, Checksum::Valid),
        ]);
        assert_eq!(merged.len(), 1);
        assert_eq!(merged[0].category, Category::Financial);
    }

    #[test]
    fn wider_wins_within_category() {
        let merged = merge(vec![
            span(0, 5, Category::Url, Checksum::None),
            span(0, 9, Category::Url, Checksum::None),
        ]);
        assert_eq!((merged[0].start, merged[0].end), (0, 9));
    }

    #[test]
    fn disjoint_spans_are_kept_in_order() {
        let merged = merge(vec![
            span(10, 12, Category::Email, Checksum::None),
            span(0, 3, Category::Phone, Checksum::None),
        ]);
        assert_eq!(merged.iter().map(|s| s.start).collect::<Vec<_>>(), [0, 10]);
    }
}
