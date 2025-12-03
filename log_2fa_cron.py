#!/usr/bin/env python3
import os
import time
from datetime import datetime, timezone
import pyotp
import binascii
import base64

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED_PATH = os.path.join(SCRIPT_DIR, "data", "seed.txt")

def read_seed():
    print(f"Looking for seed at: {SEED_PATH}")
    try:
        with open(SEED_PATH, "r") as f:
            hex_seed = f.read().strip()
            return hex_seed
    except FileNotFoundError:
        print("Seed file not found.")
        return None

def generate_totp(hex_seed):
    key_bytes = binascii.unhexlify(hex_seed)
    base32_seed = base64.b32encode(key_bytes).decode("utf-8")
    totp = pyotp.TOTP(base32_seed)
    return totp.now()

def main():
    seed = read_seed()
    if not seed:
        return
    code = generate_totp(seed)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - 2FA Code: {code}")

if __name__ == "__main__":
    main()
