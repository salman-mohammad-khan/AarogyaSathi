import json
import time
import urllib.request

payload = json.dumps({"message": "what is dengue?", "session_id": "warm_test"}).encode("utf-8")
req = urllib.request.Request(
    "http://130.210.56.87:8000/api/chat",
    data=payload,
    headers={"Content-Type": "application/json"},
)
t = time.time()
with urllib.request.urlopen(req, timeout=90) as r:
    d = json.loads(r.read().decode("utf-8"))
print(f"FIRST RESPONSE: {int((time.time()-t)*1000)}ms, backend={d['llm_backend']}")
print(d["reply"][:100].replace("\n", " "))
