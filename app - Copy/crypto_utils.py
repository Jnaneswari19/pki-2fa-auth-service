import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP (SHA-256)
    Returns: decrypted 64-character hex seed
    """

    # 1. Base64 decode the ciphertext
    ciphertext = base64.b64decode(encrypted_seed_b64)

    # 2. RSA/OAEP decrypt (SHA-256, MGF1-SHA-256)
    decrypted_bytes = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 3. Convert decrypted bytes to UTF-8 string
    seed_hex = decrypted_bytes.decode("utf-8")

    # 4. Validate: must be 64-character hexadecimal
    if len(seed_hex) != 64:
        raise ValueError("Seed must be 64 characters")

    valid_chars = "0123456789abcdef"
    if any(c not in valid_chars for c in seed_hex.lower()):
        raise ValueError("Seed contains non-hex characters")

    # 5. Return the decrypted hex seed
    return seed_hex
