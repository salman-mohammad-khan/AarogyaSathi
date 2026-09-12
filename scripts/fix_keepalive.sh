#!/bin/bash
mkdir -p /etc/systemd/system/ollama.service.d
cat > /etc/systemd/system/ollama.service.d/keepalive.conf <<'EOF'
[Service]
Environment="OLLAMA_KEEP_ALIVE=-1"
EOF
systemctl daemon-reload
systemctl restart ollama
sleep 6
echo "drop-in content:"
cat /etc/systemd/system/ollama.service.d/keepalive.conf
echo "ollama env:"
systemctl show ollama -p Environment
