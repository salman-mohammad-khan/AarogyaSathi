#!/bin/bash
KEY=$(grep '^OLLAMA_API_KEY=' /opt/healthbot/.env | cut -d= -f2)
echo "=== verbose POST, IPv4 forced ==="
curl -4 -v -o /tmp/v.json -w '\nHTTP %{http_code} time %{time_total}s\n' \
  -X POST https://ollama.com/api/chat \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-oss:20b","messages":[{"role":"user","content":"Say OK"}],"stream":false}' 2>&1 | head -40
echo
echo "=== retry default (no -4) ==="
curl -v -o /dev/null -w 'HTTP %{http_code} time %{time_total}s\n' \
  -X POST https://ollama.com/api/chat \
  -H "Authorization: Bearer $KEY" \
  -d '{"model":"gpt-oss:20b","messages":[{"role":"user","content":"Say OK"}],"stream":false}' 2>&1 | head -30
