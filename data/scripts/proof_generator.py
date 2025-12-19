from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import base64

def generate_proof(instructor_pubkey_pem: str, message_bytes: bytes):
    key = RSA.import_key(instructor_pubkey_pem)
    cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
    ciphertext = cipher.encrypt(message_bytes)  # 256 bytes for 2048-bit key
    with open("signature.bin", "wb") as f:
        f.write(ciphertext)
    with open("signature_base64.txt", "w") as f:
        f.write(base64.b64encode(ciphertext).decode("ascii"))
