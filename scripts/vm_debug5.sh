#!/bin/bash
KEY=$(grep '^OLLAMA_API_KEY=' /opt/healthbot/.env | cut -d= -f2)
echo "=== curl with --http1.1 ==="
curl --http1.1 -sS -o /tmp/h1.json -w 'HTTP %{http_code} time %{time_total}s\n' \
  -X POST https://ollama.com/api/chat \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"model":"gpt-oss:20b","messages":[{"role":"user","content":"Say OK"}],"stream":false,"think":false,"options":{"num_predict":20}}'
head -c 400 /tmp/h1.json; echo; echo

echo "=== app's httpx call (as generator does) ==="
cd /opt/healthbot
./venv/bin/python - <<'PYEOF'
import httpx, os
key = os.popen("grep '^OLLAMA_API_KEY=' .env | cut -d= -f2").read().strip()
try:
    r = httpx.post(
        "https://ollama.com/api/chat",
        json={"model":"gpt-oss:20b","messages":[{"role":"user","content":"Say OK"}],"stream":False,"think":False,"options":{"num_predict":20}},
        headers={"Authorization": "Bearer "+key},
        timeout=30,
    )
    print("httpx status:", r.status_code)
    print("body:", r.text[:200])
except Exception as e:
    print("httpx EXCEPTION:", type(e).__name__, str(e)[:300])
PYEOF
