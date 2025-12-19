import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.Hash import SHA256
from app.config import STUDENT_PRIV_PATH, STUDENT_PUB_PATH
from app.storage import read_text

def load_student_private():
    pem = read_text(STUDENT_PRIV_PATH)
    return RSA.import_key(pem)

def load_student_public():
    pem = read_text(STUDENT_PUB_PATH)
    return RSA.import_key(pem)

def decrypt_base64_ciphertext_with_student(cipher_b64: str, padding: str = "OAEP") -> bytes:
    """Decrypt base64 ciphertext using student 4096-bit private key."""
    priv = load_student_private()
    cipher_bytes = base64.b64decode(cipher_b64)
    key_bytes = (priv.size_in_bits() + 7) // 8  # 512 bytes for 4096-bit
    if len(cipher_bytes) != key_bytes:
        raise ValueError(f"Ciphertext length {len(cipher_bytes)} != key size {key_bytes}")

    if padding.upper() == "OAEP":
        cipher = PKCS1_OAEP.new(priv, hashAlgo=SHA256)
        return cipher.decrypt(cipher_bytes)
    elif padding.upper() == "PKCS1V15":
        cipher = PKCS1_v1_5.new(priv)
        sentinel = b"__RSA_DECRYPT_FAIL__"
        pt = cipher.decrypt(cipher_bytes, sentinel)
        if pt == sentinel:
            raise ValueError("RSA PKCS#1 v1.5 decryption failed")
        return pt
    else:
        raise ValueError("Unsupported padding")
