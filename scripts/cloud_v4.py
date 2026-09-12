import json
import time
import urllib.request

BASE = "http://130.210.56.87:8000"


def chat(msg, sid):
    payload = json.dumps({"message": msg, "session_id": sid}).encode("utf-8")
    req = urllib.request.Request(BASE + "/api/chat", data=payload, headers={"Content-Type": "application/json"})
    t = time.time()
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read().decode("utf-8"))
    print(f"[{int((time.time()-t)*1000)}ms] intent={d['intent']}")
    print(f"  Q: {msg}")
    print(f"  A: {d['reply'][:400].replace(chr(10),' | ')}")
    print()


chat("नमस्ते", "g1")
chat("what is phenylketonuria and its treatment?", "g2")
