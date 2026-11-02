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
        'AarogyaSathi is built as a set of small, loosely connected services that run asynchronously. This suits the cloud virtual machines we had available, which have limited memory and CPU. Language understanding, vector retrieval, claim checking, symptom tracking and the messaging channels are each kept as a separate subsystem, so a change in one does not force changes in the others. Figure 4.1 shows the Work Breakdown Structure (WBS) we followed over the life of the project:'
    )

    add_figure(doc, "fig_wbs.png", "4.1", 
               'Work Breakdown Structure (WBS) of the AarogyaSathi Modules.', 
               width_inches=5.6)

    add_body_p(doc,
        'The WBS has four main work packages. Package 1.0 (Core NLP & Fast-Path Routing) covers the intent classifiers, the regex entity extractors and the session caches. Package 2.0 (Retrieval & Knowledge Infrastructure) covers LaBSE embeddings, the lexical reranker and the RAG context builder. Package 3.0 (Fact-Checking & Clinical Safety) covers the 64-myth verifier, emergency phrase interception and disclaimer injection. Package 4.0 (Multi-Channel Ingress & Deployment) covers the FastAPI ASGI services, the Meta WhatsApp Cloud API webhooks and the Cloudflare HTTPS tunnel.'
    )

    add_heading_1(doc, "4.2 Detailed Module Responsibilities")
    add_body_p(doc,
        'At runtime the system is made up of ten modules, coordinated by one central orchestrator:'
    )
    add_bullet_p(doc, "1. Orchestrator Router (app/core/router.py)", 
                 'The main execution pipeline. It runs the fast-path checks, keeps the multi-turn dialogue history, applies the emergency red-flag safeguards and coordinates calls to the language model.')
    add_bullet_p(doc, "2. Language Detector (app/core/language.py)", 
                 'Looks at the script and the character distribution of a message across 12 Indian languages and sets the language flag for the conversation.')
    add_bullet_p(doc, "3. Fast-Path Heuristic Engine (_try_fast_path)", 
                 'Runs pre-compiled regular expressions over the query to pick out standard disease questions, infant age milestones and greetings, so the language model is not needed for them.')
    add_bullet_p(doc, "4. Dense Vector Retriever (app/core/retriever.py)", 
                 'Turns the query into a 768-dimensional LaBSE vector and runs a cosine-similarity search over the indexed disease and FAQ records.')
    add_bullet_p(doc, "5. Context Builder & LLM Generator (app/core/generator.py)", 
                 "Builds a clinical prompt from the retrieved records and sends it to Ollama's local C++ runtime, which produces a grounded answer with Qwen3:1.7b.")
    add_bullet_p(doc, "6. Health Claim Verifier (app/factcheck/verifier.py)", 
                 'Takes viral rumours, matches them across languages against the 64 curated Indian myths and returns one of the four verdicts.')
    add_bullet_p(doc, "7. Clinical Safety Filter (app/core/safety.py, app/core/entities.py)", 
                 'Matches a fixed list of acute red-flag terms (chest pain, stroke, breathlessness) in entities.py, builds the emergency reply in safety.py and adds the required disclaimer.')
    add_bullet_p(doc, "8. Session Context Cache (app/core/session.py)", 
                 "Keeps each user's conversation state (the current flow, recent turns and a running summary) in memory, and drops it after 30 minutes.")
    add_bullet_p(doc, "9. Syndromic Surveillance Engine (app/surveillance/syndromic.py)", 
                 'Writes anonymous symptom and pincode events to SQLite and checks them against a rolling 7-day statistical baseline to find unusual rises.')
    add_bullet_p(doc, "10. WhatsApp Channel Adapter (app/channels/whatsapp.py)", 
                 'Handles two-way Meta Graph API v25.0 webhooks. It validates HMAC-SHA256 signatures and sends outgoing messages.')

    add_heading_1(doc, "4.3 Data Storage Architecture: SQLite vs. Curated JSON vs. Sessions")
    add_body_p(doc,
        'The storage layers are kept apart on purpose, according to how long the data lives, how volatile it is and how sensitive it is. We did not put everything into one database. The hybrid storage layout (Figure 4.2) has three parts:'
    )

    add_figure(doc, "fig_er_class.png", "4.2", 
               'Data Storage Layout: SQLite Symptom Data, Curated JSON Files and In-Memory Sessions.', 
               width_inches=5.2)

    add_body_p(doc,
        '1. Persistent Relational Storage (SQLite): The only data that goes to disk is anonymised symptom data, kept in a local SQLite database (data/surveillance.db). It has three tables: events (id, pincode, symptom, lang, ts), messages (id, pincode, intent, lang, verdict, ts) and alerts (id, pincode, symptom, current_count, baseline, severity, ts). Message text, phone numbers and user names are never written to this database.'
    )
    add_body_p(doc,
        '2. Static Curated Knowledge Store (JSON): The clinical content lives in version-controlled JSON files under data/kb/ that are not changed at runtime. They hold 14 disease profiles (diseases.json), 35 FAQs (faq.json), 13 vaccine milestones (vaccines.json), 64 myth records (myths.json) and 8 illustrative outbreak advisories (outbreaks.json). All of them are indexed in memory when the server starts.'
    )
    add_body_p(doc,
        '3. Volatile Ephemeral Session Cache (RAM): Conversation state is held in memory by the Session Python class (session.py). A session has an identifier (the web session ID or the WhatsApp sender), a key-value dictionary with the active flow, recent turns and a summary, and a last-updated timestamp. A session expires after 30 minutes without activity, and all sessions are lost when the server restarts. The WhatsApp handler also keeps a separate in-memory buffer of 4,096 processed message IDs so that duplicate deliveries can be ignored.'
    )

    add_heading_1(doc, "4.4 Knowledge Base Schema and Domain Taxonomy")
    add_body_p(doc,
        'The knowledge base is the clinical foundation of AarogyaSathi. Each record was written by working from official bulletins of the World Health Organization (WHO), the Ministry of Health and Family Welfare (MoHFW), the National Vector Borne Disease Control Programme (NVBDCP) and the Indian Council of Medical Research (ICMR). Table 4.1 lists what the knowledge base contains:'
    )

    kb_headers = ["Domain Category", "Record Count", "Core Entities Covered", "Clinical Source Grounding"]
    kb_rows = [
        ["Endemic Diseases", "14 Profiles", "Dengue, Malaria, Typhoid, Tuberculosis, Cholera, COVID-19, Chikungunya, Rabies, Hepatitis, Diarrhea, Jaundice, Pneumonia, Anemia, Measles", "WHO Fact Sheets, MoHFW Clinical Management Guidelines, NVBDCP National Guidelines"],
        ["Health FAQs", "35 Records", "Water purification, ORS preparation, mosquito net usage, fever management, sanitation, maternal nutrition", "National Health Mission (NHM) IEC Bulletins, UNICEF Water & Sanitation Manuals"],
        ["Child Immunization", "13 Milestones", "Birth, 6 weeks, 10 weeks, 14 weeks, 9-12 months, 16-24 months, 5-6 years (BCG, OPV, Pentavalent, Rotavirus, PCV, MR, DPT)", "Universal Immunization Programme (UIP) National Schedule, MoHFW 2024 Guidelines"],
        ["Misinformation Myths", "64 Claims", "Raw garlic cures dengue, Papaya leaf extracts replace blood transfusion, Vaccines cause autism, Heat destroys all viruses, Onion juice cures fever", "PIB Fact Check India, WHO Mythbusters, ICMR Public Advisories"],
        ["Outbreak Advisories", "8 Advisories", "Seasonal monsoon dengue alerts, tribal malaria warnings, flood-related diarrheal protocols (Sample / Illustrative)", "Integrated Disease Surveillance Programme (IDSP) Weekly Bulletins (Illustrative Demo)"]
    ]
    add_table(doc, kb_headers, kb_rows, "4.1", 'What the Curated Knowledge Base Contains, by Topic', [1.2, 0.9, 2.0, 1.66])

    add_heading_1(doc, "4.5 Cross-Lingual Semantic Retrieval and Dense Vector Search")
    add_body_p(doc,
        'For cross-lingual retrieval without machine translation, the system uses the Language-agnostic BERT Sentence Embedding (LaBSE) transformer (Feng et al., 2022). The 49 main clinical records (14 disease profiles and 35 FAQs) are embedded in advance as normalised 768-dimensional vectors. When a query q arrives, it is tokenised, cut to at most 128 tokens and passed through the LaBSE encoder. Attention-mask weighted mean pooling then gives a normalised query vector e(q).'
    )
    add_body_p(doc,
        'The ranking score S(q, d) between the query vector e(q) and a document vector e(d) combines dense cosine similarity with a simple lexical match:'
    )
    add_code_block(doc, "S(q, d) = cos(e(q), e(d)) + 0.22 * L(q, d)")
    add_body_p(doc,
        'Here cos(e(q), e(d)) is the cosine of the angle between the two normalised 768-dimensional vectors. L(q, d) is the fraction of lowercased query terms (longer than two characters) that appear as exact substrings in document record d. In the deployed system the retriever returns at most the top 5 records whose score is above a confidence threshold of 0.52. The dense part picks up everyday paraphrases, while the lexical part keeps exact drug and disease names from being blurred.'
    )

    add_heading_1(doc, "4.6 Fallback Intent Classification Taxonomy")
    add_body_p(doc,
        'A query that the fast-path rules do not catch goes to a second-stage machine learning intent classifier. It was trained on 289 curated multilingual examples spread over 14 intent classes (Table 4.2). Text is converted to character n-grams of length 2 to 5 with sublinear term-frequency scaling and a vocabulary cap of 30,000 features. A multinomial Logistic Regression model (C=8, L-BFGS solver, at most 1,000 iterations) in scikit-learn 1.9.0 does the classification.'
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
    add_table(doc, intent_headers, intent_rows, "4.2", 'Intent Classes and Distribution of the Training Examples', [1.1, 0.7, 2.3, 1.66])

    add_heading_1(doc, "4.7 Multi-Tier Triage, Fast-Path Heuristics, and Routing Flow")
    add_body_p(doc,
        'We wanted fast answers, but safety checks had to come first. So every message goes through a four-tier decision tree. Figure 4.3 shows the route a message takes:'
    )

    add_figure(doc, "fig_flowchart.png", "4.3", 
               'Flowchart of the Multi-Tier Triage and Fast-Path Routing Decisions.', 
               width_inches=4.7)

    add_body_p(doc,
        "Tier 1 (Emergency Filter): The query is checked first against a compiled regex list of life-threatening presentations. On a match, no neural component runs and the user gets the emergency instruction at once, without any model call. Tier 2 (Fact-Check Ingress): If the query starts with 'fact check:' or closely matches a known health rumour, it goes to the misinformation engine. Tier 3 (Fast-Path Rules): The router looks for common disease names and vaccination age patterns. If one is found, a pre-written, WHO-grounded template is sent right away, so no generative model is used. Tier 4 (Dense RAG Fallback): If none of the rules apply, the query goes to LaBSE retrieval and then to the local Qwen3:1.7b model."
    )

    add_heading_1(doc, "4.8 Health Misinformation Verification Engine")
    add_body_p(doc,
        'The fact-checking subsystem (app/factcheck/verifier.py) is meant to deal with viral health rumours. A claim goes through two stages. First, the engine computes its semantic similarity to the 64 curated Indian health myths. A stored verdict is returned if the best match is close enough and is not about a different disease. Close enough means an embedding similarity of at least 0.70 with enough word overlap, or the configured fact-check threshold with a higher overlap. The verdict is one of four categories: VERIFIED (supported by medical evidence), MYTH (false or harmful), PARTLY TRUE (some truth, but misleading) or UNVERIFIABLE (not enough evidence). If there is no good match, the engine tries an online evidence lookup and then a remedy-pattern fallback. If both fail, it returns UNVERIFIABLE and points to official sources. A few dangerous first-aid myths are caught earlier by fixed rules.'
    )

    add_heading_1(doc, "4.9 Syndromic Telemetry and Outbreak Surveillance Modeling")
    add_body_p(doc,
        'The syndromic surveillance module (app/surveillance/syndromic.py) tracks symptoms reported by 6-digit pincode, to give an early warning. When a user chooses to send a symptom query with a pincode, the event is stored in the local SQLite table. The algorithm compares the count of that symptom in the latest 24 hours, written c(p,s)(t), with its historical baseline b(p,s)(t). The baseline is the mean daily count over the previous seven complete 24-hour periods.'
    )
    add_body_p(doc,
        'An alert candidate is created when the following condition holds:'
    )
    add_code_block(doc, "c(p,s) >= 6  AND  ( b(p,s) < 1.0  OR  c(p,s) >= 3.0 * b(p,s) )")
    add_body_p(doc,
        'If the baseline b(p,s) is at least 1.0, the alert is HIGH severity when c(p,s) reaches 5.0 times the baseline, and MEDIUM otherwise. To avoid flooding officers with alerts, once an alert has been logged for a pincode and symptom pair, further alerts for that pair are held back for 24 hours. These alerts appear on the administrative dashboard (/admin), where health officers can see a summary of the submitted events.'
    )

    add_heading_1(doc, "4.10 Meta WhatsApp Cloud API Channel Sequence Flow")
    add_body_p(doc,
        'The Meta WhatsApp integration lets people use AarogyaSathi directly in WhatsApp. Figure 4.4 follows one request across the network boundaries:'
    )

    add_figure(doc, "fig_whatsapp_seq.png", "4.4", 
               'Message Sequence of the Meta WhatsApp Cloud API Integration and Webhook Path.', 
               width_inches=5.2)

    add_body_p(doc,
        "A citizen sends a message to the test sender number (+1 555 626 0618). Meta's Graph API v25.0 then sends an HTTPS POST webhook to our Cloudflare Tunnel endpoint (route /webhook/whatsapp). The payload carries an HMAC-SHA256 signature in the X-Hub-Signature-256 header. Our FastAPI handler checks that signature against the shared WHATSAPP_APP_SECRET and looks the message ID up in a 4,096-entry deduplication set. It returns HTTP 200 OK to Meta immediately, before any real processing is done. The work itself runs in an asynchronous background task. The task calls the fast-path router, formats the clinical reply and posts it to Meta's messages endpoint, which delivers it to the user's phone."
    )

def add_chapter_5(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_figure, add_code_block):
    add_chapter_title(doc, "5", "Implementation")

    add_heading_1(doc, "5.1 System Implementation Overview and Service Topology")
    add_body_p(doc,
        'AarogyaSathi is written in Python 3.12.3 and runs on an Oracle Cloud Infrastructure (OCI) Arm virtual machine (VM.Standard.A1.Flex) in the Mumbai region (ap-mumbai-1). The machine has 2 OCPUs (Arm-based Ampere Altra), 12 GiB of RAM and a 50 GB boot volume, and runs Ubuntu 24.04 LTS. Two systemd services keep the application running. healthbot.service runs the Uvicorn ASGI web server on internal port 8000. aarogya-tunnel.service runs the official Cloudflare Tunnel daemon (cloudflared v2026.10.3), which provides the HTTPS access from outside.'
    )

    add_heading_1(doc, "5.2 Core Router and Fast-Path Heuristic Implementation")
    add_body_p(doc,
        'The main routing logic is in app/core/router.py. Interpreting a routine message with a language model call would be wasteful, so the router first tries a fast path. This combines the TF-IDF intent classifier with regular-expression entity matching. An excerpt of _try_fast_path follows:'
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
        'When a query matches a pre-compiled disease entity or a greeting, the fast-path engine formats the verified WHO/MoHFW advice and returns it directly. No language model tokens are generated.'
    )

    add_heading_1(doc, "5.3 Knowledge Base Retrieval and Dense Vector Search Implementation")
    add_body_p(doc,
        'Semantic search is implemented in app/core/retriever.py and app/core/embeddings.py. Document embeddings come from the pretrained sentence-transformers/LaBSE checkpoint, loaded through HuggingFace Transformers. Pooling and similarity are computed in PyTorch:'
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
        "The fact-checking pipeline (app/factcheck/verifier.py) handles claims that start with 'fact check:' or that resemble known rumours. It compares the claim text with data/kb/myths.json and produces a structured result:"
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
        "The WhatsApp integration (app/channels/whatsapp.py) follows the security requirements in Meta's developer guidelines. Each incoming webhook payload is authenticated with an HMAC-SHA256 signature, which stops forged requests and tampering in transit:"
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
        "The web interface (web/index.html and web/chat.js) is a light, mobile-friendly single-page app. It has a chat area, quick-prompt chips ('Dengue info', 'Symptom check', 'Vaccines', 'Fact check') and an optional 6-digit pincode field for local alerts. Figure 5.1(a) shows the landing screen after a greeting."
    )

    add_heading_1(doc, "5.7 Conversational Walkthrough on the Deployed Service")
    add_body_p(doc,
        'All screenshots in this section were taken from the web interface served by the Oracle Cloud deployment. They show four kinds of response (a greeting, a disease-information answer, a claim check and a Hindi answer) and then the administrative dashboard.'
    )

    add_heading_2(doc, "5.7.1 Disease Information Retrieval")
    add_body_p(doc,
        "For the question 'What are dengue symptoms?', the system recognised the disease 'dengue' and returned the stored profile. The single response we timed on 26 October 2026 took 2.32 seconds. As Figure 5.1(b) shows, the answer lists the main symptoms (high fever, severe headache, pain behind the eyes, muscle and joint pain, nausea and vomiting, skin rash, and bleeding in severe cases). It also names its sources (WHO Dengue Fact Sheet, NVBDCP, MoHFW guidelines) and ends with the non-diagnostic disclaimer."
    )
    add_figure(doc, "fig51_landing_dengue.png", "5.1",
               "(a) Web chat landing view after a greeting; (b) disease-information answer for 'What are dengue symptoms?'.",
               width_inches=5.3)

    add_heading_2(doc, "5.7.2 Forwarded Myth Fact-Checking")
    add_body_p(doc,
        "Figure 5.2(a) shows the reply to 'fact check: garlic cures dengue'. The verifier matched the claim to a stored myth record (data/kb/myths.json) and gave a MYTH verdict with a heuristic confidence of 85.4%. The explanation says that garlic has no antiviral effect on the dengue virus and that treatment is supportive. Sources and the disclaimer follow. The 85.4% is a heuristic score, not a calibrated probability."
    )
    add_heading_2(doc, "5.7.3 Vernacular Hindi Dialogue Interaction")
    add_body_p(doc,
        "Figure 5.2(b) shows a conversation in Hindi. The system detected the language code 'hi' and the disease 'malaria', and answered in Devanagari Hindi, listing symptoms such as chills with fever, sweating, headache and tiredness. It cited the WHO Malaria Fact Sheet and MoHFW guidelines and added the Hindi disclaimer."
    )
    add_figure(doc, "fig52_factcheck_hindi.png", "5.2",
               "(a) Fact-check verdict (MYTH) with explanation and sources; (b) Hindi answer for a malaria query.",
               width_inches=5.3)

    add_heading_2(doc, "5.7.4 Syndromic Surveillance Administrative Interface")
    add_body_p(doc,
        'Figure 5.3 shows the administrative dashboard (/admin) filled with demonstration data. It has counters for messages and symptom submissions, charts of intent and language, fact-check verdict counts, and buttons to run detection, add demonstration records or clear them. When submissions for one pincode and symptom pass the baseline rule from Section 4.9, a spike alert appears in the alert panel. No spike alert was active when this screenshot was taken.'
    )
    add_figure(doc, "05_admin_dashboard.png", "5.3",
               'Admin Surveillance Dashboard Filled with Demonstration Data.',
               width_inches=4.7)

    add_heading_2(doc, "5.7.5 WhatsApp Channel Exchange")
    add_body_p(doc,
        "Figure 5.4 shows three test messages on the phone of an approved test recipient: a greeting, the dengue-symptoms question and the claim check 'Fact check: garlic cures dengue'. Each was answered through the Meta WhatsApp Cloud API and the Cloudflare HTTPS tunnel from Section 4.10. The verification steps are summarised in Section 6.6. In panel (b) the welcome text comes first because it was the first message of a new session, and the dengue answer follows it."
    )
    add_figure(doc, "fig54_whatsapp.png", "5.4",
               "WhatsApp Messages on an Approved Test Recipient's Phone: (a) Greeting; (b) Dengue Symptoms; (c) Fact-Check Verdict.",
               width_inches=5.6)

print("Chapters 4-5 generator module defined successfully.")
