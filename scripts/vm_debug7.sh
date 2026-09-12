#!/bin/bash
cd /opt/healthbot
echo "=== deployed config check ==="
grep -n "CLOUD_TIMEOUT" app/config.py
echo "=== raw cloud call with app's EXACT system prompt ==="
PYTHONPATH=/opt/healthbot ./venv/bin/python - <<'PYEOF'
import os, time, httpx
from app.core import generator

key = os.popen("grep '^OLLAMA_API_KEY=' .env | cut -d= -f2").read().strip()
ctx = "Disease: malaria. Malaria is spread by Anopheles mosquitoes. Prevention: use nets, remove stagnant water."
q = "மலேரியா எப்படி பரவுகிறது?"
user_prompt = f"CONTEXT:\n{ctx}\n\nQUESTION: {q}\n\nAnswer in Tamil. Keep it under 70 words."

payload = {
    "model": "gpt-oss:20b",
    "messages": [
        {"role": "system", "content": generator.SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ],
    "stream": False, "think": False,
    "options": {"temperature": 0.1, "num_predict": 600, "num_ctx": 1024, "thinking": {"type": "disabled"}},
}
t = time.time()
try:
    r = httpx.post("https://ollama.com/api/chat", json=payload, headers={"Authorization": "Bearer "+key}, timeout=120)
    print(f"status={r.status_code} after {time.time()-t:.1f}s")
    d = r.json()
    print("content:", repr((d.get('message') or {}).get('content','')[:120]))
    print("done_reason:", d.get("done_reason"), "eval_count:", d.get("eval_count"))
except Exception as e:
    print(f"EXCEPTION after {time.time()-t:.1f}s:", type(e).__name__, str(e)[:200])
PYEOF
