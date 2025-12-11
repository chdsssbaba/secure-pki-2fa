import os
import base64
import time
import pyotp
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

app = FastAPI()
SEED_FILE = "/data/seed.txt"
PRIVATE_KEY = "student_private.pem"

class SeedPayload(BaseModel):
    encrypted_seed: str

class VerifyPayload(BaseModel):
    code: str

@app.post("/decrypt-seed")
def decrypt_seed(payload: SeedPayload, response: Response):
    try:
        # Load Private Key
        with open(PRIVATE_KEY, "rb") as f:
            priv_key = serialization.load_pem_private_key(f.read(), password=None)
        
        # Decrypt Seed
        decrypted = priv_key.decrypt(
            base64.b64decode(payload.encrypted_seed),
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        # Save to Volume
        with open(SEED_FILE, "w") as f:
            f.write(decrypted.decode('utf-8'))
        return {"status": "ok"}
    except Exception as e:
        print(f"Decryption Error: {e}")
        response.status_code = 500
        return {"error": "Decryption failed"}

@app.get("/generate-2fa")
def generate_2fa(response: Response):
    if not os.path.exists(SEED_FILE):
        response.status_code = 500
        return {"error": "Seed not decrypted yet"}
    
    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()
    
    # Generate TOTP
    totp = pyotp.TOTP(base64.b32encode(bytes.fromhex(hex_seed)).decode('utf-8'))
    return {"code": totp.now(), "valid_for": totp.interval - (int(time.time()) % totp.interval)}

@app.post("/verify-2fa")
def verify_2fa(payload: VerifyPayload, response: Response):
    if not os.path.exists(SEED_FILE):
        response.status_code = 500
        return {"error": "Seed not decrypted yet"}
    
    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()
        
    totp = pyotp.TOTP(base64.b32encode(bytes.fromhex(hex_seed)).decode('utf-8'))
    # Verify with +/- 30s tolerance
    return {"valid": totp.verify(payload.code, valid_window=1)}