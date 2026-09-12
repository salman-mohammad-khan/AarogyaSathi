import json
import urllib.request

BASE = "http://130.210.56.87:8000"

tests = [
    ("garlic cures dengue", "plain claim (should NOT fact-check now)"),
    ("fact check: garlic cures dengue", "explicit prefix (SHOULD fact-check)"),
    ("फैक्ट चेक: लहसुन से डेंगू ठीक होता है", "hindi prefix (SHOULD fact-check)"),
    ("I have stoamch ache", "typo stomach"),
    ("mera pet kharab hai", "colloquial hindi"),
    ("is there a treatment for cat scratch disease in adults", "info question"),
]

for msg, desc in tests:
    payload = json.dumps({"message": msg, "session_id": "s_clean"}).encode("utf-8")
    req = urllib.request.Request(BASE + "/api/chat", data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.loads(r.read().decode("utf-8"))
    fc = d.get("factcheck") or {}
    print(f"[{desc}]")
    print(f"  Q: {msg} -> intent={d['intent']} verdict={fc.get('verdict', '-')}")
    print(f"  A: {d['reply'][:120].replace(chr(10), ' | ')}")
    print()