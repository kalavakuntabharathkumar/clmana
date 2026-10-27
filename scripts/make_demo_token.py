import os
import time
import jwt

secret = os.getenv("DEMO_JWT_SECRET")
if not secret:
    raise SystemExit("Set DEMO_JWT_SECRET before creating a local demo token.")
print(jwt.encode({"sub": "demo-reviewer", "exp": int(time.time()) + 900}, secret, algorithm="HS256"))
