import json
import time
import urllib.request

BASE = "http://127.0.0.1:8000"


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def post(path, body):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


print("=== 1. Seed demo outbreak (pincode 110001) ===")
alerts = post("/api/surveillance/seed", {})
print("new alerts:", json.dumps(alerts, indent=2)[:400])

print("\n=== 2. Chat with pincode -> event recorded + spike check ===")
r = post("/api/chat", {"message": "I have loose motions", "pincode": "110001", "session_id": "surv1"})
print("flow:", r["flow"], "| intent:", r["intent"])

print("\n=== 3. Stats ===")
stats = get("/api/stats")
print("messages_24h:", stats["messages_24h"], "| symptom_events_24h:", stats["symptom_events_24h"], "| alerts_7d:", stats["alerts_7d"])

print("\n=== 4. Bengali + Tamil + Telugu + Kannada queries ===")
for msg, exp in [
    ("ডেঙ্গু থেকে কীভাবে বাঁচব?", "bn"),
    ("மலேரியா எப்படி பரவுகிறது?", "ta"),
    ("డెంగ్యూ లక్షణాలు ఏమిటి?", "te"),
    ("ಕರೋನಾ ಲಕ್ಷಣಗಳು ಯಾವುವು?", "kn"),
]:
    r = post("/api/chat", {"message": msg, "session_id": "lang_" + exp})
    print(f"[{exp}] intent={r['intent']} lang={r['language']} backend={r['llm_backend']} | {r['reply'][:110].replace(chr(10),' | ')}")

print("\n=== 5. Fact-check unknown claim (no Google key -> curated fallback) ===")
r = post("/api/chat", {"message": "fact check: some random new drink cures all diseases", "session_id": "fc_unknown"})
print("verdict:", r["factcheck"]["verdict"], "| confidence:", r["factcheck"]["confidence"])
