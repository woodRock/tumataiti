//! Browser bindings. Values cross the boundary as JSON strings, and span
//! offsets are converted from UTF-8 bytes to UTF-16 code units so they index
//! JavaScript strings directly.

use serde::Serialize;
use tumataiti_rules::{Finding, Policy};
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

/// Redact `text` with the rules. `policy_json` may be empty for the default
/// policy. Returns JSON: `{ output, findings, blocked }`. The placeholder map
/// is deliberately not returned to the page.
#[wasm_bindgen]
pub fn redact(text: &str, policy_json: &str) -> Result<String, JsError> {
    let policy = if policy_json.is_empty() {
        Policy::default()
    } else {
        serde_json::from_str(policy_json)?
    };
    let r = tumataiti_rules::redact(text, &policy);
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
}
