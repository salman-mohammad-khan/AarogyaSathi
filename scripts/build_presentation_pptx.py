import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    # 16:9 Widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # completely blank layout

    # Palette
    c_navy = RGBColor(15, 32, 67)
    c_teal = RGBColor(22, 160, 133)
    c_white = RGBColor(255, 255, 255)
    c_dark = RGBColor(33, 47, 61)
    c_gray = RGBColor(100, 110, 120)
    c_light_bg = RGBColor(245, 247, 250)
    c_card_bg = RGBColor(235, 245, 251)
    c_card_border = RGBColor(169, 204, 227)
    c_gold = RGBColor(212, 172, 13)

    def add_header(slide, title_text, category_text="MINOR PROJECT 1ST DEFENSE | ES-451"):
        # Top banner background
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = c_navy
        top_bar.line.fill.background()

        # Accent line
        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.15), Inches(13.333), Inches(0.06))
        accent.fill.solid()
        accent.fill.fore_color.rgb = c_teal
        accent.line.fill.background()

        # Text
        tx = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.95))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0)
        tf.margin_bottom = Inches(0)
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(9.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = c_gold
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = c_white

    def add_footer(slide):
        # Bottom line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(210, 215, 220)
        line.line.fill.background()

        tx = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
        tf = tx.text_frame
        p = tf.paragraphs[0]
        p.text = "AarogyaSathi: Multilingual Public Health Agent | Department of Computer Science & Engineering (Data Science)"
        p.font.size = Pt(9)
        p.font.color.rgb = c_gray

    # -------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = c_navy
    bg1.line.fill.background()

    # Decorative accent
    acc1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.3), Inches(1.2), Inches(0.08))
    acc1.fill.solid()
    acc1.fill.fore_color.rgb = c_teal
    acc1.line.fill.background()

    tx1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(5.2))
    tf1 = tx1.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "MINOR PROJECT (ES-451) — 1ST DEFENSE PRESENTATION"
    p_badge.font.size = Pt(12)
    p_badge.font.bold = True
    p_badge.font.color.rgb = c_gold

    p_main = tf1.add_paragraph()
    p_main.text = "AarogyaSathi"
    p_main.font.size = Pt(38)
    p_main.font.bold = True
    p_main.font.color.rgb = c_white
    p_main.space_before = Pt(8)

    p_sub = tf1.add_paragraph()
    p_sub.text = "A Multilingual Retrieval-Augmented Public Health Conversational Agent with Autonomous Multi-Tier Fact-Checking and Community Syndromic Surveillance"
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = RGBColor(200, 220, 240)
    p_sub.space_before = Pt(6)

    p_team_h = tf1.add_paragraph()
    p_team_h.text = "PROJECT TEAM MEMBERS:"
    p_team_h.font.size = Pt(11)
    p_team_h.font.bold = True
    p_team_h.font.color.rgb = c_teal
    p_team_h.space_before = Pt(28)

    p_team = tf1.add_paragraph()
    p_team.text = "• Salman Mohammad Khan  (Enrollment / Roll No: 00520815723)\n• Dhairya Summi                  (Enrollment / Roll No: 00420815723)\n• Siddharth Singh                (Enrollment / Roll No: 01820815723)"
    p_team.font.size = Pt(13)
    p_team.font.color.rgb = c_white
    p_team.space_before = Pt(4)

    p_dept = tf1.add_paragraph()
    p_dept.text = "Department of Computer Science & Engineering (Data Science)\nBachelor of Technology (B.Tech) | Evaluation Date: September 14, 2026"
    p_dept.font.size = Pt(11)
    p_dept.font.italic = True
    p_dept.font.color.rgb = RGBColor(170, 185, 205)
    p_dept.space_before = Pt(16)

    # -------------------------------------------------------------
    # SLIDE 2: BACKGROUND & MOTIVATION
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Background & Problem Motivation")
    add_footer(s2)

    # 3 Cards
    cards_data = [
        ("Severe Healthcare Accessibility Divide", 
         "• India's doctor-to-population ratio is 1:1456, falling far below the WHO norm of 1:1000.\n• Rural PHCs suffer chronic diagnostic backlogs; over 70% of citizens rely on informal health conduits.\n• Citizens need instant, culturally aligned preventive health awareness in their native tongue.",
         "#FDEDEC", "#C0392B"),
        ("The Medical Infodemic on Social Media", 
         "• Unverified, pseudoscientific health advice spreads virally on WhatsApp and Telegram groups.\n• Baseless rumours cause pediatric immunization hesitancy (e.g. false polio infertility myths).\n• Lethal first-aid practices (cutting snakebites, chilli powder on dog bites) cause severe tissue necrosis.",
         "#FEF9E7", "#D4AC0D"),
        ("14-21 Day Surveillance Lag in IDSP", 
         "• Traditional centralized surveillance (IDSP) depends on clinical laboratory confirmation registries.\n• By the time an outbreak is officially recorded, community transmission has peaked.\n• Lack of localized, real-time syndromic signal capture at the postal pincode level.",
         "#EBF5FB", "#2980B9")
    ]

    for idx, (head, body, bg_col, bdr_col) in enumerate(cards_data):
        x = Inches(0.8 + idx * 3.95)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.6), Inches(3.8), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor.from_string(bg_col.replace("#", ""))
        card.line.color.rgb = RGBColor.from_string(bdr_col.replace("#", ""))
        card.line.width = Pt(1.5)

        tx = s2.shapes.add_textbox(x + Inches(0.15), Inches(1.75), Inches(3.5), Inches(4.8))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = head
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = RGBColor.from_string(bdr_col.replace("#", ""))
        
        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(11)
        p2.font.color.rgb = c_dark
        p2.space_before = Pt(12)

    # -------------------------------------------------------------
    # SLIDE 3: PROBLEM STATEMENT & OBJECTIVES
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Problem Statement & Project Objectives")
    add_footer(s3)

    # Left: Problem Statement
    box_l = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
    box_l.fill.solid()
    box_l.fill.fore_color.rgb = c_card_bg
    box_l.line.color.rgb = c_navy
    box_l.line.width = Pt(1.5)

    tx_l = s3.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(5.2), Inches(4.8))
    tf_l = tx_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Formal Problem Statement"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_navy

    p = tf_l.add_paragraph()
    p.text = "To design, develop, and deploy an autonomous, zero-cost, multilingual conversational public health agent that delivers verified preventive healthcare education, deterministic emergency triage escalation, autonomous rumor fact-checking without third-party API dependencies, and proactive community syndromic surveillance across rural and semi-urban Indian populations."
    p.font.size = Pt(11.5)
    p.font.color.rgb = c_dark
    p.space_before = Pt(10)

    # Right: Objectives
    box_r = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1))
    box_r.fill.solid()
    box_r.fill.fore_color.rgb = RGBColor(232, 248, 245)
    box_r.line.color.rgb = c_teal
    box_r.line.width = Pt(1.5)

    tx_r = s3.shapes.add_textbox(Inches(7.0), Inches(1.75), Inches(5.3), Inches(4.8))
    tf_r = tx_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Primary Research Objectives"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_teal

    objectives = [
        "1. Multilingual Semantic Grounding: Integrate Google LaBSE to map English, Hindi, and Hinglish queries into a unified 768-dimensional metric space.",
        "2. Zero-Hallucination RAG: Constrain an open-weights Small Language Model (Qwen3-1.7B-Instruct) to strictly verified WHO/MoHFW context.",
        "3. Deterministic Safety Boundaries: Enforce sub-10ms triage escalation for life-threatening medical emergencies (108/112 ambulance prompt).",
        "4. Autonomous Fact-Checking: Develop a 4-tier verification engine combining local lexical coverage and open-web news evidence synthesis ($0 API cost).",
        "5. Community Syndromic Surveillance: Establish automated spatial anomaly detection (7-day rolling baseline vs 24h count) across 6-digit Indian PIN codes."
    ]
    for obj in objectives:
        p = tf_r.add_paragraph()
        p.text = obj
        p.font.size = Pt(10.5)
        p.font.color.rgb = c_dark
        p.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 4: LITERATURE SURVEY & GAP ANALYSIS
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Literature Survey & Critical Gap Analysis")
    add_footer(s4)

    lit_data = [
        ("Existing Solution", "Methodology / Approach", "Critical Gap / Vulnerability", "AarogyaSathi Advantage"),
        ("Ada Health / Babylon Health", "Proprietary Bayesian nets & clinical decision trees", "Closed-source, high licensing cost, no Hinglish/Indic support, legal liability in self-diagnosis", "Open-source, non-diagnostic awareness framing, native Hindi/Hinglish NLP"),
        ("CoWIN / Aarogya Setu", "Centralized transactional databases (Bluetooth, OTP)", "Static registries without interactive symptom exploration, triage, or myth-busting capabilities", "Multi-turn empathetic symptom clarification & autonomous fact-checking"),
        ("Google Fact Check Tools API", "ClaimReview structured JSON schema aggregation", "Index sparsity for village health rumors; commercial billing/card restrictions in Global South", "Autonomous multi-tier engine: local semantic corpus + live open-web/news synthesis ($0 cost)"),
        ("Google Flu Trends (GFT)", "Correlating aggregated search engine keywords", "Prone to panic-induced search spikes; lacks clinical symptom parsing or geocoded triage", "Pincode-level geocoded symptom event logging with rolling 7-day baseline anomaly regression")
    ]

    # Create Table on slide
    rows = len(lit_data)
    cols = 4
    t = s4.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.1)).table
    t.columns[0].width = Inches(2.2)
    t.columns[1].width = Inches(2.8)
    t.columns[2].width = Inches(3.4)
    t.columns[3].width = Inches(3.333)

    for r_idx, row in enumerate(lit_data):
        for c_idx, val in enumerate(row):
            cell = t.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            if r_idx == 0:
                p.font.bold = True
                p.font.size = Pt(11)
                p.font.color.rgb = c_white
                cell.fill.solid()
                cell.fill.fore_color.rgb = c_navy
            else:
                p.font.size = Pt(9.5)
                p.font.color.rgb = c_dark
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(245, 248, 250) if r_idx % 2 == 0 else c_white

    # -------------------------------------------------------------
    # SLIDE 5: SYSTEM ARCHITECTURE
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "End-to-End System Architecture")
    add_footer(s5)

    if os.path.exists("docs/fig1_architecture.png"):
        s5.shapes.add_picture("docs/fig1_architecture.png", Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3))

    # -------------------------------------------------------------
    # SLIDE 6: CORE NLP & CROSS-LINGUAL RETRIEVAL
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Core Methodology: Multilingual NLP & LaBSE Retrieval")
    add_footer(s6)

    # 2-column layout
    tx_a = s6.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    tf_a = tx_a.text_frame
    tf_a.word_wrap = True
    p = tf_a.paragraphs[0]
    p.text = "1. Language ID & Intent Classification"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = c_navy

    points_a = [
        "• Language Identification: fastText (lid.176) hierarchically classifies inputs across 176 languages; transliteration heuristics detect romanized Hinglish.",
        "• Intent Classifier: TF-IDF feature extraction (unigram/bigram, sublinear scaling) + L2-regularized Logistic Regression.",
        "• 13 Public Health Classes: emergency, fact_check, disease_info, symptom_check, prevention, vaccination, outbreak, greeting, help, etc.",
        "• Macro F1-Score: 0.942 across validation benchmarks with 1.000 precision on safety-critical red-flag emergency detection.",
        "• Entity Extraction: Regex and dictionary ontologies extract 14 diseases, 42 symptoms, 12 vaccines, and age milestones."
    ]
    for pt in points_a:
        p = tf_a.add_paragraph()
        p.text = pt
        p.font.size = Pt(10.5)
        p.font.color.rgb = c_dark
        p.space_before = Pt(6)

    tx_b = s6.shapes.add_textbox(Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2))
    tf_b = tx_b.text_frame
    tf_b.word_wrap = True
    p = tf_b.paragraphs[0]
    p.text = "2. Cross-Lingual LaBSE Embedding Metric"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = c_teal

    points_b = [
        "• Google LaBSE (Language-Agnostic BERT Sentence Embeddings): Dual-encoder contrastive learning across 109 languages.",
        "• Unified Latent Space: Projects Hindi, English, and Hinglish queries into a shared 768-dimensional Hilbert space.",
        "• Metric Formula: Dense vector mean-pooling and L2 normalization:",
        "    vq = MeanPool(LaBSE(q)) / ||MeanPool(LaBSE(q))||2",
        "• Cosine Similarity Distance over pre-computed matrix:",
        "    S(q, ci) = vq · vci = SUM_{k=1}^{768} (vq,k * vci,k)",
        "• Pre-Cached Matrices: Pre-indexed memory-mapped NumPy arrays with SHA-256 cache keys provide instant <0.10s lookup."
    ]
    for pt in points_b:
        p = tf_b.add_paragraph()
        p.text = pt
        p.font.size = Pt(10.5)
        p.font.color.rgb = c_dark
        p.space_before = Pt(5)

    # -------------------------------------------------------------
    # SLIDE 7: GROUNDED RAG & SMALL LANGUAGE MODELS
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Retrieval-Augmented Generation & Edge SLM Reasoning")
    add_footer(s7)

    # 3 horizontal steps
    rag_steps = [
        ("Step 1: Curated Knowledge Retrieval",
         "• Strict factual grounding in Tier-1 national and international repositories: WHO, MoHFW, ICMR, NHM.\n• 14 Comprehensive Disease Profiles (Dengue, Malaria, TB, Rabies...).\n• National Immunization Schedule (UIP) from birth to pregnancy.\n• Zero ungrounded clinical hallucination.",
         "#EBF5FB", "#2980B9"),
        ("Step 2: Edge-Quantized SLM (Qwen3-1.7B)",
         "• Runs locally via Ollama with 4-bit quantization (Q4_K_M GGUF).\n• Memory footprint: only 1.6GB RAM/VRAM — runs smoothly on 4GB instances.\n• High-speed generation without sending citizen data to external third-party servers.\n• Automatic circuit breaker fallback to template answers if Ollama is unreachable.",
         "#FEF9E7", "#D4AC0D"),
        ("Step 3: Negative Prompt Constraints",
         "• Enforces strict negative operational boundaries:\n  1. Answer strictly and only from retrieved context.\n  2. Hard constraint: response must be under 70 words.\n  3. Never prescribe medicines or deliver clinical diagnosis.\n  4. Append validated WHO/MoHFW source citation and medical disclaimer.",
         "#E8F8F5", "#16A085")
    ]

    for idx, (head, body, bg_col, bdr_col) in enumerate(rag_steps):
        x = Inches(0.8 + idx * 3.95)
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.6), Inches(3.8), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor.from_string(bg_col.replace("#", ""))
        card.line.color.rgb = RGBColor.from_string(bdr_col.replace("#", ""))
        card.line.width = Pt(1.5)

        tx = s7.shapes.add_textbox(x + Inches(0.15), Inches(1.75), Inches(3.5), Inches(4.8))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = head
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = RGBColor.from_string(bdr_col.replace("#", ""))
        
        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = c_dark
        p2.space_before = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 8: AUTONOMOUS FACT-CHECKING ENGINE
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Autonomous Multi-Tier Fact-Checking Engine ($0 Cost)")
    add_footer(s8)

    tx_fc = s8.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.3))
    tf_fc = tx_fc.text_frame
    tf_fc.word_wrap = True

    p = tf_fc.paragraphs[0]
    p.text = "Why We Replaced Google Fact Check API with Our Own Autonomous Engine:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_navy

    p = tf_fc.add_paragraph()
    p.text = "• Google's API mandates linked Cloud Billing Accounts (which fail across Indian students/developers due to RBI e-mandate rules) and returns 404 on uncatalogued regional claims.\n• Our custom engine operates 100% autonomously with ZERO external API keys and $0 cloud billing."
    p.font.size = Pt(10.5)
    p.font.color.rgb = c_dark
    p.space_before = Pt(3)

    tiers_data = [
        ("Tier 0: Dangerous First-Aid Fast Guard (0.01s)", "Sub-10ms regex interceptor for lethal first-aid advice (sucking snakebite, red chilli on dog bite, butter on burns) returning instant critical MYTH with life-saving WHO protocols."),
        ("Tier 1: Semantic Matching + Dual-Metric Lexical Coverage (0.10s)", "Eliminates positive/negative myth collisions (e.g. polio drops protect vs cause infertility) using composite token coverage: Omega = min(Dice(q, ci), Cov(q, ci)) >= 0.35. Ensures true immunization facts never get marked as myths."),
        ("Tier 2: Real-Time Multi-Strategy Open Web Evidence Retrieval", "Decoupled web evidence harvesting using DuckDuckGo News protocol, Wikipedia MediaWiki REST API (EN + Hindi), and whitelisted domain filtering (who.int, mohfw.gov.in, cdc.gov, mayoclinic.org)."),
        ("Tier 3: Grounded LLM Evidence Synthesis", "Local SLM reads harvested snippets, evaluates consensus, and emits structured JSON verdict: VERIFIED / MYTH / PARTLY TRUE / UNVERIFIABLE with calibrated confidence % and live source URLs.")
    ]

    for t_head, t_body in tiers_data:
        p_th = tf_fc.add_paragraph()
        p_th.text = "• " + t_head
        p_th.font.size = Pt(11.5)
        p_th.font.bold = True
        p_th.font.color.rgb = c_teal
        p_th.space_before = Pt(6)

        p_tb = tf_fc.add_paragraph()
        p_tb.text = "    " + t_body
        p_tb.font.size = Pt(10)
        p_tb.font.color.rgb = c_dark
        p_tb.space_before = Pt(1)

    # -------------------------------------------------------------
    # SLIDE 9: PINCODE SURVEILLANCE & EARLY WARNING
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Community Syndromic Surveillance (Early Warning)")
    add_footer(s9)

    tx_s9 = s9.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    tf_s9 = tx_s9.text_frame
    tf_s9.word_wrap = True

    p = tf_s9.paragraphs[0]
    p.text = "Surveillance Mathematical Formulation"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = c_navy

    surv_pts = [
        "• Citizen-Driven Signal Capture: Symptom inquiries tagged with pincodes are logged as anonymized tuples e = (pincode, symptom, lang, ts) in SQLite.",
        "• Rolling 7-Day Baseline Formulation:",
        "    B_{p,s} = (1/7) * SUM_{d=1}^{7} N_{p,s}(t - d)",
        "• Spatio-Temporal Anomaly Threshold:",
        "    If C_{24h} >= 6 and C_{24h} >= 3.0 * B_{p,s} -> [MEDIUM SPIKE ALERT]",
        "    If C_{24h} >= 6 and C_{24h} >= 5.0 * B_{p,s} -> [HIGH SPIKE ALERT]",
        "• Outbreak Mitigation: Detects clusters 10-14 days before clinical hospital registries update.",
        "• Admin Dashboard: Live web dashboard at /admin for municipal Chief Medical Officers (CMOs)."
    ]
    for pt in surv_pts:
        p = tf_s9.add_paragraph()
        p.text = pt
        p.font.size = Pt(10.5)
        p.font.color.rgb = c_dark
        p.space_before = Pt(4)

    if os.path.exists("docs/fig3_surveillance_dashboard.png"):
        s9.shapes.add_picture("docs/fig3_surveillance_dashboard.png", Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.0))

    # -------------------------------------------------------------
    # SLIDE 10: RESULTS & EMPIRICAL BENCHMARKS
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Empirical Results: 100% Fact-Check Success (15/15)")
    add_footer(s10)

    # Left: Summary stats
    tx_s10 = s10.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(4.5), Inches(5.2))
    tf_s10 = tx_s10.text_frame
    tf_s10.word_wrap = True

    p = tf_s10.paragraphs[0]
    p.text = "Evaluation Highlights"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = c_navy

    eval_highlights = [
        "• 15-Claim Comprehensive Suite: Tested live on Oracle VM across 15 distinct health claim typologies.",
        "• 15 / 15 Passed (100% Success Rate):",
        "  - Vaccine autism myth -> MYTH (95%)",
        "  - Toothpaste on burns -> MYTH (95%)",
        "  - Paracetamol Machupo hoax -> MYTH (85%)",
        "  - Ripe papaya pregnancy -> MYTH (95%)",
        "  - Cow urine cancer cure -> MYTH (84%)",
        "  - 5G COVID-19 conspiracy -> MYTH (93%)",
        "  - Female Aedes dengue -> VERIFIED (94%)",
        "  - Polio drops prevent paralysis -> VERIFIED (89%)",
        "  - 10 blue marbles -> UNVERIFIABLE (30%)",
        "• Sub-second Latency: <0.15s for local knowledge base matches; 5–7s for dynamic open-web evidence synthesis."
    ]
    for eh in eval_highlights:
        p = tf_s10.add_paragraph()
        p.text = eh
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_before = Pt(3)

    if os.path.exists("docs/fig4_benchmark_latency.png"):
        s10.shapes.add_picture("docs/fig4_benchmark_latency.png", Inches(5.5), Inches(1.6), Inches(7.0), Inches(4.9))

    # -------------------------------------------------------------
    # SLIDE 11: LIVE DEMO & PRODUCTION DEPLOYMENT
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Live Production Deployment on Oracle Cloud Infrastructure")
    add_footer(s11)

    tx_dep = s11.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    tf_dep = tx_dep.text_frame
    tf_dep.word_wrap = True

    p = tf_dep.paragraphs[0]
    p.text = "Hosting Specs & Production Status"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = c_navy

    dep_points = [
        "• Cloud Server: Oracle Cloud Infrastructure (OCI)",
        "• Compute Specification: 2 vCPU AMD EPYC, 4GB RAM",
        "• Operating System: Ubuntu 24.04 LTS",
        "• Systemd Service: healthbot.service (auto-restart on failure, enabled on system boot)",
        "• Memory Footprint: ~3.05GB aggregate (LaBSE: 1.05GB, Qwen 1.7B Q4: 1.62GB, FastAPI: 0.38GB)",
        "• Live Public Endpoints:",
        "   👉 Web App: http://130.210.56.87:8000/",
        "   👉 Admin Dashboard: http://130.210.56.87:8000/admin",
        "   👉 Interactive API Docs: http://130.210.56.87:8000/docs",
        "• Git Repository: Synced with origin/main on GitHub"
    ]
    for dp in dep_points:
        p = tf_dep.add_paragraph()
        p.text = dp
        p.font.size = Pt(10)
        p.font.color.rgb = c_dark
        p.space_before = Pt(3)

    if os.path.exists("docs/fig2_chat_interface.png"):
        s11.shapes.add_picture("docs/fig2_chat_interface.png", Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.0))

    # -------------------------------------------------------------
    # SLIDE 12: PLANNED WORK AHEAD (ROADMAP)
    # -------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Planned Work Ahead (Phase 4 Roadmap)")
    add_footer(s12)

    roadmap_data = [
        ("Phase 4A: WhatsApp & SMS Integration",
         "• Implement official Meta WhatsApp Cloud API webhooks.\n• Integrate SMS/USSD gateway for basic feature-phone users without internet access in remote hamlets.\n• Enables friction-free access without requiring app downloads.",
         "#EBF5FB", "#2980B9"),
        ("Phase 4B: Vernacular Voice Interface (ASR/TTS)",
         "• Incorporate OpenAI Whisper and AI4Bharat / Bhashini speech models.\n• Voice Activity Detection (VAD) for bidirectional spoken interaction in rural dialects.\n• Empowers non-literate and elderly rural populations.",
         "#FEF9E7", "#D4AC0D"),
        ("Phase 4C: Clinical Field Validation & IDSP Sync",
         "• Conduct pilot field trials in collaboration with rural Primary Health Centres (PHCs).\n• Evaluate patient comprehension and usability metrics across ASHAs (community health workers).\n• Establish automated anonymized data pipeline feeding into district IDSP dashboards.",
         "#E8F8F5", "#16A085")
    ]

    for idx, (head, body, bg_col, bdr_col) in enumerate(roadmap_data):
        x = Inches(0.8 + idx * 3.95)
        card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.6), Inches(3.8), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor.from_string(bg_col.replace("#", ""))
        card.line.color.rgb = RGBColor.from_string(bdr_col.replace("#", ""))
        card.line.width = Pt(1.5)

        tx = s12.shapes.add_textbox(x + Inches(0.15), Inches(1.75), Inches(3.5), Inches(4.8))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = head
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = RGBColor.from_string(bdr_col.replace("#", ""))
        
        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = c_dark
        p2.space_before = Pt(12)

    # -------------------------------------------------------------
    # SLIDE 13: CONCLUSION & SUMMARY
    # -------------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Conclusion & Project Summary")
    add_footer(s13)

    box_concl = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1))
    box_concl.fill.solid()
    box_concl.fill.fore_color.rgb = c_card_bg
    box_concl.line.color.rgb = c_navy
    box_concl.line.width = Pt(1.5)

    tx_c = s13.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(11.133), Inches(4.6))
    tf_c = tx_c.text_frame
    tf_c.word_wrap = True

    p = tf_c.paragraphs[0]
    p.text = "Key Deliverables Accomplished in Minor Project:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_navy

    concl_pts = [
        "1. Complete Working System: End-to-end operational public health chatbot successfully deployed on Oracle Cloud Infrastructure.",
        "2. Deterministic Safety Guards: Sub-10ms red-flag emergency escalation to 108/112 ambulance services with zero LLM hallucination risk.",
        "3. Cross-Lingual Metric Retrieval: Google LaBSE embedding alignment enabling seamless English, Hindi, and colloquial Hinglish interaction.",
        "4. Autonomous Fact-Checking Engine: 100% verification success rate (15/15 test claims passed) operating with zero external API keys and $0 cost.",
        "5. Community Syndromic Surveillance: Real-time 7-day rolling baseline anomaly detector with geocoded pincode resolution and live CMO dashboard.",
        "6. Academic Research Paper Draft: 11-page manuscript prepared in IEEE format complete with mathematical formulations, benchmarks, and citations."
    ]
    for cpt in concl_pts:
        p = tf_c.add_paragraph()
        p.text = cpt
        p.font.size = Pt(11.5)
        p.font.color.rgb = c_dark
        p.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 14: THANK YOU & Q&A
    # -------------------------------------------------------------
    s14 = prs.slides.add_slide(blank_layout)
    bg14 = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg14.fill.solid()
    bg14.fill.fore_color.rgb = c_navy
    bg14.line.fill.background()

    tx14 = s14.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(4.5))
    tf14 = tx14.text_frame
    tf14.word_wrap = True

    p = tf14.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "Thank You!"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = c_white

    p = tf14.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.text = "Questions & Discussion"
    p.font.size = Pt(22)
    p.font.color.rgb = c_teal
    p.space_before = Pt(8)

    p = tf14.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.text = "AarogyaSathi — AI-Driven Public Health Chatbot for Disease Awareness\nSalman Mohammad Khan (00520815723)  |  Dhairya Summi (00420815723)  |  Siddharth Singh (01820815723)\nDepartment of Computer Science & Engineering (Data Science)\n\nLive Demo: http://130.210.56.87:8000/  |  Admin Dashboard: http://130.210.56.87:8000/admin"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(180, 200, 220)
    p.space_before = Pt(24)

    output_pptx = "docs/AarogyaSathi_1st_Defense_Presentation.pptx"
    prs.save(output_pptx)
    print(f"Presentation PPTX saved to: {output_pptx}")

if __name__ == "__main__":
    build_presentation()
