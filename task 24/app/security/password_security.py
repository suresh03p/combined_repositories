import re
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def validate_password_strength(password: str) -> None:
    if len(password) < 12 or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"\d", password) or not re.search(r"[^A-Za-z0-9]", password):
        raise ValueError("Password must be 12+ characters with upper, lower, number, and symbol")

def hash_password(password: str) -> str:
    validate_password_strength(password)
    return password_hash.hash(password)

def verify_password(password: str, stored_hash: str) -> bool:
    return password_hash.verify(password, stored_hash)
