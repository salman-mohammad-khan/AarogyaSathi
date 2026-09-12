import json
import time
import urllib.request

BASE = "http://130.210.56.87:8000"


def chat(msg, sid="o", pincode=None):
    body = {"message": msg, "session_id": sid}
    if pincode:
        body["pincode"] = pincode
    payload = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(BASE + "/api/chat", data=payload, headers={"Content-Type": "application/json"})
    t = time.time()
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.loads(r.read().decode("utf-8"))
    print(f"[{int((time.time()-t)*1000)}ms] {msg!r}")
    print("   " + d["reply"][:400].replace("\n", "\n   "))
    print()


chat("any dengue alert near me?", "o1")
chat("alerts near 110001", "o2")
chat("alerts near 400001", "o3")
chat("alerts near 171001", "o4")
chat("any outbreak in my area?", "o5", pincode="560001")
