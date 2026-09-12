#!/usr/bin/env bash
# AarogyaSathi - one-shot Oracle Cloud Always Free (Ubuntu ARM) provisioning.
# Run as root: sudo bash oracle_setup.sh
set -euo pipefail

APP_DIR="/opt/healthbot"
REPO_URL="${REPO_URL:-https://github.com/salman-mohammad-khan/AarogyaSathi.git}"

echo "[1/8] Updating system..."
apt-get update -y
apt-get upgrade -y
apt-get install -y python3 python3-venv python3-pip git curl ufw unzip

echo "[2/8] Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh
systemctl enable --now ollama

echo "[3/8] Pulling local LLM (qwen3:1.7b, ~1.4GB)..."
ollama pull qwen3:1.7b || echo "model pull failed - cloud API fallback will be used"

echo "[4/8] Cloning project..."
if [ -d "$APP_DIR" ]; then
    cd "$APP_DIR" && git pull || true
else
    git clone "$REPO_URL" "$APP_DIR"
fi
cd "$APP_DIR"

echo "[5/8] Setting up Python venv..."
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

echo "[6/8] Creating .env (edit values AFTER this script finishes!)..."
if [ ! -f .env ]; then
    cp .env.example .env
fi

echo "[7/8] Pre-building the embedding index (downloads LaBSE ~2.2GB, ~2-4 min)..."
mkdir -p data/models data/embeddings
if [ ! -f data/models/lid.176.bin ]; then
    echo "  downloading fastText language model..."
    curl -fsSL -o data/models/lid.176.bin https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
fi
PYTHONPATH=/opt/healthbot ./venv/bin/python scripts/build_index.py
chown -R ubuntu:ubuntu data || true

echo "[8/8] Installing systemd service..."
cp scripts/healthbot.service /etc/systemd/system/healthbot.service
systemctl daemon-reload
systemctl enable --now healthbot

echo "Opening firewall port 8000 (also add an Ingress rule in Oracle console!)."
ufw allow 8000/tcp || true

echo ""
echo "DONE. Chat: http://<VM_PUBLIC_IP>:8000 | Dashboard: /admin | Health: /api/health"
echo "NEXT STEPS:"
echo "  1. Edit /opt/healthbot/.env and add your OLLAMA_API_KEY"
echo "  2. systemctl restart healthbot"
echo "  3. Oracle console -> Networking -> VCN -> Security List -> add Ingress TCP 8000 (0.0.0.0/0)"
echo "  4. Check logs: journalctl -u healthbot -f"
