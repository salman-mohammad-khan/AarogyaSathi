#!/bin/bash
# Make Ollama keep models loaded indefinitely + reload on boot.
set -e

echo "[1] Setting OLLAMA_KEEP_ALIVE=-1 system-wide for the ollama service..."
mkdir -p /etc/systemd/system/ollama.service.d
cat > /etc/systemd/system/ollama.service.d/keepalive.conf <<'EOF'
[Service]
Environment="OLLAMA_KEEP_ALIVE=-1"
EOF
systemctl daemon-reload

echo "[2] Restarting ollama to apply..."
systemctl restart ollama
sleep 6

echo "[3] Loading qwen3 model (warmup)..."
curl -s http://localhost:11434/api/generate \
  -d '{"model":"qwen3:1.7b","prompt":"hi","stream":false,"options":{"num_predict":3}}' \
  -o /dev/null -w 'warmup HTTP %{http_code}\n'

echo "[4] Model status (should say 'Forever' / 'Until stopped'):"
ollama ps
