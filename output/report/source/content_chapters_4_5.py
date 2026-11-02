"""
Chapters 4 and 5 Generator for AarogyaSathi Minor Project Report
- Chapter 4: Design and Architecture (8 pages)
- Chapter 5: Implementation (8 pages)
"""

from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_chapter_4(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_figure, add_table, add_code_block):
    add_chapter_title(doc, "4", "Design and Architecture")

    add_heading_1(doc, "4.1 System Architecture and Work Breakdown Structure (WBS)")
    add_body_p(doc,
        "The design of AarogyaSathi follows an asynchronous, modular service-oriented architecture specifically optimized for deployment on "
        "resource-constrained cloud virtual machines. The system decouples natural language understanding, dense vector retrieval, factual "
        "claim verification, epidemiological telemetry, and multi-channel communication into cohesive, loosely coupled subsystems. "
        "Figure 4.1 illustrates the Work Breakdown Structure (WBS) governing the engineering lifecycle of the project:"
    )

    add_figure(doc, "fig_wbs.png", "4.1", 
               "Work Breakdown Structure (WBS) of AarogyaSathi Engineering Modules.", 
               width_inches=5.6)

    add_body_p(doc,
        "The WBS is structured across four primary technical work packages: Package 1.0 (Core NLP & Fast-Path Routing), encompassing intent classifiers, "
        "regex entity extractors, and session caches; Package 2.0 (Retrieval & Knowledge Infrastructure), governing LaBSE dense embeddings, lexical rerankers, "
        "and RAG context builders; Package 3.0 (Fact-Checking & Clinical Safety), covering the 64-myth verifier, emergency phrase interception, and clinical "
        "disclaimer injectors; and Package 4.0 (Multi-Channel Ingress & Deployment), managing FastAPI ASGI services, Meta WhatsApp Cloud API webhooks, "
        "and Cloudflare secure HTTPS ingress tunnels."
    )

    add_heading_1(doc, "4.2 Detailed Module Responsibilities")
    add_body_p(doc,
        "The runtime execution environment consists of ten tightly integrated modules operating under the control of a centralized orchestrator:"
    )
    add_bullet_p(doc, "1. Orchestrator Router (app/core/router.py)", 
                 "Master execution pipeline managing fast-path evaluation, multi-turn dialogue history, emergency red-flag safeguards, and LLM orchestration.")
    add_bullet_p(doc, "2. Language Detector (app/core/language.py)", 
                 "Performs lightweight script and character-distribution analysis across 12 Indian languages to set conversational locale flags.")
    add_bullet_p(doc, "3. Fast-Path Heuristic Engine (_try_fast_path)", 
                 "Evaluates pre-compiled regexes against queries to identify standard disease inquiries, infant age milestones, and greetings without invoking the language model.")
    add_bullet_p(doc, "4. Dense Vector Retriever (app/core/retriever.py)", 
                 "Computes 768-dimensional LaBSE query vectors and executes cosine-similarity searches across indexed disease and FAQ records.")
    add_bullet_p(doc, "5. Context Builder & LLM Generator (app/core/generator.py)", 
                 "Assembles retrieved knowledge into clinical prompts and interfaces with Ollama's local C++ runtime to synthesize grounded responses via Qwen3:1.7b.")
    add_bullet_p(doc, "6. Health Claim Verifier (app/factcheck/verifier.py)", 
                 "Processes viral rumors, performs cross-lingual matching against 64 curated Indian myths, and outputs categorical truth verdicts.")
    add_bullet_p(doc, "7. Clinical Safety Filter (app/core/safety.py, app/core/entities.py)", 
                 "Matches a deterministic lexicon of acute medical red flags (chest pain, stroke, breathlessness) in entities.py, composes the emergency reply in safety.py, and injects the mandatory disclaimer.")
    add_bullet_p(doc, "8. Session Context Cache (app/core/session.py)", 
                 "Maintains per-user conversation state (current flow, recent turns and a running summary) in volatile RAM with a 30-minute expiration TTL.")
    add_bullet_p(doc, "9. Syndromic Surveillance Engine (app/surveillance/syndromic.py)", 
                 "Logs anonymous symptom-pincode events into SQLite and evaluates rolling 7-day statistical baseline algorithms to identify disease anomalies.")
    add_bullet_p(doc, "10. WhatsApp Channel Adapter (app/channels/whatsapp.py)", 
                 "Manages bidirectional Meta Graph API v25.0 webhooks, validating HMAC-SHA256 signatures and dispatching outbound messages.")

    add_heading_1(doc, "4.3 Data Storage Architecture: SQLite vs. Curated JSON vs. Sessions")
    add_body_p(doc,
        "A critical architectural requirement emphasized in this dissertation is the rigorous separation of data storage layers based on persistence, "
        "volatility, and privacy guarantees. Rather than conflating all data into a monolithic database, AarogyaSathi employs a hybrid storage "
        "topology (Figure 4.2):"
    )

    add_figure(doc, "fig_er_class.png", "4.2", 
               "Data Storage Architecture: SQLite Telemetry vs. Curated JSON Repositories vs. In-Memory RAM Sessions.", 
               width_inches=5.2)

    add_body_p(doc,
        "1. Persistent Relational Storage (SQLite): The only data written to persistent disk storage is anonymized syndromic telemetry stored in a local "
        "SQLite database (data/surveillance.db). The schema has three tables: events (id, pincode, symptom, lang, ts), messages (id, pincode, intent, lang, verdict, ts) and alerts (id, pincode, symptom, current_count, baseline, severity, ts). "
        "Message text, phone numbers and user names are not written to this database."
    )
    add_body_p(doc,
        "2. Static Curated Knowledge Store (JSON): Authoritative clinical information is maintained in immutable, version-controlled JSON files located in "
        "data/kb/. This includes 14 disease profiles (diseases.json), 35 FAQs (faq.json), 13 vaccine milestones (vaccines.json), 64 myth verification records "
        "(myths.json), and 8 illustrative outbreak advisories (outbreaks.json). These records are pre-indexed into memory at server startup."
    )
    add_body_p(doc,
        "3. Volatile Ephemeral Session Cache (RAM): Multi-turn conversation state is stored in application RAM through the Session Python class (session.py). "
        "Each session holds an identifier (web session identifier or WhatsApp sender), a key-value state dictionary containing the active flow, recent turns and a summary, "
        "and a last-updated timestamp. Sessions expire after 30 minutes of inactivity and are lost when the server restarts. The WhatsApp handler separately keeps an "
        "in-memory buffer of 4,096 completed message identifiers for duplicate suppression."
    )

    add_heading_1(doc, "4.4 Knowledge Base Schema and Domain Taxonomy")
    add_body_p(doc,
        "The curated knowledge base represents the clinical foundation of AarogyaSathi. Every record was authored by synthesizing official public health "
        "bulletins published by the World Health Organization (WHO), the Ministry of Health and Family Welfare (MoHFW), the National Vector Borne Disease "
        "Control Programme (NVBDCP), and the Indian Council of Medical Research (ICMR). Table 4.1 summarizes the knowledge inventory:"
    )

    kb_headers = ["Domain Category", "Record Count", "Core Entities Covered", "Clinical Source Grounding"]
    kb_rows = [
        ["Endemic Diseases", "14 Profiles", "Dengue, Malaria, Typhoid, Tuberculosis, Cholera, COVID-19, Chikungunya, Rabies, Hepatitis, Diarrhea, Jaundice, Pneumonia, Anemia, Measles", "WHO Fact Sheets, MoHFW Clinical Management Guidelines, NVBDCP National Guidelines"],
        ["Health FAQs", "35 Records", "Water purification, ORS preparation, mosquito net usage, fever management, sanitation, maternal nutrition", "National Health Mission (NHM) IEC Bulletins, UNICEF Water & Sanitation Manuals"],
        ["Child Immunization", "13 Milestones", "Birth, 6 weeks, 10 weeks, 14 weeks, 9-12 months, 16-24 months, 5-6 years (BCG, OPV, Pentavalent, Rotavirus, PCV, MR, DPT)", "Universal Immunization Programme (UIP) National Schedule, MoHFW 2024 Guidelines"],
        ["Misinformation Myths", "64 Claims", "Raw garlic cures dengue, Papaya leaf extracts replace blood transfusion, Vaccines cause autism, Heat destroys all viruses, Onion juice cures fever", "PIB Fact Check India, WHO Mythbusters, ICMR Public Advisories"],
        ["Outbreak Advisories", "8 Advisories", "Seasonal monsoon dengue alerts, tribal malaria warnings, flood-related diarrheal protocols (Sample / Illustrative)", "Integrated Disease Surveillance Programme (IDSP) Weekly Bulletins (Illustrative Demo)"]
    ]
    add_table(doc, kb_headers, kb_rows, "4.1", "Curated Knowledge Base Inventory Across Public Health Domains", [1.2, 0.9, 2.0, 1.66])

    add_heading_1(doc, "4.5 Cross-Lingual Semantic Retrieval and Dense Vector Search")
    add_body_p(doc,
        "To enable cross-lingual retrieval without machine translation, the system integrates the Language-agnostic BERT Sentence Embedding (LaBSE) transformer "
        "(Feng et al., 2022). The 49 primary clinical records (14 disease profiles and 35 FAQs) are pre-embedded into 768-dimensional normalized dense vectors. "
        "When an incoming query q arrives, it is tokenized, truncated to a maximum of 128 tokens, and passed through the LaBSE encoder with attention-mask "
        "weighted mean pooling to produce a normalized query vector e(q)."
    )
    add_body_p(doc,
        "The ranking score S(q, d) between query vector e(q) and pre-indexed document vector e(d) is computed using a hybrid scoring function combining dense "
        "cosine similarity with surface lexical term matching:"
    )
    add_code_block(doc, "S(q, d) = cos(e(q), e(d)) + 0.22 * L(q, d)")
    add_body_p(doc,
        "where cos(e(q), e(d)) represents the cosine angle between normalized 768-dimensional vectors, and L(q, d) is the fraction of lowercased query terms "
        "(longer than two characters) appearing as exact substrings within document record d. In production deployment, the retrieval engine retrieves up to "
        "the top-5 candidate records exceeding a strict confidence threshold of 0.52. This hybrid formulation ensures that colloquial semantic variations "
        "are captured by dense embeddings while preserving precise lexical specificity for pharmaceutical terms and clinical disease names."
    )

    add_heading_1(doc, "4.6 Fallback Intent Classification Taxonomy")
    add_body_p(doc,
        "When incoming queries bypass fast-path regex rules, they are evaluated by a secondary machine learning intent classifier. The classifier is trained "
        "on 289 curated multilingual examples distributed across 14 operational intent classes (Table 4.2). Text is vectorized using character-boundary n-grams "
        "ranging from length 2 to 5 with sublinear term-frequency scaling and a vocabulary ceiling of 30,000 features. Classification is performed via a "
        "multinomial Logistic Regression model (regularization C=8, L-BFGS solver, 1,000 maximum iterations) implemented in scikit-learn 1.9.0."
    )

    intent_headers = ["Intent Label", "Train N", "Core Semantics & Exemplar Query", "Production Pipeline Action"]
    intent_rows = [
        ["disease_info", "34", "What is dengue? Malaria symptoms", "Retrieves disease profile & triggers RAG"],
        ["prevention", "28", "How to prevent typhoid? Safety tips", "Returns verified preventive guidance"],
        ["vaccination", "26", "Vaccines for 6 week baby", "Extracts infant age & matches UIP table"],
        ["symptom_check", "32", "Fever, shivering, and headache", "Initiates multi-turn symptom inquiry"],
        ["myth_fact", "24", "Does garlic cure dengue?", "Routes to 64-myth fact-check engine"],
        ["outbreak_alert", "22", "Any dengue alert near 751001?", "Queries localized geographic advisories"],
        ["greeting", "20", "Hi, Hello, Namaste, Kemon acho", "Returns localized greeting prompt"],
        ["emergency", "18", "Severe chest pain, breathlessness", "Immediate 108/112 emergency escalation"],
        ["smalltalk", "16", "Who made you? What is your name?", "Returns bot identity & SIH context"],
        ["affirmation", "15", "Yes, sure, okay, please continue", "Advances conversational state"],
        ["negation", "14", "No, I don't have that symptom", "Updates clinical differential context"],
        ["gratitude", "14", "Thank you, Dhanyavad, Shukriya", "Dispatches closing acknowledgment"],
        ["language_switch", "14", "Speak in Hindi, Odia me batao", "Switches session locale flag"],
        ["fallback", "12", "Ambiguous or out-of-domain query", "Triggers knowledge disclaimer"]
    ]
    add_table(doc, intent_headers, intent_rows, "4.2", "Intent Classification Taxonomy and Training Corpus Distribution", [1.1, 0.7, 2.3, 1.66])

    add_heading_1(doc, "4.7 Multi-Tier Triage, Fast-Path Heuristics, and Routing Flow")
    add_body_p(doc,
        "To keep responses fast while giving clinical safety checks priority, AarogyaSathi executes a multi-tier triage "
        "decision tree. Figure 4.3 illustrates the routing lifecycle of every incoming message:"
    )

    add_figure(doc, "fig_flowchart.png", "4.3", 
               "Activity and Decision Flowchart of Multi-Tier Triage and Fast-Path Routing.", 
               width_inches=4.7)

    add_body_p(doc,
        "Tier 1 (Emergency Filter): The query is first scanned against a compiled regex lexicon of life-threatening clinical presentations. If an affirmative "
        "match is detected, all neural processing is bypassed, and the user receives an emergency escalation directive without any model call. "
        "Tier 2 (Fact-Check Ingress): If the query begins with the prefix 'fact check:' or semantically matches a known health rumor, it is routed to the "
        "misinformation engine. Tier 3 (Fast-Path Rules): The router tests for common disease names and vaccination age patterns. If a match is verified, "
        "a pre-compiled, WHO-grounded template is dispatched immediately, avoiding generative model latency. Tier 4 (Dense RAG Fallback): If heuristic rules "
        "fail, the query engages LaBSE dense retrieval and prompts the local Qwen3:1.7b language model."
    )

    add_heading_1(doc, "4.8 Health Misinformation Verification Engine")
    add_body_p(doc,
        "The fact-checking subsystem (app/factcheck/verifier.py) is engineered to neutralize viral health rumors. When a claim is ingested, the engine "
        "executes a two-stage verification pipeline. First, it computes semantic similarity against the curated repository of 64 Indian health myths. "
        "If the best match is close enough (embedding similarity of at least 0.70 with sufficient word overlap, or the configured fact-check threshold with higher overlap) and does not concern a conflicting disease, "
        "the engine returns the stored verdict, assigning one of four standard truth categories: VERIFIED (empirically supported medical fact), MYTH (demonstrably false or harmful claim), "
        "PARTLY TRUE (contains a kernel of truth but misleading context), or UNVERIFIABLE (insufficient empirical evidence). Otherwise it tries an online evidence lookup and a remedy-pattern "
        "fallback and, failing those, returns UNVERIFIABLE with pointers to official sources. A small set of dangerous first-aid myths is intercepted earlier by fixed rules."
    )

    add_heading_1(doc, "4.9 Syndromic Telemetry and Outbreak Surveillance Modeling")
    add_body_p(doc,
        "The syndromic surveillance module (app/surveillance/syndromic.py) provides early warning capabilities by tracking citizen-reported symptoms by "
        "6-digit postal pincodes. When a user voluntarily submits a symptom query accompanied by a pincode, the event is logged into the local SQLite table. "
        "The detection algorithm compares the symptom submission count in the latest 24-hour window, denoted as c(p,s)(t), against the historical baseline "
        "b(p,s)(t), defined as the mean daily count over the preceding seven complete 24-hour periods."
    )
    add_body_p(doc,
        "An automated outbreak alert candidate is generated if the following mathematical condition is satisfied:"
    )
    add_code_block(doc, "c(p,s) >= 6  AND  ( b(p,s) < 1.0  OR  c(p,s) >= 3.0 * b(p,s) )")
    add_body_p(doc,
        "When baseline b(p,s) >= 1.0, an alert is escalated to HIGH severity if c(p,s) reaches 5.0 times the baseline; otherwise, it is designated MEDIUM. "
        "To prevent alert fatigue, after an alert is logged for a specific pincode-symptom pair, subsequent alerts for that pair are suppressed for 24 hours. "
        "These cluster anomalies are rendered on the administrative dashboard (/admin), providing public health officers with summaries of submitted syndromic events."
    )

    add_heading_1(doc, "4.10 Meta WhatsApp Cloud API Channel Sequence Flow")
    add_body_p(doc,
        "The Meta WhatsApp channel integration enables citizens to access AarogyaSathi directly over WhatsApp. Figure 4.4 details the complete request "
        "lifecycle across network boundaries:"
    )

    add_figure(doc, "fig_whatsapp_seq.png", "4.4", 
               "Meta WhatsApp Cloud API Integration Sequence Flow and Webhook Ingress Architecture.", 
               width_inches=5.2)

    add_body_p(doc,
        "When a citizen sends a WhatsApp message to the dedicated test sender (+1 555 626 0618), Meta's Graph API v25.0 issues an HTTPS POST webhook event "
        "to our Cloudflare Tunnel endpoint (route /webhook/whatsapp). The webhook payload includes an HMAC-SHA256 "
        "signature in the X-Hub-Signature-256 header. The FastAPI handler verifies the signature against the pre-shared WHATSAPP_APP_SECRET, checks the "
        "incoming message ID against a 4,096-entry deduplication set, and immediately returns an HTTP 200 OK acknowledgement to Meta before background processing completes. "
        "Processing is offloaded to an asynchronous background task, which executes the fast-path router, formats the clinical response, and dispatches an "
        "outbound HTTPS payload to Meta’s messages endpoint for instant delivery to the user’s handset."
    )

def add_chapter_5(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_figure, add_code_block):
    add_chapter_title(doc, "5", "Implementation")

    add_heading_1(doc, "5.1 System Implementation Overview and Service Topology")
    add_body_p(doc,
        "AarogyaSathi is implemented in Python 3.12.3 and deployed on an Oracle Cloud Infrastructure (OCI) Arm virtual machine "
        "(VM.Standard.A1.Flex) located in the Mumbai (ap-mumbai-1) region. The host environment provides 2 OCPUs (Arm-based Ampere Altra processor), "
        "12 GiB of unified physical RAM, and a 50 GB boot volume running Ubuntu 24.04 LTS. The application architecture is managed under "
        "systemd process supervision via two dedicated service daemons: healthbot.service, which manages the Uvicorn ASGI web server listening on internal "
        "port 8000, and aarogya-tunnel.service, which executes the official Cloudflare Tunnel daemon (cloudflared v2026.10.3) providing secure HTTPS ingress."
    )

    add_heading_1(doc, "5.2 Core Router and Fast-Path Heuristic Implementation")
    add_body_p(doc,
        "The central dispatching logic is implemented in app/core/router.py. To avoid a separate language-model call for interpreting routine messages, the router first tries a fast path that combines the "
        "TF-IDF intent classifier with regular-expression entity matching (excerpt of _try_fast_path):"
    )
    add_code_block(doc,
        "def _try_fast_path(text, lang, session, pincode):\n"
        "    intent_name, confidence = intent.predict_intent(text, INTENT_CONFIDENCE_THRESHOLD)\n"
        "    disease_id = entities.find_disease(text)\n"
        "    vaccine_id = entities.find_vaccine(text)\n"
        "    milestone = _age_to_milestones(text)\n"
        "    # 1. High-priority safety / emergency\n"
        "    if intent_name == \"emergency\":\n"
        "        session.clear()\n"
        "        return {\"text\": safety.emergency_response(lang),\n"
        "                \"meta\": {\"intent\": \"emergency\", \"lang\": lang, \"route\": \"fast_path\"}}\n"
        "    # 2. Fact-check triggered or predicted\n"
        "    if intent_name == \"fact_check\":\n"
        "        session.clear()\n"
        "        result = verifier.verify_claim(text, lang)\n"
        "        return {\"text\": verifier.format_verdict(result, lang), ...}\n"
        "    # 3. Conversational intents (greeting, help, smalltalk, thanks) ..."
    )
    add_body_p(doc,
        "When an incoming query matches a pre-compiled disease entity or greeting, the fast-path engine formats the verified WHO/MoHFW clinical advice "
        "and dispatches the response directly, bypassing language model token generation."
    )

    add_heading_1(doc, "5.3 Knowledge Base Retrieval and Dense Vector Search Implementation")
    add_body_p(doc,
        "Semantic vector search is implemented in app/core/retriever.py and app/core/embeddings.py. Document embeddings are computed using the pretrained "
        "sentence-transformers/LaBSE checkpoint loaded via HuggingFace Transformers. Vector pooling and similarity computation are executed in PyTorch:"
    )
    add_code_block(doc,
        "def embed_texts(texts):\n"
        "    tokenizer, model = get_model()\n"
        "    ...\n"
        "    encoded = tokenizer(batch, padding=True, truncation=True,\n"
        "                        max_length=128, return_tensors=\"pt\")\n"
        "    with torch.no_grad():\n"
        "        out = model(**encoded)\n"
        "    pooled = _mean_pool(out.last_hidden_state, encoded[\"attention_mask\"])\n"
        "    pooled = torch.nn.functional.normalize(pooled, p=2, dim=1)\n\n"
        "def retrieve(query, top_k=MAX_RETRIEVED, threshold=RETRIEVAL_SIM_THRESHOLD):\n"
        "    qv = embeddings.embed_texts([query])[0]\n"
        "    sims = embeddings.cosine_similarity(qv, index[\"matrix\"])\n"
        "    query_words = [w for w in query.lower().split() if len(w) > 2]\n"
        "    for i, sim in enumerate(sims):\n"
        "        score = float(sim)\n"
        "        if query_words:\n"
        "            matched = sum(1 for w in query_words if w in index[\"texts\"][i].lower())\n"
        "            score += 0.22 * matched / len(query_words)\n"
        "    ..."
    )

    add_heading_1(doc, "5.4 Misinformation Verification Engine Implementation")
    add_body_p(doc,
        "The fact-checking pipeline (app/factcheck/verifier.py) analyzes claims submitted with the prefix 'fact check:' or matching known rumors. "
        "It matches the claim text against data/kb/myths.json and generates structured verification outputs:"
    )
    add_code_block(doc,
        "def verify_claim(text, lang=\"en\"):\n"
        "    index = _ensure_index()\n"
        "    claim = clean_claim(text)\n"
        "    dangerous_fa = _check_dangerous_first_aid(claim)\n"
        "    if dangerous_fa:\n"
        "        return dangerous_fa\n"
        "    qv = embeddings.embed_texts([claim])[0]\n"
        "    sims = embeddings.cosine_similarity(qv, index[\"matrix\"])\n"
        "    # disease-aware re-ranking: +0.15 same disease, -0.30 conflicting disease\n"
        "    ...\n"
        "    use_curated = (\n"
        "        (best_sim >= 0.70 and overlap >= 0.35 and not disease_conflict)\n"
        "        or (best_sim >= FACTCHECK_SIM_THRESHOLD and overlap >= 0.40 and not disease_conflict))\n"
        "    if not use_curated:\n"
        "        live = _live_lookup(claim, lang)   # online evidence, if available\n"
        "        ..."
    )

    add_heading_1(doc, "5.5 Meta WhatsApp Webhook Security and Handler Implementation")
    add_body_p(doc,
        "The WhatsApp integration (app/channels/whatsapp.py) enforces strict production security protocols mandated by Meta’s developer guidelines. "
        "Incoming webhook payloads are authenticated using HMAC-SHA256 signatures, preventing man-in-the-middle or spoofing attacks:"
    )
    add_code_block(doc,
        "@whatsapp_router.post(\"\")\n"
        "async def meta_webhook_message(request: Request, background_tasks: BackgroundTasks):\n"
        "    raw_body = await request.body()\n"
        "    expected = \"sha256=\" + hmac.new(\n"
        "        config.WHATSAPP_APP_SECRET.encode(), raw_body, hashlib.sha256).hexdigest()\n"
        "    supplied = request.headers.get(\"x-hub-signature-256\", \"\")\n"
        "    if not hmac.compare_digest(expected, supplied):\n"
        "        raise HTTPException(status_code=403, detail=\"Invalid webhook signature\")\n"
        "    body = json.loads(raw_body)\n"
        "    background_tasks.add_task(_handle_meta_inbound_payload, body)\n"
        "    return {\"status\": \"ok\"}   # acknowledge immediately, process in background"
    )

    add_heading_1(doc, "5.6 Web Conversational Interface Implementation")
    add_body_p(doc,
        "The web user interface (web/index.html and web/chat.js) is a lightweight, mobile-responsive single-page application. "
        "It provides a chat container, quick-prompt chips ('Dengue info', 'Symptom check', 'Vaccines', 'Fact check'), "
        "and an optional 6-digit pincode field for localized alerts. Figure 5.1(a) shows the landing interface after a greeting."
    )

    add_heading_1(doc, "5.7 Conversational Walkthrough on the Deployed Service")
    add_body_p(doc,
        "The screenshots in this section were captured from the web interface served by the Oracle Cloud deployment. They illustrate four response paths: "
        "a greeting, a disease-information answer, a claim check and a Hindi answer, followed by the administrative dashboard."
    )

    add_heading_2(doc, "5.7.1 Disease Information Retrieval")
    add_body_p(doc,
        "When presented with the inquiry 'What are dengue symptoms?', the system identified the disease entity 'dengue' and returned the curated profile; the "
        "single response time observed on 26 October 2026 was 2.32 seconds. As shown in Figure 5.1(b), the response lists the principal symptoms (high fever, "
        "severe headache, pain behind the eyes, muscle and joint pain, nausea and vomiting, skin rash, and bleeding in severe cases), names its sources "
        "(WHO Dengue Fact Sheet, NVBDCP, MoHFW guidelines), and appends the non-diagnostic disclaimer."
    )
    add_figure(doc, "fig51_landing_dengue.png", "5.1",
               "(a) Web chat landing view after a greeting; (b) disease-information answer for 'What are dengue symptoms?'.",
               width_inches=5.3)

    add_heading_2(doc, "5.7.2 Forwarded Myth Fact-Checking")
    add_body_p(doc,
        "Figure 5.2(a) shows the response to 'fact check: garlic cures dengue'. The verifier matched the claim to a stored myth record (data/kb/myths.json) "
        "and returned a MYTH verdict with a heuristic confidence of 85.4%, together with the explanation that garlic has no antiviral effect against the dengue "
        "virus and that treatment is supportive, followed by sources and the disclaimer. The confidence figure is a heuristic score and not a calibrated probability."
    )
    add_heading_2(doc, "5.7.3 Vernacular Hindi Dialogue Interaction")
    add_body_p(doc,
        "Figure 5.2(b) shows a Hindi exchange. The system detected the Hindi language code ('hi'), identified the disease entity 'malaria', and returned the "
        "answer in Devanagari Hindi (symptoms such as chills with fever, sweating, headache and fatigue), citing WHO Malaria Fact Sheet and MoHFW guidelines "
        "and appending the Hindi disclaimer."
    )
    add_figure(doc, "fig52_factcheck_hindi.png", "5.2",
               "(a) Fact-check verdict (MYTH) with explanation and sources; (b) Hindi answer for a malaria query.",
               width_inches=5.3)

    add_heading_2(doc, "5.7.4 Syndromic Surveillance Administrative Interface")
    add_body_p(doc,
        "Figure 5.3 displays the administrative dashboard (/admin) populated with demonstration data. It shows summary counters for messages and symptom "
        "submissions, intent and language distributions, fact-check verdict counts, and controls to run detection, seed demonstration records or clear them. "
        "When submissions for one pincode and symptom exceed the baseline rule described in Section 4.9, a spike alert is listed in the alert panel; in this capture "
        "no spike alert was active."
    )
    add_figure(doc, "05_admin_dashboard.png", "5.3",
               "Administrative Syndromic Surveillance Dashboard Populated with Demonstration Data.",
               width_inches=4.7)

    add_heading_2(doc, "5.7.5 WhatsApp Channel Exchange")
    add_body_p(doc,
        "Figure 5.4 shows the three test messages as they appeared on the phone of an approved test recipient: a greeting, the dengue-symptoms question and the "
        "claim check 'Fact check: garlic cures dengue'. Each message was answered through the Meta WhatsApp Cloud API and the Cloudflare HTTPS tunnel "
        "described in Section 4.10; the verification steps are summarized in Section 6.6. In panel (b) the welcome text appears first because it was the first "
        "message of a new session, followed by the dengue answer."
    )
    add_figure(doc, "fig54_whatsapp.png", "5.4",
               "WhatsApp Exchange on an Approved Test Recipient's Phone: (a) Greeting; (b) Dengue Symptoms; (c) Fact-Check Verdict.",
               width_inches=5.6)

print("Chapters 4-5 generator module defined successfully.")
