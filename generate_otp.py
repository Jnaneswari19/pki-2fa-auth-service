# generate_otp.py
import base64
import pyotp

def generate_otp(seed: str) -> str:
    """
    Generate a TOTP code from a hex seed string
    """
    # Convert hex → bytes
    seed_bytes = bytes.fromhex(seed)

    # Convert bytes → base32 (TOTP requires base32)
    base32_seed = base64.b32encode(seed_bytes).decode()

    # Generate TOTP
    totp = pyotp.TOTP(base32_seed)
    return totp.now()
