import json
import urllib.request

BASE = "http://130.210.56.87:8000"


def chat(msg, sid):
    payload = json.dumps({"message": msg, "session_id": sid}).encode("utf-8")
    req = urllib.request.Request(BASE + "/api/chat", data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.loads(r.read().decode("utf-8"))
    print(f"intent={d['intent']} flow={d.get('flow')}")
    print(f"  Q: {msg}")
    print(f"  A: {d['reply'][:260].replace(chr(10), ' | ')}")
    print()


print("=== neck pain full flow ===")
chat("my neck pains", "np1")
chat("neck pain is from 2 days, no fever or vomiting", "np1")
print("=== stoamch ache still works ===")
chat("I have stoamch ache", "np2")
print("=== back pain ===")
chat("my back hurts since a week", "np3")