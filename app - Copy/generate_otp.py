import pyotp
import base64
import os

def generate_secret() -> str:
    """
    Generate a new random base32 secret for TOTP.
    """
    return pyotp.random_base32()

def generate_totp(secret: str) -> str:
    """
    Generate a current TOTP code from a base32 secret.
    """
    totp = pyotp.TOTP(secret)
    return totp.now()

def verify_totp(secret: str, code: str, window: int = 1) -> bool:
    """
    Verify a TOTP code against the given secret.
    Allows a small time window for clock drift.
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=window)
