from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import os, base64

pub = RSA.import_key(open("student_public.pem").read())
cipher = PKCS1_v1_5.new(pub)

seed = os.urandom(20)
print("Dummy seed (hex):", seed.hex())

ct = cipher.encrypt(seed)
print("Ciphertext (base64):", base64.b64encode(ct).decode())
