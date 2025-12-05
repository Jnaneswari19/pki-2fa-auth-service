from totp import generate_totp
from datetime import datetime

def main():
    # Read the seed
    with open("/data/seed.txt") as f:
        seed = f.read().strip()

    # Generate TOTP
    code = generate_totp(seed)

    # Prepare log line
    line = f"{datetime.now()} 2FA Code: {code}\n"

    # Write to /data/2fa.log
    with open("/data/2fa.log", "a") as log_file:
        log_file.write(line)

    # Print to console
    print(line, end="")

if __name__ == "__main__":
    main()
