use serde::{Deserialize, Serialize};

/// PII categories from SPEC §6.2. Rules emit only the structured ones; the
/// rest are filled by the model and gazetteers in later milestones.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum Category {
    Person,
    Address,
    Email,
    Phone,
    Url,
    IpAddress,
    Date,
    NzGovId,
    Financial,
    Secret,
    Affiliation,
    Health,
    CulturalRestricted,
}

impl Category {
    pub const ALL: [Category; 13] = [
        Category::Person,
        Category::Address,
        Category::Email,
        Category::Phone,
        Category::Url,
        Category::IpAddress,
        Category::Date,
        Category::NzGovId,
        Category::Financial,
        Category::Secret,
        Category::Affiliation,
        Category::Health,
        Category::CulturalRestricted,
    ];

    /// Placeholder label, e.g. `[EMAIL_1]`.
    pub fn label(self) -> &'static str {
        match self {
            Category::Person => "PERSON",
            Category::Address => "ADDRESS",
            Category::Email => "EMAIL",
            Category::Phone => "PHONE",
            Category::Url => "URL",
            Category::IpAddress => "IP_ADDRESS",
            Category::Date => "DATE",
            Category::NzGovId => "NZ_GOV_ID",
            Category::Financial => "FINANCIAL",
            Category::Secret => "SECRET",
            Category::Affiliation => "AFFILIATION",
            Category::Health => "HEALTH",
            Category::CulturalRestricted => "CULTURAL_RESTRICTED",
        }
    }

    /// When spans overlap, the higher priority category wins (after checksum).
    pub fn priority(self) -> u8 {
        match self {
            Category::Secret => 100,
            Category::NzGovId => 90,
            Category::Financial => 85,
            Category::CulturalRestricted => 80,
            Category::Health => 70,
            Category::Email => 60,
            Category::Phone => 55,
            Category::Person => 50,
            Category::Address => 45,
            Category::Affiliation => 40,
            Category::IpAddress => 35,
            Category::Url => 30,
            Category::Date => 20,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Source {
    Rule,
    Model,
    Gazetteer,
}

/// Whether the matched text passed the identifier's check-digit algorithm.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Checksum {
    Valid,
    Invalid,
    /// The format has no check digit, or it is not verified yet.
    None,
}

/// A detected span. Offsets are UTF-8 byte offsets into the scanned text.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Span {
    pub start: usize,
    pub end: usize,
    pub text: String,
    pub category: Category,
    pub confidence: f32,
    pub source: Source,
    /// Which detector fired, e.g. `nz_ird` or a model name.
    pub detector: String,
    pub checksum: Checksum,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub note: Option<String>,
}

impl Span {
    pub fn len(&self) -> usize {
        self.end - self.start
    }

    pub fn is_empty(&self) -> bool {
        self.start == self.end
    }

    pub fn overlaps(&self, other: &Span) -> bool {
        self.start < other.end && other.start < self.end
    }
}
