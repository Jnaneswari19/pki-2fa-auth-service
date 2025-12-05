import pyotp
from app.generate_otp import generate_secret, generate_totp, verify_totp

def test_generate_and_verify_totp():
    secret = generate_secret()
    code = generate_totp(secret)
    assert verify_totp(secret, code)

def test_fixed_secret_verification():
    secret_b32 = "JBSWY3DPEHPK3PXP"
    code = generate_totp(secret_b32)
    assert verify_totp(secret_b32, code)
