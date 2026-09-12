#!/bin/bash
KEY=$(grep '^OLLAMA_API_KEY=' /opt/healthbot/.env | cut -d= -f2)
curl -4 -sS -o /tmp/final.json -w 'FINAL: HTTP %{http_code} time %{time_total}s\n' \
  -X POST https://ollama.com/api/chat \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-oss:20b","messages":[{"role":"user","content":"Say OK"}],"stream":false,"think":false,"options":{"num_predict":20}}'
echo "--- response body ---"
cat /tmp/final.json 2>/dev/null | head -c 600
echo
