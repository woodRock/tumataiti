//! Tūmataiti deterministic redaction rules.
//!
//! The rules cover structured identifiers that a checksum or a strict format
//! can verify (SPEC §6.1). Names, addresses and other open-ended categories
//! come from the model; its spans go through the same [`merge`] and
//! [`redact::apply`] steps.

pub mod checksum;
mod merge;
pub mod policy;
pub mod redact;
pub mod rules;
pub mod span;

pub use merge::merge;
pub use policy::{Action, Policy};
pub use redact::{restore, Finding, Redaction};
pub use span::{Category, Checksum, Source, Span};

/// Detect spans with the rules only, merged and sorted.
pub fn scan(text: &str) -> Vec<Span> {
    merge(text, rules::candidates(text))
}

/// Detect with the rules and apply `policy`.
pub fn redact(text: &str, policy: &Policy) -> Redaction {
    redact::apply(text, scan(text), policy)
}
