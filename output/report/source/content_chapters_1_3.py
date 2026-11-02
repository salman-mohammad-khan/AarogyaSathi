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
        "In contemporary public health administration, the rapid proliferation of digital communication networks has fundamentally altered "
        "how citizens seek, interpret, and act upon health-related information. While internet connectivity has expanded dramatically across "
        "developing nations, the sheer volume of unfiltered digital content has precipitated what the World Health Organization (WHO) formally "
        "classifies as an infodemic—an overabundance of information, both accurate and inaccurate, that accompanies an acute health emergency or "
        "pervades routine healthcare management (World Health Organization et al., 2020). In India, where mobile internet penetration exceeds 800 million "
        "broadband subscribers, digital messaging platforms such as WhatsApp have become the primary conduit for informal communication. However, this "
        "ubiquitous reach is accompanied by profound risks: unverified home remedies for vector-borne diseases (e.g., claims that raw garlic or papaya leaf "
        "extracts eliminate dengue viruses), vaccine hesitancy stoked by baseless assertions connecting immunizations to neurological disorders, and delayed "
        "hospital presentations caused by misdiagnosed acute symptoms, translating directly into preventable morbidity and severe economic stress."
    )

    add_heading_1(doc, "1.2 Target Audience and Socio-Economic Context in Rural India")
    add_body_p(doc,
        "The primary beneficiaries of this project are citizens residing in rural, peri-urban, and tribal districts of India, with specific initial "
        "contextualization toward the state of Odisha under the Smart India Hackathon 2025 mandate. In these geographic regions, healthcare infrastructure "
        "is characterized by a severe density deficit of qualified allopathic clinicians, where the doctor-to-population ratio frequently falls significantly "
        "below the WHO-recommended threshold of 1:1,000. Rural primary health centres (PHCs) and community health centres (CHCs) operate under severe "
        "diagnostic constraints, placing enormous responsibility on frontline community health workers—Accredited Social Health Activists (ASHAs) "
        "and Auxiliary Nurse Midwives (ANMs). Compounding this deficit are formidable linguistic and digital literacy barriers across 22 scheduled "
        "languages. Monolingual English health portals fail completely when accessed by rural citizens communicating exclusively in regional idioms "
        "such as Odia or Hindi, creating an urgent societal imperative for an accessible, voice- and text-compatible vernacular conversational interface."
    )

    add_heading_1(doc, "1.3 Project Motivation and Clinical Scope Boundaries")
    add_body_p(doc,
        "AarogyaSathi (आरोग्यसाथी, translating to 'Healthcare Companion') was conceived as an intelligent, automated digital public health assistant "
        "engineered to bridge the gap between authoritative clinical knowledge and grassroots citizen inquiries. The core motivation is to empower "
        "every citizen with immediate, low-cost access to medically grounded disease awareness, immunization tracking, and health rumor verification, "
        "without requiring personal travel or financial sacrifice. Crucially, the system is designed with rigorous and unambiguous clinical scope boundaries: "
        "AarogyaSathi is strictly an informational and educational health awareness tool; it is explicitly not a diagnostic system, a medical triage substitute, "
        "or an automated prescribing platform (Semigran et al., 2015). Routine queries receive educational guidance accompanied by mandatory clinical disclaimers, "
        "while potential emergencies immediately trigger hardcoded red-flag escalations directing users to national emergency hotlines (108/112)."
    )

    add_heading_1(doc, "1.4 Smart India Hackathon Brief (SIH25049) and Objectives")
    add_body_p(doc,
        "The project was formulated under the auspices of Smart India Hackathon 2025, specifically addressing problem statement SIH25049 released by the "
        "Government of Odisha under the Healthcare Technology theme (DRIEMS University, 2025). The official challenge brief mandated developing an "
        "AI-driven, multilingual public health chatbot capable of disseminating disease prevention information, symptoms, national immunization schedules, "
        "outbreak warnings, and health-forward verification via web, WhatsApp, and SMS channels. In response, five technical objectives were established:"
    )
    add_bullet_p(doc, "Objective 1 (Curated Knowledge Grounding)", 
                 "Construct an authoritative structured knowledge base encompassing major endemic diseases, childhood immunization milestones, and rural health inquiries grounded strictly in WHO, MoHFW, and ICMR guidelines.")
    add_bullet_p(doc, "Objective 2 (Cross-Lingual Semantic Retrieval)", 
                 "Implement a cross-lingual retrieval pipeline using Language-agnostic BERT Sentence Embeddings (LaBSE) to support queries in regional Indian languages without multi-stage translation errors.")
    add_bullet_p(doc, "Objective 3 (Automated Misinformation Verification)", 
                 "Engineer an automated fact-checking engine matching forwarded claims against curated myth repositories to assign categorical truth verdicts with transparent clinical rationales.")
    add_bullet_p(doc, "Objective 4 (Ubiquitous Multi-Channel Ingress)", 
                 "Deploy the solution across a lightweight web portal and an automated Meta WhatsApp Cloud API channel, ensuring friction-free access on basic smartphones.")
    add_bullet_p(doc, "Objective 5 (Syndromic Anomaly Surveillance)", 
                 "Incorporate localized geographic telemetry based on citizen symptom submissions and postal pincodes for rolling 7-day syndromic outbreak detection.")

    add_heading_1(doc, "1.5 Overview of the AarogyaSathi Solution Architecture")
    add_body_p(doc,
        "To achieve these objectives within strict operational constraints, AarogyaSathi implements a multi-tier hybrid architecture (Figure 1.1). "
        "Incoming messages from web or WhatsApp ingress points first traverse deterministic safety and fast-path heuristic filters. Queries exhibiting "
        "acute red-flag terminology bypass all machine learning inference and immediately return urgent medical dispatch directives. Routine health inquiries "
        "undergo rule-based fast-path pattern extraction; if a known disease profile or immunization milestone is identified, pre-compiled verified templates "
        "are dispatched instantly, avoiding generative-model latency for routine requests."
    )
    
    add_figure(doc, "architecture_publication.png", "1.1", 
               "High-Level Solution Topology and Channel Architecture of AarogyaSathi (Adapted from Khan et al., 2026).", 
               width_inches=5.5)

    add_body_p(doc,
        "When queries exhibit complex syntax, the system engages its dense vector semantic retrieval pipeline. The query is embedded via a 768-dimensional "
        "LaBSE transformer, scored against indexed records using a composite cosine-lexical similarity function, and injected as grounded context into a "
        "locally hosted Qwen3 (1.7B parameter) large language model running via Ollama. By constraining generation to retrieved clinical records, the "
        "architecture minimizes hallucination while preserving fluent vernacular expression. Simultaneously, symptom submissions are aggregated into SQLite "
        "for rolling seven-day syndromic cluster detection."
    )

    add_heading_1(doc, "1.6 Background and Literature Review")
    add_body_p(doc,
        "The conceptual foundation of AarogyaSathi builds upon Retrieval-Augmented Generation (RAG; Lewis et al., 2020) and cross-lingual representation "
        "via Language-agnostic BERT Sentence Embeddings (LaBSE; Feng et al., 2022). RAG pairs parametric neural generators with non-parametric dense vector "
        "document indices, dramatically reducing factual hallucination while allowing domain knowledge to be updated without model retraining. LaBSE maps "
        "semantically equivalent sentences across 109 languages into a shared embedding space, allowing colloquial Hindi queries to exhibit high cosine "
        "similarity with English clinical disease records without translation pipeline latency."
    )
    add_body_p(doc,
        "However, medical conversational literature urges extreme caution. Systematic reviews by Laranjo et al. (2018) and Milne-Ives et al. (2020) revealed "
        "that the majority of medical chatbots were evaluated on small developer-curated dialogue subsets without independent clinical validation, blinded review, "
        "or safety testing under adversarial negation. Semigran et al. (2015) audited symptom checkers and discovered that triage advice was appropriate in only "
        "57% of cases. These empirical findings directly informed our testing philosophy: rather than claiming unsubstantiated clinical perfection, AarogyaSathi’s "
        "evaluation explicitly highlights failure modes, training overlap, and negation vulnerabilities. Table 1.1 provides a comparative feature summary:"
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
        "The remainder of this dissertation is organized into seven subsequent chapters conforming strictly to the BPIT B.Tech Minor Project format. "
        "Chapter 2 formalizes the Problem Statement, defining core objectives, stakeholder personas, and system boundaries. "
        "Chapter 3 presents the Analysis phase, detailing the Software Requirements Specification (SRS), functional and non-functional requirements, feasibility studies, use cases, and Data Flow Diagrams. "
        "Chapter 4 outlines the Design and Architecture, covering the Work Breakdown Structure (WBS), module responsibilities, database schemas, LaBSE retrieval mathematics, and WhatsApp sequence models. "
        "Chapter 5 elaborates upon the Implementation, analyzing key algorithms, service topologies, and providing a visual screenshot walkthrough of web and WhatsApp channels. "
        "Chapter 6 details Testing and Quality Assurance, reviewing the automated test suite, component benchmarks, training overlap analysis, clinical spot-check defects, and Meta WhatsApp live delivery. "
        "Chapter 7 provides the Summary and Conclusion. Finally, Chapter 8 transparently articulates Project Limitations and a Prioritized Strategic Roadmap for Future Work, followed by an APA Bibliography and Technical Appendices."
    )

def add_chapter_2(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_table):
    add_chapter_title(doc, "2", "Problem Statement")

    add_heading_1(doc, "2.1 Formal Problem Definition")
    add_body_p(doc,
        "The fundamental problem addressed by this project can be formally stated as follows: Rural and semi-urban populations in India suffer from "
        "an acute lack of timely, linguistically accessible, and clinically verified healthcare information, resulting in widespread vulnerability to "
        "viral health misinformation, delayed medical care presentation, low childhood vaccination compliance, and uncontrolled seasonal epidemic surges."
    )
    add_body_p(doc,
        "This overarching problem decomposes into three distinct structural challenges:"
    )
    add_bullet_p(doc, "1. The Vernacular Accessibility Barrier", 
                 "While official public health guidelines issued by the Ministry of Health and Family Welfare (MoHFW) and the World Health Organization (WHO) are comprehensive, they are overwhelmingly published in dense, academic English or formal bureaucratic Hindi. Over 70% of rural Indian citizens communicate in regional languages and vernacular dialects, rendering official digital health advisories functionally inaccessible.")
    add_bullet_p(doc, "2. Uninhibited Proliferation of Digital Health Misinformation", 
                 "Social messaging platforms facilitate the frictionless, viral transmission of pseudoscientific health claims. Forwarded messages advocating unproven herbal cures for vector-borne diseases or stoking vaccine hesitancy circulate without any automated fact-checking mechanism, actively undermining national immunization programs and public health interventions.")
    add_bullet_p(doc, "3. Critical Clinical Latency and Triage Failures", 
                 "Citizens experiencing early-stage symptoms often struggle to determine whether their condition warrants routine home care, an outpatient primary health clinic visit, or immediate emergency ambulance escalation. Generic internet search engines return overwhelming lists of potential diagnoses ranging from benign fatigue to terminal malignancies, causing unnecessary panic or dangerous complacency.")

    add_heading_1(doc, "2.2 Core Project Objectives")
    add_body_p(doc,
        "To systematically address the formal problem statement, AarogyaSathi establishes five precise, measurable technical objectives:"
    )
    add_bullet_p(doc, "Objective 1: Multi-Tier Hybrid Conversational Pipeline",
                 "Architect and deploy a high-performance conversational engine capable of resolving citizen inquiries via deterministic safety rules, rule-based fast-path heuristics, and dense vector semantic retrieval, with model-generated answers returned within a few seconds on the cloud virtual machine.")
    add_bullet_p(doc, "Objective 2: Authoritative Multilingual Knowledge Grounding",
                 "Curate and maintain an authoritative, structured digital knowledge base covering 14 major endemic diseases, 13 national childhood vaccination milestones, and 35 frequent health inquiries in English and Hindi, with semantic cross-lingual detection across 12 Indian languages.")
    add_bullet_p(doc, "Objective 3: Heuristic Misinformation Fact-Checking",
                 "Develop a dedicated claim-verification engine capable of ingesting forwarded text claims, performing cross-lingual similarity matching against a curated catalog of 64 Indian health myths, and returning transparent, categorical verdicts (VERIFIED, MYTH, PARTLY TRUE, UNVERIFIABLE) with clinical rationales.")
    add_bullet_p(doc, "Objective 4: Ubiquitous Dual-Channel Mobile Ingress",
                 "Implement dual interfaces: a responsive, zero-install mobile web application and a Meta WhatsApp Cloud API integration (demonstrated with an approved test recipient), enabling citizens to interact with the chatbot on basic smartphones without incurring data or subscription costs.")
    add_bullet_p(doc, "Objective 5: Geospatial Syndromic Outbreak Telemetry",
                 "Engineer an experimental geographic surveillance module that aggregates voluntary, anonymous citizen symptom submissions by postal pincode and evaluates rolling 7-day statistical anomaly baselines to detect potential syndromic disease clusters.")

    add_heading_1(doc, "2.3 Key Stakeholders and User Personas")
    add_body_p(doc,
        "To ensure human-centered engineering, the system was designed around three illustrative personas (composite examples, not real individuals) representing key stakeholders in India’s public healthcare delivery chain:"
    )
    add_bullet_p(doc, "Persona 1: Ramesh (Rural Smallholder Farmer, Mayurbhanj, Odisha)",
                 "Ramesh is 42 years old, speaks Odia, and possesses basic functional literacy in Hindi. He accesses the internet exclusively through a low-cost Android smartphone with prepaid 4G data. His family lives 18 kilometers from the nearest Primary Health Centre. When his son develops acute fever, chills, and muscle soreness, Ramesh needs immediate, trusted advice in simple Hindi or Odia to determine whether it could be malaria and what immediate steps must be taken, without being misled by WhatsApp remedies.")
    add_bullet_p(doc, "Persona 2: Sunita Devi (ASHA Community Health Worker, Rural Cuttack)",
                 "Sunita is an Accredited Social Health Activist responsible for monitoring maternal and child health across two village hamlets (population ~1,800). She requires an authoritative, instant reference tool on her smartphone to verify exact national immunization milestones for infants at 6, 10, and 14 weeks, and to debunk prevalent village rumors regarding measles-rubella vaccine safety during community immunization drives.")
    add_bullet_p(doc, "Persona 3: Dr. Patnaik (District Surveillance Officer, IDSP Odisha)",
                 "Dr. Patnaik oversees communicable disease monitoring across the district. He requires automated digital tools capable of identifying unusual spikes in reported syndromic symptoms (such as acute febrile illness or loose stools) mapped by postal pincode, providing early indicator telemetry days before formal lab-confirmed cases are logged in the Integrated Disease Surveillance Programme (IDSP) portal.")

    add_heading_1(doc, "2.4 System Boundaries, Operating Assumptions, and Clinical Non-Claims")
    add_body_p(doc,
        "A foundational requirement of this dissertation is establishing transparent boundaries regarding what the system can and cannot perform. "
        "AarogyaSathi operates strictly under the following system boundaries and assumptions:"
    )
    add_bullet_p(doc, "1. Non-Diagnostic Posture", 
                 "AarogyaSathi does not provide differential diagnoses, does not issue clinical prescriptions, and does not calculate pharmaceutical dosages. All generated responses include mandatory medical disclaimers emphasizing that information is for awareness only and cannot substitute for an examination by a registered medical practitioner.")
    add_bullet_p(doc, "2. Ephemeral Session Telemetry", 
                 "To limit data retention, the persistent SQLite database stores only pincode, symptom, intent, language and verdict fields, and no message text, names or phone numbers. Short conversational history is held in volatile memory with a 30-minute Time-To-Live (TTL) and is discarded when the session expires.")
    add_bullet_p(doc, "3. Outbreak Advisory Illustrative Nature", 
                 "While the system features an operational syndromic cluster detection algorithm, its bundled outbreak records are illustrative seasonal advisories designed for demonstration purposes, and do not represent an authenticated, synchronized live feed from state or central government epidemiologists.")
    add_bullet_p(doc, "4. Restricted Demonstration Environment", 
                 "The Meta WhatsApp Cloud API channel operates under an approved developer test-number deployment (+1 555 626 0618) restricted to authorized recipient phone numbers, rather than an unconstrained commercial enterprise production number.")

    add_heading_1(doc, "2.5 Acceptance Criteria and Success Metrics")
    add_body_p(doc,
        "The project’s engineering completion was governed by six rigorous acceptance criteria:"
    )
    add_bullet_p(doc, "AC-1 (Test Suite Integrity)", "100% pass rate across the comprehensive automated test suite (spanning core routing, RAG retrieval, ML classifiers, and channel adapters) run on the deployment host.")
    add_bullet_p(doc, "AC-2 (Fast-Path Latency)", "Deterministic rule-based replies (greetings, emergency red flags) are returned without invoking the language model, and model-generated answers are returned within a few seconds on the cloud virtual machine.")
    add_bullet_p(doc, "AC-3 (Retrieval Precision)", "Top-1 retrieval accuracy exceeding 90% across curated clinical test queries evaluated against the 49-record indexed health corpus.")
    add_bullet_p(doc, "AC-4 (Fact-Checking Coverage)", "Accurate categorical truth assignment across a curated test suite of common Indian public health myths without unhandled runtime exceptions.")
    add_bullet_p(doc, "AC-5 (Channel Operational Verification)", "Verified bidirectional message transmission and webhook signature validation across both the web application and the Meta WhatsApp Cloud API test number.")
    add_bullet_p(doc, "AC-6 (Clinical Safety Red-Flag Assurance)", "Deterministic interception and urgent hotline escalation for critical emergency phrases, ensuring safety paths bypass all probabilistic language models.")

def add_chapter_3(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_figure, add_table):
    add_chapter_title(doc, "3", "Analysis")

    add_heading_1(doc, "3.1 Software Requirement Specifications (SRS Overview)")
    add_body_p(doc,
        "The Software Requirement Specification (SRS) for AarogyaSathi defines the complete functional and non-functional capabilities of the system, "
        "establishing the technical baseline against which the software was engineered, deployed, and evaluated. The system is designed as an asynchronous, "
        "service-oriented web and messaging platform optimized for high concurrency, low latency, and free-tier hosting on cloud infrastructure."
    )

    add_heading_1(doc, "3.2 Functional Requirements (FR)")
    add_body_p(doc,
        "The functional scope of AarogyaSathi is organized into eight primary requirement modules (FR-1 through FR-8), detailed in Table 3.2:"
    )

    fr_headers = ["Req ID", "Functional Module", "Detailed Requirement Specification"]
    fr_rows = [
        ["FR-1", "Multilingual Ingress & Language Detection", "The system shall ingest free-text messages via Web and WhatsApp webhooks, detect user language across 12 Indian languages, and maintain session context in volatile memory."],
        ["FR-2", "Deterministic Emergency Triage", "The system shall immediately intercept predefined red-flag symptoms (chest pain, acute dyspnea, severe hemorrhaging) and return emergency hotline dispatch directives (108/112), bypassing ML pipelines."],
        ["FR-3", "Fast-Path Rule Execution", "The system shall match routine queries (greetings, standard disease inquiries, vaccine ages) using compiled regex patterns to return verified responses without invoking the generative model."],
        ["FR-4", "Dense Vector Semantic Retrieval", "The system shall embed unresolved health inquiries using LaBSE (768-dim vectors) and retrieve the top-k matching clinical profiles from the indexed corpus using cosine-lexical reranking."],
        ["FR-5", "Retrieval-Augmented Generation", "The system shall inject retrieved clinical context into an open-source language model (Qwen3:1.7b) running via Ollama to synthesize concise, grounded advice in the user's language."],
        ["FR-6", "Health Misinformation Fact-Checking", "The system shall process forwarded claims prefixed with 'fact check:' or matching known rumors, compare them against 64 curated Indian myths, and return categorized verdicts with source citations."],
        ["FR-7", "Syndromic Anomaly Detection", "The system shall log voluntary citizen symptom-pincode pairs into SQLite and trigger automated severity alerts when 24-hour counts exceed 3x the 7-day rolling historical baseline."],
        ["FR-8", "Meta WhatsApp Cloud API Integration", "The system shall receive webhook payloads from Meta Graph API v25.0, cryptographically verify HMAC-SHA256 signatures, deduplicate message IDs, and dispatch split replies via HTTPS."]
    ]
    add_table(doc, fr_headers, fr_rows, "3.1", "Functional Requirements Specification (FR-1 through FR-8)", [0.8, 1.8, 3.16])

    add_heading_1(doc, "3.3 Non-Functional Requirements (NFR)")
    add_body_p(doc,
        "In addition to functional capabilities, the architecture enforces six critical non-functional engineering standards (Table 3.2):"
    )

    nfr_headers = ["Req ID", "Quality Attribute", "Target Specification & Evaluation Criterion"]
    nfr_rows = [
        ["NFR-1", "Latency & Performance", "Rule-based replies are returned without invoking the language model; model-assisted answers are returned within a few seconds; webhook requests are acknowledged before background processing completes."],
        ["NFR-2", "Privacy & Ethical Security", "No message text, names or phone numbers stored in the database; ephemeral in-memory sessions with 30-min TTL; HMAC-SHA256 signature validation on webhooks."],
        ["NFR-3", "Reliability & Availability", "Continuous operation via systemd services on Oracle VM; automatic service recovery on unexpected process termination; graceful degradation if Ollama fails."],
        ["NFR-4", "Hosting Resource Efficiency", "Operational within 2 OCPUs and 12 GiB RAM on an Oracle Cloud Arm virtual machine without specialized GPU hardware acceleration."],
        ["NFR-5", "Linguistic Adaptability", "Cross-lingual semantic understanding across English, Hindi, and 10 regional Indian languages via LaBSE multilingual embeddings."],
        ["NFR-6", "Clinical Grounding & Safety", "Mandatory inclusion of clinical disclaimers on every non-emergency output; citation of verified public health authorities (WHO, MoHFW, NVBDCP)."]
    ]
    add_table(doc, nfr_headers, nfr_rows, "3.2", "Non-Functional Requirements Specification (NFR-1 through NFR-6)", [0.8, 1.6, 3.36])

    add_heading_1(doc, "3.4 Feasibility Study (Technical, Operational, Economic)")
    add_body_p(doc,
        "Before architectural commitment, a comprehensive three-dimensional feasibility study was conducted:"
    )
    add_bullet_p(doc, "1. Technical Feasibility", 
                 "Deployment of transformer embeddings and quantized language models on ARM64 cloud architecture was evaluated. The LaBSE transformer and Qwen3:1.7b under Ollama's C++ runtime operate within 3.5 GiB active memory, well below the 12 GiB threshold of our Oracle Cloud VM. Asynchronous FastAPI request handling ensures high concurrency without worker starvation.")
    add_bullet_p(doc, "2. Operational Feasibility", 
                 "In rural India, citizens are heavily accustomed to WhatsApp and lightweight mobile browsers. By deploying AarogyaSathi directly over WhatsApp and responsive HTML5 web interfaces, little installation or onboarding friction is introduced, which fits existing rural communication habits.")
    add_bullet_p(doc, "3. Economic Feasibility", 
                 "The solution relies exclusively on open-source software (Python 3.12, FastAPI, PyTorch, Ollama, SQLite) and free-tier infrastructure (an Oracle Cloud Arm virtual machine, a Cloudflare HTTPS tunnel, and the Meta WhatsApp Developer test number). No recurring software or API license fees were incurred during the prototype phase; long-term costs of a public deployment were not assessed.")

    add_heading_1(doc, "3.5 Tools, Technologies, and Hardware Platform")
    add_body_p(doc,
        "The software stack and production hardware specifications deployed on Oracle Cloud Infrastructure are summarized in Table 3.3:"
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
        "The functional capabilities of AarogyaSathi are formally modeled through UML Use Case diagrams. The system interacts with three primary actors: "
        "the Citizen / Mobile User, the Frontline Health Worker (ASHA), and the Public Health Administrator / Surveillance Officer (Figure 3.1):"
    )

    add_figure(doc, "fig_usecase.png", "3.1", 
               "Use Case Model for Citizen, Health Worker, and Administrative Actors.", 
               width_inches=4.9)

    add_body_p(doc,
        "The primary use cases encompass: UC-1 (Inquire Disease and Symptoms), where citizens input natural language symptom queries and receive grounded clinical descriptions; "
        "UC-2 (Verify Forwarded Health Claim), where users submit viral messages to receive categorical truth verdicts; UC-3 (Query Vaccination Milestones), "
        "enabling parents and ASHA workers to check required vaccines by infant age; UC-4 (Emergency Red-Flag Triage), which immediately flags acute medical distress; "
        "UC-5 (Report Symptoms with Pincode), allowing voluntary contribution to community health monitoring; UC-6 (Interact via WhatsApp), extending all capabilities to mobile messaging; "
        "and UC-7 (Monitor Syndromic Cluster Alerts), enabling health officers to inspect localized disease anomaly alerts on the admin dashboard."
    )

    add_heading_1(doc, "3.7 Data Flow Modeling (Level 0 and Level 1 DFD)")
    add_body_p(doc,
        "The movement of information across system boundaries and internal transformations is captured through structured Data Flow Diagrams (DFDs). "
        "Figure 3.2 depicts the Context-Level DFD (Level 0), showing external entities interfacing with the centralized AarogyaSathi process:"
    )

    add_figure(doc, "fig_dfd_lvl0.png", "3.2", 
               "Context-Level Data Flow Diagram (DFD Level 0) for Public Health Inquiries.", 
               width_inches=5.0)

    add_body_p(doc,
        "Figure 3.3 expands the internal architecture into a Detailed Level 1 DFD, detailing the six core transformation processes: "
        "Process 1.0 (Emergency Filter & Red-Flag Validation), Process 2.0 (Fast-Path Heuristic Router), Process 3.0 (Health Misinformation Verifier), "
        "Process 4.0 (LaBSE Dense Vector Semantic Retriever), Process 5.0 (RAG Context Synthesis & LLM Generation), and Process 6.0 (Syndromic Anomaly Surveillance). "
        "The diagram explicitly shows data flows connecting four distinct data stores: D1 (Volatile User Session Cache), D2 (Curated 64-Myth Store), "
        "D3 (Clinical Knowledge Base: 14 Diseases, 35 FAQs, 13 Vaccines), and D4 (Relational Telemetry DB in SQLite)."
    )

    add_figure(doc, "fig_dfd_lvl1.png", "3.3", 
               "Detailed Functional Data Flow Diagram (DFD Level 1) of Core Engine and Data Stores.", 
               width_inches=4.7)

print("Chapters 1-3 generator module defined successfully.")
