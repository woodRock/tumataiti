//! The browser-side half of the student model (SPEC §7, §10.0). It tokenises
//! text into the same overlapping windows as training, and decodes the model's
//! per-token tag probabilities back into spans, exactly as
//! `ml/src/tumataiti_ml/student/encode.py` does. The page only runs the ONNX
//! model in between. Span offsets are UTF-16 code units, so they index
//! JavaScript strings directly.

use serde::Serialize;
use tokenizers::{Tokenizer, TruncationDirection, TruncationParams, TruncationStrategy};
use wasm_bindgen::prelude::*;

/// Identifier field labels, never PII themselves: a span that is exactly one
/// of these is dropped (a stray tag on the "I" of "NHI" would otherwise widen
/// to redact the label). Same list as `FIELD_LABELS` in the Python decoder.
const FIELD_LABELS: [&str; 21] = [
    "NHI", "IRD", "GST", "DOB", "DL", "SSN", "PIN", "CVV", "CVC", "IBAN", "BSB", "TFN", "NZBN", "ACC", "NI", "ID",
    "SIN", "EIN", "ITIN", "MRN", "VIN",
];

/// Window length and overlap in tokens, as in training.
const MAX_LENGTH: usize = 512;
const STRIDE: usize = 128;

#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct ModelSpan {
    /// UTF-16 offsets into the input text.
    pub start: usize,
    pub end: usize,
    /// Student label, e.g. `PERSON` or `ID`.
    pub label: String,
    /// P(not O), the lowest over the span's tokens.
    pub confidence: f32,
}

#[wasm_bindgen]
pub struct Student {
    tokenizer: Tokenizer,
    /// Tag names by id, e.g. `B-PERSON`; id 0 must be `O`.
    tags: Vec<String>,
}

#[wasm_bindgen]
impl Student {
    /// `tokenizer_json` and `config_json` are the exported model's
    /// `tokenizer.json` and `config.json` (for the tag names).
    #[wasm_bindgen(constructor)]
    pub fn new(tokenizer_json: &str, config_json: &str) -> Result<Student, JsError> {
        let mut tokenizer = Tokenizer::from_bytes(tokenizer_json.as_bytes()).map_err(|e| JsError::new(&e.to_string()))?;
        tokenizer
            .with_truncation(Some(TruncationParams {
                max_length: MAX_LENGTH,
                stride: STRIDE,
                strategy: TruncationStrategy::LongestFirst,
                direction: TruncationDirection::Right,
            }))
            .map_err(|e| JsError::new(&e.to_string()))?;
        tokenizer.with_padding(None);
        Ok(Student { tokenizer, tags: tags_from_config(config_json)? })
    }

    /// Number of tags the model predicts per token.
    #[wasm_bindgen(js_name = numTags)]
    pub fn num_tags(&self) -> usize {
        self.tags.len()
    }

    /// Tokenise `text` into overlapping windows.
    pub fn windows(&self, text: &str) -> Result<Windows, JsError> {
        let enc = self.tokenizer.encode(text, true).map_err(|e| JsError::new(&e.to_string()))?;
        let utf16 = utf16_offsets(text);
        let mut ids = Vec::new();
        let mut offsets = Vec::new();
        for e in std::iter::once(&enc).chain(enc.get_overflowing()) {
            ids.push(e.get_ids().iter().map(|&i| i as i64).collect());
            offsets.push(
                e.get_offsets()
                    .iter()
                    .zip(e.get_special_tokens_mask())
                    .map(|(&(a, b), &special)| if special == 1 { (0, 0) } else { (utf16[a], utf16[b]) })
                    .collect(),
            );
        }
        Ok(Windows { text: text.encode_utf16().collect(), ids, offsets, found: Vec::new() })
    }
}

/// One document's windows. Feed each window's logits back with
/// [`Windows::add_logits`], then read the spans with [`Windows::spans`].
#[wasm_bindgen]
pub struct Windows {
    text: Vec<u16>,
    ids: Vec<Vec<i64>>,
    offsets: Vec<Vec<(usize, usize)>>,
    found: Vec<ModelSpan>,
}

#[wasm_bindgen]
impl Windows {
    pub fn count(&self) -> usize {
        self.ids.len()
    }

    /// Token ids of window `i` (a `BigInt64Array` in JavaScript).
    pub fn ids(&self, i: usize) -> Vec<i64> {
        self.ids[i].clone()
    }

    /// Decode window `i` from its logits, `[tokens × tags]` row-major.
    #[wasm_bindgen(js_name = addLogits)]
    pub fn add_logits(&mut self, student: &Student, i: usize, logits: &[f32], threshold: f32) {
        let spans = decode(&self.text, &self.offsets[i], logits, &student.tags, threshold);
        self.found.extend(spans);
    }

    /// Spans from every window so far, overlaps merged, as JSON.
    pub fn spans(&self) -> String {
        serde_json::to_string(&union(self.found.clone())).expect("spans serialise")
    }
}

fn tags_from_config(config_json: &str) -> Result<Vec<String>, JsError> {
    let config: serde_json::Value = serde_json::from_str(config_json)?;
    let id2label = config["id2label"].as_object().ok_or_else(|| JsError::new("config.json has no id2label"))?;
    let mut tags = vec![String::new(); id2label.len()];
    for (id, label) in id2label {
        let i: usize = id.parse()?;
        *tags.get_mut(i).ok_or_else(|| JsError::new("id2label ids are not 0..n"))? =
            label.as_str().unwrap_or_default().to_string();
    }
    if tags.first().map(String::as_str) != Some("O") {
        return Err(JsError::new("tag 0 must be O"));
    }
    Ok(tags)
}

/// Byte offset → UTF-16 offset, for every char boundary in `text`.
fn utf16_offsets(text: &str) -> Vec<usize> {
    let mut map = vec![0; text.len() + 1];
    let mut pos = 0;
    for (byte, c) in text.char_indices() {
        map[byte] = pos;
        pos += c.len_utf16();
    }
    map[text.len()] = pos;
    map
}

fn is_space(unit: u16) -> bool {
    char::from_u32(unit as u32).is_some_and(char::is_whitespace)
}

/// Letters and digits. Surrogate halves (characters outside the BMP) count as
/// not part of a word.
fn is_word(unit: u16) -> bool {
    char::from_u32(unit as u32).is_some_and(char::is_alphanumeric)
}

/// Spans from one window's logits (`encode.decode` in the Python package). A
/// token is part of an entity when P(not O) >= threshold; its label is the most
/// likely non-O tag. An I- tag that does not continue a span of the same label
/// starts a new one. Span ends are trimmed of whitespace, then widened to
/// whole words, so no part of a word is left exposed. Spans that are exactly
/// a field label are dropped.
fn decode(text: &[u16], offsets: &[(usize, usize)], logits: &[f32], tags: &[String], threshold: f32) -> Vec<ModelSpan> {
    let n = tags.len();
    let mut spans: Vec<ModelSpan> = Vec::new();
    let mut prev: Option<&str> = None;
    for (t, &(a, b)) in offsets.iter().enumerate() {
        if a == b {
            continue;
        }
        let row = &logits[t * n..(t + 1) * n];
        let max = row.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
        let exp: Vec<f32> = row.iter().map(|x| (x - max).exp()).collect();
        let sum: f32 = exp.iter().sum();
        let conf = 1.0 - exp[0] / sum;
        if conf < threshold {
            prev = None;
            continue;
        }
        let best = (1..n).max_by(|&i, &j| exp[i].total_cmp(&exp[j])).expect("at least one entity tag");
        let (kind, label) = tags[best].split_once('-').unwrap_or(("B", &tags[best]));
        match spans.last_mut() {
            Some(last) if kind == "I" && prev == Some(label) => {
                last.end = b;
                last.confidence = last.confidence.min(conf);
            }
            _ => spans.push(ModelSpan { start: a, end: b, label: label.to_string(), confidence: conf }),
        }
        prev = Some(label);
    }
    spans
        .into_iter()
        .filter_map(|mut s| {
            while s.start < s.end && is_space(text[s.start]) {
                s.start += 1;
            }
            while s.end > s.start && is_space(text[s.end - 1]) {
                s.end -= 1;
            }
            if s.start == s.end {
                return None;
            }
            while s.start > 0 && is_word(text[s.start - 1]) && is_word(text[s.start]) {
                s.start -= 1;
            }
            while s.end < text.len() && is_word(text[s.end]) && is_word(text[s.end - 1]) {
                s.end += 1;
            }
            let word = String::from_utf16_lossy(&text[s.start..s.end]).to_uppercase();
            (!FIELD_LABELS.contains(&word.as_str())).then_some(s)
        })
        .collect()
}

/// Merge overlapping spans from different windows (`encode.union`).
fn union(mut spans: Vec<ModelSpan>) -> Vec<ModelSpan> {
    spans.sort_by(|x, y| {
        (x.start, x.end, &x.label).cmp(&(y.start, y.end, &y.label)).then(x.confidence.total_cmp(&y.confidence))
    });
    let mut merged: Vec<ModelSpan> = Vec::new();
    for s in spans {
        match merged.last_mut() {
            Some(last) if s.start < last.end => {
                if s.end - s.start > last.end - last.start {
                    last.label = s.label;
                }
                last.end = last.end.max(s.end);
                last.confidence = last.confidence.max(s.confidence);
            }
            _ => merged.push(s),
        }
    }
    merged
}

#[cfg(test)]
mod tests {
    use super::*;

    fn tags() -> Vec<String> {
        ["O", "B-PERSON", "I-PERSON", "B-EMAIL", "I-EMAIL"].map(String::from).to_vec()
    }

    /// Logits that put almost all mass on one tag per token.
    fn logits(tag_per_token: &[usize]) -> Vec<f32> {
        tag_per_token.iter().flat_map(|&t| (0..5).map(move |i| if i == t { 10.0 } else { 0.0 })).collect()
    }

    #[test]
    fn decode_joins_inside_tags_and_trims_space() {
        let text: Vec<u16> = "Kia ora Hēmi Ngata!".encode_utf16().collect();
        // Tokens: "Kia", " ora", " Hēmi", " Ngata", "!"; a special token first.
        let offsets = [(0, 0), (0, 3), (3, 7), (7, 12), (12, 18), (18, 19)];
        let spans = decode(&text, &offsets, &logits(&[1, 0, 0, 1, 2, 0]), &tags(), 0.5);
        assert_eq!(spans.len(), 1);
        assert_eq!((spans[0].start, spans[0].end, spans[0].label.as_str()), (8, 18, "PERSON"));
    }

    #[test]
    fn spans_widen_to_whole_words() {
        let text: Vec<u16> = "NHI ZZZ0016, Ngata's".encode_utf16().collect();
        // "I" alone (inside "NHI"), and "Nga" (inside "Ngata").
        let spans = decode(&text, &[(2, 3), (3, 4), (13, 16), (16, 18)], &logits(&[3, 0, 1, 0]), &tags(), 0.5);
        let got: Vec<(usize, usize)> = spans.iter().map(|s| (s.start, s.end)).collect();
        assert_eq!(got, [(13, 18)], "\"NHI\" is a field label, so its widened span is dropped");
    }

    #[test]
    fn inside_tag_after_other_label_starts_new_span() {
        let text: Vec<u16> = "a b".encode_utf16().collect();
        let spans = decode(&text, &[(0, 1), (1, 3)], &logits(&[3, 2]), &tags(), 0.5);
        assert_eq!(spans.iter().map(|s| s.label.as_str()).collect::<Vec<_>>(), ["EMAIL", "PERSON"]);
    }

    #[test]
    fn union_keeps_the_longer_label() {
        let s = |start, end, label: &str| ModelSpan { start, end, label: label.into(), confidence: 0.9 };
        let merged = union(vec![s(5, 9, "PERSON"), s(0, 4, "EMAIL"), s(3, 12, "ADDRESS")]);
        assert_eq!(merged, vec![ModelSpan { start: 0, end: 12, label: "ADDRESS".into(), confidence: 0.9 }]);
    }
}

/// Parity with the Python tokeniser on real text. Needs an exported model and
/// a reference file written by Python, so it only runs when pointed at them:
/// `TUMATAITI_TOKENIZER=.../onnx TUMATAITI_EXPECTED=tok.json cargo test -- --ignored`.
#[cfg(test)]
mod parity {
    use super::*;

    #[test]
    #[ignore]
    fn windows_match_python() {
        let dir = std::env::var("TUMATAITI_TOKENIZER").expect("TUMATAITI_TOKENIZER");
        let read = |f: &str| std::fs::read_to_string(format!("{dir}/{f}")).unwrap();
        let student = Student::new(&read("tokenizer.json"), &read("config.json")).unwrap_or_else(|_| panic!("load"));
        let expected: serde_json::Value =
            serde_json::from_str(&std::fs::read_to_string(std::env::var("TUMATAITI_EXPECTED").unwrap()).unwrap()).unwrap();
        for case in expected.as_array().unwrap() {
            let w = student.windows(case["text"].as_str().unwrap()).unwrap_or_else(|_| panic!("encode"));
            let ids: Vec<Vec<i64>> = serde_json::from_value(case["ids"].clone()).unwrap();
            let offsets: Vec<Vec<(usize, usize)>> = serde_json::from_value(case["offsets"].clone()).unwrap();
            assert_eq!(w.ids, ids);
            assert_eq!(w.offsets, offsets);
        }
    }
}
