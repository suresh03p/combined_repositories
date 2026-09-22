"""Examples covering Python regular expressions for validation and parsing."""

from __future__ import annotations

import re
from typing import Any

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_PATTERN = re.compile(r"^\+?\d{1,3}?[- .]?\(?\d{2,4}\)?[- .]?\d{3}[- .]?\d{4}$")
PASSWORD_PATTERN = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$")
PAN_PATTERN = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")
AADHAAR_PATTERN = re.compile(r"^\d{4}\s?\d{4}\s?\d{4}$")
GST_PATTERN = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")
IPV4_PATTERN = re.compile(r"^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}$")
IPV6_PATTERN = re.compile(r"^(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4}$")
URL_PATTERN = re.compile(r"^https?://(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}(?:/[^\s]*)?$", re.IGNORECASE)
CC_PATTERN = re.compile(r"^(?:4\d{12}(?:\d{3})?|5[1-5]\d{14}|6(?:011|5\d{2})\d{12})$")


def is_valid_email(value: str) -> bool:
    """Validate a basic email address."""
    return bool(EMAIL_PATTERN.fullmatch(value.strip()))


def is_valid_phone(value: str) -> bool:
    """Validate a phone number."""
    return bool(PHONE_PATTERN.fullmatch(value.strip()))


def validate_password(value: str) -> bool:
    """Require uppercase, lowercase, digit, special character, and minimum length."""
    return bool(PASSWORD_PATTERN.fullmatch(value))


def is_valid_pan(value: str) -> bool:
    """Validate a PAN card number."""
    return bool(PAN_PATTERN.fullmatch(value.strip().upper()))


def is_valid_aadhaar(value: str) -> bool:
    """Validate an Aadhaar number with optional spaces."""
    return bool(AADHAAR_PATTERN.fullmatch(value.strip()))


def is_valid_gst(value: str) -> bool:
    """Validate a GST number."""
    return bool(GST_PATTERN.fullmatch(value.strip().upper()))


def is_valid_ipv4(value: str) -> bool:
    """Validate an IPv4 address."""
    return bool(IPV4_PATTERN.fullmatch(value.strip()))


def is_valid_ipv6(value: str) -> bool:
    """Validate an IPv6 address."""
    return bool(IPV6_PATTERN.fullmatch(value.strip()))


def is_valid_url(value: str) -> bool:
    """Validate an HTTP or HTTPS URL."""
    return bool(URL_PATTERN.fullmatch(value.strip()))


def is_valid_credit_card(value: str) -> bool:
    """Validate a standard credit card number."""
    digits = re.sub(r"\D", "", value)
    return bool(CC_PATTERN.fullmatch(digits))


def extract_named_groups(text: str) -> dict[str, str]:
    """Parse a message using a named regex group."""
    pattern = re.compile(r"(?P<user>[A-Za-z0-9._-]+)@(?P<domain>[a-z0-9.-]+\.[a-z]{2,})")
    match = pattern.search(text)
    return match.groupdict() if match else {}


def rewrite_text(text: str) -> str:
    """Replace words with placeholders using regex substitution."""
    return re.sub(r"\bsecret\b", "[REDACTED]", text, flags=re.IGNORECASE)


def split_records(text: str) -> list[str]:
    """Split a multiline string with regex."""
    return re.split(r"\n+", text.strip())


def demo() -> list[dict[str, Any]]:
    """Run simple demonstrations and return sample outputs."""
    examples = [
        ("Email", is_valid_email("user.name+tag@example.com")),
        ("Phone", is_valid_phone("+91-9876543210")),
        ("Password", validate_password("Abcd@1234")),
        ("PAN", is_valid_pan("ABCDE1234F")),
        ("Aadhaar", is_valid_aadhaar("1234 5678 9012")),
        ("GST", is_valid_gst("22AAAAA0000A1Z5")),
        ("IPv4", is_valid_ipv4("192.168.1.10")),
        ("IPv6", is_valid_ipv6("2001:db8::1")),
        ("URL", is_valid_url("https://example.com/path")),
        ("Credit Card", is_valid_credit_card("4111111111111111")),
    ]
    for name, result in examples:
        print(f"{name}: {result}")
    print("Named groups:", extract_named_groups("Contact support@company.com"))
    print("Rewritten:", rewrite_text("The secret token is secret"))
    return [{"name": name, "result": result} for name, result in examples]


if __name__ == "__main__":
    demo()
