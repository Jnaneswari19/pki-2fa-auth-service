import base64
import pyotp

# Paste your decrypted seed here
hex_seed = "1e6d65925fdbb82e5f840db7239fd73c60227de1953cd46ee1d0bda859634814"

# Convert hex → bytes
seed_bytes = bytes.fromhex(hex_seed)

# Convert bytes → base32 (TOTP requires base32)
base32_seed = base64.b32encode(seed_bytes).decode()

print("Base32 Seed:", base32_seed)

# Generate TOTP
totp = pyotp.TOTP(base32_seed)
print("Current OTP:", totp.now())
