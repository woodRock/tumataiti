use std::collections::{BTreeMap, HashMap};

use serde::{Deserialize, Serialize};

use crate::policy::{Action, Policy};
use crate::span::{Category, Span};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Finding {
    #[serde(flatten)]
    pub span: Span,
    pub action: Action,
    /// Text that replaces the span in the outbound text; `None` if sent as-is.
    pub replacement: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Redaction {
    /// Sanitised text. Empty when `blocked`, because nothing may be sent.
    pub output: String,
    pub findings: Vec<Finding>,
    pub blocked: bool,
    /// Placeholder → original text, for [`restore`]. Stays on the device.
    pub placeholders: BTreeMap<String, String>,
}

/// Key under which mentions count as the same entity: case, spacing,
/// punctuation and macrons are ignored, so `Hēmi` and `hemi` share a placeholder.
fn entity_key(category: Category, text: &str) -> (Category, String) {
    let folded = text
        .chars()
        .filter(|c| c.is_alphanumeric())
        .flat_map(char::to_lowercase)
        .map(|c| match c {
            'ā' => 'a',
            'ē' => 'e',
            'ī' => 'i',
            'ō' => 'o',
            'ū' => 'u',
            c => c,
        })
        .collect();
    (category, folded)
}

fn generalise(span: &Span) -> String {
    if span.category == Category::Date {
        let year = span
            .text
            .as_bytes()
            .windows(4)
            .position(|w| w.iter().all(u8::is_ascii_digit))
            .map(|i| &span.text[i..i + 4]);
        if let Some(year) = year {
            return format!("[YEAR {year}]");
        }
    }
    format!("[{}]", span.category.label())
}

/// Apply `policy` to already-merged, sorted, non-overlapping spans.
pub fn apply(text: &str, spans: Vec<Span>, policy: &Policy) -> Redaction {
    let mut counters: HashMap<Category, usize> = HashMap::new();
    let mut seen: HashMap<(Category, String), String> = HashMap::new();
    let mut placeholders = BTreeMap::new();
    let mut findings = Vec::with_capacity(spans.len());
    let mut blocked = false;

    for span in spans {
        let action = if span.confidence < policy.threshold {
            Action::Flag
        } else {
            policy.action(span.category)
        };
        let replacement = match action {
            Action::Allow | Action::Flag => None,
            Action::Pseudonymise => {
                let key = entity_key(span.category, &span.text);
                let placeholder = seen.entry(key).or_insert_with(|| {
                    let n = counters.entry(span.category).or_insert(0);
                    *n += 1;
                    format!("[{}_{}]", span.category.label(), n)
                });
                placeholders
                    .entry(placeholder.clone())
                    .or_insert_with(|| span.text.clone());
                Some(placeholder.clone())
            }
            Action::Generalise => Some(generalise(&span)),
            Action::Mask => Some(format!("[{}]", span.category.label())),
            Action::Block => {
                blocked = true;
                Some(format!("[{}]", span.category.label()))
            }
        };
        findings.push(Finding {
            span,
            action,
            replacement,
        });
    }

    let output = if blocked {
        String::new()
    } else {
        let mut out = String::with_capacity(text.len());
        let mut cursor = 0;
        for f in &findings {
            if let Some(r) = &f.replacement {
                out.push_str(&text[cursor..f.span.start]);
                out.push_str(r);
                cursor = f.span.end;
            }
        }
        out.push_str(&text[cursor..]);
        out
    };

    Redaction {
        output,
        findings,
        blocked,
        placeholders,
    }
}

/// Put original values back into a model response. Only placeholders issued
/// for this session are replaced, so a response cannot inject new ones.
pub fn restore(text: &str, placeholders: &BTreeMap<String, String>) -> String {
    let mut out = String::with_capacity(text.len());
    let mut rest = text;
    while let Some(open) = rest.find('[') {
        out.push_str(&rest[..open]);
        let tail = &rest[open..];
        match tail.find(']').map(|close| &tail[..=close]) {
            Some(token) if placeholders.contains_key(token) => {
                out.push_str(&placeholders[token]);
                rest = &tail[token.len()..];
            }
            _ => {
                out.push('[');
                rest = &tail[1..];
            }
        }
    }
    out.push_str(rest);
    out
}
