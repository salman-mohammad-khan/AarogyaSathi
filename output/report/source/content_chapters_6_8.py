"""
Chapters 6 to 8, Bibliography, and Appendices Generator for AarogyaSathi Minor Project Report
- Chapter 6: Testing and Quality Assurance (6 pages)
- Chapter 7: Summary and Conclusion (2 pages)
- Chapter 8: Limitations and Future Work (2 pages)
- Bibliography: APA 7th Edition (2 pages)
- Appendix A: Hardware & Environment Specifications (1 page)
- Appendix B: Intent Taxonomy & API Directory (1 page)
"""

from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_chapter_6(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_table, add_code_block):
    add_chapter_title(doc, "6", "Testing and Quality Assurance")

    add_heading_1(doc, "6.1 Comprehensive Verification and Testing Strategy")
    add_body_p(doc,
        "Testing a public health conversational assistant requires an evaluation strategy that looks well beyond standard software unit checks. "
        "In healthcare informatics, an application that returns an HTTP 200 OK status code and generates grammatically fluent text can still deliver "
        "catastrophic clinical advice if medical negations are inverted, age milestones are miscalculated, or ungrounded language models hallucinate "
        "unsupported therapies (Semigran et al., 2015; Milne-Ives et al., 2020). Consequently, our testing methodology combines four distinct "
        "levels of empirical inquiry:"
    )
    add_bullet_p(doc, "1. Automated Unit and Regression Testing", 
                 "Systematic pytest verification of core modules, input validators, cryptographic signatures, and vector retrieval functions.")
    add_bullet_p(doc, "2. Component Benchmark Evaluation", 
                 "Isolated quantitative scoring of intent classification accuracy, dense vector retrieval precision, and fact-check agreement against ground-truth datasets.")
    add_bullet_p(doc, "3. Live Synthetic Query Spot Checks", 
                 "Direct submission of clinical vignettes (affirmative/negated emergencies, vaccine queries, disease symptoms, and vernacular prompts) to the live Oracle VM.")
    add_bullet_p(doc, "4. End-to-End Channel Delivery Verification", 
                 "Webhook handshake and signature verification, and message exchange between the deployed service and one approved test recipient through the Meta WhatsApp Cloud API.")

    add_heading_1(doc, "6.2 Unit and Regression Test Suite Execution")
    add_body_p(doc,
        "The automated test suite was run on the Oracle Cloud Infrastructure virtual machine (Ubuntu 24.04 ARM64, Python 3.12.3) on 26 October 2026: "
        "all 37 unit and regression tests passed in 24.24 seconds. Five WhatsApp webhook security tests, added during the channel integration, passed "
        "separately on 31 October 2026 (5.12 seconds), so the repository now holds 42 tests. Table 6.1 details the test distribution and functional verification coverage:"
    )

    test_headers = ["Test Suite File", "Test Count", "Functional Scope Evaluated", "Execution Result"]
    test_rows = [
        ["tests/test_core.py", "12 Tests", "Fast-path heuristics, LaBSE vector embedding normalization, cosine ranking, language identification, entity extraction", "12 / 12 Passed (100%)"],
        ["tests/test_flow.py", "8 Tests", "Multi-turn symptom dialogue state transitions, session TTL expiration, user language switching, disclaimer injection", "8 / 8 Passed (100%)"],
        ["tests/test_ml.py", "9 Tests", "TF-IDF n-gram vectorization, logistic regression intent extraction, threshold filtering, claim verification matching", "9 / 9 Passed (100%)"],
        ["tests/test_surveillance.py", "4 Tests", "SQLite symptom telemetry insertion, 7-day rolling baseline calculation, cluster alert condition evaluation", "4 / 4 Passed (100%)"],
        ["tests/test_whatsapp.py", "4 Tests", "Meta webhook challenge handshake, WhatsApp simulation endpoint, Twilio adapter", "4 / 4 Passed"],
        ["tests/test_meta_webhook_security.py", "5 Tests", "HMAC-SHA256 signature validation, tampered or unsigned rejection, duplicate suppression, receiver filtering (added 31 October 2026)", "5 / 5 Passed"]
    ]
    add_table(doc, test_headers, test_rows, "6.1", "Automated Test Suite Coverage (37 Tests Run on 26 October 2026; 5 Channel Security Tests Added on 31 October 2026)", [1.3, 0.8, 2.7, 0.96])

    add_heading_1(doc, "6.3 Component Benchmark Evaluation (Intent, Retrieval, Fact-Check)")
    add_body_p(doc,
        "The system's isolated machine learning components were evaluated using the standardized benchmark runner (scripts/eval.py) against curated "
        "ground-truth datasets stored in data/training/eval.json. Table 6.2 presents the empirical benchmark findings alongside critical methodological limits:"
    )

    bench_headers = ["Component Evaluated", "Benchmark Metric", "Observed Result", "Critical Methodological Limitation"]
    bench_rows = [
        ["Fallback Intent Classifier", "Exact Match Accuracy", "30 / 30 (100.0%)", "14/30 inputs exactly duplicate training text; evaluation threshold 0.45 vs 0.55 production"],
        ["LaBSE Dense Retrieval", "Top-1 Retrieval Accuracy", "15 / 15 (100.0%)", "Evaluated against known-KB queries; evaluation threshold 0.35 vs 0.52 production"],
        ["Claim Verification Engine", "Verdict Classification", "34 / 34 (100.0%)\n(Mean 387 ms)", "Severe class imbalance: 24 MYTH, 4 TRUE, 5 PARTLY TRUE, 1 UNVERIFIABLE; curated examples"]
    ]
    add_table(doc, bench_headers, bench_rows, "6.2", "Component Benchmark Evaluation Results on Deployed Host", [1.3, 1.2, 1.1, 2.16])

    add_heading_2(doc, "6.3.1 Critical Analysis of Training Overlap in Intent Evaluation")
    add_body_p(doc,
        "While the intent classifier achieved a perfect score of 30/30 (100%) on the benchmark set, inspection of the underlying data revealed "
        "that 14 of the 30 evaluation questions (46.7%) were exact textual duplicates of sentences in the training corpus (data/training/intents.json). "
        "To verify generalization capabilities, an isolated evaluation was conducted on 29 October 2026 using only the 16 non-duplicate questions. "
        "All 16 unseen questions were classified correctly at threshold 0.45. Nonetheless, because these questions were assembled by the development "
        "team rather than sampled from genuine patient interactions, this score cannot be interpreted as an unbiased estimate of real-world population accuracy."
    )

    add_heading_2(doc, "6.3.2 Retrieval Precision and Myth Class Imbalance")
    add_body_p(doc,
        "The LaBSE retrieval evaluation demonstrated 100% top-1 accuracy across 15 curated queries (5 disease targets and 10 FAQ targets) under relaxed "
        "benchmark settings (top-3, threshold 0.35) versus production deployment (top-5, threshold 0.52). Similarly, while the health-claim verifier "
        "correctly classified all 34 benchmark rumors in an average of 387 ms, the test set exhibits extreme class imbalance: 24 of 34 claims (70.6%) belong "
        "to the MYTH category, with only 4 TRUE, 5 PARTLY TRUE, and 1 UNVERIFIABLE claim. Consequently, the benchmark confirms rumor debunking efficacy "
        "but provides minimal statistical certainty regarding rarer verdict classes."
    )

    add_heading_1(doc, "6.4 Synthetic End-to-End Query Spot Checks and Clinical Defect Analysis")
    add_body_p(doc,
        "To evaluate whole-pipeline behavior beyond developer benchmarks, five synthetic clinical queries were submitted directly to the live "
        "Oracle Cloud API (/api/chat). Table 6.3 summarizes the results, exposing critical discrepancies between component scores and integrated safety:"
    )

    spot_headers = ["Synthetic Input Query", "Intended Clinical Action", "Observed Route & Response", "Latency"]
    spot_rows = [
        ["I have severe chest pain and cannot breathe", "Immediate emergency triage escalation", "Routed to emergency; returned 108 hotline advice & snakebite guide", "0.29 s"],
        ["I have no chest pain, only a mild headache", "Benign symptom triage (headache advice)", "FALSE EMERGENCY: Triggered acute emergency escalation", "0.08 s"],
        ["fact check: vaccines cause autism", "Neutralize misinformation with myth verdict", "Dispatched MYTH verdict with clinical explanation & sources", "0.15 s"],
        ["What are dengue symptoms?", "Provide disease profile & warning signs", "Dispatched verified dengue profile, prevention tips & disclaimer", "2.32 s"],
        ["ଡେଙ୍ଗୁ ପ୍ରତିଷେଧକ କ’ଣ? (Odia dengue query)", "Provide preventive advice in Odia", "FALLBACK GAP: Returned generic apology stating no reliable info", "11.41 s"]
    ]
    add_table(doc, spot_headers, spot_rows, "6.3", "Selected Live Synthetic Query Spot Checks and Clinical Response Observations", [1.5, 1.4, 2.1, 0.76])

    add_heading_2(doc, "6.4.1 The Negation Handling Vulnerability in Emergency Safety")
    add_body_p(doc,
        "The most critical defect uncovered during live testing was the failure of lexical negation handling. When the user submitted 'I have no chest pain, "
        "only a mild headache', the red-flag matcher (entities.py, invoked through safety.py) matched 'chest pain' without evaluating negation. Consequently, the system "
        "erroneously classified a mild headache as an emergency, instructing the user to dial 108, while inadvertently appending snakebite first-aid "
        "instructions. While false positives are clinically preferable to missed emergencies, this failure demonstrates that keyword matching cannot "
        "differentiate between reported and denied symptoms."
    )

    add_heading_2(doc, "6.4.2 Regional Vernacular Fallback Gaps")
    add_body_p(doc,
        "When presented with an Odia query ('ଡେଙ୍ଗୁ ପ୍ରତିଷେଧକ କ’ଣ?'), the system identified the language code ('or') but failed to retrieve context above "
        "the 0.52 threshold. It degraded into a safe fallback ('I am sorry, I do not have reliable health information about that') after 11.41 s—the longest "
        "observed latency. This confirms that while language detection supports 12 languages, authoritative knowledge coverage remains concentrated in English and Hindi."
    )

    add_heading_1(doc, "6.5 Code Inspection Findings: Vaccination Age Conversion Defect")
    add_body_p(doc,
        "Rigorous static code analysis of app/core/router.py revealed a significant mathematical defect in the infant age-to-milestone conversion function "
        "(_age_to_milestones). The function contains a logic branch error when parsing infant ages expressed in months versus years:"
    )
    add_code_block(doc,
        "# app/core/router.py, _age_to_milestones (excerpt)\n"
        "if unit in (\"month\", \"months\", \"mahine\", \"mahina\"):\n"
        "    if n < 12:\n"
        "        return \"9_12_months\"      # a 2-month-old is mapped here\n"
        "    if 12 <= n <= 24:\n"
        "        return \"16_24_months\"\n"
        "if unit in (\"year\", \"years\", \"saal\", \"sal\"):\n"
        "    if n < 7:\n"
        "        return \"5_6_years\"        # a 1-year-old is mapped here"
    )
    add_body_p(doc,
        "Consequently, inquiries for 2-month infants are mapped to the 9–12 month milestone (MR/JE vaccines rather than Pentavalent/Rotavirus/OPV). "
        "While local LLM refusals mitigated incorrect outputs during tests, this underscores that neural generation can mask underlying deterministic "
        "logic defects, reinforcing the necessity of exhaustive milestone unit tests."
    )

    add_heading_1(doc, "6.6 Meta WhatsApp Cloud API Channel Live Verification")
    add_body_p(doc,
        "On 31 October 2026, comprehensive live channel verification was conducted connecting the Oracle Cloud deployment to Meta’s WhatsApp "
        "Cloud API. Table 6.4 summarizes the verification milestones:"
    )

    wa_headers = ["Verification Stage", "Observed Host Telemetry", "Status / Performance Result"]
    wa_rows = [
        ["HTTPS Webhook Handshake", "Meta GET challenge matched WHATSAPP_VERIFY_TOKEN exactly", "HTTP 200 OK (Confirmed)"],
        ["Cryptographic Security", "Valid HMAC-SHA256 signature accepted (0.024 s); unsigned request rejected with HTTP 403", "Security Verified"],
        ["Isolated Channel Tests", "5 channel test cases (valid signature, tampered body, dedup, status callbacks) executed on VM", "5 / 5 Passed in 5.12 s"],
        ["Live Handset Exchange", "Registered test recipient sent 'hi', 'What are dengue symptoms?', 'fact check: garlic cures dengue'", "3 / 3 Replies Received (user-confirmed)"],
        ["Server Log Telemetry", "Server window recorded: 3 incoming text messages, 3 outbound accepted by Meta, 0 send errors", "0 Send Errors"]
    ]
    add_table(doc, wa_headers, wa_rows, "6.4", "Meta WhatsApp Cloud API Channel Live Verification Summary", [1.4, 2.6, 1.76], pad_v=45, font_sz=8.5)

    add_heading_1(doc, "6.7 SIH25049 Challenge Compliance Matrix")
    add_body_p(doc,
        "Table 6.5 provides a transparent reconciliation comparing the original Smart India Hackathon brief requirements against the demonstrated "
        "capabilities of the delivered AarogyaSathi prototype:"
    )

    sih_headers = ["Brief Requirement", "Demonstrated Implementation Evidence", "Compliance Status"]
    sih_rows = [
        ["Disease & Prevention Info", "14 curated profiles, 35 FAQs; English & Hindi RAG responses verified on live VM", "Fully Operational Prototype"],
        ["National Immunization Schedules", "13 UIP milestones encoded; month-unit conversion defect identified for remediation", "Prototype (Correction Required)"],
        ["Multilingual Communication", "12 detected language codes; fluent Hindi verified; Odia preventive query fell back safely", "Partial (English and Hindi strongest)"],
        ["WhatsApp & SMS Access", "Meta WhatsApp Cloud API v25.0 verified with live recipient delivery; SMS unverified", "WhatsApp Verified / SMS Unmet"],
        ["Outbreak Advisory Telemetry", "7-day rolling statistical anomaly detector; illustrative advisories rendered on /admin", "Operational Demonstration"],
        ["Government Database Linkage", "No direct API synchronization with official state IDSP databases demonstrated", "Out of Scope / Future Work"]
    ]
    add_table(doc, sih_headers, sih_rows, "6.5", "SIH25049 Challenge Compliance Matrix: Brief Requirements vs. Prototype Status", [1.4, 2.7, 1.66], pad_v=45, font_sz=8.5)

def add_chapter_7(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2):
    add_chapter_title(doc, "7", "Summary and Conclusion")

    add_heading_1(doc, "7.1 Summary of Delivered Work and Technical Achievements")
    add_body_p(doc,
        "This minor project dissertation has detailed the complete architectural design, engineering implementation, and multi-level empirical evaluation "
        "of AarogyaSathi (आरोग्यसाथी)—an AI-driven public health conversational assistant developed in response to Smart India Hackathon challenge SIH25049 "
        "under the Government of Odisha’s healthcare technology theme. The project successfully bridged the gap between complex natural language processing "
        "and accessible, grassroots public health delivery."
    )
    add_body_p(doc,
        "The key technical deliverables achieved during this project encompass:"
    )
    add_bullet_p(doc, "1. Hybrid Multi-Tier Conversational Architecture",
                 "Successfully engineered an asynchronous service pipeline in FastAPI that integrates deterministic safety interception, rule-based fast-path routing, and dense vector semantic retrieval; a disease-information answer was returned in 2.32 seconds in a single observation on 26 October 2026.")
    add_bullet_p(doc, "2. Authoritative Clinical Knowledge Base",
                 "Curated and indexed 14 major endemic disease profiles, 35 public health FAQs, 13 national childhood immunization milestones, and 64 prevalent Indian health myths grounded strictly in WHO, MoHFW, and ICMR published guidance.")
    add_bullet_p(doc, "3. Cross-Lingual Semantic Retrieval Pipeline",
                 "Integrated the 768-dimensional LaBSE sentence embedding transformer with a hybrid cosine-lexical reranker, enabling semantic document retrieval across regional languages without machine translation dependencies.")
    add_bullet_p(doc, "4. Dedicated Health Misinformation Verifier",
                 "Developed an automated fact-checking engine capable of analyzing forwarded viral claims, categorizing them into four standardized truth verdicts (VERIFIED, MYTH, PARTLY TRUE, UNVERIFIABLE), and returning clear explanations (mean 387 ms per claim on the 34-claim development set).")
    add_bullet_p(doc, "5. Low-Cost Cloud Deployment & Multi-Channel Ingress",
                 "Deployed the full operational software stack on an Oracle Cloud Infrastructure virtual machine (2 OCPUs, 12 GiB RAM, Ubuntu 24.04 ARM64), providing access through a responsive web application and, for an approved test recipient, a Meta WhatsApp Cloud API channel (outbound API v25.0) reached through a Cloudflare HTTPS tunnel with signature-verified webhooks.")
    add_bullet_p(doc, "6. Rigorous Software Quality Verification",
                 "All 37 automated tests of the 26 October run passed, and the five channel security tests added later also passed. Component benchmarks gave 30/30 intent, 15/15 retrieval and 34/34 claim verdicts on the supplied development sets, and three WhatsApp test messages were answered for an approved recipient with no sending errors in the server logs.")

    add_heading_1(doc, "7.2 Significance for Public Health Information Dissemination")
    add_body_p(doc,
        "The broader significance of AarogyaSathi lies in demonstrating that high-quality, privacy-preserving digital public health infrastructure "
        "can be engineered and operated on free-tier infrastructure with no recurring software licence cost in the prototype phase. By utilizing open-source models (Qwen3:1.7b, LaBSE) running under "
        "local C++ runtime environments on free-tier cloud resources, developing nations can deploy authoritative conversational assistants without "
        "incurring unsustainable software-as-a-service licensing fees or vendor lock-in. Furthermore, deploying conversational AI directly over "
        "ubiquitous mobile platforms like WhatsApp fundamentally democratizes health literacy, empowering rural citizens and frontline ASHA workers "
        "with verified clinical knowledge at their fingertips."
    )

    add_heading_1(doc, "7.3 Concluding Remarks")
    add_body_p(doc,
        "AarogyaSathi represents a balanced, evidence-based prototype that unites modern AI capabilities with transparent engineering restraint. "
        "By enforcing hard clinical boundaries, acknowledging evaluation limitations, and exposing real-world failure modes alongside technical successes, "
        "this minor project establishes a solid, reproducible foundation for the future deployment of ethical, vernacular public health conversational "
        "agents across India."
    )

def add_chapter_8(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_table):
    add_chapter_title(doc, "8", "Limitations and Future Work")

    add_heading_1(doc, "8.1 Identified Architectural and Clinical Safety Limitations")
    add_body_p(doc,
        "A primary commitment of this dissertation is the transparent documentation of system limitations uncovered during static code analysis, "
        "automated test execution, and live synthetic query spot checks:"
    )
    add_bullet_p(doc, "1. Lexical Negation Blindness in Emergency Triage",
                 "Surface phrase matching in the red-flag lexicon (entities.py) does not interpret negation. 'No chest pain, only a mild headache' triggered an erroneous cardiac emergency escalation. Fine-tuned negation classifiers are required to differentiate reported from denied symptoms.")
    add_bullet_p(doc, "2. Irrelevant Emergency Instruction Concatenation",
                 "The emergency response template bundles venomous snakebite first-aid guidelines alongside acute cardiac and respiratory protocols. In life-threatening crises, dispatching unrelated bite advice increases cognitive load and degrades triage clarity.")
    add_bullet_p(doc, "3. Infant Vaccination Age-Unit Conversion Defect",
                 "A hardcoded logic defect in router.py::_age_to_milestones maps all infant ages expressed in months to the 9–12 month milestone. Strict numerical normalization across days, weeks, months, and years must be implemented against the complete UIP schedule.")
    add_bullet_p(doc, "4. Ungrounded Generative Fallback Risks",
                 "When local document retrieval falls below the confidence cutoff, generator.general_answer() invokes parametric LLM completion. Although disclaimers are appended, parametric generation carries hallucination risks; strict refusal should govern out-of-domain clinical questions.")

    add_heading_1(doc, "8.2 Geographic and Epidemiological Surveillance Modeling Constraints")
    add_body_p(doc,
        "While the syndromic anomaly detector successfully logs symptom-pincode events into SQLite and evaluates rolling statistical thresholds, "
        "its epidemiological utility is constrained by voluntary reporting bias and the absence of census population denominators. A cluster spike "
        "may reflect localized bot adoption or media coverage rather than genuine outbreak transmission. Furthermore, current outbreak records "
        "represent illustrative advisories rather than live authenticated linkages to the Integrated Disease Surveillance Programme (IDSP)."
    )

    add_heading_1(doc, "8.3 Linguistic and Regional Knowledge Base Gaps")
    add_body_p(doc,
        "Although language detection supports 12 Indian languages, verified clinical profiles are overwhelmingly authored in English and Hindi. "
        "As shown by the Odia dengue query spot check (which required 11.41 s before returning an uninformative fallback), cross-lingual comprehension "
        "does not ensure localized generation. Translating and curating knowledge bases into native Odia, Bengali, Telugu, and Tamil is essential for state-wide deployment."
    )

    add_heading_1(doc, "8.4 Deployment, Privacy, and Channel Constraints")
    add_body_p(doc,
        "The Meta WhatsApp channel currently operates over an ephemeral Cloudflare Tunnel, requiring manual webhook updates upon restart. "
        "Production deployment mandates a permanent domain with static SSL reverse proxies, a durable Redis/Celery queue for reliable outbound delivery, "
        "and transition from the developer test sender (+1 555 626 0618) to an approved production WhatsApp Business Account."
    )

    add_heading_1(doc, "8.5 Prioritized Strategic Roadmap for Future Enhancements")
    add_body_p(doc,
        "Table 8.1 outlines a prioritized engineering and clinical validation roadmap transitioning AarogyaSathi from an academic prototype to a certified public health intervention:"
    )

    road_headers = ["Priority Phase", "Target Milestone", "Technical Scope & Methodology", "Validation Standard"]
    road_rows = [
        ["Phase 1 (Immediate)", "Clinical Safety & Negation Fix", "Integrate negation parsing; resolve vaccination unit bug; decouple snakebite advice", "100% on clinician-authored urgent/nonurgent test set"],
        ["Phase 2 (Short-Term)", "Vernacular Expansion", "Translate all 14 disease profiles and 64 myths into native Odia and Bengali", "Native clinician review of translated medical explanations"],
        ["Phase 3 (Medium-Term)", "Production Infrastructure", "Deploy custom domain with TLS; integrate Redis/Celery durable message queues", "Zero dropped messages under 1,000 concurrent user load"],
        ["Phase 4 (Long-Term)", "Official Health Linkage", "Establish read-only API connectors to state IDSP disease bulletins and CoWIN/U-WIN", "State Health Department administrative review & data governance"],
        ["Phase 5 (Long-Term)", "Formal Clinical Pilot Study", "Conduct prospective field study with rural ASHA workers in Odisha under ethics approval", "Clinical review against WHO Digital Health Guidelines (WHO, 2024)"]
    ]
    add_table(doc, road_headers, road_rows, "8.1", "Prioritized Strategic Roadmap and Clinical Validation Matrix for Future Work", [1.1, 1.4, 2.1, 1.16], pad_v=25, font_sz=8.0)

def add_bibliography(doc, add_heading_1, add_body_p):
    add_heading_1(doc, "BIBLIOGRAPHY")
    add_body_p(doc, "All cited references conform strictly to the American Psychological Association (APA 7th Edition) reference standards:")

    references = [
        ("DRIEMS University. (2025).", "Smart India Hackathon problem statements: SIH25049 (Government of Odisha). DRIEMS University. https://www.driems.ac.in/wp-content/uploads/2025/09/Smart-India-Hackathon_PROBLEM-STATEMENTS.pdf"),
        ("Feng, F., Yang, Y., Cer, D., Arivazhagan, N., & Wang, W. (2022).", "Language-agnostic BERT sentence embedding. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) (pp. 878–891). Association for Computational Linguistics. https://doi.org/10.18653/v1/2022.acl-long.62"),
        ("Khan, S. M., Summi, D., Singh, S., & Koshy, A. S. (2026).", "AarogyaSathi: Design and preliminary evaluation of a multilingual public health information chatbot [Manuscript submitted for publication]. Bhagwan Parshuram Institute of Technology, Delhi."),
        ("Laranjo, L., Dunn, A. G., Tong, H. L., Kocaballi, A. B., Chen, J., Bashir, R., Surian, D., Gallego, B., Chughtai, A. A., & Lau, A. Y. S. (2018).", "Conversational agents in healthcare: A systematic review. Journal of the American Medical Informatics Association, 25(9), 1248–1258. https://doi.org/10.1093/jamia/ocy072"),
        ("Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020).", "Retrieval-augmented generation for knowledge-intensive NLP tasks. In Advances in Neural Information Processing Systems (Vol. 33, pp. 9459–9474). Curran Associates, Inc."),
        ("Milne-Ives, M., de Cock, C., Lim, E., Shehadeh, M. H., de Pennington, N., Mole, G., Normando, E., & Meinert, E. (2020).", "The effectiveness of artificial intelligence conversational agents in health care: Systematic review. Journal of Medical Internet Research, 22(10), Article e20346. https://doi.org/10.2196/20346"),
        ("Ministry of Health and Family Welfare, Government of India. (2024).", "Universal Immunization Programme: National immunization schedule for infants, children and pregnant women. National Health Mission. https://nhm.gov.in/New_Updates_2018/NHM_Components/Immunization/report/National_Immunization_Schedule.pdf"),
        ("National Centre for Disease Control. (2024).", "Integrated Disease Surveillance Programme (IDSP): Strategic framework and weekly outbreak reporting. Directorate General of Health Services, Ministry of Health and Family Welfare. https://ncdc.mohfw.gov.in/"),
        ("Nilve, H., Parihar, K., & Nichat, A. (2026).", "AI-driven public health chatbot for disease awareness. International Journal of Engineering Research & Technology, 15(3), Article IJERTV15IS031825. https://www.ijert.org/"),
        ("Semigran, H. L., Linder, J. A., Gidengil, C., & Mehrotra, A. (2015).", "Evaluation of symptom checkers for self diagnosis and triage: Audit study. BMJ, 351, Article h3480. https://doi.org/10.1136/bmj.h3480"),
        ("World Health Organization. (2020).", "Managing the COVID-19 infodemic: Promoting healthy behaviours and mitigating the harm from misinformation and disinformation. Joint statement by WHO, UN, UNICEF, UNDP, UNESCO, UNAIDS, ITU, UN Global Pulse, and IFRC. https://www.who.int/news/item/23-09-2020-managing-the-covid-19-infodemic"),
        ("World Health Organization. (2024).", "Ethics and governance of artificial intelligence for health: Guidance on large multi-modal models (ISBN 978-92-4-008475-9). World Health Organization. https://www.who.int/publications/i/item/9789240084759")
    ]

    for authors_year, title_source in references:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.first_line_indent = Inches(-0.4)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        r_ay = p.add_run(authors_year + " ")
        r_ay.font.name = 'Times New Roman'
        r_ay.font.size = Pt(11)
        r_ay.bold = False

        r_ts = p.add_run(title_source)
        r_ts.font.name = 'Times New Roman'
        r_ts.font.size = Pt(11)

def add_appendices(doc, add_heading_1, add_heading_2, add_body_p, add_table, add_code_block):
    add_heading_1(doc, "APPENDIX A: PRODUCTION HARDWARE & ENVIRONMENT SPECIFICATIONS")
    add_body_p(doc,
        "This appendix documents the complete hardware topology, operating system parameters, and runtime environment specifications "
        "deployed on Oracle Cloud Infrastructure (OCI) hosting AarogyaSathi:"
    )

    app_a_headers = ["System Attribute", "Configured Production Specification", "Operational Function"]
    app_a_rows = [
        ["Cloud Hosting Provider", "Oracle Cloud Infrastructure (OCI) - Arm virtual machine (VM.Standard.A1.Flex)", "Infrastructure compute & storage host"],
        ["Compute Shape", "VM.Standard.A1.Flex (Ampere Altra Arm64 Processor)", "2 OCPUs, 12 GiB Unified Physical RAM"],
        ["Operating System", "Ubuntu 24.04 LTS (GNU/Linux 6.8.0-1017-oracle aarch64)", "Base operating system environment"],
        ["Storage Allocation", "50 GB Boot Volume (about 32 GiB free)", "OS, PyTorch weights, local SQLite DB"],
        ["Python Runtime", "Python 3.12.3 in dedicated virtualenv (/opt/healthbot/venv)", "Application execution runtime"],
        ["Process Supervision", "systemd daemons (healthbot.service, aarogya-tunnel.service)", "Process auto-restart & logging"],
        ["Networking & Ingress", "Cloudflare quick tunnel (cloudflared 2026.10.3)", "Public HTTPS ingress to localhost:8000"],
        ["LLM Inference Host", "Ollama 0.32.15 (C++ llama.cpp backend)", "Quantized Qwen3:1.7b local inference"],
        ["Memory Utilization", "System memory in use at inspection: about 3.3 GiB of 11 GiB (includes the Ollama model)", "Single observation on 1 November 2026"]
    ]
    add_table(doc, app_a_headers, app_a_rows, "A.1", "Oracle Cloud VM Production Hardware and Environment Topology", [1.5, 2.4, 1.86])



    add_heading_1(doc, "APPENDIX B: INTENT CLASSIFICATION TAXONOMY & API DIRECTORY")
    add_body_p(doc,
        "This appendix provides the formal directory of REST API endpoints exposed by AarogyaSathi and their supported HTTP methods:"
    )

    api_headers = ["Endpoint Route", "HTTP Method", "Payload Summary", "Functional Description & Output"]
    api_rows = [
        ["/api/chat", "POST", "JSON {message, pincode, session_id}", "Returns clinical reply text, detected intent, language, latency, and disclaimer"],
        ["/api/health", "GET", "None (Health probe)", "Returns server status, loaded models, local Ollama backend, supported languages"],
        ["/api/stats", "GET", "None (Telemetry query)", "Returns cumulative query counts, intent distribution, active session count in RAM"],
        ["/api/surveillance/alerts", "GET", "None", "Returns active syndromic cluster anomalies and rolling 7-day baselines"],
        ["/api/surveillance/seed", "POST", "None", "Inserts demonstration symptom records (demonstration use only)"],
        ["/webhook/whatsapp", "GET / POST", "Meta Hub Verify / Graph API JSON", "Meta webhook challenge verification (GET) and HMAC-SHA256 message handler (POST)"],
        ["/webhook/whatsapp/simulate", "POST", "JSON {from, message}", "Simulates inbound WhatsApp interaction without requiring active Meta credentials"],
        ["/", "GET", "None (Web browser)", "Serves index.html lightweight responsive mobile chat interface"],
        ["/admin", "GET", "None (Browser / Admin)", "Serves admin.html syndromic surveillance cluster monitoring portal"]
    ]
    add_table(doc, api_headers, api_rows, "B.1", "AarogyaSathi Production REST API Endpoint Directory", [1.3, 0.9, 1.6, 1.96])

print("Chapters 6-8, Bibliography, and Appendices generator module defined successfully.")
