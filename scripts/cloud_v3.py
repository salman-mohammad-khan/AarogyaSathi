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
    first = d["reply"].split("\n")[0] if d["reply"] else ""
    fc = d.get("factcheck") or {}
    print(f"[{int((time.time()-t)*1000)}ms] intent={d['intent']} src={d.get('llm_backend')}")
    print(f"  Q: {msg}")
    print(f"  A: {d['reply'][:240].replace(chr(10),' | ')}")
    print()


chat("How to check if I have a STD?", "s1")
chat("नमस्ते", "s2")
chat("what is migraine and how to treat it?", "s3")
chat("I have chest pain and can't breathe", "s4")
chat("drinking kadha boosts immunity", "s5")
