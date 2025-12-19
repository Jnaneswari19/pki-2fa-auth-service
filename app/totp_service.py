import pyotp
import base64
import binascii

def _hex_to_base32(hex_str: str) -> str:
    seed_bytes = binascii.unhexlify(hex_str)
    return base64.b32encode(seed_bytes).decode("utf-8")

def set_seed(seed_hex: str):
    # Keep this if main.py imports set_seed
    with open("/app/data/seed.txt", "w") as f:
        f.write(seed_hex.strip())

def generate_code() -> str:
    with open("/app/data/seed.txt") as f:
        seed_hex = f.read().strip()
    secret = _hex_to_base32(seed_hex)
    totp = pyotp.TOTP(secret)
    return totp.now()

def verify_code(code: str) -> bool:
    with open("/app/data/seed.txt") as f:
        seed_hex = f.read().strip()
    secret = _hex_to_base32(seed_hex)
    totp = pyotp.TOTP(secret)
    # Allow ±1 time step to tolerate clock drift or request lag
    return totp.verify(code, valid_window=1)
