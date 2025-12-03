import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP

    Args:
        encrypted_seed_b64: Base64-encoded ciphertext
        private_key: RSA private key object

    Returns:
        Decrypted hex seed (64-character string)
    """
    # Step 1: Decode base64
    encrypted_seed = base64.b64decode(encrypted_seed_b64)

    # Step 2: RSA/OAEP decrypt
    decrypted_bytes = private_key.decrypt(
        encrypted_seed,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Step 3: Decode to UTF-8 string
    seed_str = decrypted_bytes.decode()

    # Step 4: Validate length
    if len(seed_str) != 64:
        raise ValueError("Decrypted seed is not a 64-character hex string")

    return seed_str

# Load private key and encrypted seed from files
if __name__ == "__main__":
    with open("student_private.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    with open("encrypted_seed.txt", "r") as f:
        encrypted_seed_b64 = f.read().strip()

    seed = decrypt_seed(encrypted_seed_b64, private_key)
    print("✅ Decrypted seed:", seed)