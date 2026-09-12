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
    ms = int((time.time() - t) * 1000)
    print(f"[{ms}ms] intent={d['intent']} | {d['reply'][:100].replace(chr(10), ' | ')}")


print("--- red flag (must be instant, no LLM) ---")
chat("my father has chest pain and can't breathe", "s1")
print("--- fact check prefix (must be verdict) ---")
chat("fact check: garlic cures dengue", "s2")
print("--- unclear message ---")
chat("xyz qwerty something", "s3")
print("--- fallback with memory: headache then 'is it serious?' ---")
chat("I have headache", "s4")
chat("2 days", "s4")
chat("is it serious?", "s4")