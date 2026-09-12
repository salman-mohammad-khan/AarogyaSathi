import json
import time
import urllib.request

BASE = "http://130.210.56.87:8000"

for msg, sid in [("மலேரியா எப்படி பரவுகிறது?", "rt1"), ("డెంగ్యూ లక్షణాలు ఏమిటి?", "rt2")]:
    payload = json.dumps({"message": msg, "session_id": sid}).encode("utf-8")
    req = urllib.request.Request(BASE + "/api/chat", data=payload, headers={"Content-Type": "application/json"})
    t = time.time()
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read().decode("utf-8"))
    print(f"[{int((time.time()-t)*1000)}ms] gen={d['generator']}/{d['llm_backend']}: {d['reply'][:140].replace(chr(10),' ')}")
