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
    print(f"[{int((time.time()-t)*1000)}ms] intent={d['intent']} flow={d.get('flow')} src={d['llm_backend']}")
    print(f"  Q: {msg}")
    print(f"  A: {d['reply'][:220].replace(chr(10), ' | ')}")
    print()


print("=== 1. neck pain flow (LLM analysis expected) ===")
chat("my neck pains", "h1")
chat("neck pain is from 2 days, no fever or vomiting", "h1")

print("=== 2. fever + headache flow ===")
chat("I have fever and headache", "h2")
chat("since 3 days", "h2")

print("=== 3. normal questions ===")
chat("what is dengue?", "h3")
chat("vaccines for 6 week baby", "h4")