import json
import time
import urllib.request

BASE = "http://130.210.56.87:8000"

CASES = [
    ("drinking homemade kadha boosts immunity to fight diseases", "claim-kadha"),
    ("garlic cures dengue", "claim-garlic"),
    ("turmeric cures cancer", "claim-turmeric"),
    ("I have fever", "symptom"),
    ("how to prevent dengue", "question"),
    ("what are dengue symptoms", "question2"),
    ("kadha se immunity badhti hai", "claim-hindi"),
]

for msg, sid in CASES:
    payload = json.dumps({"message": msg, "session_id": sid}).encode("utf-8")
    req = urllib.request.Request(BASE + "/api/chat", data=payload, headers={"Content-Type": "application/json"})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read().decode("utf-8"))
        first = d["reply"].split("\n")[0] if d["reply"] else ""
        fc = d.get("factcheck") or {}
        print(f"[{int((time.time()-t)*1000)}ms] intent={d['intent']} {msg!r}")
        print(f"    verdict={fc.get('verdict')} | {first[:130]}")
    except Exception as e:
        print(f"[ERR] {msg!r}: {e}")
    print()
