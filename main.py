from fastapi import FastAPI
from pydantic import BaseModel
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import os

app = FastAPI()

class SeedRequest(BaseModel):
    encrypted_seed: str

@app.post("/decrypt-seed")
async def decrypt_seed_endpoint(req: SeedRequest):
    try:
        # Load private key
        with open("student_private.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )

        # Decode base64
        encrypted_seed = base64.b64decode(req.encrypted_seed)

        # Decrypt using RSA/OAEP-SHA256
        decrypted_bytes = private_key.decrypt(
            encrypted_seed,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Convert to string
        seed_str = decrypted_bytes.decode()

        # Validate length
        if len(seed_str) != 64:
            raise ValueError("Invalid seed length")

        # Save to /data/seed.txt
        os.makedirs("data", exist_ok=True)
        with open("data/seed.txt", "w") as f:
            f.write(seed_str)

        return {"status": "ok"}

    except Exception:
        return {"error": "Decryption failed"}