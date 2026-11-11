use std::collections::BTreeMap;

use serde::{Deserialize, Serialize};

use crate::span::Category;

/// What to do with a detected span (SPEC §6.3).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Action {
    /// Send unchanged.
    Allow,
    /// Send unchanged, but surface for human review.
    Flag,
    /// Replace with a consistent, reversible placeholder such as `[EMAIL_1]`.
    Pseudonymise,
    /// Replace with a coarser value, e.g. a date of birth becomes its year.
    Generalise,
    /// Replace with the category label; not restored afterwards.
    Mask,
    /// Refuse to send the request at all.
    Block,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(default)]
pub struct Policy {
    pub actions: BTreeMap<Category, Action>,
    /// Spans below this confidence are flagged instead of acted on.
    pub threshold: f32,
}

impl Policy {
    pub fn action(&self, category: Category) -> Action {
        self.actions.get(&category).copied().unwrap_or(Action::Flag)
    }
}

impl Default for Policy {
    /// The recall-first defaults from SPEC §6.2.
    fn default() -> Self {
        use Action::*;
        use Category::*;
        let actions = [
            (Person, Pseudonymise),
            (Address, Pseudonymise),
            (Email, Pseudonymise),
            (Phone, Pseudonymise),
            (Url, Pseudonymise),
            (IpAddress, Pseudonymise),
            (Date, Generalise),
            (NzGovId, Mask),
            (Financial, Mask),
            (OtherId, Mask),
            (Secret, Block),
            // Flag would send it to the cloud unchanged; a placeholder keeps it on the
            // device until the kaitiaki/legal workstream sets this policy (SPEC §6.2).
            (Affiliation, Pseudonymise),
            (Health, Flag),
            (CulturalRestricted, Block),
        ];
        Policy {
            actions: actions.into_iter().collect(),
            threshold: 0.5,
        }
    }
}
