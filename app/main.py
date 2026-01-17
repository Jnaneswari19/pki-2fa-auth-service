from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64

app = FastAPI()

# Load private key once at startup
with open("/app/student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

class SeedRequest(BaseModel):
    ciphertext_b64: str

@app.post("/decrypt-seed")
def decrypt_seed(req: SeedRequest):
    try:
        # Decode base64
        ciphertext = base64.b64decode(req.ciphertext_b64)

        # Decrypt with private key
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Save to file
        with open("/app/data/seed.txt", "wb") as f:
            f.write(plaintext)

        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"decrypt_failed: {e}")
