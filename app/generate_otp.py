import pyotp

def generate_totp(secret: str) -> str:
    totp = pyotp.TOTP(secret)
    return totp.now()
