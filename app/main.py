from fastapi import FastAPI
from generate_otp import generate_totp

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "PKI 2FA Microservice Running"}

@app.get("/2fa")
def get_2fa():
    from pathlib import Path
    seed_file = Path("/data/seed.txt")
    if not seed_file.exists():
        return {"error": "Seed file missing"}
    
    seed = seed_file.read_text().strip()
    code = generate_totp(seed)
    
    # Log code
    log_file = Path("/data/2fa.log")
    log_file.write_text(f"{code}\n", append=True)
    
    return {"2FA_code": code}
