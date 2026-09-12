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
    print(f"  A: {d['reply'][:180].replace(chr(10), ' | ')}")
    print()


sid = "summary_test"

print("=== Rolling summary memory test ===")
chat("I have headache since 2 days", sid)      # msg 1 - symptom probe
chat("also have fever now", sid)                # msg 2 - flow finalize
chat("is that dangerous?", sid)                 # msg 3 - ambiguous, uses summary (updates every 3rd)
chat("should I see a doctor?", sid)             # msg 4 - ambiguous follow-up with summary+history