from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

# Load private key
with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Load encrypted seed
with open("encrypted_seed.txt", "r") as f:
    encrypted_seed_b64 = f.read()

encrypted_seed = base64.b64decode(encrypted_seed_b64)

# Decrypt
seed = private_key.decrypt(
    encrypted_seed,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Decrypted Seed:", seed.decode())
