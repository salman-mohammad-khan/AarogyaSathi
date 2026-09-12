#!/bin/bash
cd /opt/healthbot
PYTHONPATH=/opt/healthbot ./venv/bin/python - <<'PYEOF'
import os
os.environ.setdefault("PYTHONPATH", "/opt/healthbot")
from app.core import generator
generator.reset_availability()
print("backend():", generator.backend())

ctx = "Disease: malaria. Malaria is spread by Anopheles mosquitoes. Prevention: use nets, remove stagnant water."
q = "மலேரியா எப்படி பரவுகிறது?"
import time
t = time.time()
r = generator.grounded_answer(ctx, q, "ta")
print(f"result after {time.time()-t:.1f}s: last_backend={generator.last_backend()}")
print("reply:", repr(r[:150]) if r else None)

# raw cloud call with the app's exact options to inspect content vs thinking
import httpx
key = os.popen("grep '^OLLAMA_API_KEY=' .env | cut -d= -f2").read().strip()
payload = {
    "model": "gpt-oss:20b",
    "messages": [
        {"role": "system", "content": "You are a health assistant. Answer only from context, under 50 words, in Tamil."},
        {"role": "user", "content": f"CONTEXT:\n{ctx}\n\nQUESTION: {q}"},
    ],
    "stream": False, "think": False,
    "options": {"temperature": 0.1, "num_predict": 600, "num_ctx": 1024, "thinking": {"type": "disabled"}},
}
r2 = httpx.post("https://ollama.com/api/chat", json=payload, headers={"Authorization": "Bearer "+key}, timeout=60)
print("cloud status:", r2.status_code)
d = r2.json()
print("content:", repr((d.get("message") or {}).get("content", "")[:150]))
print("thinking:", repr((d.get("message") or {}).get("thinking", "")[:100]))
PYEOF
