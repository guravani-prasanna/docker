import pyotp
import base64

# Read the hex seed from file
with open("data/seed.txt", "r") as f:
    hex_seed = f.read().strip()

# Convert hex -> bytes
seed_bytes = bytes.fromhex(hex_seed)

# Convert bytes -> base32 string
base32_seed = base64.b32encode(seed_bytes).decode("utf-8")

# Create TOTP generator with base32 seed
totp = pyotp.TOTP(base32_seed)

print("Your current OTP:", totp.now())