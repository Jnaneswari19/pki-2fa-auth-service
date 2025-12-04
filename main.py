from fastapi import FastAPI
from totp import generate_totp

app = FastAPI()

# Load seed from file
with open("data/seed.txt", "r") as f:
    SEED = f.read().strip()

@app.get("/generate-otp")
def generate_otp():
    otp = generate_totp(SEED)
    return {"otp": otp}

