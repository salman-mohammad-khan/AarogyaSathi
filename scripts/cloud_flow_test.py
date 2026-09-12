import json
import time
import urllib.request

BASE = "http://130.210.56.87:8000"


def chat(msg, sid):
    payload = json.dumps({"message": msg, "session_id": sid}).encode("utf-8")
    req = urllib.request.Request(BASE + "/api/chat", data=payload, headers={"Content-Type": "application/json"})
    t = time.time()
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.loads(r.read().decode("utf-8"))
    print(f"[{int((time.time()-t)*1000)}ms] intent={d['intent']} flow={d.get('flow')}")
    print(f"  Q: {msg}")
    print(f"  A: {d['reply'][:200].replace(chr(10), ' | ')}")
    print()


print("=== same session, two turns ===")
chat("I have headache", "m1")
chat("2 days", "m1")
print("=== new session, two turns ===")
chat("I have headache", "m2")
chat("since 2 days and also fever", "m2")