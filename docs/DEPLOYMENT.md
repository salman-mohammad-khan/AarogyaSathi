# Deployment Guide (non-WhatsApp / cloud hosting)

The bot is a plain FastAPI app — it can run anywhere Python 3.12 runs.

## Option 1: Local Windows (dev/demo) — current setup

```powershell
powershell -File scripts\start_dev.ps1        # starts Ollama + server
# open http://127.0.0.1:8000  (chat)  and  http://127.0.0.1:8000/admin (dashboard)
```

## Option 2: Docker

```bash
docker compose up --build -d
```

## Option 3: Any free-tier cloud (Render / Railway / Fly / Oracle)

1. Push this repo to GitHub (`.env` is gitignored — never commit it).
2. Create the service from the repo. Build command: `pip install -r requirements.txt && python scripts/build_index.py`. Start command: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
3. Set environment variables in the dashboard:
   - `OLLAMA_API_KEY` — Ollama Cloud key (used automatically when no local Ollama exists)
   - `GOOGLE_FACTCHECK_API_KEY` — optional live fact-check
   - `LLM_CLOUD_MODEL=gpt-oss:20b` — cloud model (qwen3:1.7b is not in the cloud catalog)
4. Health check: `GET /api/health` → `{"llm": {"backend": "cloud"}}`

## Notes

- First startup builds the embedding cache (`data/embeddings/*.npy`) — keep that volume
  mounted/persisted, or every cold start re-embeds the corpus (~2-5 min).
- RAM: LaBSE fp16 ~1GB + local LLM ~1.6GB (only if Ollama runs on the same host).
  Cloud-only inference needs just ~1.5GB total.
- WhatsApp/SMS webhooks are added later via the same `/webhook` pattern
  (Phase 4) — no architecture change required.
