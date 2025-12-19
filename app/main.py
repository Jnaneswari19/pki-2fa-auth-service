from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

from app.storage import ensure_dirs, file_exists
from app.crypto_rsa import decrypt_base64_ciphertext_with_student
from app.totp_service import set_seed, generate_code, verify_code
from app.config import SEED_PATH, STUDENT_PRIV_PATH, STUDENT_PUB_PATH, API_PORT

app = FastAPI(title="PKI 2FA Auth Service", version="1.0.0")

class CipherRequest(BaseModel):
    ciphertext_b64: str = Field(..., description="Base64 RSA ciphertext block")
    padding: str = Field("OAEP", description="RSA padding: OAEP or PKCS1v15")

class VerifyRequest(BaseModel):
    code: str = Field(..., min_length=6, max_length=10)

@app.on_event("startup")
def startup():
    ensure_dirs()
    if not file_exists(STUDENT_PRIV_PATH) or not file_exists(STUDENT_PUB_PATH):
        raise RuntimeError("student_private.pem or student_public.pem not found in container")

@app.post("/decrypt-seed")
def decrypt_seed(req: CipherRequest):
    try:
        pt = decrypt_base64_ciphertext_with_student(req.ciphertext_b64, req.padding)
        seed_hex = pt.hex()
        set_seed(seed_hex)
        return {"status": "ok", "seed_preview": seed_hex[:16]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"decrypt_failed: {e}")

@app.get("/generate-2fa")
def generate_2fa():
    if not file_exists(SEED_PATH):
        raise HTTPException(status_code=400, detail="seed_missing")
    code = generate_code()
    return {"code": code}

@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    if not file_exists(SEED_PATH):
        raise HTTPException(status_code=400, detail="seed_missing")
    valid = verify_code(req.code.strip())
    return {"valid": valid}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=API_PORT, reload=False)
