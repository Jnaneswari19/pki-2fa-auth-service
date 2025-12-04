#!/usr/bin/env python3
import sys
import os
from datetime import datetime

# Add /app to path so Python can find totp.py
sys.path.append('/app')

from totp import generate_totp  # Use your existing totp.py module

SEED_FILE = "/data/seed.txt"

def read_seed():
    try:
        with open(SEED_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def main():
    seed = read_seed()
    if not seed:
        print(f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} 2FA Code: Seed not found")
        return

    try:
        code = generate_totp(seed)
    except Exception as e:
        print(f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} 2FA Code: Error {e}")
        return

    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{timestamp} 2FA Code: {code}")

if __name__ == "__main__":
    main()
