use std::cmp::{Ordering, Reverse};

use crate::span::{Checksum, Source, Span};

/// Spans at or above this confidence are redacted under the default policy,
/// so they outrank weaker spans regardless of category.
const STRONG: f32 = 0.5;

/// Ranking for overlapping spans: a verified checksum beats everything, then
/// a confident span beats a weak one, then a rule beats the model (a format
/// match knows the exact category, where the model's single ID label cannot
/// tell a bank account from a passport), then category priority, then the
/// wider span, then confidence.
fn rank(a: &Span, b: &Span) -> Ordering {
    let verified = |s: &Span| s.checksum == Checksum::Valid;
    let strong = |s: &Span| s.confidence >= STRONG;
    let rule = |s: &Span| s.source == Source::Rule;
    verified(a)
        .cmp(&verified(b))
        .then(strong(a).cmp(&strong(b)))
        .then(rule(a).cmp(&rule(b)))
        .then(a.category.priority().cmp(&b.category.priority()))
        .then(a.len().cmp(&b.len()))
        .then(a.confidence.total_cmp(&b.confidence))
}

/// One span for a cluster of overlapping candidates: the best-ranked span's
/// label, stretched over the whole cluster so no overlapping text is left out.
fn resolve(text: &str, cluster: &mut Vec<Span>) -> Span {
    let start = cluster.iter().map(|s| s.start).min().expect("cluster is non-empty");
    let end = cluster.iter().map(|s| s.end).max().expect("cluster is non-empty");
    let mut best = cluster.drain(..).max_by(rank).expect("cluster is non-empty");
    if (best.start, best.end) != (start, end) {
        best.start = start;
        best.end = end;
        best.text = text[start..end].to_string();
    }
    best
}

/// Resolve overlapping candidates from rules, model and gazetteers into a
/// non-overlapping list sorted by position. Overlapping spans merge into one
/// covering all of them (recall first), labelled by the best-ranked span.
pub fn merge(text: &str, mut candidates: Vec<Span>) -> Vec<Span> {
    candidates.retain(|s| !s.is_empty());
    candidates.sort_by_key(|s| (s.start, Reverse(s.end)));

    let mut merged = Vec::with_capacity(candidates.len());
    let mut cluster: Vec<Span> = Vec::new();
    let mut cluster_end = 0;
    for span in candidates {
        if !cluster.is_empty() && span.start >= cluster_end {
            merged.push(resolve(text, &mut cluster));
        }
        cluster_end = if cluster.is_empty() { span.end } else { cluster_end.max(span.end) };
        cluster.push(span);
    }
    if !cluster.is_empty() {
        merged.push(resolve(text, &mut cluster));
    }
    merged
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::span::{Category, Source};

    const TEXT: &str = "0123456789abcdef";

    fn span(start: usize, end: usize, category: Category, checksum: Checksum) -> Span {
        Span {
            start,
            end,
            text: TEXT[start..end].to_string(),
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
        let merged = merge(TEXT, vec![
            span(0, 10, Category::Secret, Checksum::None),
            span(2, 8, Category::Financial, Checksum::Valid),
        ]);
        assert_eq!(merged.len(), 1);
        assert_eq!(merged[0].category, Category::Financial);
        // The winner is stretched over the whole cluster.
        assert_eq!((merged[0].start, merged[0].end, merged[0].text.as_str()), (0, 10, "0123456789"));
    }

    #[test]
    fn confident_span_beats_weak_higher_priority_span() {
        let mut weak = span(0, 8, Category::NzGovId, Checksum::None);
        weak.confidence = 0.4;
        let merged = merge(TEXT, vec![weak, span(0, 12, Category::Phone, Checksum::None)]);
        assert_eq!(merged[0].category, Category::Phone);
    }

    fn model(start: usize, end: usize, category: Category, confidence: f32) -> Span {
        Span { source: Source::Model, detector: "student".into(), confidence, ..span(start, end, category, Checksum::None) }
    }

    #[test]
    fn confident_rule_keeps_its_label_over_the_model() {
        // The model's ID maps to NZ_GOV_ID, which outranks FINANCIAL by priority.
        let mut rule = span(2, 10, Category::Financial, Checksum::None);
        rule.confidence = 0.7;
        let merged = merge(TEXT, vec![model(0, 10, Category::NzGovId, 1.0), rule]);
        assert_eq!(merged.len(), 1);
        assert_eq!((merged[0].category, merged[0].source), (Category::Financial, Source::Rule));
        // Recall first: the model's wider span still sets the extent.
        assert_eq!((merged[0].start, merged[0].end), (0, 10));
    }

    #[test]
    fn confident_model_beats_weak_rule() {
        let mut weak = span(0, 8, Category::NzGovId, Checksum::None);
        weak.confidence = 0.4;
        let merged = merge(TEXT, vec![weak, model(0, 8, Category::Person, 0.9)]);
        assert_eq!((merged[0].category, merged[0].source), (Category::Person, Source::Model));
    }

    #[test]
    fn chained_overlaps_form_one_cluster() {
        let merged = merge(
            TEXT,
            vec![
                span(0, 4, Category::Email, Checksum::None),
                span(3, 8, Category::Url, Checksum::None),
                span(7, 12, Category::Url, Checksum::None),
            ],
        );
        assert_eq!(merged.len(), 1);
        assert_eq!((merged[0].start, merged[0].end), (0, 12));
        assert_eq!(merged[0].category, Category::Email);
    }

    #[test]
    fn wider_wins_within_category() {
        let merged = merge(TEXT, vec![
            span(0, 5, Category::Url, Checksum::None),
            span(0, 9, Category::Url, Checksum::None),
        ]);
        assert_eq!((merged[0].start, merged[0].end), (0, 9));
    }

    #[test]
    fn disjoint_spans_are_kept_in_order() {
        let merged = merge(TEXT, vec![
            span(10, 12, Category::Email, Checksum::None),
            span(0, 3, Category::Phone, Checksum::None),
        ]);
        assert_eq!(merged.iter().map(|s| s.start).collect::<Vec<_>>(), [0, 10]);
    }
}
