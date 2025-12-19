# Generates 4096-bit RSA keys with e=65537 and writes student_private.pem and student_public.pem
from Crypto.PublicKey import RSA

def generate_rsa_keypair(key_size: int = 4096):
    key = RSA.generate(key_size, e=65537)
    return key, key.publickey()

if __name__ == "__main__":
    priv, pub = generate_rsa_keypair(4096)
    with open("student_private.pem", "wb") as f:
        f.write(priv.export_key(format="PEM"))
    with open("student_public.pem", "wb") as f:
        f.write(pub.export_key(format="PEM"))
    print("Generated student_private.pem and student_public.pem (4096-bit, e=65537). Commit them to Git.")
