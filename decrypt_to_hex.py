# decrypt_to_hex.py
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Load your private key
with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Load encrypted seed
with open("encrypted_seed.txt", "r") as f:
    encrypted_seed_b64 = f.read().strip()
encrypted_seed = base64.b64decode(encrypted_seed_b64)

# Decrypt seed
seed_bytes = private_key.decrypt(
    encrypted_seed,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Save as hex string for your app
with open("data/seed.txt", "w") as f:
    f.write(seed_bytes.hex())

print("Hex seed written to data/seed.txt")
