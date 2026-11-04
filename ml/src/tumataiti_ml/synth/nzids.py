"""Generate NZ identifiers with valid or deliberately broken check digits.

These are independent Python implementations of the check-digit algorithms,
so the synthetic data also cross-checks the Rust rules rather than echoing them.
"""

from __future__ import annotations

import random

NHI_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ"  # A–Z without I and O, valued 1–24


def ird_check_digit(base: str) -> int | None:
    """Check digit for an IRD base (7 or 8 digits), or None if no valid digit exists."""
    digits = [int(c) for c in base.zfill(8)]
    for weights in ((3, 2, 7, 6, 5, 4, 3, 2), (7, 4, 3, 2, 5, 2, 7, 6)):
        r = sum(d * w for d, w in zip(digits, weights)) % 11
        c = 0 if r == 0 else 11 - r
        if c != 10:
            return c
    return None


def ird_is_valid(s: str) -> bool:
    d = "".join(c for c in s if c.isdigit())
    if len(d) not in (8, 9) or not 10_000_000 <= int(d) <= 150_000_000:
        return False
    return ird_check_digit(d[:-1]) == int(d[-1])


def gen_ird(rng: random.Random, valid: bool = True) -> str:
    while True:
        base = str(rng.randint(1_000_000, 14_999_999))
        check = ird_check_digit(base)
        if check is None:
            continue
        digit = check if valid else (check + rng.randint(1, 9)) % 10
        n = base + str(digit)
        if valid != ird_is_valid(n):
            continue
        style = rng.random()
        if len(n) == 8:
            if style < 0.6:
                return f"{n[:2]}-{n[2:5]}-{n[5:]}"
            return n if style < 0.85 else f"{n[:2]} {n[2:5]} {n[5:]}"
        return f"{n[:3]}-{n[3:6]}-{n[6:]}" if style < 0.7 else n


def _nhi_values(s: str) -> list[int]:
    return [NHI_ALPHABET.index(c) + 1 if c.isalpha() else int(c) for c in s[:6]]


def nhi_check(first6: str, new_format: bool) -> str | None:
    total = sum(v * w for v, w in zip(_nhi_values(first6), (7, 6, 5, 4, 3, 2)))
    if new_format:
        return NHI_ALPHABET[23 - total % 23 - 1]
    r = total % 11
    return None if r == 0 else str((11 - r) % 10)


def nhi_is_valid(s: str) -> bool:
    if len(s) != 7 or any(c not in NHI_ALPHABET for c in s[:3]) or not s[3:5].isdigit():
        return False
    if s[5].isdigit() and s[6].isdigit():
        return nhi_check(s[:6], False) == s[6]
    if s[5] in NHI_ALPHABET and s[6] in NHI_ALPHABET:
        return nhi_check(s[:6], True) == s[6]
    return False


def gen_nhi(rng: random.Random, valid: bool = True, new_format: bool = False) -> str:
    while True:
        letters = "".join(rng.choice(NHI_ALPHABET) for _ in range(3))
        if new_format:
            first6 = letters + f"{rng.randint(0, 99):02d}" + rng.choice(NHI_ALPHABET)
            check = nhi_check(first6, True)
            if not valid:
                check = rng.choice([c for c in NHI_ALPHABET if c != check])
        else:
            first6 = letters + f"{rng.randint(0, 999):03d}"
            check = nhi_check(first6, False)
            if check is None:
                continue
            if not valid:
                check = str((int(check) + rng.randint(1, 9)) % 10)
        return first6 + check


def luhn_ok(digits: str) -> bool:
    total = 0
    for i, c in enumerate(reversed(digits)):
        d = int(c)
        if i % 2 == 1:
            d = d * 2 - 9 if d > 4 else d * 2
        total += d
    return total % 10 == 0


def gen_card(rng: random.Random, valid: bool = True) -> str:
    prefix = rng.choice(["4", "51", "52", "53", "54", "55"])
    body = prefix + "".join(str(rng.randint(0, 9)) for _ in range(15 - len(prefix)))
    check = next(d for d in "0123456789" if luhn_ok(body + d))
    if not valid:
        check = str((int(check) + rng.randint(1, 9)) % 10)
    n = body + check
    sep = rng.choice([" ", "-", ""])
    return sep.join(n[i : i + 4] for i in range(0, 16, 4))


def gen_bank(rng: random.Random) -> str:
    bank = rng.choice([1, 2, 3, 6, 11, 12, 15, 30, 38])
    suffix = f"{rng.randint(0, 99):02d}" if rng.random() < 0.7 else f"{rng.randint(0, 999):03d}"
    sep = rng.choice(["-", "-", " "])
    return sep.join([f"{bank:02d}", f"{rng.randint(1, 9999):04d}", f"{rng.randint(0, 9_999_999):07d}", suffix])


def gen_phone(rng: random.Random, mobile: bool | None = None) -> str:
    if mobile is None:
        mobile = rng.random() < 0.65
    if mobile:
        prefix = rng.choice(["21", "22", "27", "29", "20"])
        a, b = rng.randint(100, 999), rng.randint(1000, 9999)
        style = rng.random()
        if style < 0.45:
            return f"0{prefix} {a} {b}"
        if style < 0.65:
            return f"0{prefix}{a}{b}"
        if style < 0.85:
            return f"+64 {prefix} {a} {b}"
        return f"0{prefix}-{a}-{b}"
    area = rng.choice(["3", "4", "6", "7", "9"])
    a, b = rng.randint(200, 999), rng.randint(1000, 9999)
    style = rng.random()
    if style < 0.5:
        return f"0{area} {a} {b}"
    if style < 0.75:
        return f"(0{area}) {a} {b}"
    return f"+64 {area} {a} {b}"


def gen_passport(rng: random.Random) -> str:
    return rng.choice(["LA", "LB", "LC", "LD", "LE", "LF", "LH", "LJ"]) + f"{rng.randint(0, 999_999):06d}"


def gen_licence(rng: random.Random) -> str:
    return "".join(rng.choice("ABCDEFGHJKLMNPRSTUVWXYZ") for _ in range(2)) + f"{rng.randint(0, 999_999):06d}"


def gen_ipv4(rng: random.Random) -> str:
    # Documentation ranges (RFC 5737) and private ranges only.
    return rng.choice(
        [
            f"192.0.2.{rng.randint(1, 254)}",
            f"198.51.100.{rng.randint(1, 254)}",
            f"203.0.113.{rng.randint(1, 254)}",
            f"10.{rng.randint(0, 255)}.{rng.randint(0, 255)}.{rng.randint(1, 254)}",
            f"192.168.{rng.randint(0, 255)}.{rng.randint(1, 254)}",
        ]
    )


def gen_secret(rng: random.Random) -> tuple[str, str]:
    """(text, kind). Values are random and match no real credential."""
    alnum = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    pick = lambda n: "".join(rng.choice(alnum) for _ in range(n))  # noqa: E731
    kind = rng.choice(["anthropic", "github", "aws", "password"])
    if kind == "anthropic":
        return "sk-ant-api03-" + pick(40), kind
    if kind == "github":
        return "ghp_" + pick(36), kind
    if kind == "aws":
        return "AKIA" + "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567") for _ in range(16)), kind
    words = ["kumara", "tuatara", "kereru", "pohutukawa", "harakeke", "kaimoana"]
    return f"{rng.choice(words)}-{rng.choice(words)}-{rng.randint(10, 9999)}", kind
