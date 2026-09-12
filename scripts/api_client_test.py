import json
import time
import urllib.request

CASES = [
    "डेंगू से कैसे बचें?",
    "fact check: शहद नवजात के लिए अच्छा है",
    "fact check: मोबाइल फोन से ब्रेन कैंसर होता है",
    "మలేరియా ఎలా వ్యాపిస్తుంది",
    "I have fever, body pain and joint pain",
    "vaccines during pregnancy",
]

for msg in CASES:
    payload = json.dumps({"message": msg}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    start = time.time()
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    ms = int((time.time() - start) * 1000)
    line = data["reply"].replace("\n", " | ")
    print(f"--- [{ms}ms] intent={data['intent']} lang={data['language']}")
    print(f"    Q: {msg}")
    print(f"    A: {line[:230]}")
