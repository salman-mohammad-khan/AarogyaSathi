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
        'A public health chatbot needs more than ordinary software testing. An application can return HTTP 200 OK and fluent text, and still give dangerous clinical advice if it reverses a negation, miscalculates an age milestone, or lets a language model invent a treatment (Semigran et al., 2015; Milne-Ives et al., 2020). So we tested at four levels:'
    )
    add_bullet_p(doc, "1. Automated Unit and Regression Testing", 
                 'Systematic pytest checks of the core modules, input validators, cryptographic signatures and vector retrieval functions.')
    add_bullet_p(doc, "2. Component Benchmark Evaluation", 
                 'Separate scoring of intent classification accuracy, dense retrieval precision and fact-check agreement against ground-truth datasets.')
    add_bullet_p(doc, "3. Live Synthetic Query Spot Checks", 
                 'Clinical test messages (emergencies stated and negated, vaccine questions, disease symptoms and prompts in regional languages) sent directly to the live Oracle VM.')
    add_bullet_p(doc, "4. End-to-End Channel Delivery Verification", 
                 'The webhook handshake and signature check, and a message exchange between the deployed service and one approved test recipient through the Meta WhatsApp Cloud API.')

    add_heading_1(doc, "6.2 Unit and Regression Test Suite Execution")
    add_body_p(doc,
        'We ran the automated test suite on the Oracle Cloud Infrastructure virtual machine (Ubuntu 24.04 ARM64, Python 3.12.3) on 26 October 2026. All 37 unit and regression tests passed in 24.24 seconds. Five WhatsApp webhook security tests were added during the channel integration and passed separately on 31 October 2026 (5.12 seconds), so the repository now has 42 tests. Table 6.1 shows how the tests are distributed and what they cover:'
    )

    test_headers = ["Test Suite File", "Test Count", "Functional Scope Evaluated", "Execution Result"]
    test_rows = [
        ["tests/test_core.py", "12 Tests", 'Fast-path rules, LaBSE embedding normalisation, cosine ranking, language identification, entity extraction', "12 / 12 Passed (100%)"],
        ["tests/test_flow.py", "8 Tests", "Multi-turn symptom dialogue states, session TTL expiry, switching the user's language, adding disclaimers", "8 / 8 Passed (100%)"],
        ["tests/test_ml.py", "9 Tests", 'TF-IDF n-gram vectors, logistic regression intent detection, threshold filtering, claim verification matching', "9 / 9 Passed (100%)"],
        ["tests/test_surveillance.py", "4 Tests", "SQLite symptom telemetry insertion, 7-day rolling baseline calculation, cluster alert condition evaluation", "4 / 4 Passed (100%)"],
        ["tests/test_whatsapp.py", "4 Tests", "Meta webhook challenge handshake, WhatsApp simulation endpoint, Twilio adapter", "4 / 4 Passed"],
        ["tests/test_meta_webhook_security.py", "5 Tests", 'HMAC-SHA256 signature checks, rejection of tampered or unsigned requests, duplicate suppression, receiver filtering (added 31 October 2026)', "5 / 5 Passed"]
    ]
    add_table(doc, test_headers, test_rows, "6.1", "Automated Test Suite Coverage (37 Tests Run on 26 October 2026; 5 Channel Security Tests Added on 31 October 2026)", [1.3, 0.8, 2.7, 0.96])

    add_heading_1(doc, "6.3 Component Benchmark Evaluation (Intent, Retrieval, Fact-Check)")
    add_body_p(doc,
        'The machine learning components were evaluated one by one with the benchmark runner (scripts/eval.py) on the ground-truth datasets in data/training/eval.json. Table 6.2 gives the results together with the important limits of each benchmark:'
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
        'The intent classifier scored a perfect 30/30 (100%) on the benchmark set. When we looked at the data, though, 14 of the 30 evaluation questions (46.7%) were exact copies of sentences in the training data (data/training/intents.json). To see how well the model generalises, we ran a separate evaluation on 29 October 2026 using only the 16 questions that were not duplicates. All 16 were classified correctly at threshold 0.45. Even so, the development team wrote these questions. They were not sampled from real patient conversations, so the score should not be read as an unbiased estimate of real-world accuracy.'
    )

    add_heading_2(doc, "6.3.2 Retrieval Precision and Myth Class Imbalance")
    add_body_p(doc,
        'The LaBSE retrieval test gave 100% top-1 accuracy on 15 curated queries (5 disease targets and 10 FAQ targets). It used relaxed benchmark settings (top-3, threshold 0.35) rather than the production settings (top-5, threshold 0.52). The claim verifier likewise classified all 34 benchmark rumours correctly, in 387 ms on average. But the test set is very unbalanced. Of the 34 claims, 24 (70.6%) are MYTH, and only 4 are TRUE, 5 PARTLY TRUE and 1 UNVERIFIABLE. The benchmark therefore shows that the verifier handles myths well, and tells us very little about the rarer verdicts.'
    )

    add_heading_1(doc, "6.4 Synthetic End-to-End Query Spot Checks and Clinical Defect Analysis")
    add_body_p(doc,
        'Developer benchmarks do not show how the whole pipeline behaves, so we sent five synthetic clinical queries directly to the live Oracle Cloud API (/api/chat). Table 6.3 gives the results. They show that good component scores do not guarantee safe behaviour end to end:'
    )

    spot_headers = ["Synthetic Input Query", "Intended Clinical Action", "Observed Route & Response", "Latency"]
    spot_rows = [
        ["I have severe chest pain and cannot breathe", "Immediate emergency triage escalation", 'Sent to the emergency route; replied with the 108 hotline advice and a snakebite guide', "0.29 s"],
        ["I have no chest pain, only a mild headache", "Benign symptom triage (headache advice)", 'FALSE EMERGENCY: triggered the acute emergency reply', "0.08 s"],
        ["fact check: vaccines cause autism", "Neutralize misinformation with myth verdict", 'Returned a MYTH verdict with an explanation and sources', "0.15 s"],
        ["What are dengue symptoms?", "Provide disease profile & warning signs", 'Returned the verified dengue profile, prevention tips and disclaimer', "2.32 s"],
        ["ଡେଙ୍ଗୁ ପ୍ରତିଷେଧକ କ’ଣ? (Odia dengue query)", "Provide preventive advice in Odia", 'FALLBACK GAP: returned a generic apology saying no reliable information was available', "11.41 s"]
    ]
    add_table(doc, spot_headers, spot_rows, "6.3", "Selected Live Synthetic Query Spot Checks and Clinical Response Observations", [1.5, 1.4, 2.1, 0.76])

    add_heading_2(doc, "6.4.1 The Negation Handling Vulnerability in Emergency Safety")
    add_body_p(doc,
        "The most serious problem we found in live testing was that negation is not handled. We sent 'I have no chest pain, only a mild headache'. The red-flag matcher (entities.py, called through safety.py) matched 'chest pain' without checking for the negation. The system treated a mild headache as an emergency, told the user to dial 108 and, by mistake, added snakebite first-aid instructions. A false alarm is better than a missed emergency, but this shows that keyword matching cannot tell a symptom the user has from one they say they do not have."
    )

    add_heading_2(doc, "6.4.2 Regional Vernacular Fallback Gaps")
    add_body_p(doc,
        "For an Odia query ('ଡେଙ୍ଗୁ ପ୍ରତିଷେଧକ କ’ଣ?'), the system recognised the language code ('or') but could not retrieve any context above the 0.52 threshold. It fell back to a safe reply ('I am sorry, I do not have reliable health information about that') after 11.41 s, the longest delay we saw. So language detection covers 12 languages, but reliable medical content exists mainly in English and Hindi."
    )

    add_heading_1(doc, "6.5 Code Inspection Findings: Vaccination Age Conversion Defect")
    add_body_p(doc,
        'Reading through app/core/router.py, we found a logic error in the function that converts infant age to a vaccination milestone (_age_to_milestones). The branch that handles ages given in months and the one that handles years are mixed up:'
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
        'As a result, a question about a 2-month-old infant is mapped to the 9–12 month milestone (MR/JE vaccines instead of Pentavalent/Rotavirus/OPV). In our tests the local language model happened to refuse some of these questions, which hid the wrong output. This is a good reason to write full unit tests for the milestone logic, because a language model can cover up a bug in the fixed rules.'
    )

    add_heading_1(doc, "6.6 Meta WhatsApp Cloud API Channel Live Verification")
    add_body_p(doc,
        "On 31 October 2026 we ran a full live check of the channel, connecting the Oracle Cloud deployment to Meta's WhatsApp Cloud API. Table 6.4 lists the milestones we verified:"
    )

    wa_headers = ["Verification Stage", "Observed Host Telemetry", "Status / Performance Result"]
    wa_rows = [
        ["HTTPS Webhook Handshake", "Meta GET challenge matched WHATSAPP_VERIFY_TOKEN exactly", "HTTP 200 OK (Confirmed)"],
        ["Cryptographic Security", 'A valid HMAC-SHA256 signature was accepted (0.024 s); an unsigned request was rejected with HTTP 403', "Security Verified"],
        ["Isolated Channel Tests", '5 channel test cases (valid signature, tampered body, deduplication, status callbacks) run on the VM', "5 / 5 Passed in 5.12 s"],
        ["Live Handset Exchange", "The registered test recipient sent 'hi', 'What are dengue symptoms?' and 'fact check: garlic cures dengue'", "3 / 3 Replies Received (user-confirmed)"],
        ["Server Log Telemetry", 'The server log shows 3 incoming text messages, 3 outbound messages accepted by Meta and 0 send errors', "0 Send Errors"]
    ]
    add_table(doc, wa_headers, wa_rows, "6.4", "Meta WhatsApp Cloud API Channel Live Verification Summary", [1.4, 2.6, 1.76], pad_v=45, font_sz=8.5)

    add_heading_1(doc, "6.7 SIH25049 Challenge Compliance Matrix")
    add_body_p(doc,
        'Table 6.5 sets the requirements in the original Smart India Hackathon brief against what the delivered prototype actually demonstrates:'
    )

    sih_headers = ["Brief Requirement", "Demonstrated Implementation Evidence", "Compliance Status"]
    sih_rows = [
        ["Disease & Prevention Info", '14 curated profiles and 35 FAQs; English and Hindi RAG answers checked on the live VM', "Fully Operational Prototype"],
        ["National Immunization Schedules", '13 UIP milestones encoded; a month-unit conversion bug was found and needs fixing', "Prototype (Correction Required)"],
        ["Multilingual Communication", '12 language codes detected; Hindi answers checked; an Odia prevention query fell back safely', "Partial (English and Hindi strongest)"],
        ["WhatsApp & SMS Access", 'Meta WhatsApp Cloud API v25.0 checked with live delivery to a recipient; SMS not verified', "WhatsApp Verified / SMS Unmet"],
        ["Outbreak Advisory Telemetry", '7-day rolling anomaly detector; illustrative advisories shown on /admin', "Operational Demonstration"],
        ["Government Database Linkage", 'No direct API link to the official state IDSP databases was demonstrated', "Out of Scope / Future Work"]
    ]
    add_table(doc, sih_headers, sih_rows, "6.5", "SIH25049 Challenge Compliance Matrix: Brief Requirements vs. Prototype Status", [1.4, 2.7, 1.66], pad_v=45, font_sz=8.5)

def add_chapter_7(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2):
    add_chapter_title(doc, "7", "Summary and Conclusion")

    add_heading_1(doc, "7.1 Summary of Delivered Work and Technical Achievements")
    add_body_p(doc,
        "This report has described the design, implementation and testing of AarogyaSathi (आरोग्यसाथी), an AI-based public health chatbot built for Smart India Hackathon problem SIH25049 in the Government of Odisha's healthcare technology theme. The project connects natural language processing with simple, practical health information for people in villages and small towns."
    )
    add_body_p(doc,
        'The main things we achieved are:'
    )
    add_bullet_p(doc, "1. Hybrid Multi-Tier Conversational Architecture",
                 'Built an asynchronous FastAPI pipeline that combines deterministic safety interception, rule-based fast-path routing and dense semantic retrieval. In a single observation on 26 October 2026, a disease-information answer took 2.32 seconds.')
    add_bullet_p(doc, "2. Authoritative Clinical Knowledge Base",
                 'Curated and indexed 14 major endemic disease profiles, 35 public health FAQs, 13 national childhood immunisation milestones and 64 common Indian health myths, all based only on published WHO, MoHFW and ICMR guidance.')
    add_bullet_p(doc, "3. Cross-Lingual Semantic Retrieval Pipeline",
                 'Integrated the 768-dimensional LaBSE sentence embedding model with a hybrid cosine and lexical reranker, so that documents can be retrieved across regional languages without translating first.')
    add_bullet_p(doc, "4. Dedicated Health Misinformation Verifier",
                 'Developed a fact-checking engine that takes forwarded viral claims, sorts them into four verdicts (VERIFIED, MYTH, PARTLY TRUE, UNVERIFIABLE) and returns a clear explanation (mean 387 ms per claim on the 34-claim development set).')
    add_bullet_p(doc, "5. Low-Cost Cloud Deployment & Multi-Channel Ingress",
                 'Deployed the whole stack on an Oracle Cloud Infrastructure virtual machine (2 OCPUs, 12 GiB RAM, Ubuntu 24.04 ARM64). Users can reach it through a responsive web app and, for an approved test recipient, through a Meta WhatsApp Cloud API channel (outbound API v25.0) behind a Cloudflare HTTPS tunnel with signature-verified webhooks.')
    add_bullet_p(doc, "6. Rigorous Software Quality Verification",
                 'All 37 automated tests from the 26 October run passed, and so did the five channel security tests added later. On the development sets the component benchmarks scored 30/30 for intent, 15/15 for retrieval and 34/34 for claim verdicts. Three WhatsApp test messages were answered for an approved recipient, and the server logs showed no sending errors.')

    add_heading_1(doc, "7.2 Significance for Public Health Information Dissemination")
    add_body_p(doc,
        'We think the wider point of AarogyaSathi is that a privacy-conscious digital health service can be built and run on free-tier infrastructure, with no recurring software licence cost during the prototype phase. It uses open-source models (Qwen3:1.7b, LaBSE) that run locally, so a country with limited funds could deploy a similar assistant without paying for a commercial AI service or being tied to one vendor. Delivering it through WhatsApp, which people already use every day, also puts verified health information within reach of rural citizens and ASHA workers.'
    )

    add_heading_1(doc, "7.3 Concluding Remarks")
    add_body_p(doc,
        'AarogyaSathi is a prototype that tries to be honest about itself. It sets firm clinical limits, says where its evaluation is weak, and reports real failures next to its successes. We hope that makes it a sound and reproducible starting point for ethical, vernacular public health chatbots in India.'
    )

def add_chapter_8(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_table):
    add_chapter_title(doc, "8", "Limitations and Future Work")

    add_heading_1(doc, "8.1 Identified Architectural and Clinical Safety Limitations")
    add_body_p(doc,
        "We have tried to document the system's weaknesses openly. The ones below came out of code reading, automated tests and live spot checks:"
    )
    add_bullet_p(doc, "1. Lexical Negation Blindness in Emergency Triage",
                 "The red-flag list in entities.py matches surface phrases and ignores negation. 'No chest pain, only a mild headache' triggered a false cardiac emergency. A trained negation classifier is needed to separate reported symptoms from denied ones.")
    add_bullet_p(doc, "2. Irrelevant Emergency Instruction Concatenation",
                 "The emergency reply template puts snakebite first-aid advice in the same message as the cardiac and breathing instructions. In a real emergency, unrelated advice adds to the reader's confusion and makes the triage message less clear.")
    add_bullet_p(doc, "3. Infant Vaccination Age-Unit Conversion Defect",
                 'A hardcoded logic error in router.py::_age_to_milestones maps every infant age given in months to the 9–12 month milestone. Ages in days, weeks, months and years need to be normalised properly and checked against the full UIP schedule.')
    add_bullet_p(doc, "4. Ungrounded Generative Fallback Risks",
                 'When local retrieval falls below the confidence cutoff, generator.general_answer() asks the language model to answer from its own knowledge. A disclaimer is added, but the model can still hallucinate. Out-of-domain clinical questions should be refused.')

    add_heading_1(doc, "8.2 Geographic and Epidemiological Surveillance Modeling Constraints")
    add_body_p(doc,
        'The syndromic detector does log symptom and pincode events in SQLite and checks them against rolling thresholds. Its value for epidemiology is limited, however. Reporting is voluntary and therefore biased, and there are no census population denominators. A spike may come from people newly trying the bot, or from media coverage, and not from real disease spread. The outbreak records are also illustrative advisories, not a live link to the Integrated Disease Surveillance Programme (IDSP).'
    )

    add_heading_1(doc, "8.3 Linguistic and Regional Knowledge Base Gaps")
    add_body_p(doc,
        'Language detection covers 12 Indian languages, but the verified clinical profiles are written almost entirely in English and Hindi. The Odia dengue spot check shows the gap: it took 11.41 s and returned an unhelpful fallback. Understanding a language does not mean being able to answer in it. For a state-wide rollout the knowledge base would have to be translated and curated in Odia, Bengali, Telugu and Tamil.'
    )

    add_heading_1(doc, "8.4 Deployment, Privacy, and Channel Constraints")
    add_body_p(doc,
        'The WhatsApp channel currently runs behind a temporary Cloudflare Tunnel, so the webhook has to be updated by hand after each restart. A production setup needs a permanent domain with an SSL reverse proxy, a durable Redis/Celery queue for reliable outbound delivery, and a move from the developer test sender (+1 555 626 0618) to an approved WhatsApp Business Account.'
    )

    add_heading_1(doc, "8.5 Prioritized Strategic Roadmap for Future Enhancements")
    add_body_p(doc,
        'Table 8.1 lays out a prioritised plan of engineering and clinical validation work that would take AarogyaSathi from a college prototype towards a certified public health tool:'
    )

    road_headers = ["Priority Phase", "Target Milestone", "Technical Scope & Methodology", "Validation Standard"]
    road_rows = [
        ["Phase 1 (Immediate)", "Clinical Safety & Negation Fix", 'Add negation parsing; fix the vaccination unit bug; separate the snakebite advice', "100% on clinician-authored urgent/nonurgent test set"],
        ["Phase 2 (Short-Term)", "Vernacular Expansion", 'Translate all 14 disease profiles and 64 myths into Odia and Bengali', 'Review of the translated medical explanations by native-speaking clinicians'],
        ["Phase 3 (Medium-Term)", "Production Infrastructure", 'Set up a custom domain with TLS; add durable Redis/Celery message queues', "Zero dropped messages under 1,000 concurrent user load"],
        ["Phase 4 (Long-Term)", "Official Health Linkage", 'Build read-only API connectors to the state IDSP disease bulletins and CoWIN/U-WIN', "State Health Department administrative review & data governance"],
        ["Phase 5 (Long-Term)", "Formal Clinical Pilot Study", 'Run a prospective field study with rural ASHA workers in Odisha, with ethics approval', "Clinical review against WHO Digital Health Guidelines (WHO, 2024)"]
    ]
    add_table(doc, road_headers, road_rows, "8.1", "Prioritized Strategic Roadmap and Clinical Validation Matrix for Future Work", [1.1, 1.4, 2.1, 1.16], pad_v=25, font_sz=8.0)

def add_bibliography(doc, add_heading_1, add_body_p):
    add_heading_1(doc, "BIBLIOGRAPHY")
    add_body_p(doc, 'All references follow the American Psychological Association (APA 7th Edition) style:')

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
        'This appendix describes the hardware, operating system settings and runtime environment of the Oracle Cloud Infrastructure (OCI) host that runs AarogyaSathi:'
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
        'This appendix lists the REST API endpoints exposed by AarogyaSathi and the HTTP methods each one supports:'
    )

    api_headers = ["Endpoint Route", "HTTP Method", "Payload Summary", "Functional Description & Output"]
    api_rows = [
        ["/api/chat", "POST", "JSON {message, pincode, session_id}", 'Returns the reply text, detected intent, language, latency and disclaimer'],
        ["/api/health", "GET", "None (Health probe)", 'Returns server status, loaded models, the local Ollama backend and supported languages'],
        ["/api/stats", "GET", "None (Telemetry query)", 'Returns total query counts, the intent distribution and the number of active sessions in memory'],
        ["/api/surveillance/alerts", "GET", "None", 'Returns the active syndromic cluster anomalies and the rolling 7-day baselines'],
        ["/api/surveillance/seed", "POST", "None", "Inserts demonstration symptom records (demonstration use only)"],
        ["/webhook/whatsapp", "GET / POST", "Meta Hub Verify / Graph API JSON", 'Meta webhook challenge check (GET) and HMAC-SHA256 message handler (POST)'],
        ["/webhook/whatsapp/simulate", "POST", "JSON {from, message}", 'Simulates an incoming WhatsApp message without needing active Meta credentials'],
        ["/", "GET", "None (Web browser)", 'Serves index.html, the light responsive mobile chat page'],
        ["/admin", "GET", "None (Browser / Admin)", 'Serves admin.html, the syndromic surveillance monitoring page']
    ]
    add_table(doc, api_headers, api_rows, "B.1", "AarogyaSathi Production REST API Endpoint Directory", [1.3, 0.9, 1.6, 1.96])

print("Chapters 6-8, Bibliography, and Appendices generator module defined successfully.")
