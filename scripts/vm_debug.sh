#!/bin/bash
KEY=$(grep '^OLLAMA_API_KEY=' /opt/healthbot/.env | cut -d= -f2)
echo "=== CLOUD API test (gpt-oss:20b) ==="
curl -s -o /tmp/c.json -w 'HTTP %{http_code}  time %{time_total}s\n' \
  -X POST https://ollama.com/api/chat \
  -H "Authorization: Bearer $KEY" \
  -d '{"model":"gpt-oss:20b","messages":[{"role":"user","content":"Say OK"}],"stream":false,"think":false,"options":{"num_predict":20}}'
head -c 400 /tmp/c.json; echo; echo

echo "=== LOCAL Ollama Tamil test ==="
curl -s -o /tmp/t.json -w 'HTTP %{http_code}  time %{time_total}s\n' \
  -X POST http://localhost:11434/api/chat \
  -d '{"model":"qwen3:1.7b","messages":[{"role":"user","content":"மலேரியா எப்படி பரவுகிறது? சுருக்கமாக பதில்"}],"stream":false,"options":{"num_predict":80}}'
head -c 400 /tmp/t.json; echo
