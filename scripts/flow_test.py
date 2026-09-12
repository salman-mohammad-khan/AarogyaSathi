import json
import time
import urllib.request

SESSION = "conv_test_1"

def chat(msg, session):
    payload = json.dumps({"message": msg, "session_id": session}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    start = time.time()
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    ms = int((time.time() - start) * 1000)
    print(f"[{ms}ms] intent={data['intent']} flow={data.get('flow')} gen={data['generator']}")
    print("  Q:", msg)
    print("  A:", data["reply"][:260].replace("\n", " | "))
    print()

print("=== Conversation 1: two-turn symptom flow (Hinglish) ===")
chat("mujhe sar dard hai", SESSION)
chat("2 din se hai, aur bukhar bhi aa raha hai", SESSION)

print("=== Conversation 2: smalltalk + help ===")
chat("who are you", "conv_test_2")
chat("what can you do", "conv_test_2")

print("=== Conversation 3: stomach ache alone -> should probe, not diagnose ===")
chat("I have stomach ache", "conv_test_3")
chat("just started today, no fever", "conv_test_3")
