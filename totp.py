# totp.py
import base64
import pyotp

def _is_hex(s: str) -> bool:
    try:
        int(s, 16)
        return True
    except Exception:
        return False

def hex_to_base32(hex_seed: str) -> str:
    b = bytes.fromhex(hex_seed)
    return base64.b32encode(b).decode().strip('=')

def generate_totp(seed: str) -> str:
    """
    Accepts either a hex seed (0-9a-f) or a base32 seed (A-Z2-7). Returns 6-digit string.
    """
    if _is_hex(seed):
        base32_seed = hex_to_base32(seed)
    else:
        base32_seed = seed  # assume already base32
    totp = pyotp.TOTP(base32_seed)
    return totp.now()
