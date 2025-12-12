from fastapi import FastAPI
from pydantic import BaseModel
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os
import pyotp

app = FastAPI()

class CipherRequest(BaseModel):
    ciphertext: str

class VerifyRequest(BaseModel):
    code: str

@app.post("/decrypt-seed")
def decrypt_seed(request: CipherRequest):
    try:
        private_key = RSA.import_key(open("keys/private.pem").read())
        cipher = PKCS1_OAEP.new(private_key)
        decoded = base64.b64decode(request.ciphertext)
        seed = cipher.decrypt(decoded).decode()

        # Convert to Base32 for pyotp
        base32_seed = base64.b32encode(seed.encode()).decode()

        os.makedirs("data", exist_ok=True)
        with open("data/encrypted_seed.txt", "w") as f:
            f.write(base32_seed)

        return {"seed": seed}
    except Exception as e:
        return {"error": str(e)}

@app.get("/generate-2fa")
def generate_2fa():
    try:
        with open("data/encrypted_seed.txt") as f:
            seed = f.read().strip()
        totp = pyotp.TOTP(seed)
        return {"code": totp.now()}
    except Exception as e:
        return {"error": str(e)}

@app.post("/verify-2fa")
def verify_2fa(request: VerifyRequest):
    try:
        with open("data/encrypted_seed.txt") as f:
            seed = f.read().strip()
        totp = pyotp.TOTP(seed)
        return {"valid": totp.verify(request.code)}
    except Exception as e:
        return {"error": str(e)}
