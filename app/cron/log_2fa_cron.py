from totp import generate_totp
from datetime import datetime
from pathlib import Path

def main():
    seed_file = Path("/data/seed.txt")
    if not seed_file.exists():
        print("Seed file missing")
        return
    
    seed = seed_file.read_text().strip()
    code = generate_totp(seed)
    
    log_file = Path("/data/2fa.log")
    line = f"{datetime.now()} 2FA Code: {code}\n"
    log_file.write_text(line, append=True)
    print(line, end="")

if __name__ == "__main__":
    main()
