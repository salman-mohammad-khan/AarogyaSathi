# AarogyaSathi — AI-Driven Public Health Chatbot for Disease Awareness

Minor project (ES-451) for SIH-25049: a multilingual, NLP/ML-powered public-health
chatbot that delivers verified preventive-health information, symptom awareness,
vaccination schedules, outbreak alerts and **health-forward verification (myth-vs-fact)**
over WhatsApp/SMS, built for rural and semi-urban India.

> Awareness system only — it is NOT a doctor and never diagnoses.

## Features

| Module | Description |
|---|---|
| NLP engine | Language detection (fastText lid.176), intent classification (TF-IDF + Logistic Regression), symptom/red-flag entity extraction |
| RAG generation | **Qwen3-1.7B-Instruct (Ollama)** generates natural-language answers grounded ONLY in retrieved KB context, with sources appended; graceful fallback to template answers if the LLM is unavailable |
| Conversation memory | Session-based multi-turn flow: symptom reports trigger one empathetic clarifying question (duration, fever/vomiting) before listing possible conditions; negation understood ("no fever"); hard intents interrupt the flow |
| Safety-critical paths | Red-flag escalation, fact-check verdicts and the final symptom answer stay deterministic — the LLM never touches them |
| Cross-lingual retrieval | LaBSE multilingual embeddings + lexical boost over the curated knowledge base — understands English, Hindi, Hinglish and regional languages (Telugu/Tamil/Kannada tested) |
| Disease awareness | 14 diseases: symptoms, prevention, first aid, when-to-see-a-doctor, sources (WHO/MoHFW/ICMR) |
| Vaccination | UIP schedule lookups by age/pregnancy + individual vaccine info |
| Fact check | Paste/forward any health message → verdict `VERIFIED / MYTH / PARTLY TRUE / UNVERIFIABLE` with confidence %, explanation, sources, and fear-mongering flag |
| Safety | Red-flag detection (chest pain, snake bite, seizure...) → immediate 108/112 escalation; disclaimer on every answer |
| Channels | Web chat demo UI now; WhatsApp Cloud API + SMS integration next (Phase 4) |
| Surveillance | Syndromic early-warning module (pincode-tagged query spikes) — Phase 3 |

## Architecture

```
User (web / WhatsApp / SMS)
      │
      ▼
FastAPI backend ──► router
                      │ 1. red-flag safety check (always first)
                      │ 2. fact-check trigger detection
                      │ 3. intent classifier (TF-IDF + LogisticRegression, 13 intents)
                      │ 4. entity extraction (symptoms, diseases, vaccines, ages)
                      │ 5. LaBSE cross-lingual retrieval over curated KB
                      │ 6. RAG generation (Qwen3-1.7B via Ollama, grounded in KB context)
                      ▼
        KB (diseases / vaccines / FAQ / myths / alerts, EN+HI) + sources
```

Generation is retrieval-augmented: the LLM receives only the retrieved KB entry as
context and strict system rules (answer only from context, <70 words, user's language,
no diagnosis, no prescriptions). Emergency and fact-check paths stay deterministic.
If Ollama is unreachable, the bot automatically falls back to template answers.

## Setup (Windows)

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
$env:PYTHONPATH = "$PWD"
python scripts/setup.py          # downloads LaBSE (~2.2GB) + lid.176.bin (125MB), one-time
ollama serve                     # start Ollama (needed for LLM answers, optional otherwise)
ollama pull qwen3:1.7b           # ~1.3GB, one-time; qwen3:0.6b works as a lighter alternative
```

## Run

```powershell
$env:PYTHONPATH = "$PWD"
python -m uvicorn app.main:app --port 8000
```

or start everything (Ollama + server) with `scripts/start_dev.ps1`.

Open http://127.0.0.1:8000 — WhatsApp-style chat UI. LLM answers are marked
"AarogyaSathi (AI answer)"; template fallback shows "AarogyaSathi".

RAM footprint: LaBSE fp16 ~1GB + Qwen3-1.7B Q4 ~1.6GB + Python ~0.5GB ≈ 3GB total —
fits the 2 vCPU / 4GB cloud spec from the synopsis.

Optional cloud inference: set `OLLAMA_API_KEY` (from ollama.com) to use Ollama's
hosted API as an automatic fallback when no local Ollama server is reachable.

**Auto-fallback mechanism (verified end-to-end):**
1. Try local Ollama first (`LLM_MODEL`, default `qwen3:1.7b`)
2. If local is down, times out or returns an error → 60s cooldown → retry on
   Ollama Cloud (`LLM_CLOUD_MODEL`, default `gpt-oss:20b` — qwen3:1.7b is not in
   the cloud catalog) using `OLLAMA_API_KEY`
3. If cloud also fails (bad key, quota, network) → deterministic template answers
4. After the cooldown, local is retried automatically and resumes when healthy

`/api/health` reports the active backend (`local`/`cloud`); every chat response
includes `llm_backend`. Note: cloud models may think first — the payload disables
thinking and uses a 600-token budget.

**Testing with an Ollama Cloud API key:**
1. Create an account at ollama.com, then create a key at https://ollama.com/settings/keys
2. Copy `.env.example` to `.env` and paste your key into `OLLAMA_API_KEY=`
3. Stop local Ollama (or just run on a machine without it) and run:
   `python scripts/test_cloud.py` — prints which backend is used and a sample generation

API: `POST /api/chat` with `{"message": "...", "pincode": "..."}` → `{reply, intent, language, latency_ms, factcheck}`.
Swagger: http://127.0.0.1:8000/docs

## Evaluation & Tests

```powershell
python scripts/eval.py      # benchmark report
python -m pytest tests -q   # 20 unit/ML tests
```

Latest benchmark (held-out set, `data/training/eval.json`):

| Suite | Accuracy |
|---|---|
| Intent classification (30 queries, EN/HI/Hinglish) | 100% |
| Cross-lingual retrieval (15 queries) | 100% |
| Health-claim fact check (34 claims) | 100% |
| SIH target | >= 80% |

## Project layout

```
app/core/      NLP: language, embeddings, intent, entities, retriever, safety, router
app/factcheck/ myth-vs-fact verifier (verity scores, source tiers)
app/channels/  WhatsApp / SMS integration (Phase 4)
app/surveillance/ syndromic early-warning (Phase 3)
data/kb/       curated knowledge base (diseases, vaccines, faq, myths, alerts, messages)
data/training/ intent training examples + held-out eval set
web/           WhatsApp-style demo UI
scripts/       setup (model download), eval, smoke tests
```

## Deployment

- **Recommended: Oracle Cloud Always Free** (2 vCPU/12GB, $0 forever) — full step-by-step
  guide in `docs/ORACLE_DEPLOY.md`, one-shot setup script in `scripts/oracle_setup.sh`,
  systemd unit in `scripts/healthbot.service`.
- Docker: `docker compose up -d`
- Generic cloud (Render/Railway): see `docs/DEPLOYMENT.md`

## Roadmap

- Phase 2: fact-check module (done) + optional live verification via Google Fact Check Tools API
- Phase 3: syndromic surveillance (pincode-tagged symptom-query spikes → early-warning)
- Phase 4: Meta WhatsApp Cloud API webhook + Twilio SMS + free-tier cloud deploy (Render/Railway), ngrok for local demo

## Sources

WHO fact sheets, MoHFW/NHM/IDSP/NTEP/NACO advisories, PIB Fact Check, ICMR — curated
for awareness purposes. Every answer carries a source list and a medical disclaimer.
