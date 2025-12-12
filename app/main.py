from fastapi import FastAPI
from app.generate_otp import generate_totp   # fixed import
import os

app = FastAPI()

@app.get("/generate-2fa")
def generate_2fa():
    secret = "JBSWY3DPEHPK3PXP"  # example secret
    code = generate_totp(secret)
    return {"2fa_code": code}
