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
    print(f"  A: {d['reply'][:200].replace(chr(10), ' | ')}")
    print()


print("=== 1. Short non-health msg, fresh session (should NOT search web) ===")
chat("2 days", "n1")
print("=== 2. Same-session symptom flow still works ===")
chat("I have headache", "n2")
chat("2 days", "n2")
print("=== 3. Real health question via internet ===")
chat("what causes dengue fever", "n3")