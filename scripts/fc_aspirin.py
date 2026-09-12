import json
import time
import urllib.request

BASE = "http://130.210.56.87:8000"

for msg in ["fact check: chewing aspirin during a heart attack helps", "fact check: aspirin helps during heart attack"]:
    payload = json.dumps({"message": msg, "session_id": "fc_asp"}).encode("utf-8")
    req = urllib.request.Request(BASE + "/api/chat", data=payload, headers={"Content-Type": "application/json"})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read().decode("utf-8"))
        fc = d.get("factcheck") or {}
        print(f"[{int((time.time()-t)*1000)}ms] verdict={fc.get('verdict')} intent={d['intent']}")
        print("   " + d["reply"][:220].replace("\n", " "))
    except Exception as e:
        print(f"[{int((time.time()-t)*1000)}ms] FAILED: {e}")
