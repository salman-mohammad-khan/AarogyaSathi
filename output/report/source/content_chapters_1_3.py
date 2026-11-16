"""
Chapters 1 to 3 Generator for AarogyaSathi Minor Project Report
- Chapter 1: Introduction (5 pages)
- Chapter 2: Problem Statement (4 pages)
- Chapter 3: Analysis (6 pages)
"""

from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_chapter_1(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_figure, add_table):
    add_chapter_title(doc, "1", "Introduction")

    add_heading_1(doc, "1.1 Healthcare Information Landscape and the Infodemic")
    add_body_p(doc, 
        'Over the last decade the way people in India look for health information has changed a lot. Phones are cheap, mobile data is cheaper, and most of what people read about their health now arrives through a screen. The WHO calls the resulting flood of material an infodemic: too much information, some of it right and some of it wrong, appearing during a health emergency or even during ordinary healthcare (World Health Organization et al., 2020). India has more than 800 million broadband subscribers, and WhatsApp is where much of the informal sharing happens. That reach has a cost. Forwards claim that raw garlic or papaya leaf extract cures dengue. Others link vaccines to neurological disease with no evidence. Meanwhile people misread early symptoms, reach a hospital late, and end up with illness and bills that could have been avoided.'
    )

    add_heading_1(doc, "1.2 Target Audience and Socio-Economic Context in Rural India")
    add_body_p(doc,
        'This project is meant for people in rural, peri-urban and tribal districts of India. We started with Odisha because of the Smart India Hackathon 2025 problem statement. In these areas there are few qualified doctors, and the doctor-to-population ratio is often well below the WHO benchmark of 1:1,000. Primary health centres (PHCs) and community health centres (CHCs) have limited diagnostic facilities, so a great deal rests on frontline workers such as Accredited Social Health Activists (ASHAs) and Auxiliary Nurse Midwives (ANMs). Language makes things harder. India has 22 scheduled languages, and an English-only health portal is of no use to someone who speaks only Odia or Hindi. What these users need is a chatbot that answers in their own language and works for typed messages and, ideally, voice.'
    )

    add_heading_1(doc, "1.3 Project Motivation and Clinical Scope Boundaries")
    add_body_p(doc,
        "AarogyaSathi (आरोग्यसाथी, meaning 'Healthcare Companion') is a chatbot that tries to put reliable clinical knowledge in front of ordinary people who have health questions. The idea is simple. Someone should be able to learn about a disease, check a vaccination schedule or test a rumour without travelling to a clinic or paying for advice. We were also careful about what the system should not do. AarogyaSathi is an awareness and education tool. It does not diagnose, it does not replace triage by a health professional, and it does not prescribe (Semigran et al., 2015). Ordinary questions get an educational answer with a clear disclaimer attached. If a message describes a possible emergency, hardcoded red-flag rules take over and send the user to the national emergency numbers, 108 and 112."
    )

    add_heading_1(doc, "1.4 Smart India Hackathon Brief (SIH25049) and Objectives")
    add_body_p(doc,
        'The work began as an entry to Smart India Hackathon 2025, under problem statement SIH25049 from the Government of Odisha in the Healthcare Technology theme (DRIEMS University, 2025). The brief asked for a multilingual, AI-based public health chatbot that could share information on disease prevention, symptoms, national immunisation schedules and outbreak warnings, and could help verify health claims, over web, WhatsApp and SMS. We set ourselves five objectives:'
    )
    add_bullet_p(doc, "Objective 1 (Curated Knowledge Grounding)", 
                 'Build a structured knowledge base of the major endemic diseases, childhood immunisation milestones and common rural health questions, using only WHO, MoHFW and ICMR guidance as sources.')
    add_bullet_p(doc, "Objective 2 (Cross-Lingual Semantic Retrieval)", 
                 'Use Language-agnostic BERT Sentence Embeddings (LaBSE) for cross-lingual retrieval, so that queries in Indian languages can be matched directly without a lossy translation step.')
    add_bullet_p(doc, "Objective 3 (Automated Misinformation Verification)", 
                 'Build a fact-checking engine that compares forwarded claims against a curated list of myths and returns a clear verdict with a short clinical explanation.')
    add_bullet_p(doc, "Objective 4 (Ubiquitous Multi-Channel Ingress)", 
                 'Deliver the system through a light web portal and a Meta WhatsApp Cloud API channel, so that it works on a basic smartphone.')
    add_bullet_p(doc, "Objective 5 (Syndromic Anomaly Surveillance)", 
                 'Use anonymous symptom reports tagged with a postal pincode to detect possible local outbreaks over a rolling 7-day window.')

    add_heading_1(doc, "1.5 Overview of the AarogyaSathi Solution Architecture")
    add_body_p(doc,
        'These goals had to be met on a small budget, so AarogyaSathi uses a layered hybrid design (Figure 1.1). Every message, whether it comes from the web or from WhatsApp, first passes through deterministic safety checks and fast-path rules. A message containing an emergency red flag never reaches a machine learning model; it gets an urgent instruction straight away. For routine questions, simple pattern rules look for a known disease or immunisation milestone. When one is found, a pre-written and verified template is returned immediately, which saves the delay of calling a generative model for questions that do not need one.'
    )
    
    add_figure(doc, "architecture_publication.png", "1.1", 
               "High-Level Solution Topology and Channel Architecture of AarogyaSathi (Adapted from Khan et al., 2026).", 
               width_inches=5.5)

    add_body_p(doc,
        'Messages with more complex wording go to the semantic retrieval pipeline. The query is converted by a 768-dimensional LaBSE model into an embedding and compared with the indexed records using a combined cosine and lexical similarity score. The best matches are then passed as context to Qwen3 (1.7B parameters), a language model that runs locally through Ollama. Because the model is told to answer only from the retrieved records, it has much less room to make things up, and it can still reply in fluent regional language. In parallel, symptom submissions are stored in SQLite so that the system can look for clusters over seven days.'
    )

    add_heading_1(doc, "1.6 Background and Literature Review")
    add_body_p(doc,
        'Two ideas underpin the design. The first is Retrieval-Augmented Generation (RAG; Lewis et al., 2020), which combines a neural text generator with an external document index. This sharply cuts factual hallucination, and the knowledge base can be updated without retraining the model. The second is cross-lingual embedding with LaBSE (Feng et al., 2022). LaBSE places sentences with the same meaning close together across 109 languages, so a casual Hindi question can match an English clinical record directly, with no translation step in between.'
    )
    add_body_p(doc,
        'The literature on medical chatbots, however, gives good reason to be careful. The systematic reviews by Laranjo et al. (2018) and Milne-Ives et al. (2020) found that most chatbots had only been tested on small dialogue sets written by their own developers. There was little independent clinical validation, blinded review or safety testing with negated statements. Semigran et al. (2015) audited online symptom checkers and found the triage advice was correct in only 57% of cases. These findings shaped how we tested. We did not try to show that AarogyaSathi is clinically perfect. We tried to show where it fails, how much its test data overlaps with its training data, and how it handles negation. Table 1.1 compares the main features:'
    )

    # Comparative Table
    headers = ["Feature Dimension", "Conventional Commercial Bots", "Generic Generative LLMs", "AarogyaSathi Hybrid Pipeline"]
    rows = [
        ["Knowledge Provenance", "Static rule trees or closed API", "Parametric web training memory", "Curated WHO/MoHFW Grounded Store"],
        ["Cross-Lingual Support", "Machine translated English", "Multilingual token completion", "Native LaBSE Dense Vector Space"],
        ["Misinformation Checking", "Not supported / out of scope", "Variable parametric hallucination", "Dedicated 64-Myth Verification Engine"],
        ["Emergency Triage", "Generic disclaimer", "Varies with prompt engineering", "Hardcoded Deterministic Red-Flag Bypass"],
        ["Operating Cost", "High SaaS per-user licensing", "Expensive token API metering", "Open-source stack on free-tier hosting"],
        ["Channel Accessibility", "Proprietary standalone app", "Web browser interface only", "Dual: Lightweight Web + Meta WhatsApp"]
    ]
    col_w = [1.2, 1.45, 1.45, 1.66]
    add_table(doc, headers, rows, "1.1", "Comparative Analysis of Conventional Chatbots vs. AarogyaSathi Hybrid Pipeline", col_w)

    add_heading_1(doc, "1.7 Organization of the Report")
    add_body_p(doc,
        'The rest of this report has seven more chapters and follows the BPIT B.Tech Minor Project format. Chapter 2 states the problem, the objectives, the stakeholder personas and the system boundaries. Chapter 3 covers analysis: the Software Requirements Specification (SRS), functional and non-functional requirements, feasibility, use cases and data flow diagrams. Chapter 4 describes the design, including the work breakdown structure (WBS), the modules, the database schema, the LaBSE retrieval maths and the WhatsApp sequence diagram. Chapter 5 explains the implementation, the key algorithms and the services, with screenshots of the web and WhatsApp channels. Chapter 6 is about testing: the automated suite, component benchmarks, the training-overlap analysis, defects found in clinical spot checks, and live WhatsApp delivery. Chapter 7 gives the summary and conclusion. Chapter 8 lists the limitations honestly and sets out what we would do next. The APA bibliography and technical appendices follow.'
    )

def add_chapter_2(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_table):
    add_chapter_title(doc, "2", "Problem Statement")

    add_heading_1(doc, "2.1 Formal Problem Definition")
    add_body_p(doc,
        'The problem this project addresses can be stated in one sentence. People in rural and semi-urban India often cannot get health information that is timely, available in their language and clinically checked. As a result they are exposed to health misinformation, seek care late, vaccinate their children less often than they should, and are caught out by seasonal epidemics.'
    )
    add_body_p(doc,
        'That one problem breaks down into three smaller ones:'
    )
    add_bullet_p(doc, "1. The Vernacular Accessibility Barrier", 
                 'Guidelines from the Ministry of Health and Family Welfare (MoHFW) and the WHO are thorough, but they are mostly written in dense academic English or formal official Hindi. More than 70% of rural Indians speak regional languages and dialects, so for them these advisories are effectively out of reach.')
    add_bullet_p(doc, "2. Uninhibited Proliferation of Digital Health Misinformation", 
                 'Messaging apps make it easy for pseudoscientific health claims to spread. Forwards that promote unproven herbal cures for mosquito-borne diseases, or that feed doubts about vaccines, travel with nothing to check them. They weaken immunisation programmes and other public health efforts.')
    add_bullet_p(doc, "3. Critical Clinical Latency and Triage Failures", 
                 'Someone with early symptoms often cannot tell whether to rest at home, visit the local health centre, or call an ambulance. A general web search returns long lists of possible diagnoses, from simple tiredness to cancer. That produces needless panic in some people and dangerous complacency in others.')

    add_heading_1(doc, "2.2 Core Project Objectives")
    add_body_p(doc,
        'To tackle this problem, AarogyaSathi sets out five specific and measurable technical objectives:'
    )
    add_bullet_p(doc, "Objective 1: Multi-Tier Hybrid Conversational Pipeline",
                 'Build a conversational engine that answers citizen questions using deterministic safety rules, rule-based fast-path matching and dense semantic retrieval, with model-generated answers returned within a few seconds on the cloud virtual machine.')
    add_bullet_p(doc, "Objective 2: Authoritative Multilingual Knowledge Grounding",
                 'Create and maintain a structured knowledge base of 14 major endemic diseases, 13 national childhood vaccination milestones and 35 common health questions in English and Hindi, with semantic cross-lingual detection across 12 Indian languages.')
    add_bullet_p(doc, "Objective 3: Heuristic Misinformation Fact-Checking",
                 'Develop a claim-verification engine that accepts a forwarded text claim, matches it across languages against a curated catalogue of 64 Indian health myths, and returns one of four verdicts (VERIFIED, MYTH, PARTLY TRUE, UNVERIFIABLE) with a clinical explanation.')
    add_bullet_p(doc, "Objective 4: Ubiquitous Dual-Channel Mobile Ingress",
                 'Provide two interfaces: a responsive mobile web app that needs no installation, and a Meta WhatsApp Cloud API integration (demonstrated with an approved test recipient). Both let people use the chatbot on a basic smartphone without paying for a subscription.')
    add_bullet_p(doc, "Objective 5: Geospatial Syndromic Outbreak Telemetry",
                 'Build an experimental surveillance module that collects voluntary and anonymous symptom reports by postal pincode and checks them against a rolling 7-day baseline, in order to spot possible disease clusters.')

    add_heading_1(doc, "2.3 Key Stakeholders and User Personas")
    add_body_p(doc,
        "To keep the design grounded in real needs, we wrote three personas. They are composite examples, not real people, and they stand for key groups in India's public healthcare chain:"
    )
    add_bullet_p(doc, "Persona 1: Ramesh (Rural Smallholder Farmer, Mayurbhanj, Odisha)",
                 'Ramesh is 42, speaks Odia and reads some Hindi. He uses a low-cost Android phone on prepaid 4G, and his family lives 18 kilometres from the nearest Primary Health Centre. When his son gets a high fever, chills and body aches, Ramesh wants quick, trustworthy advice in simple Hindi or Odia. He needs to know whether it could be malaria and what to do next, without being steered by WhatsApp home remedies.')
    add_bullet_p(doc, "Persona 2: Sunita Devi (ASHA Community Health Worker, Rural Cuttack)",
                 'Sunita is an Accredited Social Health Activist who looks after maternal and child health in two hamlets of about 1,800 people. She needs a reliable reference on her phone for the exact immunisation milestones at 6, 10 and 14 weeks. She also needs something to counter the rumours about measles-rubella vaccine safety that come up during village immunisation drives.')
    add_bullet_p(doc, "Persona 3: Dr. Patnaik (District Surveillance Officer, IDSP Odisha)",
                 'Dr. Patnaik oversees communicable disease monitoring for a district. He wants a tool that can show unusual rises in reported symptoms, such as acute febrile illness or loose stools, mapped by pincode. Ideally it would give an early signal days before lab-confirmed cases show up on the Integrated Disease Surveillance Programme (IDSP) portal.')

    add_heading_1(doc, "2.4 System Boundaries, Operating Assumptions, and Clinical Non-Claims")
    add_body_p(doc,
        'It matters to be clear about what the system can and cannot do. AarogyaSathi works within the following boundaries and assumptions:'
    )
    add_bullet_p(doc, "1. Non-Diagnostic Posture", 
                 'AarogyaSathi does not give differential diagnoses, write prescriptions or calculate drug doses. Every response carries a disclaimer saying the information is for awareness only and is not a substitute for examination by a registered medical practitioner.')
    add_bullet_p(doc, "2. Ephemeral Session Telemetry", 
                 'The persistent SQLite database stores only the pincode, symptom, intent, language and verdict. It holds no message text, names or phone numbers. Short conversation history is kept in memory with a 30-minute Time-To-Live (TTL) and is dropped when the session expires.')
    add_bullet_p(doc, "3. Outbreak Advisory Illustrative Nature", 
                 'The cluster detection algorithm works, but the outbreak records bundled with the project are illustrative seasonal advisories used for demonstration. They are not a live, authenticated feed from state or central epidemiologists.')
    add_bullet_p(doc, "4. Restricted Demonstration Environment", 
                 'The Meta WhatsApp Cloud API channel runs on a developer test number (+1 555 626 0618) and can message only authorised recipients. It is not a full commercial production number.')

    add_heading_1(doc, "2.5 Acceptance Criteria and Success Metrics")
    add_body_p(doc,
        'We treated the engineering work as complete when it met six acceptance criteria:'
    )
    add_bullet_p(doc, "AC-1 (Test Suite Integrity)", 'Every test in the automated suite passes on the deployment host. The suite covers core routing, RAG retrieval, the ML classifiers and the channel adapters.')
    add_bullet_p(doc, "AC-2 (Fast-Path Latency)", 'Rule-based replies (greetings, emergency red flags) are returned without calling the language model, and model-generated answers arrive within a few seconds on the cloud virtual machine.')
    add_bullet_p(doc, "AC-3 (Retrieval Precision)", 'Top-1 retrieval accuracy is above 90% on the curated clinical test queries, measured against the 49-record indexed health corpus.')
    add_bullet_p(doc, "AC-4 (Fact-Checking Coverage)", 'The system assigns the correct verdict across a curated test set of common Indian health myths, with no unhandled runtime exceptions.')
    add_bullet_p(doc, "AC-5 (Channel Operational Verification)", 'Messages are delivered in both directions on the web app and on the Meta WhatsApp Cloud API test number, and webhook signature validation works.')
    add_bullet_p(doc, "AC-6 (Clinical Safety Red-Flag Assurance)", 'Critical emergency phrases are caught by fixed rules and sent to the hotline message, so the safety path never depends on a probabilistic language model.')

def add_chapter_3(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_figure, add_table):
    add_chapter_title(doc, "3", "Analysis")

    add_heading_1(doc, "3.1 Software Requirement Specifications (SRS Overview)")
    add_body_p(doc,
        'The Software Requirement Specification (SRS) sets out what AarogyaSathi must do and how well it must do it. It is the technical baseline we built, deployed and evaluated against. The system is an asynchronous, service-oriented web and messaging platform. It is designed to handle many users at once, respond quickly and run on free-tier cloud hosting.'
    )

    add_heading_1(doc, "3.2 Functional Requirements (FR)")
    add_body_p(doc,
        'The functional scope is split into eight requirement modules, FR-1 to FR-8, listed in Table 3.1:'
    )

    fr_headers = ["Req ID", "Functional Module", "Detailed Requirement Specification"]
    fr_rows = [
        ["FR-1", "Multilingual Ingress & Language Detection", 'The system shall accept free-text messages from the web app and from WhatsApp webhooks, detect which of 12 Indian languages the user is writing in, and keep session context in volatile memory.'],
        ["FR-2", "Deterministic Emergency Triage", 'The system shall catch predefined red-flag symptoms (chest pain, acute breathlessness, severe bleeding) straight away and reply with the emergency numbers (108/112), without using any ML component.'],
        ["FR-3", "Fast-Path Rule Execution", 'The system shall recognise routine queries (greetings, common disease questions, vaccine ages) with compiled regex patterns and return verified answers without calling the generative model.'],
        ["FR-4", "Dense Vector Semantic Retrieval", 'The system shall embed any health question that the rules could not answer with LaBSE (768-dimensional vectors) and retrieve the top-k matching clinical profiles from the indexed corpus, reranked by cosine and lexical score.'],
        ["FR-5", "Retrieval-Augmented Generation", "The system shall pass the retrieved clinical context to an open-source language model (Qwen3:1.7b, run through Ollama) so that it writes a short, grounded answer in the user's language."],
        ["FR-6", "Health Misinformation Fact-Checking", "The system shall take forwarded claims that start with 'fact check:' or resemble known rumours, compare them with the 64 curated Indian myths, and return a categorised verdict with source citations."],
        ["FR-7", "Syndromic Anomaly Detection", 'The system shall store voluntary symptom and pincode pairs in SQLite and raise an alert, with a severity level, when the 24-hour count goes above 3x the 7-day rolling baseline.'],
        ["FR-8", "Meta WhatsApp Cloud API Integration", 'The system shall receive webhook payloads from Meta Graph API v25.0, verify their HMAC-SHA256 signatures, ignore duplicate message IDs and send replies over HTTPS, splitting long ones.']
    ]
    add_table(doc, fr_headers, fr_rows, "3.1", "Functional Requirements Specification (FR-1 through FR-8)", [0.8, 1.8, 3.16])

    add_heading_1(doc, "3.3 Non-Functional Requirements (NFR)")
    add_body_p(doc,
        'Beyond the functions, the architecture follows six non-functional standards (Table 3.2):'
    )

    nfr_headers = ["Req ID", "Quality Attribute", "Target Specification & Evaluation Criterion"]
    nfr_rows = [
        ["NFR-1", "Latency & Performance", 'Rule-based replies are sent without calling the language model. Model-assisted answers arrive within a few seconds. Webhook requests are acknowledged before the background work finishes.'],
        ["NFR-2", "Privacy & Ethical Security", 'The database holds no message text, names or phone numbers. Sessions live only in memory with a 30-minute TTL. Webhooks are checked with HMAC-SHA256 signatures.'],
        ["NFR-3", "Reliability & Availability", 'The services run continuously under systemd on the Oracle VM, restart on their own if a process dies, and degrade gracefully if Ollama fails.'],
        ["NFR-4", "Hosting Resource Efficiency", 'Runs within 2 OCPUs and 12 GiB RAM on an Oracle Cloud Arm virtual machine, with no GPU.'],
        ["NFR-5", "Linguistic Adaptability", 'Understands queries across English, Hindi and 10 regional Indian languages through LaBSE multilingual embeddings.'],
        ["NFR-6", "Clinical Grounding & Safety", 'Every non-emergency reply carries a clinical disclaimer and cites the public health authority it relies on (WHO, MoHFW, NVBDCP).']
    ]
    add_table(doc, nfr_headers, nfr_rows, "3.2", "Non-Functional Requirements Specification (NFR-1 through NFR-6)", [0.8, 1.6, 3.36])

    add_heading_1(doc, "3.4 Feasibility Study (Technical, Operational, Economic)")
    add_body_p(doc,
        'Before committing to the architecture we looked at feasibility from three angles:'
    )
    add_bullet_p(doc, "1. Technical Feasibility", 
                 "We checked whether transformer embeddings and a quantised language model would run on an ARM64 cloud machine. The LaBSE model and Qwen3:1.7b under Ollama's C++ runtime use about 3.5 GiB of memory, well within the 12 GiB on our Oracle Cloud VM. FastAPI handles requests asynchronously, so a slow request does not block the others.")
    add_bullet_p(doc, "2. Operational Feasibility", 
                 'People in rural India already use WhatsApp and simple mobile browsers every day. Because AarogyaSathi works inside WhatsApp and through a responsive HTML5 page, users have little to install or learn, which suits their existing habits.')
    add_bullet_p(doc, "3. Economic Feasibility", 
                 'Everything in the stack is open source (Python 3.12, FastAPI, PyTorch, Ollama, SQLite), and the infrastructure is free-tier: an Oracle Cloud Arm virtual machine, a Cloudflare HTTPS tunnel and the Meta WhatsApp Developer test number. We paid no recurring software or API fees during the prototype phase. We did not estimate what a public deployment would cost in the long run.')

    add_heading_1(doc, "3.5 Tools, Technologies, and Hardware Platform")
    add_body_p(doc,
        'Table 3.3 summarises the software stack and the hardware specification of the virtual machine on Oracle Cloud Infrastructure:'
    )

    env_headers = ["Layer / Domain", "Technology Component", "Version", "Role in System Architecture"]
    env_rows = [
        ["Compute Platform", "Oracle Cloud Infrastructure (OCI)", "Free-tier eligible Arm shape", "2 OCPU, 12 GiB RAM, 50 GB boot volume (Ubuntu 24.04 ARM64)"],
        ["Backend Framework", "FastAPI / Uvicorn", "0.115.0", "Asynchronous ASGI web server and API routing"],
        ["NLP / Vector Search", "HuggingFace Transformers", "5.15.1", "LaBSE 768-dim multilingual sentence embeddings"],
        ["Machine Learning", "scikit-learn", "1.9.0", "TF-IDF character n-gram extraction & Logistic Regression"],
        ["Deep Learning Runtime", "PyTorch", "2.6.0", "Tensor pooling and cosine similarity computation"],
        ["LLM Inference Engine", "Ollama Runtime", "0.32.15", "Local quantized inference for Qwen3 (1.7B parameter)"],
        ["Database Management", "SQLite 3", "3.45.1", "Persistent relational storage for syndromic telemetry"],
        ["Ingress / Networking", "Cloudflare Tunnel (cloudflared)", "2026.10.3", "Secure HTTPS tunnel exposing VM port 8000 to public web"],
        ["Messaging Gateway", "Meta WhatsApp Cloud API", "v25.0", "Bidirectional webhook gateway for WhatsApp mobile client"]
    ]
    add_table(doc, env_headers, env_rows, "3.3", "Minimum Hardware and Software Execution Environment Specifications", [1.3, 1.6, 0.9, 1.96])

    add_heading_1(doc, "3.6 Use Case Modeling and Actor Interactions")
    add_body_p(doc,
        'The functions of AarogyaSathi are modelled with UML use case diagrams. There are three main actors: the Citizen / Mobile User, the Frontline Health Worker (ASHA), and the Public Health Administrator / Surveillance Officer (Figure 3.1):'
    )

    add_figure(doc, "fig_usecase.png", "3.1", 
               "Use Case Model for Citizen, Health Worker, and Administrative Actors.", 
               width_inches=4.9)

    add_body_p(doc,
        'There are seven main use cases. UC-1 (Inquire Disease and Symptoms): a citizen types a question in natural language and gets a grounded clinical description. UC-2 (Verify Forwarded Health Claim): a user submits a viral message and gets a verdict. UC-3 (Query Vaccination Milestones): parents and ASHA workers look up which vaccines are due at a given age. UC-4 (Emergency Red-Flag Triage): signs of acute distress are flagged straight away. UC-5 (Report Symptoms with Pincode): users can voluntarily add to community health monitoring. UC-6 (Interact via WhatsApp): all of the above are available on WhatsApp. UC-7 (Monitor Syndromic Cluster Alerts): health officers review local anomaly alerts on the admin dashboard.'
    )

    add_heading_1(doc, "3.7 Data Flow Modeling (Level 0 and Level 1 DFD)")
    add_body_p(doc,
        'Data flow diagrams (DFDs) show how information moves across the system boundary and how it is changed inside. Figure 3.2 is the context-level DFD (Level 0), which shows the external entities that connect to the single AarogyaSathi process:'
    )

    add_figure(doc, "fig_dfd_lvl0.png", "3.2", 
               "Context-Level Data Flow Diagram (DFD Level 0) for Public Health Inquiries.", 
               width_inches=5.0)

    add_body_p(doc,
        'Figure 3.3 opens up the system as a detailed Level 1 DFD with six processes: 1.0 Emergency Filter & Red-Flag Validation, 2.0 Fast-Path Heuristic Router, 3.0 Health Misinformation Verifier, 4.0 LaBSE Dense Vector Semantic Retriever, 5.0 RAG Context Synthesis & LLM Generation, and 6.0 Syndromic Anomaly Surveillance. The diagram also shows four data stores: D1 (Volatile User Session Cache), D2 (Curated 64-Myth Store), D3 (Clinical Knowledge Base: 14 Diseases, 35 FAQs, 13 Vaccines) and D4 (Relational Telemetry DB in SQLite).'
    )

    add_figure(doc, "fig_dfd_lvl1.png", "3.3", 
               "Detailed Functional Data Flow Diagram (DFD Level 1) of Core Engine and Data Stores.", 
               width_inches=4.7)

print("Chapters 1-3 generator module defined successfully.")
