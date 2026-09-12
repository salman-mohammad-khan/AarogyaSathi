import json
import time
import urllib.request

payload = json.dumps({"message": "tell me about malaria", "session_id": "fallback_test"}).encode("utf-8")
req = urllib.request.Request(
    "http://127.0.0.1:8000/api/chat",
    data=payload,
    headers={"Content-Type": "application/json"},
)
start = time.time()
with urllib.request.urlopen(req, timeout=120) as r:
    d = json.loads(r.read().decode("utf-8"))
print(f"[{int((time.time()-start)*1000)}ms] generator={d['generator']} llm_backend={d['llm_backend']}")
print("reply:", d["reply"][:220].replace("\n", " | "))
