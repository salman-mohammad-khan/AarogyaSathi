#!/bin/bash
KEY=$(grep '^OLLAMA_API_KEY=' /opt/healthbot/.env | cut -d= -f2)
echo "key length: ${#KEY}"
echo "key prefix: ${KEY:0:8}..."
echo "=== POST /api/chat ==="
curl -s -o /tmp/c2.json -w 'HTTP %{http_code}  time %{time_total}s\n' \
  -X POST https://ollama.com/api/chat \
  -H "Authorization: Bearer $KEY" \
  -d '{"model":"gpt-oss:20b","messages":[{"role":"user","content":"Say OK"}],"stream":false,"think":false,"options":{"num_predict":20}}'
head -c 500 /tmp/c2.json
echo
echo "=== local qwen3 with think:false (Tamil) ==="
curl -s -o /tmp/t2.json -w 'HTTP %{http_code}  time %{time_total}s\n' \
  -X POST http://localhost:11434/api/chat \
  -d '{"model":"qwen3:1.7b","messages":[{"role":"user","content":"மலேரியா எப்படி பரவுகிறது? சுருக்கமாக பதில்"}],"stream":false,"think":false,"options":{"num_predict":100}}'
head -c 400 /tmp/t2.json
