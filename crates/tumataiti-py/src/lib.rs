//! Python bindings. Spans cross the boundary as JSON with offsets converted
//! from UTF-8 bytes to code points, so they index Python strings directly.

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use rules::{Policy, Span};

/// Byte offset → code-point offset, for every char boundary in `text`.
fn char_offsets(text: &str) -> Vec<usize> {
    let mut map = vec![0; text.len() + 1];
    let mut n = 0;
    for (byte, _) in text.char_indices() {
        map[byte] = n;
        n += 1;
    }
    map[text.len()] = n;
    map
}

fn to_chars(text: &str, spans: &mut [Span]) {
    let map = char_offsets(text);
    for s in spans {
        s.start = map[s.start];
        s.end = map[s.end];
    }
}

/// Detect spans with the rules. Returns a JSON list of spans.
#[pyfunction]
fn scan_json(text: &str) -> String {
    let mut spans = rules::scan(text);
    to_chars(text, &mut spans);
    serde_json::to_string(&spans).expect("spans serialise")
}

/// Detect and apply a policy (JSON; empty for the default). Returns JSON with
/// `output`, `findings`, `blocked` and `placeholders`.
#[pyfunction]
#[pyo3(signature = (text, policy_json = ""))]
fn redact_json(text: &str, policy_json: &str) -> PyResult<String> {
    let policy = if policy_json.is_empty() {
        Policy::default()
    } else {
        serde_json::from_str(policy_json).map_err(|e| PyValueError::new_err(e.to_string()))?
    };
    let mut r = rules::redact(text, &policy);
    let map = char_offsets(text);
    for f in &mut r.findings {
        f.span.start = map[f.span.start];
        f.span.end = map[f.span.end];
    }
    Ok(serde_json::to_string(&r).expect("redaction serialises"))
}

#[pymodule]
fn tumataiti_rules(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(scan_json, m)?)?;
    m.add_function(wrap_pyfunction!(redact_json, m)?)?;
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}
