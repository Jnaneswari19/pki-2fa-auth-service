#!/usr/bin/env python3
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from pathlib import Path

STUDENT_PRIV = Path("student_private.pem")

def _fix_b64(s: str) -> bytes:
    s = s.replace("\n", "").replace("\r", "")
    s = s + "=" * (-len(s) % 4)
    return base64.b64decode(s)

def load_private_key(path: Path = STUDENT_PRIV):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def decrypt_seed_b64(encrypted_seed_b64: str, priv_key=None) -> bytes:
    if priv_key is None:
        priv_key = load_private_key()
    enc = _fix_b64(encrypted_seed_b64)
    plaintext = priv_key.decrypt(
        enc,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(),
                     label=None)
    )
    return plaintext  # raw bytes

def decrypt_seed_hexstr_from_b64(encrypted_seed_b64: str) -> str:
    return decrypt_seed_b64(encrypted_seed_b64).hex()

# ------------------------------
# REQUIRED BY FastAPI main.py
# ------------------------------
def decrypt_seed(encrypted_seed_b64: str) -> str:
    """
    Wrapper used by FastAPI. Returns the decrypted seed as a UTF-8 string.
    """
    raw = decrypt_seed_b64(encrypted_seed_b64)
    try:
        return raw.decode()     # if seed is UTF-8 text
    except:
        return raw.hex()        # fallback if seed is binary


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 decrypt_seed.py <base64_encrypted_seed>")
        sys.exit(1)
    b64 = sys.argv[1]
    print(decrypt_seed_hexstr_from_b64(b64))
