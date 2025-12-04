from fastapi import FastAPI, HTTPException
from decrypt_seed import decrypt_seed
from generate_otp import generate_otp  # matches the function above

app = FastAPI()

# POST /decrypt-seed
@app.post("/decrypt-seed")
def decrypt_seed_route(payload: dict):
    encrypted_seed = payload.get("encrypted_seed")
    if not encrypted_seed:
        raise HTTPException(status_code=400, detail="Missing encrypted_seed")
    return {"seed": decrypt_seed(encrypted_seed)}

# GET /generate-2fa
@app.get("/generate-2fa")
def generate_2fa_route():
    try:
        # Read the decrypted seed from /data/seed.txt
        with open("/data/seed.txt", "r") as f:
            seed = f.read().strip()
        code = generate_otp(seed)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate 2FA: {e}")
    return {"code": code}
