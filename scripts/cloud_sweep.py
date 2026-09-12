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
    return d, ms


def show(label, d, ms):
    line = d["reply"][:100].replace("\n", " ")
    print(f"{label:28s} [{ms:5d}ms] gen={d['generator']}/{d['llm_backend']} intent={d['intent']} -> {line}")


tests = [
    ("smalltalk", "who are you", "s1"),
    ("help", "what can you do", "s2"),
    ("vaccination", "vaccines for 6 week baby", "s3"),
    ("outbreak", "any dengue alert near me?", "s4"),
    ("factcheck unknown", "fact check: a magic drink cures every disease", "s5"),
]

for label, msg, sid in tests:
    try:
        d, ms = chat(msg, sid)
        show(label, d, ms)
    except Exception as e:
        print(f"{label:28s} ERROR: {e}")

print("\n--- two-turn symptom flow (English) ---")
d, ms = chat("I have fever and joint pain", "f1")
show("probe", d, ms)
d, ms = chat("since 3 days and also a rash", "f1")
show("final", d, ms)

print("\n--- regional languages ---")
for msg, sid in [
    ("ডেঙ্গু থেকে কীভাবে বাঁচব?", "r_bn"),
    ("மலேரியா எப்படி பரவுகிறது?", "r_ta"),
    ("డెంగ్యూ లక్షణాలు ఏమిటి?", "r_te"),
]:
    try:
        d, ms = chat(msg, sid)
        show(f"lang {sid}", d, ms)
    except Exception as e:
        print(f"lang {sid} ERROR: {e}")
