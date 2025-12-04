import pyotp

with open("data/seed.txt") as f:
    seed = f.read().strip()

totp = pyotp.TOTP(seed)
print(totp.now())
