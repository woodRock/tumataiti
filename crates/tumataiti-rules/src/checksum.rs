//! Check-digit algorithms for NZ identifiers and payment cards.

fn digits(s: &str) -> Vec<u32> {
    s.chars().filter_map(|c| c.to_digit(10)).collect()
}

/// IRD number: 8 or 9 digits, mod-11 with primary and secondary weights.
/// Follows the check-digit algorithm Inland Revenue publishes for software developers.
pub fn ird(s: &str) -> bool {
    let d = digits(s);
    if !(8..=9).contains(&d.len()) {
        return false;
    }
    let n = d.iter().fold(0u64, |acc, &x| acc * 10 + x as u64);
    if !(10_000_000..=150_000_000).contains(&n) {
        return false;
    }
    let (base, check) = d.split_at(d.len() - 1);
    let mut padded = vec![0; 8 - base.len()];
    padded.extend_from_slice(base);

    let calc = |weights: [u32; 8]| {
        let r = padded.iter().zip(weights).map(|(x, w)| x * w).sum::<u32>() % 11;
        if r == 0 {
            0
        } else {
            11 - r
        }
    };
    let mut c = calc([3, 2, 7, 6, 5, 4, 3, 2]);
    if c == 10 {
        c = calc([7, 4, 3, 2, 5, 2, 7, 6]);
        if c == 10 {
            return false;
        }
    }
    c == check[0]
}

/// NHI alphabet: A–Z without I and O, valued 1–24.
fn nhi_letter(c: char) -> Option<u32> {
    "ABCDEFGHJKLMNPQRSTUVWXYZ".find(c).map(|i| i as u32 + 1)
}

/// NHI number (HISO 10046). Old format `AAANNNC` (mod-11 check digit) and
/// new format `AAANNAX` (mod-23 check letter), introduced from 2025.
pub fn nhi(s: &str) -> bool {
    let c: Vec<char> = s.chars().collect();
    if c.len() != 7 {
        return false;
    }
    let mut vals = [0u32; 6];
    for i in 0..3 {
        match nhi_letter(c[i]) {
            Some(v) => vals[i] = v,
            None => return false,
        }
    }
    for i in 3..5 {
        match c[i].to_digit(10) {
            Some(v) => vals[i] = v,
            None => return false,
        }
    }
    let weights = [7, 6, 5, 4, 3, 2];
    let sum = |vals: &[u32; 6]| vals.iter().zip(weights).map(|(v, w)| v * w).sum::<u32>();

    if let (Some(d5), Some(check)) = (c[5].to_digit(10), c[6].to_digit(10)) {
        vals[5] = d5;
        let r = sum(&vals) % 11;
        if r == 0 {
            return false;
        }
        return (11 - r) % 10 == check;
    }
    if let (Some(l5), Some(check)) = (nhi_letter(c[5]), nhi_letter(c[6])) {
        vals[5] = l5;
        // TODO: confirm the remainder-0 case against the published HISO 10046 test vectors.
        return 23 - sum(&vals) % 23 == check;
    }
    false
}

/// Luhn check for payment card numbers.
pub fn luhn(s: &str) -> bool {
    let d = digits(s);
    if d.len() < 2 {
        return false;
    }
    let sum: u32 = d
        .iter()
        .rev()
        .enumerate()
        .map(|(i, &x)| {
            if i % 2 == 1 {
                let y = x * 2;
                if y > 9 {
                    y - 9
                } else {
                    y
                }
            } else {
                x
            }
        })
        .sum();
    sum.is_multiple_of(10)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ird_examples_from_ir_spec() {
        assert!(ird("49091850"));
        assert!(ird("49-091-850"));
        assert!(ird("35901981"));
        assert!(ird("136410132")); // needs the secondary weights
        assert!(!ird("136410133"));
        assert!(!ird("9125568")); // too short
        assert!(!ird("49091851"));
    }

    #[test]
    fn nhi_old_format() {
        assert!(nhi("ZZZ0016"));
        assert!(nhi("ZZZ0024"));
        assert!(!nhi("ZZZ0017"));
        assert!(!nhi("ZZI0016")); // I is not in the NHI alphabet
    }

    #[test]
    fn nhi_new_format() {
        assert!(nhi("ZZZ00AC"));
        assert!(!nhi("ZZZ00AD"));
    }

    #[test]
    fn luhn_cards() {
        assert!(luhn("4111 1111 1111 1111"));
        assert!(luhn("5555-5555-5555-4444"));
        assert!(!luhn("4111 1111 1111 1112"));
    }
}
