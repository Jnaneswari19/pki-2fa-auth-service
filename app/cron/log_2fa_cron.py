from totp import generate_totp
from datetime import datetime

def main():
    # Step 1: Read the Base32 seed
    with open("/data/seed.txt") as f:
        seed = f.read().strip()

    # Step 2: Generate TOTP
    code = generate_totp(seed)

    # Step 3: Prepare log line
    line = f"{datetime.now()} 2FA Code: {code}\n"

    # Step 4: Append to log file
    with open("/data/2fa.log", "a") as log_file:
        log_file.write(line)

    # Optional: also print to console
    print(line, end="")

if __name__ == "__main__":
    main()
