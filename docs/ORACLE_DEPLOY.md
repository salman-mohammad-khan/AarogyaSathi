# Deploying on Oracle Cloud Always Free (recommended target)

Free forever: 2 vCPU / 12GB ARM VM — runs the full stack (LaBSE + local qwen3 + FastAPI + SQLite).
Costs $0 after signup; the credit card is only used for identity verification.

## Step 1 — Sign up (10 min)

1. Go to https://www.oracle.com/cloud/free/ → "Start for free"
2. Fill details + credit card (not charged). Use your real name matching the card.
3. Choose **home region carefully** (fixed forever, free resources live here):
   - For low latency in India try **Mumbai** or **Hyderabad** — but free ARM capacity
     there is often exhausted ("Out of capacity" error). If that happens, retry a few
     times over a day, or pick **Frankfurt / London / Amsterdam / Singapore**.
4. After signup, log in to https://cloud.oracle.com

## Step 2 — Create the VM (10 min)

1. Menu → Compute → Instances → **Create instance**
2. Name: `healthbot`, image: **Ubuntu 24.04**, shape: **Ampere / VM.Standard.A1.Flex**
   → set **2 OCPU / 12 GB** (the Always Free allowance; 1 OCPU/6GB also works but 2/12 is faster)
3. Add your **SSH public key** (generate one if you don't have one:
   `ssh-keygen -t ed25519` on your PC, paste the `.pub` content). This is how you'll log in.
4. Create. Once the instance is **Running**, note its **Public IP**.

## Step 3 — Open the firewall (2 min, easily forgotten!)

In the Oracle console:
1. Instance details → **Attached VNIC** → click the subnet → **Default Security List**
2. **Add Ingress Rules**: `TCP` / port `8000` / source `0.0.0.0/0` (and later 80/443 for WhatsApp)

## Step 4 — Get the code onto the VM

Push this project to a **private GitHub repo** (also useful for your report), then on the VM:

```bash
ssh ubuntu@<PUBLIC_IP>
sudo bash -c "curl -fsSL https://raw.githubusercontent.com/salman-mohammad-khan/AarogyaSathi/main/scripts/oracle_setup.sh -o /tmp/setup.sh"
sudo REPO_URL=https://github.com/salman-mohammad-khan/AarogyaSathi.git bash /tmp/setup.sh
```

Alternatively, upload the project folder with FileZilla/WinSCP to `/opt/healthbot` and
run `sudo bash scripts/oracle_setup.sh` (the script skips cloning if the folder exists).

## Step 5 — Configure and verify

```bash
sudo nano /opt/healthbot/.env        # paste OLLAMA_API_KEY (optional cloud fallback)
sudo systemctl restart healthbot
curl http://localhost:8000/api/health   # {"llm": {"backend": "local"}}
```

Open `http://<PUBLIC_IP>:8000` in your browser — the bot is live on the cloud.

## Managing the machine

```bash
journalctl -u healthbot -f            # logs
sudo systemctl restart healthbot      # restart app
sudo systemctl restart ollama         # restart LLM
```

Stopping when not needed (optional — free tier costs nothing when running):

```bash
# from your PC, after installing OCI CLI and configuring it once:
oci compute instance action --instance-id <OCID> --action STOP
oci compute instance action --instance-id <OCID> --action START
```

## Why this setup

- Local qwen3:1.7b answers English/Hindi for free with zero quota
- `OLLAMA_API_KEY` in `.env` auto-falls back to Ollama Cloud (gpt-oss:20b) for
  regional languages or if local fails — same code, no changes
- systemd keeps the bot running 24/7 (WhatsApp-ready, no cold starts)
- WhatsApp (Phase 4) later needs HTTPS: add Caddy/nginx + Let's Encrypt on port 443
  — the webhook will point to the same app
