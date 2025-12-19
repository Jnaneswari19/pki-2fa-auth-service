import pyotp
from app.config import SEED_PATH
from app.storage import read_text, write_text

def set_seed(seed_hex: str):
    write_text(SEED_PATH, seed_hex)

def get_seed():
    return read_text(SEED_PATH)

def _hex_to_base32(hex_str: str) -> str:
    return pyotp.utils.bytes_to_base32(bytes.fromhex(hex_str))

def generate_code():
    seed_hex = get_seed()
    secret = _hex_to_base32(seed_hex)
    totp = pyotp.TOTP(secret, digits=6, interval=30)
    return totp.now()

def verify_code(code: str):
    seed_hex = get_seed()
    secret = _hex_to_base32(seed_hex)
    totp = pyotp.TOTP(secret, digits=6, interval=30)
    return bool(totp.verify(code, valid_window=1))
