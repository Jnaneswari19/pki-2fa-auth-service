import base64
import subprocess
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# 1. Get latest commit hash
commit_hash = (
    subprocess.check_output(["git", "log", "-1", "--format=%H"])
    .decode()
    .strip()
)

print("Commit Hash:", commit_hash)

# 2. Load student private key
with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
    )

# 3. Sign commit hash using RSA-PSS SHA256
signature = private_key.sign(
    commit_hash.encode("utf-8"),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH,
    ),
    hashes.SHA256(),
)

# 4. Load instructor public key
with open("instructor_public.pem", "rb") as f:
    instructor_public_key = serialization.load_pem_public_key(f.read())

# 5. Encrypt signature using RSA-OAEP SHA256
ciphertext = instructor_public_key.encrypt(
    signature,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)

# 6. Base64 encode ciphertext
encrypted_signature_b64 = base64.b64encode(ciphertext).decode()

print("\n===== FINAL SUBMISSION OUTPUT =====")
print("Commit Hash:", commit_hash)
print("Encrypted Signature (Base64):")
print(encrypted_signature_b64)
print("====================================")
