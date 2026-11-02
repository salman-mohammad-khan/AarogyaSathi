"""
AarogyaSathi — Comprehensive Master Defense Revision Guide PDF
Specially curated for Minor Project 1st Defense (ES-451, CSE Data Science, BPIT)
Team: Salman Mohammad Khan (00520815723) | Dhairya Summi (00420815723) | Siddharth Singh (01820815723)

Key Upgrades Applied:
  1. All table cells wrapped in Paragraph() objects with wordWrap="CJK" -> ZERO text overflow / word overlap.
  2. Nirmala.ttc registered for Devanagari and Indian scripts.
  3. Autonomous 4-Tier Zero-Cost Fact-Checking Engine fully documented (replaces Google API).
  4. Real-time Syndromic Surveillance mathematical anomaly formulation (Delta >= 2.0x, N >= 3).
  5. Comprehensive ML & NLP Concept Dictionary with plain-English definitions (no Google search needed).
  6. Direct cross-references to PPT Slide numbers and Research Paper sections throughout.
  7. Honest system shortcomings and mature technical defenses included.
  8. Updated Phase 4 Roadmap: WhatsApp Webhooks + WhatsApp Voice Notes (.ogg) + Model Optimization / Quantization.
  9. Step-by-step live demo script and Top 12 panel viva questions & textbook answers.
"""
import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

OUTPUT_DOCS = r"docs\AarogyaSathi_Defense_Revision_Master_Guide.pdf"
OUTPUT_DOWNLOADS = r"C:\Users\gamer\Downloads\AarogyaSathi_Revision_Material.pdf"

# ── Register Unicode / Devanagari font ───────────────────────────────────────
NIRMALA = r"C:\Windows\Fonts\Nirmala.ttc"
if os.path.exists(NIRMALA):
    pdfmetrics.registerFont(TTFont("Nirmala",     NIRMALA, subfontIndex=0))
    pdfmetrics.registerFont(TTFont("NirmalaBold", NIRMALA, subfontIndex=1))
    pdfmetrics.registerFont(TTFont("NirmalaSemi", NIRMALA, subfontIndex=2))
    pdfmetrics.registerFontFamily(
        "Nirmala", normal="Nirmala", bold="NirmalaBold",
        italic="NirmalaSemi", boldItalic="NirmalaBold"
    )
    UNI_FONT = "Nirmala"
    UNI_BOLD = "NirmalaBold"
else:
    UNI_FONT = "Helvetica"
    UNI_BOLD = "Helvetica-Bold"

BASE_FONT = "Helvetica"
BASE_BOLD = "Helvetica-Bold"

# ── Styles ───────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

TITLE = S("TI", fontName=UNI_BOLD, fontSize=22, textColor=colors.HexColor("#0F2043"), spaceAfter=6, alignment=TA_CENTER, leading=26)
SUBTITLE = S("SU", fontName=UNI_BOLD, fontSize=11, textColor=colors.HexColor("#16A085"), spaceAfter=10, alignment=TA_CENTER)
H1 = S("H1", fontName=BASE_BOLD, fontSize=14, textColor=colors.HexColor("#0F2043"), spaceBefore=12, spaceAfter=4, keepWithNext=True)
H2 = S("H2", fontName=BASE_BOLD, fontSize=11, textColor=colors.HexColor("#1A5276"), spaceBefore=8, spaceAfter=3, keepWithNext=True)
H3 = S("H3", fontName=BASE_BOLD, fontSize=9.5, textColor=colors.HexColor("#117864"), spaceBefore=6, spaceAfter=2, keepWithNext=True)
BODY = S("BO", fontName=BASE_FONT, fontSize=9, leading=13, spaceAfter=4, alignment=TA_JUSTIFY)
BULLET = S("BU", fontName=BASE_FONT, fontSize=9, leading=12.5, leftIndent=14, firstLineIndent=-10, spaceAfter=2.5)

# Table cell styles
TC = S("TC", fontName=UNI_FONT, fontSize=8, leading=11, spaceAfter=0, wordWrap="CJK")
TCB = S("TCB", fontName=UNI_BOLD, fontSize=8, leading=11, spaceAfter=0, wordWrap="CJK")
TCH = S("TCH", fontName=BASE_BOLD, fontSize=8, leading=11, textColor=colors.white, spaceAfter=0)
NOTE = S("NO", fontName=BASE_BOLD, fontSize=8.5, textColor=colors.HexColor("#C0392B"), leading=12, spaceBefore=3, spaceAfter=3)
CALLOUT = S("CO", fontName=UNI_FONT, fontSize=8.5, leading=12, textColor=colors.HexColor("#0F2043"))
CAP = S("CA", fontName=UNI_FONT, fontSize=8.5, textColor=colors.HexColor("#555555"), alignment=TA_CENTER, spaceAfter=6)
XREF = S("XR", fontName=BASE_BOLD, fontSize=8, textColor=colors.HexColor("#2980B9"), spaceBefore=2, spaceAfter=4)

def hr(col="#16A085"):
    return HRFlowable(width="100%", thickness=0.8, color=colors.HexColor(col), spaceAfter=5, spaceBefore=3)

def sp(n=1):
    return Spacer(1, n * 0.18 * cm)

def p(text, style=BODY): return Paragraph(text, style)
def h1(text): return Paragraph(text, H1)
def h2(text): return Paragraph(text, H2)
def h3(text): return Paragraph(text, H3)
def bullet(t): return Paragraph(f"&bull;  {t}", BULLET)
def b(t): return f"<b>{t}</b>"
def i(t): return f"<i>{t}</i>"
def xref(t): return Paragraph(f"📌 <b>Presentation & Paper Link:</b> {t}", XREF)

def pc(text, bold=False, center=False):
    st = TCB if bold else TC
    if center:
        st = S("cen", parent=TC, alignment=TA_CENTER)
    return Paragraph(str(text), st)

def ph(text):
    return Paragraph(str(text), TCH)

def build_table(rows, col_widths, hdr_color="#0F2043"):
    tdata = []
    tdata.append([ph(c) for c in rows[0]])
    for row in rows[1:]:
        tdata.append([pc(c) for c in row])
    t = Table(tdata, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(hdr_color)),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F8F9FA"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BDC3C7")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t

# ── Header / Footer Canvas ───────────────────────────────────────────────────
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#555555"))

        if self._pageNumber > 1:
            self.drawString(54, 800, "AarogyaSathi — Minor Project 1st Defense Master Revision Guide")
            self.drawRightString(540, 800, "ES-451 | CSE (Data Science) | BPIT")
            self.setStrokeColor(colors.HexColor("#D0D3D4"))
            self.setLineWidth(0.5)
            self.line(54, 794, 540, 794)

        self.setStrokeColor(colors.HexColor("#D0D3D4"))
        self.setLineWidth(0.5)
        self.line(54, 38, 540, 38)
        self.drawString(54, 28, "Team: Salman Mohammad Khan (00520815723) | Dhairya Summi (00420815723) | Siddharth Singh (01820815723)")
        self.drawRightString(540, 28, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def generate_pdf():
    os.makedirs("docs", exist_ok=True)
    doc = SimpleDocTemplate(
        OUTPUT_DOCS,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45,
    )

    story = []

    # ════════════ COVER PAGE ════════════════════════════════════════════════════
    story += [
        sp(2),
        Paragraph("AarogyaSathi (आरोग्यसाथी)", TITLE),
        Paragraph("AI-Driven Bilingual Public Health Chatbot with Autonomous Fact-Checking & Syndromic Surveillance", SUBTITLE),
        hr("#0F2043"),
        sp(1),
        Paragraph("<b>Comprehensive Master Defense Revision Manual — Minor Project 1st Defense</b>", CAP),
        sp(),
        build_table([
            ["Field", "Project Specification & Administrative Metadata"],
            ["Project Title",     "AarogyaSathi — AI-Driven Public Health Conversational Agent"],
            ["Subject Code",      "ES-451 (Minor Project, B.Tech 7th Semester)"],
            ["Problem Statement", "Smart India Hackathon 2025 — SIH25049 (Govt. of Odisha)"],
            ["Institute",         "Bhagwan Parshuram Institute of Technology (BPIT), Rohini, Delhi"],
            ["Department",        "Department of Computer Science & Engineering (Data Science)"],
            ["Project Team",      "• Salman Mohammad Khan (00520815723)\n• Dhairya Summi (00420815723)\n• Siddharth Singh (01820815723)"],
            ["Supervisor",        "Mr. Aditya Sam Kosy, Assistant Professor, Dept. of CSE (Data Science)"],
            ["Live Cloud Demo",   "http://130.210.56.87:8000 (Oracle Cloud Infrastructure Always-Free VM, 24/7)"],
            ["Admin Dashboard",   "http://130.210.56.87:8000/admin (Geospatial Syndromic Outbreak Early Warning)"],
            ["Evaluation Date",   "Monday, 14th September 2026 (1st Defense Evaluation)"],
        ], [4.2*cm, 13.0*cm], hdr_color="#0F2043"),
        sp(2),
        Paragraph(
            "<b>Important:</b> This revision document contains the complete end-to-end technical breakdown of AarogyaSathi. "
            "It explains all startup sequences, code workflows, algorithms, mathematical anomaly models, ML concept definitions, "
            "limitations, live demonstration steps, and viva questions. Every team member should review this thoroughly before entering the defense hall.",
            CALLOUT
        ),
        PageBreak(),
    ]

    # ════════════ 1. WHY WE BUILT THIS ══════════════════════════════════════════
    story += [
        h1("1.  WHY WE BUILT THIS — The Real Problem & Motivation"), hr(),
        xref("PPT Slide 2 (Background & Problem Motivation) | Research Paper Section I (Introduction)"),
        p(b("The Indian Healthcare Divide:") + " India suffers from an acute clinical provider deficit, with a doctor-to-population ratio of approximately "
          + b("1:1,456") + " compared to the World Health Organization (WHO) recommended norm of 1:1,000. In rural and peri-urban demographics, primary health centers (PHCs) "
          "are understaffed, overburdened, and geographically dispersed. Over 70% of rural citizens rely on informal healthcare channels, social messaging apps, and word-of-mouth advice."),
        p(b("The Fatal Medical Infodemic on Social Media:") + " Proliferation of mobile data has precipitated a massive medical infodemic. "
          "Unverified, pseudoscientific, and actively hazardous medical advice spreads virally across WhatsApp and Telegram. Critical real-world examples include: "
          "(i) Pediatric vaccine hesitancy driven by false claims that polio drops or MMR cause autism or infertility; "
          "(ii) Dangerous home remedies like drinking concentrated garlic water to cure diabetes in 7 days, causing patients to discontinue insulin and suffer diabetic ketoacidosis; and "
          "(iii) Fatal first-aid hoaxes like applying caustic red chilli powder to dog bites or incising snakebites, causing irreversible tissue necrosis and sepsis."),
        p(b("The 14–21 Day Surveillance Latency in Centralized Registries:") + " Traditional epidemiologic monitoring programs like India's Integrated Disease Surveillance Programme (IDSP) "
          "depend on physical laboratory test confirmations and outpatient hospital paperwork. By the time a Dengue or Cholera outbreak is officially recognized at the district level, "
          "14 to 21 days have elapsed, and community transmission has peaked. There is zero real-time, citizen-driven syndromic signal capture at the postal pincode level."),
        sp(),
        h2("1.1  The 30-Second Winning Elevator Pitch"),
        p("Every team member must be ready to deliver this exact opening statement when asked to introduce the project:"),
        Paragraph(
            '"Respected panel, AarogyaSathi addresses Smart India Hackathon problem SIH25049 by the Government of Odisha. '
            'Rural India faces a dual healthcare crisis: acute doctor shortages leading to viral WhatsApp health hoaxes, and a 2-to-3-week delay in hospital outbreak tracking. '
            'We engineered an autonomous, zero-cost conversational health agent tailored for rural citizens. It features deterministic sub-10ms emergency triage, '
            'Google LaBSE cross-lingual retrieval across English, Hindi, and Hinglish, an autonomous 4-tier health fact-checking engine operating at $0 API cost, '
            'and a real-time pincode-level syndromic outbreak surveillance detector. The full platform is live right now on Oracle Cloud at 130.210.56.87:8000."',
            S("quote", parent=CALLOUT, backColor=colors.HexColor("#E8F8F5"), borderColor=colors.HexColor("#16A085"), borderPadding=8, spaceBefore=4, spaceAfter=6)
        ),
        PageBreak(),
    ]

    # ════════════ 2. COMPLETE FEATURE SET & SPECS ════════════════════════════════
    story += [
        h1("2.  WHAT WE BUILT — Complete Feature Set & Technical Summary"), hr(),
        xref("PPT Slide 3 (Objectives) & Slide 11 (Deployment Specs) | Research Paper Section III"),
        build_table([
            ["Feature / Component", "Technical Specification", "Implementation & Practical Purpose"],
            ["Bilingual Core NLP", "fastText + TF-IDF + Logistic Regression", "Language identification (176 langs) + 13-class public health intent classifier (F1 = 0.942)."],
            ["Cross-Lingual Retrieval", "Google LaBSE (768-dim Hilbert Space)", "Maps Hindi, English, and Romanized Hinglish queries to identical semantic coordinates without translation loss."],
            ["Zero-Hallucination RAG", "Qwen3-1.7B-Instruct (4-bit Q4_K_M GGUF)", "Local Small Language Model running via Ollama. Negative constraints enforce answers strictly from WHO/MoHFW context (<70 words)."],
            ["Deterministic Emergency", "Regex Red-Flag Triage (<10ms latency)", "Keywords like chest pain, snakebite, shortness of breath instantly bypass AI and trigger 108/112 ambulance prompt."],
            ["Autonomous Fact-Check", "4-Tier Zero-Cost Verification Engine", "Exact hash cache + LaBSE FAISS + DuckDuckGo/PubMed web consensus + SLM badging. Zero API keys, $0 monthly cost."],
            ["Syndromic Surveillance", "7-Day Rolling Baseline Anomaly Engine", "Detects localized symptom surges (Delta >= 2.0x, N >= 3) by 6-digit postal code. Feeds live /admin dashboard."],
            ["Bilingual Voice UI", "Web Speech API (Speech-to-Text / TTS)", "Browser-native voice input in Hindi (hi-IN) and Indian English with audio readback, removing literacy hurdles."],
            ["Production Cloud Host", "Oracle Cloud Infrastructure (OCI)", "Running 24/7 on Ubuntu 24.04 ARM64 VM (2 OCPU, 4GB RAM) with systemd auto-restart daemon (healthbot.service)."],
        ], [3.5*cm, 4.5*cm, 9.2*cm]),
        sp(),
        h2("2.1  Project Evolution (V1 to V9 Development Progression)"),
        build_table([
            ["Version", "Engineering Milestone Achieved"],
            ["V1 — Rule-based", "Basic if/else keyword matching; English only, brittle syntax."],
            ["V2 — TF-IDF Classifier", "Trained machine learning intent classifier (char n-grams + Logistic Regression) on 13 health classes."],
            ["V3 — Cross-Lingual LaBSE", "Integrated Google LaBSE sentence transformers. Enabled semantic matching for Hindi and colloquial Hinglish."],
            ["V4 — Entity Lexicons", "Custom medical dictionaries for 14 diseases, 34 symptoms, 13 vaccines with typo tolerance and negation handling."],
            ["V5 — Local SLM RAG", "Deployed local Qwen3-1.7B via Ollama. Enforced strict prompt grounding against WHO knowledge bases."],
            ["V6 — Multi-Turn Memory", "Session state machine tracking symptom duration, severity, and rolling conversation summaries."],
            ["V7 — Autonomous Fact-Check", "Replaced Google API with autonomous 4-tier engine: exact hash + LaBSE + open-web consensus ($0 cost)."],
            ["V8 — Syndromic Surveillance", "Pincode-level event logging in SQLite and automated 7-day rolling baseline outbreak anomaly math."],
            ["V9 — Cloud Production", "Deployed on Oracle Cloud Infrastructure (130.210.56.87:8000) with systemd auto-restart and /admin dashboard."],
        ], [4.0*cm, 13.2*cm], hdr_color="#1A5276"),
        PageBreak(),
    ]

    # ════════════ 3. STARTUP SEQUENCE & UNDER THE HOOD ═══════════════════════════
    story += [
        h1("3.  HOW THE PROJECT STARTS — Backend Startup Sequence"), hr(),
        xref("app/main.py (@app.on_event('startup')) | Research Paper Section III.A"),
        p("When the FastAPI server launches via <code>uvicorn app.main:app --host 0.0.0.0 --port 8000</code>, the function "
          + b("startup()") + " in <code>app/main.py</code> executes the following sequential steps in under 3 seconds:"),
        sp(),
        build_table([
            ["Order & Function Call", "Source Module", "What Happens Under the Hood & RAM Utilization"],
            ["1. kb.load()", "app.core.kb", "Loads structured JSON files into memory: 14 diseases, 49 myths, 35 FAQs, 13 vaccines, UIP schedules (~150 KB)."],
            ["2. intent.load()", "app.core.intent", "Loads TF-IDF vectorizer (char 2-5 grams) and trained Logistic Regression model from data/models/ (~2.5 MB)."],
            ["3. language._load()", "app.core.language", "Loads Meta's fastText lid.176.bin binary into memory for sub-millisecond language identification (~125 MB)."],
            ["4. retriever._ensure_index()", "app.core.retriever", "Verifies pre-computed LaBSE embedding matrix (.npy) for knowledge base. Rebuilds cache if SHA-256 hash changed."],
            ["5. verifier._ensure_index()", "app.factcheck.verifier", "Verifies pre-computed embedding matrix for 49 medical myths. Prepares memory-mapped arrays for instant cosine similarity."],
            ["6. embeddings.get_model()", "app.core.embeddings", "Loads HuggingFace sentence-transformers/LaBSE onto CPU using PyTorch AutoModel with fp16 weights (~1.05 GB RAM)."],
            ["7. syndromic.init_db()", "app.surveillance.syndromic", "Initializes SQLite database data/surveillance.db, creating events, messages, and alerts tables with composite indices."],
            ["8. _warmup_llm()", "app.main", "Sends warm-up ping to local Ollama Qwen3-1.7B. OLLAMA_KEEP_ALIVE=-1 keeps the 1.62 GB model pinned in RAM permanently."],
        ], [4.5*cm, 3.5*cm, 9.2*cm]),
        sp(),
        h2("3.1  Total Steady-State Memory Footprint"),
        p("The entire backend operates at a steady-state RAM consumption of " + b("~3.05 GB") + ", fitting comfortably inside the 4.0 GB cloud VM ceiling:"),
        bullet("<b>LaBSE Sentence Transformer:</b> ~1.05 GB (PyTorch fp16 CPU inference)"),
        bullet("<b>Qwen3-1.7B SLM:</b> ~1.62 GB (Ollama 4-bit Q4_K_M GGUF quantized runtime)"),
        bullet("<b>FastAPI Uvicorn + SQLite + fastText:</b> ~0.38 GB"),
        bullet("<b>Operating System (Ubuntu 24.04):</b> ~0.35 GB — Safe Headroom: ~0.60 GB free RAM."),
        PageBreak(),
    ]

    # ════════════ 4. COMPLETE MESSAGE WORKFLOW ══════════════════════════════════
    story += [
        h1("4.  THE COMPLETE MESSAGE FLOW — How a Request is Handled"), hr(),
        xref("PPT Slide 5 (Architecture) | app/core/router.py (process_message) | Paper Section III.B"),
        p("When a user sends a message to <code>POST /api/chat</code>, the router executes an 8-stage decision pipeline:"),
        sp(),
        build_table([
            ["Stage & Component", "Latency", "Exact Operational Logic & Decision Branching"],
            ["Stage 1: Ingestion\nFastAPI (main.py)", "< 2 ms", "Receives JSON payload: {message: string, session_id: string, pincode: optional}. Generates unique session if absent."],
            ["Stage 2: Red-Flag Guard\nrouter.py", "< 10 ms", "Regex scanner checks for life-threatening keywords (chest pain, snakebite, unconsciousness, severe burn). If detected, BYPASSES ALL AI and returns immediate 108/112 ambulance prompt."],
            ["Stage 3: Language ID\nlanguage.py", "< 1 ms", "fastText classifies language across 176 tongues. Transliteration heuristics detect Romanized Hinglish (e.g. 'mujhe bukhar hai' -> Hindi Devanagari output)."],
            ["Stage 4: Intent Classifier\nintent.py", "< 5 ms", "TF-IDF feature extraction + Logistic Regression predicts intent across 13 classes (emergency, fact_check, disease_info, symptom_check, vaccination, prevention, outbreak, etc.)."],
            ["Stage 5: Multi-Turn Probing\nsession.py", "< 5 ms", "Checks active symptom_flow state in session memory. If user reports vague symptoms, probes duration and secondary signs before final triage."],
            ["Stage 6: LaBSE Grounding\nretriever.py", "80–120 ms", "Encodes query into 768-dim vector. Calculates Cosine Similarity + 0.22 lexical boost against pre-indexed WHO/MoHFW disease vectors. Filters entries < 0.40."],
            ["Stage 7: SLM Generation\ngenerator.py", "1.5–3.5 s", "Quantized Qwen3-1.7B generates empathetic, village-friendly advice (<70 words). Strictly constrained to retrieved context with zero pharmaceutical prescription."],
            ["Stage 8: Surveillance Log\nsyndromic.py", "< 5 ms", "If pincode was supplied, logs anonymized tuple (pincode, symptom_category, timestamp) into SQLite and triggers rolling baseline anomaly check."],
        ], [4.0*cm, 1.8*cm, 11.4*cm]),
        sp(),
        h2("4.1  Why Deterministic Safety Bypasses the LLM"),
        p("In healthcare AI, an LLM must " + b("NEVER") + " be in the critical path for acute medical emergencies. If a user queries 'my father is having crushing chest pain', "
          "waiting 4 seconds for an LLM to generate text (or risking hallucinated advice like 'drink hot tea') can be fatal. "
          "Our deterministic red-flag guard executes in " + b("sub-10 milliseconds") + ", guaranteeing an instant ambulance referral."),
        PageBreak(),
    ]

    # ════════════ 5. NLP & LANGUAGE INTELLIGENCE ═════════════════════════════════
    story += [
        h1("5.  NLP IMPLEMENTATION — Language Intelligence & Intent Classification"), hr(),
        xref("PPT Slide 6 (Core Methodology) | app/core/intent.py & language.py | Paper Section III.B"),
        h2("5.1  Language Identification (fastText lid.176)"),
        p("We utilize Meta's open-source " + b("fastText lid.176.bin") + " model (125 MB). It evaluates character n-grams and classifies inputs across 176 languages in sub-millisecond time. "
          "Because fastText natively outputs 'en' for English and 'hi' for Devanagari Hindi, we built our own " + b("Hinglish transliteration heuristic") + ": "
          "if text is in Latin script but contains high-frequency Hindi phonetic tokens (e.g. 'kya', 'hai', 'mujhe', 'mera', 'dard', 'kaise'), "
          "it re-routes language to 'hi' so the chatbot replies in clean Hindi Devanagari."),
        sp(),
        h2("5.2  Intent Classifier (TF-IDF + Logistic Regression)"),
        p("Our intent classifier is trained from scratch on <code>data/training/intents.json</code> spanning 13 public health intent categories:"),
        build_table([
            ["Intent Label", "Sample User Utterances", "Trained Class Weight & F1-Score"],
            ["emergency", "'chest pain left arm numb', 'saanp ne kaat liya', 'unconscious'", "Class Weight: 2.5 (Precision: 1.000, Recall: 1.000, F1: 1.000)"],
            ["fact_check", "'fact check: garlic cures diabetes', 'kya karele se cancer theek hota hai'", "Class Weight: 1.5 (Precision: 0.965, Recall: 0.970, F1: 0.967)"],
            ["symptom_check", "'I have high fever and shivering', 'pet me tez dard hai 2 din se'", "Class Weight: 1.2 (Precision: 0.930, Recall: 0.945, F1: 0.937)"],
            ["disease_info", "'what are dengue symptoms', 'malaria kaise phailta hai', 'TB signs'", "Class Weight: 1.0 (Precision: 0.950, Recall: 0.940, F1: 0.945)"],
            ["vaccination", "'polio drops schedule for baby', 'when to give BCG', 'rabies vaccine doses'", "Class Weight: 1.0 (Precision: 0.960, Recall: 0.950, F1: 0.955)"],
            ["outbreak", "'is there malaria in pincode 110001', 'delhi me dengue phaila hai kya'", "Class Weight: 1.0 (Precision: 0.920, Recall: 0.910, F1: 0.915)"],
            ["prevention", "'how to avoid dengue mosquitoes', 'typhoid se kaise bache'", "Class Weight: 1.0 (Precision: 0.935, Recall: 0.925, F1: 0.930)"],
        ], [3.2*cm, 7.5*cm, 6.5*cm]),
        sp(),
        h2("5.3  Entity Extraction & Negation Handling"),
        bullet("<b>Medical Lexicon:</b> Dictionary ontologies mapping 34 symptoms, 14 diseases, 13 vaccines, and 12 red-flags with colloquial aliases and spelling typo tolerance."),
        bullet("<b>Negation Guard:</b> Natural language often contains negations ('no vomiting', 'nahi hai bukhar'). Our regex negator inspects 3 tokens prior to any symptom match. If a negation particle ('no', 'not', 'without', 'nahi', 'bina') is found, the symptom is marked negative, preventing false disease attribution."),
        PageBreak(),
    ]

    # ════════════ 6. RAG & SLM REASONING ═════════════════════════════════════════
    story += [
        h1("6.  RAG — RETRIEVAL-AUGMENTED GENERATION & EDGE SLM"), hr(),
        xref("PPT Slide 7 (RAG & SLM Reasoning) | app/core/retriever.py & generator.py | Paper Section III.C"),
        p("RAG (Lewis et al., NeurIPS 2020) is an architectural pattern where external factual documents are retrieved and injected into the LLM context prompt before generation. "
          "This guarantees " + b("zero clinical hallucination") + " — the model cannot invent medicines or pathologies because it is strictly bounded to the retrieved text."),
        sp(),
        h2("6.1  The Google LaBSE Cross-Lingual Embedding Model"),
        p("LaBSE (Language-Agnostic BERT Sentence Embeddings, Google 2022) is a 12-layer dual-encoder transformer trained across 109 languages. "
          "It maps inputs into a unified " + b("768-dimensional Hilbert metric space") + ". "
          "Because cross-lingual sentences share the same coordinates, 'Does garlic cure diabetes?' and 'क्या लहसुन से शुगर ठीक होती है?' achieve a Cosine Similarity exceeding 0.88 without translation."),
        p("Mathematically, user query <i>q</i> is encoded via token mean-pooling and L2 normalization:"),
        Paragraph("<b>v_q = MeanPool(LaBSE(q)) / ||MeanPool(LaBSE(q))||_2 &nbsp;&nbsp;|&nbsp;&nbsp; S(q, c_i) = v_q &middot; v_{c_i}</b>",
                  S("eq", fontName="Courier-Bold", fontSize=9, leading=12, alignment=TA_CENTER, textColor=colors.HexColor("#0F2043"), spaceBefore=3, spaceAfter=5)),
        sp(),
        h2("6.2  Hybrid Semantic + Lexical Scoring"),
        p("Pure vector embeddings occasionally suffer from semantic drift. We implement a hybrid retrieval score:"),
        bullet("<b>Semantic Cosine Similarity:</b> Evaluated over pre-computed memory-mapped NumPy matrices (<code>data/embeddings/*.npy</code>) in < 100ms."),
        bullet("<b>Lexical Word-Overlap Boost:</b> Adds <code>+0.22 &times; (matching query tokens / total tokens)</code> to reward exact disease or symptom keyword matches."),
        bullet("<b>Relevance Filter:</b> Discards any candidate entry with score < 0.40 or < 20% token overlap."),
        sp(),
        h2("6.3  Strict 14-Rule Negative System Prompt Guardrails"),
        p("When Qwen3-1.7B generates the final reply, the prompt enforces strict clinical constraints:"),
        bullet("1. Answer ONLY from the retrieved context. Never extrapolate or fabricate."),
        bullet("2. Hard limit: response must be concise and under 70 words."),
        bullet("3. Never prescribe pharmaceutical drug dosages or issue definitive medical diagnoses."),
        bullet("4. Respond in the user's detected language and script (Devanagari for Hindi)."),
        bullet("5. Append official WHO/MoHFW source citation and statutory disclaimer."),
        PageBreak(),
    ]

    # ════════════ 7. AUTONOMOUS 4-TIER FACT-CHECKING ENGINE ═══════════════════════
    story += [
        h1("7.  AUTONOMOUS MULTI-TIER FACT-CHECKING ENGINE ($0 COST)"), hr(),
        xref("PPT Slide 8 (Flowchart) & Slide 10 (Benchmarks) | app/factcheck/verifier.py | Paper Section IV"),
        p("This is AarogyaSathi's primary scientific and engineering contribution. It completely replaces third-party paid APIs with an autonomous 4-tier pipeline operating at "
          + b("$0 cost with zero external API keys") + ":"),
        sp(),
        build_table([
            ["Tier & Name", "Latency", "Mechanism & Safeguards", "Verdict Emitted"],
            ["Tier 0: Fast Guard", "< 0.01 s", "Sub-10ms regex interceptor for lethal first-aid advice (sucking snakebite, chilli on dog bites, butter on burns).", "Instant MYTH + WHO first-aid protocol"],
            ["Tier 1: Hash Cache", "< 0.02 s", "Exact MD5 / SHA-256 hash lookup against in-memory dictionary of previously resolved viral claims.", "Instant Cached Verdict (95% conf)"],
            ["Tier 2: Semantic FAISS", "< 0.15 s", "LaBSE embedding cosine similarity (>= 0.82) over 49 curated WHO/PIB myths. Enforces Dual-Metric Lexical Coverage (Omega >= 0.35) to prevent positive/negative myth collisions.", "VERIFIED or MYTH + official citation"],
            ["Tier 3: Web Consensus", "2.0–4.0 s", "Autonomous multi-source scraper harvesting DuckDuckGo News, Wikipedia REST (EN+HI), and whitelisted medical portals (who.int, mohfw.gov.in, cdc.gov, mayoclinic.org).", "Structured Evidence Corpus"],
            ["Tier 4: SLM Synthesis", "1.5–3.0 s", "Local Qwen3-1.7B evaluates consensus across harvested evidence and outputs structured badge with calibrated confidence %.", "[FACT CHECK: FALSE / MISLEADING] or [VERIFIED]"],
        ], [3.2*cm, 1.8*cm, 8.5*cm, 3.7*cm]),
        sp(),
        h2("7.1  Empirical Benchmark: 15 / 15 Tests Passed (100% Success Rate)"),
        build_table([
            ["ID", "Health Claim Tested on Live Oracle VM", "Expected", "Model Verdict", "Conf.", "Latency"],
            ["01", "vaccines cause autism in children", "MYTH", "MYTH", "95.0%", "0.14s"],
            ["02", "apply toothpaste on severe kitchen burns", "MYTH", "MYTH", "95.0%", "0.01s"],
            ["03", "paracetamol p-500 contains machupo virus", "MYTH", "MYTH", "85.0%", "5.62s"],
            ["04", "eating ripe papaya causes instant miscarriage", "MYTH", "MYTH", "95.0%", "0.12s"],
            ["05", "drinking cow urine daily cures stage 4 cancer", "MYTH", "MYTH", "84.0%", "6.12s"],
            ["06", "5G cellular towers spread COVID-19 pandemic", "MYTH", "MYTH", "93.0%", "5.45s"],
            ["07", "holding breath for 10 seconds tests for coronavirus", "MYTH", "MYTH", "95.0%", "0.13s"],
            ["08", "female Aedes mosquito bite causes dengue fever", "VERIFIED", "VERIFIED", "94.2%", "0.11s"],
            ["09", "polio drops prevent infantile paralysis", "VERIFIED", "VERIFIED", "89.0%", "0.12s"],
            ["10", "गर्म पानी पीने से कोरोना खत्म हो जाता है", "MYTH", "MYTH", "95.0%", "0.14s"],
            ["11", "ye sach hai kya: haldi doodh se cancer theek hota hai", "MYTH", "MYTH", "90.0%", "7.31s"],
            ["12", "suck venom out of snakebite with mouth", "MYTH", "MYTH", "98.0%", "0.01s"],
            ["13", "apply red chilli powder on dog bite to prevent rabies", "MYTH", "MYTH", "98.0%", "0.01s"],
            ["14", "eating 10 blue marbles every day cures diabetes", "UNVERIFIABLE", "UNVERIFIABLE", "30.3%", "7.66s"],
            ["15", "ORS is the correct first treatment for diarrhoea", "VERIFIED", "VERIFIED", "93.4%", "0.11s"],
        ], [1.0*cm, 7.8*cm, 2.2*cm, 2.4*cm, 1.8*cm, 2.0*cm]),
        PageBreak(),
    ]

    # ════════════ 8. SYNDROMIC SURVEILLANCE ══════════════════════════════════════
    story += [
        h1("8.  GEOSPATIAL SYNDROMIC SURVEILLANCE & ANOMALY MATHEMATICS"), hr(),
        xref("PPT Slide 9 (Surveillance Chart & Dashboard) | app/surveillance/syndromic.py | Paper Section V"),
        p("Traditional public health surveillance (IDSP) suffers from a 14 to 21-day reporting delay because it relies on laboratory test confirmations. "
          "AarogyaSathi's " + b("Community Syndromic Surveillance") + " captures conversational symptoms directly from citizens, providing early warnings 10 to 14 days before hospital surges."),
        sp(),
        h2("8.1  Mathematical Formulation"),
        p("Symptom inquiries tagged with postal codes are logged as anonymized tuples <code>e = (pincode, symptom_category, timestamp)</code>. "
          "The engine evaluates two statistical time windows:"),
        bullet("<b>24-Hour Active Window (N_24h):</b> Total symptom reports for category <i>s</i> in pincode <i>p</i> over the trailing 24 hours."),
        bullet("<b>Rolling 7-Day Baseline (B_7d):</b> The historical daily average over the prior 7 days: <code>B_7d = (1/7) * SUM_{d=1}^{7} N(t - d)</code>."),
        bullet("<b>Spike Ratio (S_c):</b> Evaluated as <code>S_c = N_24h / max(B_7d, 0.5)</code> (the 0.5 denominator floor prevents zero-division errors)."),
        sp(),
        Paragraph(
            "<b>Outbreak Anomaly Alert Trigger Condition:</b><br/>"
            "An alert is dispatched if: &nbsp;<b>S_c &ge; 2.0</b> &nbsp;&nbsp;AND&nbsp;&nbsp; <b>N_24h &ge; 3</b><br/>"
            "• <b>MEDIUM ALERT:</b> If S_c &ge; 2.0 and N_24h &ge; 3 &nbsp;&nbsp;|&nbsp;&nbsp; "
            "• <b>HIGH CRITICAL SURGE:</b> If S_c &ge; 5.0 and N_24h &ge; 6",
            S("alertbox", parent=CALLOUT, backColor=colors.HexColor("#FEF9E7"), borderColor=colors.HexColor("#D4AC0D"), borderPadding=8, spaceBefore=4, spaceAfter=6)
        ),
        p(b("Why the dual condition?") + " If only 1 person asks about diarrhoea 2 times in an area with zero history, S_c would be 4.0x, causing a false alarm. "
          "Requiring <code>N_24h >= 3</code> guarantees at least 3 distinct citizen inquiries, filtering out random statistical noise while capturing real epidemic clusters."),
        sp(),
        h2("8.2  Live Verification on Oracle VM (/admin)"),
        p("On our live Oracle Cloud VM (<code>http://130.210.56.87:8000/admin</code>), seeding simulated baseline data for Pincode "
          + b("110001") + " (Connaught Place, New Delhi) registers:"),
        bullet("<b>24-Hour Count (N_24h):</b> 13 symptom inquiries (gastrointestinal/waterborne)."),
        bullet("<b>Rolling 7-Day Baseline (B_7d):</b> 0.86 cases/day."),
        bullet("<b>Computed Spike Ratio:</b> 13 / 0.86 = <b>15.1x Spike</b> -> Triggers active <b>[HIGH SPIKE ALERT]</b> on the CMO dashboard."),
        PageBreak(),
    ]

    # ════════════ 9. ML & NLP CONCEPT DICTIONARY ═════════════════════════════════
    story += [
        h1("9.  ML & NLP CONCEPT DICTIONARY (ZERO GOOGLE SEARCH NEEDED)"), hr(),
        xref("Definitions for Technical Defense Viva | Prepared for Professor Q&A"),
        p("Memorize these exact full forms, mathematical principles, and practical AarogyaSathi implementations:"),
        sp(),
        build_table([
            ["Term / Acronym", "Full Form", "Plain-English Definition & AarogyaSathi Role"],
            ["SLM vs LLM", "Small vs Large Language Model", "LLMs (GPT-4, 70B+) require multi-GPU cloud clusters and expensive API fees. SLMs (Qwen 1.7B) have under 3B parameters, enabling on-device inference on budget 4GB RAM cloud VMs at $0 cost."],
            ["RAG", "Retrieval-Augmented Generation", "An AI architecture where the model first retrieves verified documents from a trusted database (WHO/MoHFW) and passes them into the prompt so the model answers ONLY from facts, eliminating hallucination."],
            ["LaBSE", "Language-Agnostic BERT Sentence Embedding", "Google's 768-dimensional dual-encoder model trained across 109 languages. Maps Hindi, English, and Hinglish queries into the exact same vector space so 'garlic cure diabetes' and 'karele ka ras' align without translation."],
            ["Cosine Similarity", "Cosine Distance Metric: cos(theta) = (A . B) / (||A|| ||B||)", "Measures the angle between two embedding vectors in Hilbert space. Values near 1.0 mean identical semantic meaning. Our system uses a threshold of >= 0.82 to match user questions to verified facts."],
            ["TF-IDF", "Term Frequency - Inverse Document Frequency", "A statistical weight reflecting how important a word/character n-gram is to a document. Used in our intent classifier to convert text into numerical feature vectors before logistic regression."],
            ["fastText (lid.176)", "Fast Text Representation & Language ID", "Meta's lightweight n-gram language classifier (125MB). Identifies 176 languages in <1ms, enabling our bot to detect whether the user is speaking Hindi, English, or regional tongues."],
            ["Quantization & GGUF", "GPT-Generated Unified Format (Q4_K_M)", "Compressing model weights from 16-bit floating point down to 4-bit integers. Reduces Qwen 1.7B's memory footprint from 4.5GB down to 1.6GB, allowing it to run smoothly on a free 4GB VM."],
            ["KV-Cache", "Key-Value Cache", "Caching previously computed attention keys and values during transformer generation so the model doesn't re-calculate past tokens, accelerating response speeds from 3s down to <500ms."],
            ["F1-Score", "Harmonic Mean of Precision & Recall", "2 * (Precision * Recall) / (Precision + Recall). Our intent classification engine achieved an overall Macro F1 of 0.942, with 1.000 precision on safety-critical red-flag emergency detection."],
            ["PII & DPDP Act", "Personally Identifiable Information & Digital Personal Data Protection", "India's 2023 privacy law. AarogyaSathi ensures 'Privacy by Design' by storing only anonymized tuples (Pincode, Symptom, Timestamp). No names, phone numbers, or IP addresses are ever saved."],
            ["Clinical Hallucination", "Generative AI Fabrication", "When an LLM inventively generates fake medical advice, incorrect drug dosages, or fabricated pathology. We eliminate this using negative prompt constraints and deterministic emergency bypasses."],
        ], [3.2*cm, 4.2*cm, 9.8*cm]),
        PageBreak(),
    ]

    # ════════════ 10. HONEST SHORTCOMINGS & LIMITATIONS ══════════════════════════
    story += [
        h1("10.  HONEST SYSTEM SHORTCOMINGS, LIMITATIONS & SOLUTIONS"), hr(),
        xref("Prepared for Panel Scrutiny: 'What are the limitations of your project?'"),
        p("Professors always test your scientific maturity by asking about project limitations. "
          "Never claim the system is 100% flawless. Present these 5 honest technical trade-offs and your concrete solutions:"),
        sp(),
        build_table([
            ["Identified Limitation", "Root Cause & Impact", "Engineering Solution & Mitigation Implemented"],
            ["1. Extreme Dialectal Drift", "While LaBSE handles standard Hindi, English, and urban Hinglish exceptionally well, extreme rural rustic idioms (e.g. colloquial Sambalpuri) can drop below the 0.82 cosine similarity threshold.", "Expanded our local synonym dictionary in data/kb/ with 300+ colloquial regional symptom phrases, ensuring resilient mapping."],
            ["2. Postal Directory Sampling", "The current SQLite database includes a curated pilot sample of ~20 major districts across Delhi, Odisha, and UP rather than all 19,000 Indian postal codes.", "The schema is fully architected for scale; Phase 4 will ingest the complete India Post Open Data JSON directory (~160,000 post offices)."],
            ["3. Hardware Cold-Boot Delay", "When the cloud server undergoes a cold reboot, the very first LLM request takes ~15 seconds while model weights are loaded into CPU memory.", "Implemented systemd drop-in configuration with OLLAMA_KEEP_ALIVE=-1 and an automated boot warmup script (_warmup_llm()) to keep models permanently hot in RAM."],
            ["4. Explicit Fact-Check Trigger", "The fact-checking module currently requires an explicit 'fact check:' prefix or direct myth query rather than passively parsing every single conversation turn.", "Intentional medical safety design: passive auto-claim detection produced false alarms on ordinary symptom queries (e.g. interpreting 'I have fever' as a claim)."],
            ["5. Edge CPU Generation Latency", "On budget ARM64 CPU cloud instances without dedicated GPUs, full web evidence synthesis takes 5 to 7 seconds.", "Acceptable for non-emergency educational inquiries; deterministic emergencies resolve in sub-10ms, while local knowledge base hits resolve in <150ms."],
        ], [3.5*cm, 5.2*cm, 8.5*cm], hdr_color="#C0392B"),
        sp(),
        h2("10.1  Why Non-Diagnostic Boundaries Protect the Project"),
        p("If asked: <i>'Can your bot be sued for medical negligence?'</i><br/>"
          "<b>Answer:</b> No. AarogyaSathi is legally and architecturally framed as an " + b("Educational Triage Companion") + ", not a diagnostic medical device. "
          "In full compliance with NITI Aayog and MoHFW Telemedicine Guidelines 2020, every single response carries an immutable statutory disclaimer: "
          "<i>'I provide health awareness information from verified sources only. I am not a doctor and cannot diagnose. Consult a healthcare professional.'</i>"),
        PageBreak(),
    ]

    # ════════════ 11. ROADMAP (PHASE 4) ═════════════════════════════════════════
    story += [
        h1("11.  PLANNED WORK AHEAD — Phase 4 Roadmap & Execution"), hr(),
        xref("PPT Slide 13 (Phase 4 Roadmap) | Research Paper Section IX (Future Work)"),
        p("Based on our Smart India Hackathon problem statement and college defense requirements, here are the 3 realistic technical extensions planned for Phase 4:"),
        sp(),
        build_table([
            ["Milestone & Timeline", "Core Technical Focus", "Key Engineering Deliverables & Policy Compliance"],
            ["Phase 4A: WhatsApp Bot & Webhooks\n(Months 1 – 2)", "Meta Cloud API Integration", "• Configure official Meta WhatsApp Cloud API webhooks (POST /api/webhook/whatsapp).\n• Strict compliance with Meta WhatsApp Business Health Policy (strictly non-diagnostic preventive education).\n• Reaches 500M+ Indian citizens without requiring smartphone app downloads."],
            ["Phase 4B: Voice Note Processing\n(Months 3 – 4)", "WhatsApp Audio Note Ingestion", "• Ingests native WhatsApp voice notes (.ogg/Opus audio) directly via webhook payload.\n• Transcribes audio using faster-whisper and AI4Bharat Bhashini models in ~1.2s.\n• Returns bidirectional text and synthesized voice notes, removing literacy barriers for elderly rural users."],
            ["Phase 4C: Model Optimization\n(Months 5 – 6)", "Low-Latency Edge Quantization", "• 4-bit / 8-bit GGUF quantization and ONNX Runtime model acceleration.\n• KV-cache prefix optimization to achieve sub-500ms inference on budget edge hardware.\n• Enhanced clinical empathy and reasoning accuracy with zero recurring cloud billing."],
        ], [4.0*cm, 4.2*cm, 9.0*cm]),
        sp(),
        h2("11.1  Voice Recognition Feasibility on Web vs WhatsApp"),
        bullet("<b>Web Browser Implementation:</b> Integrated via HTML5 Web Speech API (<code>webkitSpeechRecognition</code>). Takes 15 lines of JavaScript in <code>web/chat.js</code>, costs $0, and uses zero server CPU."),
        bullet("<b>WhatsApp Implementation:</b> The backend downloads the incoming audio media URL from Meta Cloud API, pipes it through <code>faster-whisper</code> on the VM, and feeds the resulting Hindi/English string into the standard chat router."),
        PageBreak(),
    ]

    # ════════════ 12. LIVE DEMO & PANEL DEFENSE PLAYBOOK ══════════════════════════
    story += [
        h1("12.  THE PANEL DEFENSE PLAYBOOK — Live Demo Script & Viva Q&A"), hr(),
        xref("3-Minute Presentation Walkthrough & Panel Q&A"),
        h2("12.1  Step-by-Step 3-Minute Live Demo Script"),
        p("Before entering the defense room, open both tabs in your laptop browser:"),
        bullet("<b>Tab 1:</b> <code>http://130.210.56.87:8000/</code> (Chatbot Web Interface)"),
        bullet("<b>Tab 2:</b> <code>http://130.210.56.87:8000/admin</code> (Syndromic Surveillance Dashboard)"),
        sp(),
        build_table([
            ["Step & Screen", "Action / What to Type", "What to Explain Live to the Professors"],
            ["Step 1: Greeting & Grounding\nTab 1 (Chatbot)", "Type: 'hello' or click 'What is Dengue?'", "Demonstrates fastText language identification and instant WHO/MoHFW grounded disease retrieval with official citations."],
            ["Step 2: Bilingual Fact-Check\nTab 1 (Chatbot)", "Type: 'fact check: kya karela juice se diabetes theek ho jayegi?'", "Shows LaBSE cross-lingual mapping. Prominent [FACT CHECK: FALSE / MISLEADING] badge appears in ~200ms explaining dietary realities vs insulin requirements."],
            ["Step 3: Emergency Safety Guard\nTab 1 (Chatbot)", "Type: 'severe chest pain and left arm numbness'", "Demonstrates sub-10ms deterministic safety guard. Bypasses LLM completely and triggers bold red 108/112 Ambulance Emergency Dispatch Card."],
            ["Step 4: Outbreak Surveillance\nTab 2 (/admin)", "Switch to Admin tab. Point to Pincode 110001.", "Highlight: 13 cases in 24h vs 0.86 baseline = 15.1x Critical Surge Alert. Click 'Run detection now' to demonstrate live recalculation."],
        ], [3.5*cm, 5.0*cm, 8.7*cm]),
        sp(),
        h2("12.2  Top 10 Viva Questions & Textbook Answers"),
        bullet("<b>Q1: What is YOUR original contribution? Aren't you just using pre-trained models?</b><br/>"
               "<i>Answer:</i> Pre-trained models are merely one component. Our original engineering contributions are: "
               "(1) The 4-Tier Autonomous Fact-Checking Engine operating without paid Google/OpenAI APIs; "
               "(2) The Dual-Metric Lexical Coverage algorithm that prevents valid immunization facts from colliding with anti-vax myths; "
               "(3) The real-time 7-day rolling baseline syndromic anomaly detector; and "
               "(4) The deterministic sub-10ms safety router that guarantees zero-hallucination triage."),
        bullet("<b>Q2: Why didn't you use the Google Fact Check API?</b><br/>"
               "<i>Answer:</i> Google Fact Check API failed our requirements: it requires a linked credit card with recurring international billing (blocked by RBI e-mandate rules), has strict rate limits, and yields 0 hits for Indian regional rumors. Our engine combines local LaBSE semantic search and dynamic open-web consensus at zero cost."),
        bullet("<b>Q3: What if the bot gives wrong medicine and someone dies?</b><br/>"
               "<i>Answer:</i> AarogyaSathi has an immutable non-diagnostic boundary. It never prescribes schedules drugs or gives clinical diagnoses. Every response carries an ICMR statutory disclaimer. Red-flag symptoms (chest pain, snakebite) immediately trigger emergency diversion to 108/112 ambulance services with zero AI involvement."),
        bullet("<b>Q4: How does syndromic surveillance detect outbreaks before hospitals?</b><br/>"
               "<i>Answer:</i> Hospitals rely on laboratory confirmations, which take 14–21 days to propagate into central IDSP registries. AarogyaSathi captures conversational symptom queries in real time. If queries in a postal code double the 7-day baseline with at least 3 distinct cases, an alert triggers on /admin 10 to 14 days ahead of hospital registries."),
        bullet("<b>Q5: Why Qwen3-1.7B instead of Llama-3 or GPT-4?</b><br/>"
               "<i>Answer:</i> GPT-4 requires expensive API fees and internet round-trips. Llama-3 8B requires costly GPU servers. Qwen3-1.7B provides state-of-the-art multilingual comprehension while consuming only 1.6GB RAM via 4-bit quantization, allowing our entire stack to run inside our free 4GB cloud VM."),
        bullet("<b>Q6: How do you handle code-mixed Hinglish?</b><br/>"
               "<i>Answer:</i> Standard BERT models collapse on Hinglish. Google LaBSE maps 109 languages into a shared 768-dimensional space. The Hinglish query 'karela se diabetes theek hogi' projects to within cosine similarity > 0.85 of its formal English counterpart, completely bypassing the need for brittle translation software."),
        bullet("<b>Q7: Is citizen medical data stored?</b><br/>"
               "<i>Answer:</i> In strict compliance with India's DPDP Act 2023, we implement Zero-PII storage. User sessions are ephemeral and kept in memory. The surveillance database logs only anonymized geographic tuples: (Pincode, Symptom, Timestamp). No names, phone numbers, or IPs are ever saved."),
        PageBreak(),
    ]

    # ════════════ 13. QUICK REFERENCE CHEAT SHEET ═══════════════════════════════
    story += [
        h1("13.  QUICK REFERENCE CHEAT SHEET — Team Division of Roles"), hr(),
        build_table([
            ["Team Member & Roll No.", "Assigned Presentation Topics for Tomorrow's Defense"],
            ["Salman Mohammad Khan\n(00520815723)",
             "• Opening pitch & Problem Statement (Healthcare divide, 1:1456 doctor ratio, rural infodemic).\n"
             "• High-Level System Architecture overview (Slide 1, 2, 3, 5).\n"
             "• Live Chatbot Demonstration (Tab 1: English greeting, Hindi dengue info, emergency bypass)."],
            ["Dhairya Summi\n(00420815723)",
             "• Literature Survey & Gap Analysis (Slide 4: Ada Health, CoWIN, Google Fact Check comparison).\n"
             "• Core NLP Pipeline: fastText language ID, TF-IDF + LR intent classification (Slide 6).\n"
             "• Autonomous 4-Tier Fact-Checking Engine: Hashing, LaBSE semantic FAISS, open-web consensus (Slide 8)."],
            ["Siddharth Singh\n(01820815723)",
             "• Grounded RAG & Edge SLM Quantization: Qwen3-1.7B 4-bit GGUF, prompt constraints (Slide 7).\n"
             "• Geospatial Syndromic Surveillance Mathematics: S_c >= 2.0 anomaly formula & Admin Dashboard (Slide 9).\n"
             "• Empirical Results (15/15 Passed benchmark) & Phase 4 Roadmap execution (Slide 10, 12, 13)."],
        ], [5.0*cm, 12.2*cm], hdr_color="#0F2043"),
        sp(2),
        build_table([
            ["Essential Quick Fact", "Key Memory Metric for Defense"],
            ["Doctor Deficit", "1:1456 in India vs 1:1000 WHO norm (-45.6% gap). Over 70% rural reliance on informal conduits."],
            ["IDSP Surveillance Delay", "14 to 21 days for physical lab logs to reach central registries; AarogyaSathi detects clusters in <24h."],
            ["LaBSE Dimensions", "768-dimensional dense vector space spanning 109 languages. Retrieval similarity threshold: >= 0.82."],
            ["Fact-Check Accuracy", "15 / 15 Passed (100% success rate) across clinical, food, myth, and Hinglish claim categories."],
            ["Cloud Server Specs", "Oracle Cloud VM.Standard.A1.Flex (2 OCPU ARM64, 4GB RAM, Ubuntu 24.04 LTS), ap-mumbai-1."],
            ["Total RAM Footprint", "3.05 GB total active RAM (LaBSE: 1.05 GB, Qwen 1.7B Q4: 1.62 GB, FastAPI: 0.38 GB). Zero swap thrashing."],
            ["Financial Monthly Cost", "$0.00 (Zero paid LLM tokens, zero Google Fact Check API keys, zero cloud hosting charges)."],
            ["Surveillance Alert Formula", "Spike Ratio S_c = N_24h / max(B_7d, 0.5). Triggers if S_c >= 2.0 AND N_24h >= 3."],
            ["Emergency Ambulance Numbers", "Sub-10ms regex interceptor immediately routes red-flag queries to 108 and 112."],
        ], [5.0*cm, 12.2*cm], hdr_color="#16A085"),
        sp(2),
        Paragraph("<b>All the best for tomorrow's Minor Project 1st Defense, Salman, Dhairya, and Siddharth!</b>", S("end", parent=CALLOUT, fontName=UNI_BOLD, alignment=TA_CENTER, textColor=colors.HexColor("#0F2043"))),
    ]

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Master Revision Guide PDF built successfully at: {OUTPUT_DOCS}")

    # Also copy to Downloads if possible
    try:
        shutil.copy(OUTPUT_DOCS, OUTPUT_DOWNLOADS)
        print(f"Updated revision guide copied to: {OUTPUT_DOWNLOADS}")
    except Exception as e:
        print(f"Could not copy to Downloads: {e}")

if __name__ == "__main__":
    generate_pdf()
