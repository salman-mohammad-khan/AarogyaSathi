import json
import urllib.request

BASE = "http://130.210.56.87:8000"


def chat(msg, sid):
    payload = json.dumps({"message": msg, "session_id": sid}).encode("utf-8")
    req = urllib.request.Request(BASE + "/api/chat", data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read().decode("utf-8"))
    print(f"intent={d['intent']} | Q: {msg}")
    print("  A:", d["reply"][:260].replace("\n", " | "))
    print()


sid = "lang_welcome_test"

print("=== 1. English first (welcome in EN + answer) ===")
chat("what is dengue", sid)

print("=== 2. Same English again (NO welcome repeat) ===")
chat("what is malaria", sid)

print("=== 3. Hindi first time (welcome in HI + probe) ===")
chat("मुझे बुखार है", sid)

print("=== 4. Hindi second time (NO welcome repeat) ===")
chat("2 दिन से, उल्टी भी है", sid)

print("=== 5. Tamil first time (welcome in TA) ===")
chat("மலேரியா எப்படி பரவுகிறது?", sid)