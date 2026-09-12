import json
import time
import urllib.request

BASE = "http://130.210.56.87:8000"

CASES = [
    "fact check: garlic cures dengue",
    "fact check: vaccines cause autism",
    "fact check: chewing aspirin during a heart attack helps",
    "fact check: मोबाइल फोन से ब्रेन कैंसर होता है",
]

for msg in CASES:
    payload = json.dumps({"message": msg, "session_id": "fc_reg"}).encode("utf-8")
    req = urllib.request.Request(BASE + "/api/chat", data=payload, headers={"Content-Type": "application/json"})
    t = time.time()
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read().decode("utf-8"))
    first = d["reply"].split("\n")[0] if d["reply"] else ""
    print(f"[{int((time.time()-t)*1000)}ms] {msg!r}")
    print("   " + first[:120])
