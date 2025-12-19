# Encrypts your latest commit hash with instructor_public.pem and writes signature.bin (OAEP/SHA256)
import subprocess, base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

def get_latest_commit_hash():
    return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()

def load_instructor_public():
    with open("instructor_public.pem", "rb") as f:
        return RSA.import_key(f.read())

if __name__ == "__main__":
    commit = get_latest_commit_hash().encode()
    key = load_instructor_public()
    cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
    ct = cipher.encrypt(commit)
    with open("signature.bin", "wb") as f:
        f.write(ct)
    with open("signature_base64.txt", "w", encoding="utf-8") as f:
        f.write(base64.b64encode(ct).decode())
    print("Wrote signature.bin and signature_base64.txt using OAEP/SHA256.")
