import base64

@app.post("/decrypt-seed")
def decrypt_seed(request: CipherRequest):
    private_key = RSA.import_key(open("keys/private.pem").read())
    cipher = PKCS1_OAEP.new(private_key)
    decoded = base64.b64decode(request.ciphertext)
    seed = cipher.decrypt(decoded).decode()

    # Convert to Base32 for pyotp
    base32_seed = base64.b32encode(seed.encode()).decode()

    os.makedirs("data", exist_ok=True)
    with open("data/encrypted_seed.txt", "w") as f:
        f.write(base32_seed)

    return {"seed": seed}
