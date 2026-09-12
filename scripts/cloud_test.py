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
    print(f"[{int((time.time()-t)*1000)}ms] {d['generator']}/{d['llm_backend']} {d['intent']}: {d['reply'][:90].replace(chr(10),' ')}")


chat("hi", "a1")
chat("tell me about dengue", "a2")
chat("fact check: garlic cures dengue", "a3")
chat("डेंगू से कैसे बचें?", "a4")
chat("mujhe bukhar aur sar dard hai", "a5")
