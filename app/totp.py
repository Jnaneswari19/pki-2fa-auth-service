import pyotp

def generate_totp(seed: str) -> str:
    totp = pyotp.TOTP(seed)
    return totp.now()
