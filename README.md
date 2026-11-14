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
| Safety-critical paths | Red-flag escalation and self-harm responses are rule-based and never call the LLM. Fact-check verdicts come from curated-myth matching first; the LLM only judges live web evidence when no curated myth matches |
| Cross-lingual retrieval | LaBSE multilingual embeddings + lexical boost over the curated knowledge base — understands English, Hindi, Hinglish and regional languages (Telugu/Tamil/Kannada tested) |
| Disease awareness | 14 diseases: symptoms, prevention, first aid, when-to-see-a-doctor, sources (WHO/MoHFW/ICMR) |
| Vaccination | UIP schedule lookups by age/pregnancy + individual vaccine info |
| Fact check | Paste/forward any health message → verdict `VERIFIED / MYTH / PARTLY TRUE / UNVERIFIABLE` with confidence %, explanation, sources, and fear-mongering flag |
| Safety | Red-flag detection (chest pain, snake bite, seizure...) → immediate 108/112 escalation; disclaimer on every answer |
| Channels | Web chat UI; Meta WhatsApp Cloud API webhook (signature-verified, demonstrated on a Meta test number); Twilio adapter included, SMS delivery not verified |
| Surveillance | Syndromic early-warning module (pincode-tagged query spikes) — Phase 3 |

## Architecture

```
User (web / WhatsApp / SMS)
      │
      ▼
FastAPI backend ──► router
                      │ 1. red-flag and self-harm check (always first, rule-based, no LLM)
                      │ 2. fact-check trigger detection
                      │ 3. fast path: intent classifier (TF-IDF + LogisticRegression, 13 intents)
                      │    plus whole-word entity matching (symptoms, diseases, vaccines, ages)
                      │ 4. if the fast path is not confident: LLM structured-JSON understanding
                      │ 5. LaBSE cross-lingual retrieval over the curated KB
                      │ 6. RAG generation (LLM tiers with template fallback, grounded in KB context)
                      ▼
        KB (diseases / vaccines / FAQ / myths / alerts, EN+HI) + sources
```

Generation is retrieval-augmented: the LLM receives only the retrieved KB entry as
context and strict system rules (answer only from context, <70 words, user's language,
no diagnosis, no prescriptions). Emergency and self-harm responses are rule-based and
never call the LLM. Fact-check verdicts come from curated-myth matching first; the LLM
only judges live web evidence when no curated myth matches. If no LLM is reachable,
the bot falls back to template answers.

### Safety behaviour

| Message | Response |
|---|---|
| Emergency terms (chest pain, snake bite, seizure, ...) | 108 / 112 guidance, checked before everything else |
| Self-harm phrases | Tele-MANAS (14416 / 1800-891-4416, the national free 24x7 mental health helpline) and 112 |
| An emergency term together with a fact-check request | Emergency guidance, plus a line telling the user to resend the claim on its own |

Entity matching uses whole words, so "tb" does not match inside "outbreak" and "fits"
does not match inside "benefits". Regression tests for these cases are in
`tests/test_safety_routing.py`.

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
hosted API as the first LLM tier. It needs account credits: when the account has none,
the hosted API answers HTTP 402 and the bot uses the local model instead.

**LLM failover order (as implemented in `app/core/generator.py`):**
1. If `OLLAMA_API_KEY` is set, try Ollama Cloud first (`LLM_CLOUD_MODEL`, default
   `gpt-oss:20b`; qwen3:1.7b is not in the cloud catalog)
2. If the cloud call fails (no credits, bad key, quota, timeout), try local Ollama
   (`LLM_MODEL`, default `qwen3:1.7b`); a local failure sets a 60 s cooldown for that tier
3. If both fail, the bot answers from deterministic templates

`/api/health` reports the active backend (`local`/`cloud`); every chat response
includes `llm_backend`. Cloud models may think first, so the payload disables
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
python -m pytest tests -q   # 72 automated tests
```

Benchmark on the supplied development sets (`data/training/eval.json`):

| Suite | Result |
|---|---|
| Intent classification (30 queries, EN/HI/Hinglish) | 30/30 |
| Cross-lingual retrieval (15 queries) | 15/15 |
| Health-claim fact check (34 claims) | 34/34 |

These sets were written by the project team: 14 of the 30 intent queries also appear in the
training data, and the benchmark thresholds differ from the production settings. Read them as
component checks, not as an estimate of real-world accuracy or clinical correctness.

## Known limitations

- The knowledge base is small (14 diseases, 35 FAQs, 64 curated myths). Questions outside it fall back to a
  whitelisted-domain web search or an honest "I don't know".
- Retrieval is cosine similarity over LaBSE embeddings with a lexical boost. There is no vector database,
  document chunking, reranker or hybrid BM25 search yet.
- The benchmarks above are team-written and partly overlap the training data, so they are component checks,
  not an estimate of real-world accuracy.
- The hosted LLM tier needs account credits. Without them the bot runs on the smaller local model, which is
  slower, especially for Hindi, before it falls back to templates.
- Awareness only: not a doctor, never diagnoses.

## WhatsApp channel

`app/channels/whatsapp.py` implements the Meta WhatsApp Cloud API webhook: verification
challenge, HMAC-SHA256 signature check, immediate acknowledgement with background processing,
duplicate suppression and reply splitting. It was demonstrated end to end with a Meta test
number and an approved test recipient. Configure it with `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_ID`,
`WHATSAPP_VERIFY_TOKEN` and `WHATSAPP_APP_SECRET` in your private `.env` (see `.env.example`).
Never commit these values. `scripts/configure_meta_whatsapp.py` helps with the subscription setup.

## Final deliverables

| Item | Location |
|---|---|
| Final project report (DOCX and PDF) | `output/report/` (builder in `output/report/source/`) |
| Second-defense presentation | `output/presentation/` |
| Research paper (final version) | `output/research/AarogyaSathi_Full_Paper_Revised_v8.*` |
| Dated verification evidence | `docs/evidence/` |

## Project layout

```
app/core/      NLP: language, embeddings, intent, entities, retriever, safety, router
app/factcheck/ myth-vs-fact verifier (verity scores, source tiers)
app/channels/  Meta WhatsApp Cloud API webhook, Twilio adapter, simulator endpoint
app/surveillance/ syndromic early-warning (pincode symptom counts vs a 7-day baseline)
data/kb/       curated knowledge base (diseases, vaccines, faq, myths, alerts, messages)
data/training/ intent training examples + held-out eval set
web/           WhatsApp-style demo UI
scripts/       setup (model download), eval, smoke tests
```

## Deployment

- **Used for the demo: an Oracle Cloud Arm VM** (2 OCPU / 12 GiB; free-tier eligible) — full step-by-step
  guide in `docs/ORACLE_DEPLOY.md`, one-shot setup script in `scripts/oracle_setup.sh`,
  systemd unit in `scripts/healthbot.service`.
- Docker: `docker compose up -d`
- Generic cloud (Render/Railway): see `docs/DEPLOYMENT.md`

## Roadmap

- Phase 2: fact-check module (done), with live web-evidence verification ranked by source trust
- Phase 3: syndromic surveillance (pincode-tagged symptom-query spikes → early-warning)
- Phase 4: Meta WhatsApp Cloud API webhook + Twilio SMS + free-tier cloud deploy (Render/Railway), ngrok for local demo

## Sources

WHO fact sheets, MoHFW/NHM/IDSP/NTEP/NACO advisories, PIB Fact Check, ICMR — curated
for awareness purposes. Every answer carries a source list and a medical disclaimer.
