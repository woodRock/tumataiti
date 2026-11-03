use tumataiti_rules::{redact, scan, Action, Category, Checksum, Policy};

/// (detector, matched text) for every span found in `text`.
fn found(text: &str) -> Vec<(String, String)> {
    scan(text).into_iter().map(|s| (s.detector, s.text)).collect()
}

fn one(text: &str) -> tumataiti_rules::Span {
    let spans = scan(text);
    assert_eq!(spans.len(), 1, "expected one span in {text:?}, got {spans:#?}");
    spans.into_iter().next().unwrap()
}

#[test]
fn email_and_url() {
    assert_eq!(
        found("Mail aroha.ngata@example.co.nz or see https://example.org/whānau?id=7."),
        [
            ("email".into(), "aroha.ngata@example.co.nz".into()),
            ("url".into(), "https://example.org/whānau?id=7".into()),
        ]
    );
}

#[test]
fn nz_phone_formats() {
    for phone in [
        "021 123 4567",
        "0211234567",
        "+64 21 123 4567",
        "+64 (0)21 123 4567",
        "04 123 4567",
        "(04) 123 4567",
        "09-123-4567",
    ] {
        let s = one(&format!("Call {phone} today"));
        assert_eq!((s.detector.as_str(), s.text.as_str()), ("nz_phone", phone));
    }
}

#[test]
fn phone_not_matched_inside_longer_numbers() {
    assert!(scan("Order 99021123456789").is_empty());
}

#[test]
fn ird_valid_is_redacted_without_context() {
    let s = one("Reference 49-091-850 attached");
    assert_eq!(s.detector, "nz_ird");
    assert_eq!(s.checksum, Checksum::Valid);
}

#[test]
fn ird_invalid_needs_context_and_is_weak() {
    assert!(scan("Reference 49-091-851 attached").is_empty());
    let s = one("My IRD number is 49-091-851");
    assert_eq!(s.checksum, Checksum::Invalid);
    assert!(s.confidence < Policy::default().threshold);
}

#[test]
fn nhi_both_formats() {
    assert_eq!(one("Patient ZZZ0016 seen").detector, "nz_nhi");
    assert_eq!(one("Patient ZZZ00AC seen").detector, "nz_nhi");
    assert!(scan("Patient ZZZ0017 seen").is_empty());
    assert_eq!(one("NHI: ZZZ0017").checksum, Checksum::Invalid);
}

#[test]
fn passport_and_licence_by_context() {
    assert_eq!(one("Passport LA123456").detector, "nz_passport");
    assert_eq!(one("Driver licence DL AB123456").detector, "nz_driver_licence");
    let s = one("Code XY123456");
    assert_eq!(s.detector, "nz_id_format");
    assert!(s.confidence < 0.5);
    // A label on the previous line does not count.
    let spans = scan("Driver licence: DL AB654321\nBooking code: XY998877");
    assert_eq!(spans[1].detector, "nz_id_format");
}

#[test]
fn payment_card_luhn() {
    let s = one("Card 4111 1111 1111 1111 exp 12/29");
    assert_eq!((s.detector.as_str(), s.checksum), ("payment_card", Checksum::Valid));
    assert!(scan("Ref 4111 1111 1111 1112").is_empty());
}

#[test]
fn bank_account_format() {
    let s = one("Pay into 12-3140-0123456-00 please");
    assert_eq!(s.detector, "nz_bank_account");
    assert_eq!(s.category, Category::Financial);
}

#[test]
fn ip_address() {
    assert_eq!(one("from 192.168.1.20 at noon").detector, "ipv4");
    assert!(scan("version 1.2.3.4.5").is_empty());
    assert!(scan("not 300.1.1.1").is_empty());
}

#[test]
fn dates_only_with_birth_or_death_context() {
    assert!(scan("The hui is on 14/03/2027").is_empty());
    assert_eq!(one("DOB 14/03/1987").detector, "date_of_birth");
    assert_eq!(one("born 3 March 1952").text, "3 March 1952");
    assert_eq!(one("Born: May 7, 1978").text, "May 7, 1978");
    assert_eq!(one("I whānau mai ia i te 12 o Hōngongoi 1948").text, "12 o Hōngongoi 1948");
}

#[test]
fn secrets() {
    assert_eq!(one("key sk-ant-api03-abcdefghijklmnopqrstuvwxyz0123").detector, "anthropic_api_key");
    assert_eq!(one("AKIAIOSFODNN7EXAMPLE").detector, "aws_access_key");
    assert_eq!(one("password: hunter2hunter2").text, "hunter2hunter2");
    assert_eq!(one("db_password: kumara-hangi-2024").text, "kumara-hangi-2024");
}

#[test]
fn offsets_are_correct_after_macrons() {
    let text = "Kōrero ki a Mereana: mereana@example.nz";
    let s = one(text);
    assert_eq!(&text[s.start..s.end], "mereana@example.nz");
}

#[test]
fn default_policy_end_to_end() {
    let r = redact(
        "Email hēmi@example.nz, again hemi@example.nz. IRD 49-091-850. Born 14/03/1987.",
        &Policy::default(),
    );
    assert!(!r.blocked);
    assert_eq!(
        r.output,
        "Email [EMAIL_1], again [EMAIL_1]. IRD [NZ_GOV_ID]. Born [YEAR 1987]."
    );
    assert_eq!(r.placeholders["[EMAIL_1]"], "hēmi@example.nz");
}

#[test]
fn weak_spans_are_flagged_not_replaced() {
    let r = redact("IRD 49-091-851", &Policy::default());
    assert_eq!(r.findings[0].action, Action::Flag);
    assert_eq!(r.output, "IRD 49-091-851");
}

#[test]
fn secrets_block_the_request() {
    let r = redact("use sk-ant-api03-abcdefghijklmnopqrstuvwxyz0123", &Policy::default());
    assert!(r.blocked);
    assert!(r.output.is_empty());
}

#[test]
fn restore_only_known_placeholders() {
    let r = redact("Text 021 123 4567", &Policy::default());
    let restored = tumataiti_rules::restore("Ring [PHONE_1], not [PHONE_9] [x", &r.placeholders);
    assert_eq!(restored, "Ring 021 123 4567, not [PHONE_9] [x");
}
