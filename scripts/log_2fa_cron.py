import base64
import pyotp
import datetime
import sys

try:
    with open("/data/seed.txt", "r") as f:
        hex_seed = f.read().strip()
    
    totp = pyotp.TOTP(base64.b32encode(bytes.fromhex(hex_seed)).decode('utf-8'))
    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    
    # Print to stdout (which cron captures)
    print(f"{now_utc} - 2FA Code: {totp.now()}")

except Exception as e:
    print(f"Cron Error: {e}", file=sys.stderr)