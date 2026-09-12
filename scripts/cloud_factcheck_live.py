import json
import time
import urllib.request

BASE = "http://130.210.56.87:8000"

CASES = [
    "fact check: drinking cow urine cures coronavirus",
    "fact check: hot water and lemon kills coronavirus instantly",
    "fact check: eating onions and garlic prevents covid",
]

for msg in CASES:
    payload = json.dumps({"message": msg, "session_id": "fc_live"}).encode("utf-8")
    req = urllib.request.Request(BASE + "/api/chat", data=payload, headers={"Content-Type": "application/json"})
    t = time.time()
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read().decode("utf-8"))
    print(f"[{int((time.time()-t)*1000)}ms] Q: {msg}")
    print("   " + d["reply"][:380].replace("\n", "\n   "))
    print()
