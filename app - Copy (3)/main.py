from fastapi import FastAPI
from generate_otp import generate_totp

app = FastAPI()

@app.get("/otp")
def get_otp():
    # read seed from file
    with open("/data/seed.txt", "r") as f:
        hex_seed = f.read().strip()

    otp = generate_totp(hex_seed)
    return {"otp": otp}
