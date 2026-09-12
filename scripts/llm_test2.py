import json
import time
import urllib.request

CASES = [
    "डेंगू से कैसे बचें?",
    "mujhe bukhar aur sar dard hai",
    "I have fever, joint pain and rash",
]

for msg in CASES:
    payload = json.dumps({"message": msg}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    start = time.time()
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    ms = int((time.time() - start) * 1000)
    print(f"=== [{ms}ms] gen={data['generator']}")
    print("Q:", msg)
    print("A:", data["reply"][:320].replace("\n", " | "))
