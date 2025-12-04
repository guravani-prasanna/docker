from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64

# Load instructor's public key
with open("instructor_public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# Create a 64-character seed
seed = "A" * 64  # replace with any 64-char string

# Encrypt using RSA OAEP SHA256
encrypted = public_key.encrypt(
    seed.encode(),
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Convert to base64 for sending
encrypted_b64 = base64.b64encode(encrypted).decode()

# Save to file
with open("encrypted_seed.txt", "w") as f:
    f.write(encrypted_b64)

print("Encrypted seed saved to encrypted_seed.txt")