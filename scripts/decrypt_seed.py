from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# Paths to your keys and encrypted seed
ENCRYPTED_SEED_FILE = Path("/data/encrypted_seed.txt")
PRIVATE_KEY_FILE = Path("student_private.pem")
OUTPUT_SEED_FILE = Path("/data/seed.txt")

def decrypt_seed():
    # Read the private key
    with open(PRIVATE_KEY_FILE, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )

    # Read the encrypted seed
    encrypted_seed = ENCRYPTED_SEED_FILE.read_bytes()

    # Decrypt the seed
    decrypted_seed = private_key.decrypt(
        encrypted_seed,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Write the decrypted seed to seed.txt
    OUTPUT_SEED_FILE.write_text(decrypted_seed.decode("utf-8"))
    print(f"Decrypted seed written to {OUTPUT_SEED_FILE}")

if __name__ == "__main__":
    decrypt_seed()
