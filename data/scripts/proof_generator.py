from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import base64

def generate_proof():
    # Load the new 2048-bit public key
    with open("public.pem", "rb") as f:
        pubkey = RSA.import_key(f.read())
    cipher = PKCS1_OAEP.new(pubkey, hashAlgo=SHA256)

    # Use commit hash or challenge string as message
    message = b"commit-proof"
    ciphertext = cipher.encrypt(message)

    # Write binary proof
    with open("signature.bin", "wb") as f:
        f.write(ciphertext)

    # Write base64 proof
    with open("signature_base64.txt", "w") as f:
        f.write(base64.b64encode(ciphertext).decode("ascii"))

if __name__ == "__main__":
    generate_proof()
