from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Load public key
public_key = RSA.import_key(open("keys/public.pem").read())
cipher = PKCS1_OAEP.new(public_key)

# Example seed to encrypt
seed = "MYSECRETSEED123"

# Encrypt and base64 encode
ciphertext = cipher.encrypt(seed.encode())
print(base64.b64encode(ciphertext).decode())
