import requests
import json

# --- CONFIGURATION ---
STUDENT_ID = "23A91A05E9"
REPO_URL = "https://github.com/chdsssbaba/secure-pki-2fa" 
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

def get_seed():
    try:
        with open("student_public.pem", "r") as f:
            public_key = f.read().strip()
        
        print("Requesting encrypted seed...")
        response = requests.post(API_URL, json={
            "student_id": STUDENT_ID,
            "github_repo_url": REPO_URL,
            "public_key": public_key
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "encrypted_seed" in data:
                with open("encrypted_seed.txt", "w") as f:
                    f.write(data["encrypted_seed"])
                print("✅ Success! Seed saved to 'encrypted_seed.txt'")
            else:
                print(f"⚠️ API returned: {data}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    get_seed()