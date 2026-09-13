import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

def build_presentation():
    prs = Presentation()
    # 16:9 Widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Palette
    c_navy = RGBColor(15, 32, 67)
    c_teal = RGBColor(22, 160, 133)
    c_cyan = RGBColor(0, 180, 216)
    c_white = RGBColor(255, 255, 255)
    c_dark = RGBColor(33, 47, 61)
    c_gray = RGBColor(110, 120, 130)
    c_card_bg = RGBColor(245, 248, 252)
    c_card_border = RGBColor(180, 210, 235)
    c_gold = RGBColor(212, 172, 13)
    c_red = RGBColor(231, 76, 60)

    def add_fitted_image(slide, img_path, left_in, top_in, max_w_in, max_h_in, center=True):
        """Preserves exact native aspect ratio without stretching or distortion."""
        if not os.path.exists(img_path):
            return None
        with Image.open(img_path) as img:
            img_w, img_h = img.size
        aspect = img_w / img_h
        box_aspect = max_w_in / max_h_in

        if aspect > box_aspect:
            # Constrain by width
            w = max_w_in
            h = max_w_in / aspect
        else:
            # Constrain by height
            h = max_h_in
            w = max_h_in * aspect

        if center:
            l = left_in + (max_w_in - w) / 2.0
            t = top_in + (max_h_in - h) / 2.0
        else:
            l = left_in
            t = top_in

        return slide.shapes.add_picture(img_path, Inches(l), Inches(t), Inches(w), Inches(h))

    def add_header(slide, title_text, category_text="MINOR PROJECT 1ST DEFENSE | ES-451"):
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = c_navy
        top_bar.line.fill.background()

        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.15), Inches(13.333), Inches(0.06))
        accent.fill.solid()
        accent.fill.fore_color.rgb = c_teal
        accent.line.fill.background()

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
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(215, 220, 225)
        line.line.fill.background()

        tx = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
        tf = tx.text_frame
        p = tf.paragraphs[0]
        p.text = "AarogyaSathi: Bilingual Healthcare Guidance & Autonomous Fact-Checking | Department of CSE (Data Science)"
        p.font.size = Pt(9)
        p.font.color.rgb = c_gray

    # =============================================================
    # SLIDE 1: TITLE SLIDE (WITH CUSTOM EMBLEM & CREDENTIALS)
    # =============================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = c_navy
    bg1.line.fill.background()

    # Left Column: Title & Metadata
    tx1 = s1.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(7.8), Inches(6.0))
    tf1 = tx1.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "MINOR PROJECT (ES-451) — 1ST DEFENSE EVALUATION"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = c_gold

    p_main = tf1.add_paragraph()
    p_main.text = "AarogyaSathi"
    p_main.font.size = Pt(40)
    p_main.font.bold = True
    p_main.font.color.rgb = c_white
    p_main.space_before = Pt(6)

    p_sub = tf1.add_paragraph()
    p_sub.text = "A Bilingual Healthcare Guidance & Autonomous Multi-Tier Fact-Checking Conversational Agent with Geospatial Syndromic Surveillance"
    p_sub.font.size = Pt(14.5)
    p_sub.font.color.rgb = RGBColor(190, 215, 240)
    p_sub.space_before = Pt(6)

    # Cloud Live status badge
    p_live = tf1.add_paragraph()
    p_live.text = "● LIVE SYSTEM DEPLOYED ON ORACLE CLOUD INFRASTRUCTURE (OCI)"
    p_live.font.size = Pt(10.5)
    p_live.font.bold = True
    p_live.font.color.rgb = RGBColor(46, 204, 113)
    p_live.space_before = Pt(12)

    p_team_h = tf1.add_paragraph()
    p_team_h.text = "PROJECT TEAM MEMBERS:"
    p_team_h.font.size = Pt(11)
    p_team_h.font.bold = True
    p_team_h.font.color.rgb = c_teal
    p_team_h.space_before = Pt(16)

    p_team = tf1.add_paragraph()
    p_team.text = "• Salman Mohammad Khan  (Enrollment: 00520815723)\n• Dhairya Summi                  (Enrollment: 00420815723)\n• Siddharth Singh                (Enrollment: 01820815723)"
    p_team.font.size = Pt(12.5)
    p_team.font.color.rgb = c_white
    p_team.space_before = Pt(4)

    p_dept = tf1.add_paragraph()
    p_dept.text = "Department of Computer Science & Engineering (Data Science)\nBachelor of Technology (B.Tech) | Evaluation Date: September 14, 2026"
    p_dept.font.size = Pt(10.5)
    p_dept.font.italic = True
    p_dept.font.color.rgb = RGBColor(160, 180, 200)
    p_dept.space_before = Pt(14)

    # Right Column: Hero Graphic Emblem
    add_fitted_image(s1, "docs/ppt_assets/hero_emblem.png", 8.8, 1.2, 3.8, 3.8)

    # Pill badge below emblem
    badge_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(5.2), Inches(3.8), Inches(1.2))
    badge_box.fill.solid()
    badge_box.fill.fore_color.rgb = RGBColor(20, 45, 90)
    badge_box.line.color.rgb = c_teal
    badge_box.line.width = Pt(1.5)

    tx_b = s1.shapes.add_textbox(Inches(8.9), Inches(5.3), Inches(3.6), Inches(1.0))
    tf_b = tx_b.text_frame
    tf_b.word_wrap = True
    p = tf_b.paragraphs[0]
    p.text = "CORE ENGINEERING HIGHLIGHTS"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = c_gold
    p = tf_b.add_paragraph()
    p.text = "✓ Dual-Model Local Edge Stack (Qwen + LaBSE)\n✓ 100% Free: $0 API Billing, Zero API Keys\n✓ Real-Time 7-Day Rolling Outbreak Anomaly Math"
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_white
    p.space_before = Pt(4)

    # =============================================================
    # SLIDE 2: BACKGROUND & MOTIVATION (WITH 3-PART INFOGRAPHIC)
    # =============================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Background & Problem Motivation: The Rural Infodemic Crisis")
    add_footer(s2)

    # Top: Visual Infographic
    add_fitted_image(s2, "docs/ppt_assets/motivation_infographic.png", 0.8, 1.4, 11.733, 2.7)

    # Bottom: 3 Matching Analytical Cards
    cards_data = [
        ("1. Severe Clinical Deficit", 
         "• 1:1456 Doctor-to-citizen ratio in India vs 1:1000 WHO benchmark.\n• 70%+ rural population depends on unverified informal conduits.\n• Critical need for instant, culturally aligned preventive triage.",
         "#FDEDEC", "#C0392B"),
        ("2. Lethal Social Infodemic", 
         "• WhatsApp/Telegram rumors cause pediatric vaccine hesitancy.\n• Dangerous first-aid (chilli on dog bites, cutting snakebites) causes catastrophic necrosis.\n• General LLMs hallucinate pharmacology.",
         "#FEF9E7", "#D4AC0D"),
        ("3. 14-21 Day Surveillance Lag", 
         "• Centralized IDSP relies on physical laboratory registries.\n• Outbreaks peak before municipal health authorities are notified.\n• Zero real-time localized syndromic signal capture.",
         "#E8F8F5", "#16A085")
    ]

    for idx, (head, body, bg_col, bdr_col) in enumerate(cards_data):
        x = 0.8 + idx * 3.95
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(4.3), Inches(3.8), Inches(2.55))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor.from_string(bg_col.replace("#", ""))
        card.line.color.rgb = RGBColor.from_string(bdr_col.replace("#", ""))
        card.line.width = Pt(1.5)

        tx = s2.shapes.add_textbox(Inches(x + 0.15), Inches(4.35), Inches(3.5), Inches(2.45))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = head
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = RGBColor.from_string(bdr_col.replace("#", ""))
        
        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = c_dark
        p2.space_before = Pt(6)

    # =============================================================
    # SLIDE 3: PROBLEM STATEMENT & CORE OBJECTIVES
    # =============================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Problem Statement & Project Objectives")
    add_footer(s3)

    # Top: Problem Statement Hero Box
    box_ps = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(1.6))
    box_ps.fill.solid()
    box_ps.fill.fore_color.rgb = c_card_bg
    box_ps.line.color.rgb = c_navy
    box_ps.line.width = Pt(1.8)

    tx_ps = s3.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(11.333), Inches(1.5))
    tf_ps = tx_ps.text_frame
    tf_ps.word_wrap = True
    p = tf_ps.paragraphs[0]
    p.text = "FORMAL PROBLEM STATEMENT"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p = tf_ps.add_paragraph()
    p.text = "\"To design, develop, and deploy an autonomous, zero-cost, multilingual public health conversational agent that delivers verified preventive healthcare education, deterministic emergency triage escalation, autonomous rumor fact-checking without third-party API dependencies, and proactive community syndromic surveillance across rural and semi-urban Indian populations.\""
    p.font.size = Pt(11)
    p.font.color.rgb = c_dark
    p.font.italic = True
    p.space_before = Pt(4)

    # Bottom: 4 Objective Pillar Cards
    pillars = [
        ("1. Bilingual Grounding", "Google LaBSE mapping English, Hindi, and colloquial Hinglish into a shared 768-dim metric space.", "#EBF5FB", "#2980B9"),
        ("2. Deterministic Safety", "Sub-10ms bypass routing acute emergencies (chest pain, snakebites) directly to 108/112 ambulance.", "#FDEDEC", "#C0392B"),
        ("3. Autonomous Fact-Check", "4-Tier verification engine combining local semantic FAISS + open-web news consensus at $0 cost.", "#FEF9E7", "#D4AC0D"),
        ("4. Syndromic Surveillance", "Pincode-level outbreak anomaly detection using 7-day rolling baselines (Delta >= 2.0x, N >= 3).", "#E8F8F5", "#16A085")
    ]

    for idx, (p_title, p_desc, bg_col, bdr_col) in enumerate(pillars):
        x = 0.8 + idx * 2.98
        box_p = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(3.2), Inches(2.82), Inches(3.6))
        box_p.fill.solid()
        box_p.fill.fore_color.rgb = RGBColor.from_string(bg_col.replace("#", ""))
        box_p.line.color.rgb = RGBColor.from_string(bdr_col.replace("#", ""))
        box_p.line.width = Pt(1.5)

        tx = s3.shapes.add_textbox(Inches(x + 0.12), Inches(3.3), Inches(2.58), Inches(3.4))
        tf = tx.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = p_title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = RGBColor.from_string(bdr_col.replace("#", ""))
        p = tf.add_paragraph()
        p.text = p_desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = c_dark
        p.space_before = Pt(8)

    # =============================================================
    # SLIDE 4: LITERATURE SURVEY & GAP ANALYSIS
    # =============================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Literature Survey & Critical Gap Analysis")
    add_footer(s4)

    lit_data = [
        ("Prior System / Study", "Core Methodology", "Critical Vulnerabilities / Gaps", "AarogyaSathi Innovation"),
        ("Ada Health / Babylon Health (2020)", "Proprietary Bayesian nets & clinical decision trees", "Closed-source, high licensing cost, no Hinglish/Indic support, legal liability in self-diagnosis", "Open-source, non-diagnostic awareness framing, native Hindi/Hinglish NLP"),
        ("CoWIN / Aarogya Setu (2021)", "Centralized transactional databases (Bluetooth, OTP)", "Static registries without interactive symptom exploration, triage, or myth-busting capabilities", "Multi-turn empathetic symptom clarification & autonomous fact-checking"),
        ("Google Fact Check API (2022)", "ClaimReview structured JSON schema aggregation", "Index sparsity for village health rumors; commercial billing/card restrictions in Global South", "Autonomous multi-tier engine: local semantic corpus + live open-web/news synthesis ($0 cost)"),
        ("Google Flu Trends (GFT) (2015)", "Correlating aggregated search engine keywords", "Prone to panic-induced search spikes; lacks clinical symptom parsing or geocoded triage", "Pincode-level geocoded symptom event logging with rolling 7-day baseline anomaly regression")
    ]

    t = s4.shapes.add_table(5, 4, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3)).table
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
                cell.fill.fore_color.rgb = RGBColor(245, 248, 252) if r_idx % 2 == 0 else c_white

    # =============================================================
    # SLIDE 5: SYSTEM ARCHITECTURE (PRESERVED NATURAL ASPECT RATIO)
    # =============================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "End-to-End System Architecture & Dataflow")
    add_footer(s5)

    # Left: Architecture Diagram with exact native aspect ratio
    add_fitted_image(s5, "docs/fig1_architecture.png", 0.8, 1.35, 8.4, 5.4, center=True)

    # Right: Key Architectural Highlights
    box_arch = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.4), Inches(1.35), Inches(3.133), Inches(5.4))
    box_arch.fill.solid()
    box_arch.fill.fore_color.rgb = c_card_bg
    box_arch.line.color.rgb = c_navy
    box_arch.line.width = Pt(1.5)

    tx_ar = s5.shapes.add_textbox(Inches(9.55), Inches(1.45), Inches(2.833), Inches(5.2))
    tf_ar = tx_ar.text_frame
    tf_ar.word_wrap = True
    p = tf_ar.paragraphs[0]
    p.text = "PIPELINE HIGHLIGHTS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_navy

    ar_pts = [
        ("Deterministic Safety", "Sub-10ms regex red-flag interceptor directly dials 108/112 ambulance services."),
        ("Dual-Model Stack", "Qwen3-1.7B (4-bit quantized SLM) + Google LaBSE on local VM."),
        ("Zero Hallucination", "Strict RAG grounding in WHO, MoHFW, and ICMR repositories with negative constraints."),
        ("Real-Time Surveillance", "Anonymized symptom events stream into rolling 7-day anomaly detector by postal code.")
    ]
    for h, b in ar_pts:
        p = tf_ar.add_paragraph()
        p.text = "• " + h
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = c_teal
        p.space_before = Pt(8)
        p = tf_ar.add_paragraph()
        p.text = b
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_before = Pt(2)

    # =============================================================
    # SLIDE 6: CORE METHODOLOGY: BILINGUAL NLP & LABSE CONVERGENCE
    # =============================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Core Methodology: Cross-Lingual Semantic Retrieval")
    add_footer(s6)

    # Top: Visual LaBSE Convergence Graphic
    add_fitted_image(s6, "docs/ppt_assets/labse_concept.png", 0.8, 1.35, 11.733, 2.7)

    # Bottom: 2 In-Depth Cards
    tx_a = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.2), Inches(5.7), Inches(2.65))
    tx_a.fill.solid()
    tx_a.fill.fore_color.rgb = RGBColor(245, 248, 252)
    tx_a.line.color.rgb = c_navy
    tx_a.line.width = Pt(1.5)

    tx_at = s6.shapes.add_textbox(Inches(0.95), Inches(4.25), Inches(5.4), Inches(2.55))
    tf_at = tx_at.text_frame
    tf_at.word_wrap = True
    p = tf_at.paragraphs[0]
    p.text = "1. Language ID & Intent Classifier"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p = tf_at.add_paragraph()
    p.text = "• fastText (lid.176) hierarchically detects 176 languages + code-mixed Hinglish.\n• TF-IDF feature extraction (unigram/bigram) + L2 Logistic Regression.\n• 13 Intent Classes: emergency, fact_check, disease_info, vaccination, etc.\n• Macro F1 = 0.942 with 1.000 precision on safety-critical red-flag emergency detection."
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_dark
    p.space_before = Pt(4)

    tx_b = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.2), Inches(5.733), Inches(2.65))
    tx_b.fill.solid()
    tx_b.fill.fore_color.rgb = RGBColor(232, 248, 245)
    tx_b.line.color.rgb = c_teal
    tx_b.line.width = Pt(1.5)

    tx_bt = s6.shapes.add_textbox(Inches(6.95), Inches(4.25), Inches(5.4), Inches(2.55))
    tf_bt = tx_bt.text_frame
    tf_bt.word_wrap = True
    p = tf_bt.paragraphs[0]
    p.text = "2. Mathematical Formulation (LaBSE Metric)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_teal
    p = tf_bt.add_paragraph()
    p.text = "• Dense Mean-Pooling & L2 Normalization into 768-dimensional Hilbert space:\n    vq = MeanPool(LaBSE(q)) / ||MeanPool(LaBSE(q))||2\n• Cosine Similarity over Pre-Indexed Knowledge Base:\n    S(q, ci) = vq · vci = SUM_{k=1}^{768} (vq,k * vci,k)\n• Sub-second lookup: <0.10s via pre-computed memory-mapped NumPy arrays."
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_dark
    p.space_before = Pt(4)

    # =============================================================
    # SLIDE 7: GROUNDED RAG & SMALL LANGUAGE MODELS
    # =============================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Retrieval-Augmented Generation & Edge SLM Reasoning")
    add_footer(s7)

    rag_steps = [
        ("Step 1: Curated Knowledge Retrieval",
         "• Strict factual grounding in Tier-1 repositories: WHO, MoHFW, ICMR, NHM.\n• 14 Comprehensive Disease Profiles (Dengue, Malaria, TB, Rabies...).\n• National Immunization Schedule (UIP) from birth to pregnancy.\n• Negative retrieval filter guarantees zero clinical hallucination.",
         "#EBF5FB", "#2980B9"),
        ("Step 2: Edge-Quantized SLM (Qwen3-1.7B)",
         "• Runs locally via Ollama with 4-bit quantization (Q4_K_M GGUF).\n• Memory footprint: only 1.6GB RAM/VRAM — runs smoothly on 4GB instances.\n• High-speed generation without sending citizen data to external third-party servers.\n• Automatic circuit breaker fallback to template answers if Ollama is unreachable.",
         "#FEF9E7", "#D4AC0D"),
        ("Step 3: Negative Prompt Constraints",
         "• Enforces strict negative operational boundaries:\n  1. Answer strictly and only from retrieved context.\n  2. Hard constraint: response must be concise (<70 words).\n  3. Never prescribe medicines or deliver clinical diagnosis.\n  4. Append validated WHO/MoHFW source citation and medical disclaimer.",
         "#E8F8F5", "#16A085")
    ]

    for idx, (head, body, bg_col, bdr_col) in enumerate(rag_steps):
        x = 0.8 + idx * 3.95
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.4), Inches(3.8), Inches(5.3))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor.from_string(bg_col.replace("#", ""))
        card.line.color.rgb = RGBColor.from_string(bdr_col.replace("#", ""))
        card.line.width = Pt(1.5)

        tx = s7.shapes.add_textbox(Inches(x + 0.15), Inches(1.55), Inches(3.5), Inches(5.0))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = head
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = RGBColor.from_string(bdr_col.replace("#", ""))
        
        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(10)
        p2.font.color.rgb = c_dark
        p2.space_before = Pt(10)

    # =============================================================
    # SLIDE 8: AUTONOMOUS FACT-CHECKING ENGINE FLOWCHART ($0 COST)
    # =============================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Autonomous Multi-Tier Fact-Checking Engine ($0 Cost)")
    add_footer(s8)

    # Top: Visual 4-Tier Flowchart
    add_fitted_image(s8, "docs/ppt_assets/factcheck_flowchart.png", 0.8, 1.35, 11.733, 2.7)

    # Bottom: 2 Comparative Analytical Boxes
    tx_w = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.2), Inches(5.7), Inches(2.65))
    tx_w.fill.solid()
    tx_w.fill.fore_color.rgb = RGBColor(253, 237, 236)
    tx_w.line.color.rgb = c_red
    tx_w.line.width = Pt(1.5)

    tx_wt = s8.shapes.add_textbox(Inches(0.95), Inches(4.25), Inches(5.4), Inches(2.55))
    tf_wt = tx_wt.text_frame
    tf_wt.word_wrap = True
    p = tf_wt.paragraphs[0]
    p.text = "Why Google Fact Check API Failed Our Needs"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_red
    p = tf_wt.add_paragraph()
    p.text = "• Google's API mandates linked Cloud Billing Accounts (which fail across Indian developers due to RBI e-mandate credit card regulations).\n• High index sparsity: Returns 404/Empty on regional Indian rumors.\n• High network latency and strict rate-limiting quotas."
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_dark
    p.space_before = Pt(6)

    tx_o = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.2), Inches(5.733), Inches(2.65))
    tx_o.fill.solid()
    tx_o.fill.fore_color.rgb = RGBColor(232, 248, 245)
    tx_o.line.color.rgb = c_teal
    tx_o.line.width = Pt(1.5)

    tx_ot = s8.shapes.add_textbox(Inches(6.95), Inches(4.25), Inches(5.4), Inches(2.55))
    tf_ot = tx_ot.text_frame
    tf_ot.word_wrap = True
    p = tf_ot.paragraphs[0]
    p.text = "Our Autonomous Multi-Tier Advantage ($0 Cost)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_teal
    p = tf_ot.add_paragraph()
    p.text = "• 100% Autonomous: ZERO external API keys, $0 monthly cloud billing.\n• Sub-second local response (<0.15s) for vetted clinical claims.\n• Real-time open web consensus harvesting (DuckDuckGo + PubMed/WHO/MoHFW) for newly emerging viral rumors.\n• Structured verdict badging with calibrated confidence scores."
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_dark
    p.space_before = Pt(6)

    # =============================================================
    # SLIDE 9: SYNDROMIC SURVEILLANCE & OUTBREAK ANOMALY DETECTION
    # =============================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Community Syndromic Surveillance (Outbreak Early Warning)")
    add_footer(s9)

    # Left: Outbreak Math & Detection Curve
    add_fitted_image(s9, "docs/ppt_assets/surveillance_chart.png", 0.8, 1.4, 5.6, 5.3)

    # Right: Live Admin Dashboard Screenshot (Preserved aspect ratio)
    add_fitted_image(s9, "docs/fig3_surveillance_dashboard.png", 6.8, 1.4, 5.733, 5.3)

    # =============================================================
    # SLIDE 10: RESULTS & EMPIRICAL BENCHMARKS (15/15 PASSED)
    # =============================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Empirical Results: 100% Fact-Check Success Rate (15/15)")
    add_footer(s10)

    # Top: Scorecard KPI Graphic
    add_fitted_image(s10, "docs/ppt_assets/results_scorecard.png", 0.8, 1.35, 11.733, 2.3)

    # Bottom Left: Test Breakdown Table / Text
    tx_bl = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.8), Inches(5.6), Inches(3.0))
    tx_bl.fill.solid()
    tx_bl.fill.fore_color.rgb = c_card_bg
    tx_bl.line.color.rgb = c_navy
    tx_bl.line.width = Pt(1.5)

    tx_blt = s10.shapes.add_textbox(Inches(0.95), Inches(3.85), Inches(5.3), Inches(2.9))
    tf_blt = tx_blt.text_frame
    tf_blt.word_wrap = True
    p = tf_blt.paragraphs[0]
    p.text = "15/15 Claim Typology Highlights"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p = tf_blt.add_paragraph()
    p.text = "• Vaccine autism myth -> [MYTH] (95% confidence)\n• Toothpaste on burns -> [MYTH] (95% confidence)\n• Paracetamol Machupo hoax -> [MYTH] (85% confidence)\n• Ripe papaya causes abortion -> [MYTH] (95% confidence)\n• Female Aedes aegypti causes dengue -> [VERIFIED] (94%)\n• Polio drops prevent paralysis -> [VERIFIED] (89%)\n• 10 blue marbles cure cancer -> [UNVERIFIABLE] (30%)"
    p.font.size = Pt(9)
    p.font.color.rgb = c_dark
    p.space_before = Pt(4)

    # Bottom Right: Empirical Latency Chart (Preserved natural aspect ratio)
    add_fitted_image(s10, "docs/fig4_benchmark_latency.png", 6.6, 3.8, 5.933, 3.0)

    # =============================================================
    # SLIDE 11: LIVE PRODUCTION DEPLOYMENT & CHAT UI
    # =============================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Live Production Deployment on Oracle Cloud Infrastructure")
    add_footer(s11)

    # Left: Infrastructure Specifications
    tx_dep = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.3))
    tx_dep.fill.solid()
    tx_dep.fill.fore_color.rgb = c_card_bg
    tx_dep.line.color.rgb = c_navy
    tx_dep.line.width = Pt(1.5)

    tx_dept = s11.shapes.add_textbox(Inches(0.95), Inches(1.5), Inches(5.3), Inches(5.1))
    tf_dept = tx_dept.text_frame
    tf_dept.word_wrap = True
    p = tf_dept.paragraphs[0]
    p.text = "Cloud Infrastructure & Production Status"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_navy

    dep_points = [
        ("Cloud Provider", "Oracle Cloud Infrastructure (OCI) Always-Free Tier"),
        ("Server Specs", "2 vCPU AMD EPYC, 4GB RAM, Ubuntu 24.04 LTS"),
        ("Systemd Daemon", "healthbot.service (Auto-restart, active systemd service)"),
        ("RAM Footprint", "3.05GB aggregate (LaBSE: 1.05GB, Qwen 1.7B: 1.62GB, FastAPI: 0.38GB)"),
        ("Live Web App", "http://130.210.56.87:8000/"),
        ("Admin Portal", "http://130.210.56.87:8000/admin"),
        ("Interactive Docs", "http://130.210.56.87:8000/docs"),
        ("Version Control", "Synced with GitHub (salman-mohammad-khan/AarogyaSathi)")
    ]
    for h, b in dep_points:
        p = tf_dept.add_paragraph()
        p.text = f"• {h}: {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_before = Pt(4)

    # Right: Live Chat UI Screenshot (Preserved aspect ratio)
    add_fitted_image(s11, "docs/fig2_chat_interface.png", 6.8, 1.4, 5.733, 5.3)

    # =============================================================
    # SLIDE 12: CLINICAL SAFETY, ETHICS & GUARDRAILS
    # =============================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Clinical Safety, Ethics & Non-Diagnostic Guardrails")
    add_footer(s12)

    safety_cards = [
        ("1. Deterministic Triage Guard", 
         "• Sub-10ms regex interceptor detects life-threatening keywords.\n• Red-flag symptoms (severe chest pain, snakebite, sudden hemiplegia) bypass AI.\n• Immediately displays prominent 108/112 ambulance dispatch card with one-click dial.",
         "#FDEDEC", "#C0392B"),
        ("2. Strict Non-Diagnostic Framing", 
         "• System prompt explicitly forbids issuing clinical diagnoses or prescribing specific pharmaceutical dosages.\n• Injects statutory ICMR disclaimer on every turn.\n• Clarifies educational/awareness purpose only.",
         "#FEF9E7", "#D4AC0D"),
        ("3. Privacy by Design (Zero PII)", 
         "• Syndromic event logger captures anonymized tuples: (pincode, symptom_category, timestamp).\n• No phone numbers, citizen names, or IP addresses stored.\n• Fully compliant with India Digital Personal Data Protection Act (DPDP).",
         "#E8F8F5", "#16A085")
    ]

    for idx, (head, body, bg_col, bdr_col) in enumerate(safety_cards):
        x = 0.8 + idx * 3.95
        card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.4), Inches(3.8), Inches(5.3))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor.from_string(bg_col.replace("#", ""))
        card.line.color.rgb = RGBColor.from_string(bdr_col.replace("#", ""))
        card.line.width = Pt(1.5)

        tx = s12.shapes.add_textbox(Inches(x + 0.15), Inches(1.55), Inches(3.5), Inches(5.0))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = head
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = RGBColor.from_string(bdr_col.replace("#", ""))
        
        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = c_dark
        p2.space_before = Pt(12)

    # =============================================================
    # SLIDE 13: PLANNED WORK AHEAD (ROADMAP)
    # =============================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Planned Work Ahead (Phase 4 Roadmap & Execution)")
    add_footer(s13)

    # Top: Visual Roadmap Timeline
    add_fitted_image(s13, "docs/ppt_assets/roadmap_visual.png", 0.8, 1.35, 11.733, 2.4)

    # Bottom: 3 Milestone Deep-Dive Cards
    roadmap_deep = [
        ("Phase 4A: WhatsApp & SMS Integration",
         "• Implement official Meta WhatsApp Cloud API webhooks.\n• Integrate SMS/USSD gateway for basic feature-phone users in remote hamlets.\n• Eliminates smartphone/app download barriers.",
         "#EBF5FB", "#2980B9"),
        ("Phase 4B: Vernacular Voice AI (ASR/TTS)",
         "• Incorporate Whisper and AI4Bharat / Bhashini speech models.\n• Voice Activity Detection (VAD) for bidirectional spoken interaction in rural dialects.\n• Empowers non-literate and elderly populations.",
         "#FEF9E7", "#D4AC0D"),
        ("Phase 4C: Clinical Pilot & IDSP Sync",
         "• Conduct pilot field trials across rural Primary Health Centres (PHCs).\n• Evaluate usability metrics with ASHAs (community health workers).\n• Automated two-way API pipeline feeding into district IDSP dashboards.",
         "#E8F8F5", "#16A085")
    ]

    for idx, (head, body, bg_col, bdr_col) in enumerate(roadmap_deep):
        x = 0.8 + idx * 3.95
        card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(3.9), Inches(3.8), Inches(2.95))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor.from_string(bg_col.replace("#", ""))
        card.line.color.rgb = RGBColor.from_string(bdr_col.replace("#", ""))
        card.line.width = Pt(1.5)

        tx = s13.shapes.add_textbox(Inches(x + 0.15), Inches(4.0), Inches(3.5), Inches(2.75))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = head
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = RGBColor.from_string(bdr_col.replace("#", ""))
        
        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = c_dark
        p2.space_before = Pt(8)

    # =============================================================
    # SLIDE 14: CONCLUSION & Q&A
    # =============================================================
    s14 = prs.slides.add_slide(blank_layout)
    bg14 = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg14.fill.solid()
    bg14.fill.fore_color.rgb = c_navy
    bg14.line.fill.background()

    # Left: Accomplishments Summary
    box_c = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.0), Inches(6.8), Inches(5.8))
    box_c.fill.solid()
    box_c.fill.fore_color.rgb = RGBColor(20, 45, 90)
    box_c.line.color.rgb = c_teal
    box_c.line.width = Pt(1.5)

    tx_c = s14.shapes.add_textbox(Inches(1.0), Inches(1.15), Inches(6.4), Inches(5.5))
    tf_c = tx_c.text_frame
    tf_c.word_wrap = True

    p = tf_c.paragraphs[0]
    p.text = "Key Deliverables Accomplished (Minor Project):"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = c_gold

    concl_pts = [
        "1. Complete Working System: Live on Oracle Cloud with auto-restart daemon.",
        "2. Deterministic Safety Guards: Sub-10ms triage escalation to 108/112 ambulance.",
        "3. Cross-Lingual Metric Retrieval: Google LaBSE alignment across English, Hindi & Hinglish.",
        "4. Autonomous Fact-Checking: 100% verification success rate (15/15 passed) at $0 cost.",
        "5. Community Syndromic Surveillance: Real-time 7-day rolling anomaly detector by postal code.",
        "6. Academic Research Paper Draft: 11-page manuscript prepared in IEEE format."
    ]
    for cpt in concl_pts:
        p = tf_c.add_paragraph()
        p.text = cpt
        p.font.size = Pt(10.5)
        p.font.color.rgb = c_white
        p.space_before = Pt(6)

    # Right: Thank You & Contact
    tx14 = s14.shapes.add_textbox(Inches(8.0), Inches(1.5), Inches(4.5), Inches(5.0))
    tf14 = tx14.text_frame
    tf14.word_wrap = True

    p = tf14.paragraphs[0]
    p.text = "Thank You!"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = c_white

    p = tf14.add_paragraph()
    p.text = "Questions & Discussion"
    p.font.size = Pt(20)
    p.font.color.rgb = c_teal
    p.space_before = Pt(6)

    p = tf14.add_paragraph()
    p.text = "AarogyaSathi: Bilingual Healthcare Guidance\n\n• Salman Mohammad Khan (00520815723)\n• Dhairya Summi (00420815723)\n• Siddharth Singh (01820815723)\n\nDepartment of Computer Science & Engineering (Data Science)\n\nLive Demo: http://130.210.56.87:8000/\nAdmin Portal: http://130.210.56.87:8000/admin"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(190, 215, 240)
    p.space_before = Pt(16)

    output_pptx = "docs/AarogyaSathi_1st_Defense_Presentation.pptx"
    prs.save(output_pptx)
    print(f"Presentation PPTX successfully compiled and saved to: {output_pptx}")

if __name__ == "__main__":
    build_presentation()
