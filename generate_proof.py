import base64
import sys
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def generate_proof(commit_hash):
    # Load keys
    with open("student_private.pem", "rb") as f:
        priv = serialization.load_pem_private_key(f.read(), password=None)
    with open("instructor_public.pem", "rb") as f:
        pub = serialization.load_pem_public_key(f.read())
    
    # Sign Commit Hash
    signature = priv.sign(
        commit_hash.strip().encode('utf-8'),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    
    # Encrypt Signature
    encrypted_sig = pub.encrypt(
        signature,
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    
    # Print Result
    print("\n--- Encrypted Signature ---")
    print(base64.b64encode(encrypted_sig).decode('utf-8'))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_proof(sys.argv[1])
    else:
        print("Usage: python generate_proof.py <commit_hash>")