# AarogyaSathi — Project Context Brief (for agent continuation)

## Project identity
"AarogyaSathi" (आरोग्यसाथी) — an AI-Driven Public Health Chatbot for Disease Awareness.
Minor project (ES-451) for B.Tech 7th semester at Bhagwan Parshuram Institute of Technology
(team: Salman Mohd. Khan, Dhairya Summi, Sidharth Singh). Based on Smart India Hackathon
problem SIH25049 (Govt. of Odisha): a multilingual AI chatbot that educates rural and
semi-urban populations about preventive healthcare, disease symptoms, vaccination schedules,
integrates with government health databases and delivers outbreak alerts, accessible over
WhatsApp/SMS. The team's submitted synopsis is in `synopsis.txt`.

## Original user requirements (accumulated across the build)
- Health chatbot running first as a **web demo**, then to be deployed on **WhatsApp** (Meta Cloud API) and possibly SMS; target users are rural Indian users with low literacy and low-end phones.
- **Deep NLP/ML** (not a shallow rules bot): intent classification, entity extraction, cross-lingual understanding, a real fact-check/misinformation module, and proper symptom analysis.
- **Multilingual**: must detect and respond in 10-12 Indian languages (Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, Urdu) including Hinglish (roman Hindi).
- **Fact-check (myth-vs-fact) module**: user pastes/forwards a health message; bot returns a verdict with a verity/confidence score: VERIFIED / MYTH / PARTLY TRUE / UNVERIFIABLE, with sources and a fear-mongering flag. MUST only trigger on an explicit "fact check: <message>" prefix in any language (user explicitly removed auto claim-detection).
- **Misinformation source**: check against trusted online sources (WHO, MoHFW, PIB, ICMR, reputable fact-checkers) when the local corpus doesn't cover the claim.
- **Symptom analysis**: when a user reports symptoms, the bot must probe (duration, other symptoms) and then give a genuine analysis of the problem, NOT just dump disease names.
- **Outbreak/health alerts**: user gives a pincode; bot reports any outbreak advisories for that area, or says "no major outbreak", using curated government advisories + trusted news (only health-related results allowed).
- **Emergency vs normal**: red-flag symptoms (chest pain, can't breathe, snake bite, seizure, etc.) must instantly escalate to 108/112 guidance, never delayed by the LLM.
- **Chat memory**: rolling LLM-generated summary of the conversation per session, so follow-ups like "is it serious?" after a symptom discussion are understood; memory is in-memory/ephemeral (privacy).
- **Welcome behavior**: on the FIRST message in a newly-detected language in a session, the bot sends the default welcome message in that language (including the "to fact-check, start with 'fact check:'" hint), then answers; never repeats the welcome for that language in the same session.
- **Deployment**: Oracle Cloud Always Free; LLM used via Ollama Cloud API as primary, local qwen3 as warm backup; cost must stay ~$0.

## Final architecture (hybrid: LLM-understanding-first with deterministic safety)
Message flow in `app/core/router.py::process_message`:
1. **Red-flag check** (lexicon, deterministic, ~150ms) → emergency response (108/112). Never LLM-dependent.
2. **Explicit "fact check:" prefix** (deterministic, ~150ms) → fact-check verdict path.
3. Pure single-word greetings → template greeting.
4. **Active symptom flow** (multi-turn probing state in session) takes priority; follow-up answers finalize with LLM symptom analysis.
5. **LLM understanding pass** (`generator.understand_message`): cloud LLM returns JSON {intent: symptom/disease_info/prevention/vaccination/outbreak/fact_check/greeting/help/smalltalk/thanks/follow_up/unclear/other, symptoms[], disease, duration, clarification, follow_up}. Routing acts on this; "unclear" → clarifying question.
6. Fallback if understanding fails (LLM down) → old NLP pipeline (TF-IDF intent classifier + LaBSE retrieval + entities).
7. Final 3-layer answer fallback for unhandled: **NLP/KB grounded → general LLM (warned) → websearch** (DuckDuckGo, whitelisted domains only: wikipedia.org, who.int, cdc.gov, nih.gov, mayoclinic.org, nhs.uk, mohfw.gov.in, icmr.gov.in, etc., and only if the query AND result contain health keywords — otherwise "I don't know").

## What is built (all deployed and verified on the VM)
- **Backend**: FastAPI (`app/main.py`), endpoints: `POST /api/chat` {message, session_id, pincode} → {reply, intent, language, latency_ms, generator, llm_backend, flow, factcheck}; `GET /api/health`; `/api/stats`; `/api/surveillance/*`; web UI at `/` and admin dashboard at `/admin`.
- **NLP core** (`app/core/`): language detection (fastText lid.176), intent classifier (TF-IDF char n-grams + LogisticRegression, trained on `data/training/intents.json`), LaBSE multilingual embeddings for KB retrieval (fp32, loaded at startup), entity lexicons (symptoms, diseases, vaccines, red flags) with typo tolerance + colloquial aliases, negation handling ("no fever" ≠ fever).
- **Knowledge base** (`data/kb/*.json`): 14 diseases, 35 FAQs, 49 myths, 13 vaccines, outbreak advisories, pincode→state/district mapping, system messages in 12 languages. Content is WHO/MoHFW-sourced, curated.
- **Fact-check** (`app/factcheck/verifier.py`): curated corpus match (LaBSE + content-overlap + disease-conflict guards) → Google Fact Check Tools API live lookup (needs GOOGLE_FACTCHECK_API_KEY) → home-remedy fallback (PARTLY TRUE, limited evidence) → UNVERIFIABLE. Verdicts VERIFIED/MYTH/PARTLY TRUE/UNVERIFIABLE with confidence and sources.
- **LLM** (`app/core/generator.py`): cloud-first (Ollama Cloud API, model gpt-oss:20b, key in .env) → local backup (Ollama qwen3:1.7b on VM, kept warm via OLLAMA_KEEP_ALIVE=-1 + boot warmup). `llm_backend` in every response shows which served. Functions: grounded_answer (KB-context only), general_answer (own knowledge, warned), understand_message (JSON routing), analyze_symptoms (caring analysis with negation awareness), summarize_conversation (rolling memory), ask_followup, looks_unsure (apostrophe-normalized).
- **Memory**: per-session history (last 12) + rolling LLM summary updated every 3rd message (background thread), used in fallback context.
- **Outbreaks** (`app/core/outbreaks.py`): curated advisories matched by pincode→state/district + Google News RSS (cached 15 min) filtered to whitelisted/health content.
- **Websearch** (`app/core/websearch.py`): DuckDuckGo (ddgs) → whitelisted domains → Wikipedia REST summary; strict `is_health_query` guard on query and result.
- **Tests**: `tests/` (pytest) — core intents, entities, fact-check, retrieval, flows, surveillance. Eval script `scripts/eval.py` (intent 100%, retrieval 100%, fact-check 100% on held-out set).
- **Idle system**: local qwen3 stays loaded (memory ~25-32% > Oracle's 20% idle-reclaim threshold), boot warmup loads it, systemd auto-restarts. Cloud-primary means local is only used as backup.

## Deployment / environment (live now)
- **Oracle Cloud Always Free VM**: public IP **130.210.56.87**, 2 OCPU / 12GB RAM, Ubuntu 24.04, ARM64 (aarch64). Region ap-mumbai-1. Firewall: Oracle security list (ingress 8000, 22) AND VM iptables (port 8000 ACCEPT, persisted via iptables-persistent).
- App at **/opt/healthbot** (venv at /opt/healthbot/venv, run as systemd unit `healthbot.service`, auto-start on boot). Deploy by `scp` of changed files then `sudo systemctl restart healthbot`. Setup script: `scripts/oracle_setup.sh`; service file: `scripts/healthbot.service`.
- **.env at /opt/healthbot/.env**: OLLAMA_API_KEY (Ollama Cloud, model gpt-oss:20b — note qwen3:1.7b is NOT in the Ollama cloud catalog), GOOGLE_FACTCHECK_API_KEY (Fact Check Tools API, free), LLM_MODEL=qwen3:1.7b, LLM_CLOUD_MODEL=gpt-oss:20b. Local .env at project root is gitignored.
- Ollama local: model qwen3:1.7b, OLLAMA_KEEP_ALIVE=-1 set via systemd drop-in `/etc/systemd/system/ollama.service.d/keepalive.conf`. Keep alive as INTEGER -1 in requests (string "-1" causes Ollama HTTP 400 "missing unit in duration").
- Embedding caches in `data/embeddings/*.npy` (rebuild automatically when KB text changes; ~1-2 min on VM, several minutes on a laptop).

## Known issues / honest notes for the agent
- **No WhatsApp integration yet** (that's the next phase): Meta WhatsApp Cloud API webhook + HTTPS (Caddy/nginx + Let's Encrypt) on the same VM.
- **No git/GitHub repo yet** (user never set it up); deploys are scp-based.
- Ollama Cloud free-tier quota is usage-based and can exhaust during heavy demos (~5h session resets) — bot then falls back to local qwen3, whose Hindi quality is noticeably worse (can produce garbled Devanagari); cloud gpt-oss is much better, especially for regional languages.
- First response after VM reboot is ~15-30s (model load), then ~2-8s warm.
- If Oracle reclaims the idle VM (7+ days of zero traffic AND memory <20% — unlikely since model stays loaded), data survives; restart from console and systemd recovers everything.
- Syndromic surveillance module (pincode-tagged symptom spike detection, `/admin` dashboard, `app/surveillance/syndromic.py`) is implemented but the user deprioritized it — it's parked, not tested end-to-end; discuss before expanding it.
- Pincode→district mapping is only a sample (~20 districts); full India pincode directory is available to add.
- The user prefers: explicit "fact check:" prefix only (no auto claim-detection), LLM-understanding-first routing, safety-deterministic emergency/fact-check paths, and $0 cloud costs.

## Next steps (priorities the user cares about)
1. WhatsApp webhook integration (Meta Cloud API, test number) — the stated Phase 4 goal.
2. Then: web demo polish, full pincode mapping, Git setup, and the final report/README for the viva.