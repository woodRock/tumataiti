//! Browser bindings. Values cross the boundary as JSON strings, and span
//! offsets are converted from UTF-8 bytes to UTF-16 code units so they index
//! JavaScript strings directly.

use serde::{Deserialize, Serialize};
use tumataiti_rules::{Category, Checksum, Finding, Policy, Source, Span};
use wasm_bindgen::prelude::*;

#[derive(Serialize)]
struct JsRedaction<'a> {
    output: &'a str,
    /// Same as the Rust findings, but with UTF-16 offsets.
    findings: Vec<Finding>,
    blocked: bool,
}

/// Byte offset → UTF-16 offset, for every char boundary in `text`.
fn utf16_offsets(text: &str) -> Vec<usize> {
    let mut map = vec![0; text.len() + 1];
    let mut u16_pos = 0;
    for (byte, c) in text.char_indices() {
        map[byte] = u16_pos;
        u16_pos += c.len_utf16();
    }
    map[text.len()] = u16_pos;
    map
}

/// A span from the student model, with UTF-16 offsets (as the student
/// module returns them).
#[derive(Deserialize)]
struct ModelSpan {
    start: usize,
    end: usize,
    label: String,
    confidence: f32,
}

/// Student label → category. The student's `ID` covers government IDs and
/// card or bank numbers alike; the rules usually find the same span with the
/// exact category and a checksum, and win the merge.
fn model_category(label: &str) -> Option<Category> {
    Some(match label {
        "PERSON" => Category::Person,
        "ADDRESS" => Category::Address,
        "EMAIL" => Category::Email,
        "PHONE" => Category::Phone,
        "URL" => Category::Url,
        "IP_ADDRESS" => Category::IpAddress,
        "DATE" => Category::Date,
        "ID" => Category::NzGovId,
        "SECRET" => Category::Secret,
        "AFFILIATION" => Category::Affiliation,
        _ => return None,
    })
}

/// UTF-16 offset → byte offset; offsets inside a surrogate pair round down.
fn byte_offsets(text: &str) -> Vec<usize> {
    let mut map = Vec::with_capacity(text.len() + 1);
    for (byte, c) in text.char_indices() {
        map.extend(std::iter::repeat_n(byte, c.len_utf16()));
    }
    map.push(text.len());
    map
}

fn parse_policy(policy_json: &str) -> Result<Policy, JsError> {
    Ok(if policy_json.is_empty() {
        Policy::default()
    } else {
        serde_json::from_str(policy_json)?
    })
}

/// Redact `text` with the rules. `policy_json` may be empty for the default
/// policy. Returns JSON: `{ output, findings, blocked }`. The placeholder map
/// is deliberately not returned to the page.
#[wasm_bindgen]
pub fn redact(text: &str, policy_json: &str) -> Result<String, JsError> {
    let r = tumataiti_rules::redact(text, &parse_policy(policy_json)?);
    to_js(text, r)
}

/// Like [`redact`], with the student model's spans (`model_json`: a JSON array
/// of `{ start, end, label, confidence }` in UTF-16 offsets) merged with the
/// rules' candidates before the policy is applied.
#[wasm_bindgen(js_name = redactWith)]
pub fn redact_with(text: &str, policy_json: &str, model_json: &str, model_name: &str) -> Result<String, JsError> {
    let policy = parse_policy(policy_json)?;
    let bytes = byte_offsets(text);
    let model: Vec<ModelSpan> = serde_json::from_str(model_json)?;
    let mut candidates = tumataiti_rules::rules::candidates(text);
    for m in model {
        let Some(category) = model_category(&m.label) else { continue };
        let (start, end) = (bytes[m.start.min(bytes.len() - 1)], bytes[m.end.min(bytes.len() - 1)]);
        if start >= end {
            continue;
        }
        candidates.push(Span {
            start,
            end,
            text: text[start..end].to_string(),
            category,
            confidence: m.confidence,
            source: Source::Model,
            detector: model_name.to_string(),
            checksum: Checksum::None,
            note: None,
        });
    }
    tumataiti_rules::review::review(&mut candidates);
    let spans = tumataiti_rules::merge(text, candidates);
    to_js(text, tumataiti_rules::redact::apply(text, spans, &policy))
}

fn to_js(text: &str, r: tumataiti_rules::Redaction) -> Result<String, JsError> {
    let offsets = utf16_offsets(text);
    let js = JsRedaction {
        output: &r.output,
        blocked: r.blocked,
        findings: r
            .findings
            .iter()
            .map(|f| {
                let mut f = f.clone();
                f.span.start = offsets[f.span.start];
                f.span.end = offsets[f.span.end];
                f
            })
            .collect(),
    };
    Ok(serde_json::to_string(&js)?)
}

#[wasm_bindgen(js_name = defaultPolicy)]
pub fn default_policy() -> String {
    serde_json::to_string(&Policy::default()).expect("policy serialises")
}

#[wasm_bindgen]
pub fn version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn utf16_offsets_after_macrons() {
        let text = "Hōhepa a@b.nz";
        let map = utf16_offsets(text);
        let start = text.find('a').unwrap(); // the 'a' in "Hōhepa"
        assert_eq!(map[start], 5);
        assert_eq!(map[text.len()], 13);
    }

    #[test]
    fn byte_offsets_invert_utf16_offsets() {
        let text = "Tūī 👋🏽 Hōhepa";
        let (to16, to8) = (utf16_offsets(text), byte_offsets(text));
        for (byte, _) in text.char_indices() {
            assert_eq!(to8[to16[byte]], byte);
        }
        assert_eq!(to8[to16[text.len()]], text.len());
    }

    #[test]
    fn model_names_merge_with_rule_ids() {
        let text = "Hōhepa Ngata, IRD 49-091-850";
        let name_end = "Hōhepa Ngata".encode_utf16().count();
        let model = format!(r#"[{{"start":0,"end":{name_end},"label":"PERSON","confidence":0.97}}]"#);
        let out: serde_json::Value = serde_json::from_str(&redact_with(text, "", &model, "student").unwrap()).unwrap();
        let cats: Vec<&str> = out["findings"].as_array().unwrap().iter().map(|f| f["category"].as_str().unwrap()).collect();
        assert_eq!(cats, ["PERSON", "NZ_GOV_ID"]);
        assert!(!out["output"].as_str().unwrap().contains("Ngata"));
    }

    #[test]
    fn kinship_words_are_flagged_and_names_redacted() {
        let text = "Koro's IRD number. Nan Li will help.";
        let span = |word: &str| {
            let start = text[..text.find(word).unwrap()].encode_utf16().count();
            format!(r#"{{"start":{start},"end":{},"label":"PERSON","confidence":0.99}}"#, start + word.encode_utf16().count())
        };
        let model = format!("[{},{}]", span("Koro"), span("Nan Li"));
        let out: serde_json::Value = serde_json::from_str(&redact_with(text, "", &model, "student").unwrap()).unwrap();
        let actions: Vec<&str> = out["findings"].as_array().unwrap().iter().map(|f| f["action"].as_str().unwrap()).collect();
        assert_eq!(actions, ["flag", "pseudonymise"]);
        let output = out["output"].as_str().unwrap();
        assert!(output.starts_with("Koro's") && !output.contains("Nan"));
    }
}
