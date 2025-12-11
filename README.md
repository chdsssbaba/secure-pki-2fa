# Secure PKI-Based 2FA Microservice

A Dockerized microservice that implements secure RSA seed decryption and TOTP (Two-Factor Authentication) generation with a background cron job.

## 📂 Project Structure

```text
/
├── cron/
│   └── 2fa-cron           # Cron schedule (runs every minute)
├── scripts/
│   └── log_2fa_cron.py    # Script that logs the 2FA code
├── app.py                 # API Source Code
├── Dockerfile             # Container definition
├── docker-compose.yml     # Orchestration config
├── requirements.txt       # Dependencies
├── setup_keys.py          # Key generation script
├── get_seed.py            # Script to fetch seed from Instructor API
├── generate_proof.py      # Proof of work generator
├── instructor_public.pem  # Instructor's Public Key
├── encrypted_seed.txt     # The encrypted secret (Committed to repo)
└── README.md              # Documentation
````

-----

## 💻 How to Run (On Any Laptop)

Follow these steps to set up the project on a new machine.

### 1\. Clone & Start

```bash
git clone https://github.com/chdsssbaba/secure-pki-2fa.git
cd secure-pki-2fa
docker-compose up -d --build
```

### 2\. Initialize System (Decrypt Seed)

The database starts empty. You must decrypt the seed to enable 2FA generation.

**Step A:** Create a file named `payload.json` and paste your encrypted seed (from `encrypted_seed.txt`) inside:

```json
{
  "encrypted_seed": "PASTE_CONTENT_FROM_ENCRYPTED_SEED_TXT_HERE"
}
```

**Step B:** Run the decryption command:

```bash
curl -X POST http://localhost:8080/decrypt-seed -H "Content-Type: application/json" -d @payload.json
```

*Expected Output:* `{"status": "ok"}`

-----

## 🧪 How to Test Task Status

Run these commands to verify everything is working correctly.

### 1\. Check API (Generate Code)

Ensure the API returns a valid TOTP code.

```bash
curl http://localhost:8080/generate-2fa
```

*Expected Output:* `{"code": "123456", "valid_for": 25}`

### 2\. Check Verification Logic

Verify the code you just received (replace `123456` with actual code).

```bash
curl -X POST http://localhost:8080/verify-2fa -H "Content-Type: application/json" -d "{\"code\": \"123456\"}"
```

*Expected Output:* `{"valid": true}`

### 3\. Check Background Cron Job

Wait 60 seconds, then check if the cron job is logging to the volume.

```bash
docker exec secure-pki-2fa-app-1 cat /cron/last_code.txt  
```

*Expected Output:* A list of logs with UTC timestamps:
`2025-12-04 10:15:00 - 2FA Code: 894302`

### 4\. Check Persistence

Restart the container and ensure the API still works without re-decrypting.

```bash
docker-compose restart
curl http://localhost:8080/generate-2fa
```

*Expected Output:* A valid code (Not an error).

### To Install Python Packages

```bash
# Create the environment
python -m venv env
```

```bash
# Activate the environment
.\\env\\Scripts\\activate
```

```bash
pip install -r requirements.txt
```