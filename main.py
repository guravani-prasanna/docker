from fastapi import FastAPI
from pydantic import BaseModel
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import os
import pyotp   # <-- add this

app = FastAPI()

class SeedRequest(BaseModel):
    encrypted_seed: str

class CodeRequest(BaseModel):
    code: str

@app.post("/decrypt-seed")
async def decrypt_seed_endpoint(req: SeedRequest):
    try:
        with open("student_private.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )

        encrypted_seed = base64.b64decode(req.encrypted_seed)

        decrypted_bytes = private_key.decrypt(
            encrypted_seed,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        seed_str = decrypted_bytes.decode()

        if len(seed_str) != 64:
            raise ValueError("Invalid seed length")

        os.makedirs("data", exist_ok=True)
        with open("data/seed.txt", "w") as f:
            f.write(seed_str)

        return {"status": "ok"}

    except Exception:
        return {"error": "Decryption failed"}

@app.get("/generate-2fa")
async def generate_2fa():
    try:
        with open("data/seed.txt", "r") as f:
            seed = f.read().strip()
        totp = pyotp.TOTP(seed)
        return {"code": totp.now()}
    except Exception:
        return {"error": "Seed not found"}

@app.post("/verify-2fa")
async def verify_2fa(req: CodeRequest):
    try:
        with open("data/seed.txt", "r") as f:
            seed = f.read().strip()
        totp = pyotp.TOTP(seed)
        if totp.verify(req.code, valid_window=1):  # <-- allow +/- 30s drift
            return {"status": "valid"}
        else:
            return {"status": "invalid"}
    except Exception:
        return {"error": "Seed not found"}