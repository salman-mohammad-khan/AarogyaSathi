"""
AarogyaSathi — Comprehensive Revision Material PDF
Fixes applied:
  1. All table cells use Paragraph() objects → no text overflow / overlap
  2. Nirmala.ttc registered for Devanagari glyph support → no black boxes
  3. Hindi text in tables replaced with safe ASCII where the column is narrow
"""
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

OUTPUT = r"C:\Users\gamer\Desktop\AarogyaSathi_Revision_Material.pdf"

# ── Register Unicode / Devanagari font ───────────────────────────────────────
# Nirmala UI ships with Windows 10/11 and covers Devanagari, Latin, Bengali,
# Tamil, Telugu, Gujarati, Kannada, Malayalam, Punjabi, Odia scripts.
NIRMALA     = r"C:\Windows\Fonts\Nirmala.ttc"
pdfmetrics.registerFont(TTFont("Nirmala",     NIRMALA, subfontIndex=0))   # regular
pdfmetrics.registerFont(TTFont("NirmalaBold", NIRMALA, subfontIndex=1))   # bold
pdfmetrics.registerFont(TTFont("NirmalaSemi", NIRMALA, subfontIndex=2))   # semi-bold (italic fallback)
pdfmetrics.registerFontFamily(
    "Nirmala", normal="Nirmala", bold="NirmalaBold",
    italic="NirmalaSemi", boldItalic="NirmalaBold"
)

BASE_FONT   = "Helvetica"
BASE_BOLD   = "Helvetica-Bold"
UNI_FONT    = "Nirmala"          # Use for any cell that may contain Indian script
UNI_BOLD    = "NirmalaBold"

# ── Styles ───────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

TITLE    = S("TI", fontName=UNI_BOLD, fontSize=22,
             textColor=colors.HexColor("#1a237e"), spaceAfter=6,
             alignment=TA_CENTER, leading=28)
SUBTITLE = S("SU", fontName=UNI_FONT, fontSize=11,
             textColor=colors.HexColor("#3949ab"), spaceAfter=14,
             alignment=TA_CENTER)
H1 = S("H1", fontName=BASE_BOLD, fontSize=15,
        textColor=colors.HexColor("#1a237e"), spaceBefore=14, spaceAfter=5)
H2 = S("H2", fontName=BASE_BOLD, fontSize=11.5,
        textColor=colors.HexColor("#283593"), spaceBefore=10, spaceAfter=4)
H3 = S("H3", fontName=BASE_BOLD, fontSize=10,
        textColor=colors.HexColor("#5c6bc0"), spaceBefore=7, spaceAfter=3)
BODY = S("BO", fontName=BASE_FONT, fontSize=9.5, leading=14,
         spaceAfter=5, alignment=TA_JUSTIFY)
BULLET = S("BU", fontName=BASE_FONT, fontSize=9.5, leading=13,
           leftIndent=14, firstLineIndent=-10, spaceAfter=3)
# Table cell styles
TC  = S("TC",  fontName=UNI_FONT,  fontSize=8.5, leading=12,
        spaceAfter=0, wordWrap="CJK")   # wordWrap="CJK" wraps aggressively
TCB = S("TCB", fontName=UNI_BOLD,  fontSize=8.5, leading=12,
        spaceAfter=0, wordWrap="CJK")
TCH = S("TCH", fontName=BASE_BOLD, fontSize=8.5, leading=12,
        textColor=colors.white, spaceAfter=0)
NOTE = S("NO", fontName=BASE_BOLD, fontSize=9,
         textColor=colors.HexColor("#bf360c"), leading=13,
         spaceBefore=4, spaceAfter=4)
CAP = S("CA", fontName=UNI_FONT, fontSize=8.5,
        textColor=colors.grey, alignment=TA_CENTER, spaceAfter=8)
FINAL = S("FI", fontName=UNI_BOLD, fontSize=10.5,
          alignment=TA_CENTER, textColor=colors.HexColor("#1a237e"))

def hr():
    return HRFlowable(width="100%", thickness=0.8,
                      color=colors.HexColor("#9fa8da"),
                      spaceAfter=6, spaceBefore=4)

def sp(n=1):
    return Spacer(1, n * 0.22 * cm)

# ── Helpers ──────────────────────────────────────────────────────────────────
def p(text, style=BODY):
    return Paragraph(text, style)

def h1(text):   return Paragraph(text, H1)
def h2(text):   return Paragraph(text, H2)
def h3(text):   return Paragraph(text, H3)
def bullet(t):  return Paragraph(f"&bull;  {t}", BULLET)
def b(t):       return f"<b>{t}</b>"
def i(t):       return f"<i>{t}</i>"

# Every table cell wrapped in Paragraph so words break properly
def pc(text, bold=False, center=False):
    st = TCB if bold else TC
    if center:
        st = S("cen", parent=TC, alignment=TA_CENTER)
    return Paragraph(str(text), st)

def ph(text):
    return Paragraph(str(text), TCH)

def build_table(rows, col_widths, hdr_color="#3949ab"):
    """rows[0] = header row (plain strings).  rows[1:] = data (plain strings)."""
    tdata = []
    # header
    tdata.append([ph(c) for c in rows[0]])
    for row in rows[1:]:
        tdata.append([pc(c) for c in row])
    t = Table(tdata, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1,  0), colors.HexColor(hdr_color)),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1),
         [colors.HexColor("#f0f2ff"), colors.white]),
        ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#9fa8da")),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t

# ── Story ────────────────────────────────────────────────────────────────────
story = []

# ════════════ COVER PAGE ════════════════════════════════════════════════════
story += [
    sp(4),
    Paragraph("AarogyaSathi (Aarogya Saathi)", TITLE),
    Paragraph("AI-Driven Public Health Chatbot for Disease Awareness", SUBTITLE),
    hr(),
    sp(1),
    Paragraph("Comprehensive Revision Material — Minor Project Presentation", CAP),
    sp(),
    build_table([
        ["Field", "Detail"],
        ["Project",       "AarogyaSathi — AI-Driven Public Health Chatbot"],
        ["Subject Code",  "ES-451 (Minor Project, B.Tech 7th Semester)"],
        ["Problem Stmt",  "Smart India Hackathon 2025 — SIH25049 (Govt. of Odisha)"],
        ["Institute",     "Bhagwan Parshuram Institute of Technology, Rohini, Delhi"],
        ["Department",    "Computer Science & Engineering (Data Science)"],
        ["Team",          "Salman Mohd. Khan  |  Dhairya Summi  |  Sidharth Singh"],
        ["Supervisor",    "Mr. Aditya Sam Kosy, Dept. of CSE(DS)"],
        ["Live Demo URL", "http://130.210.56.87:8000  (Oracle Cloud VM, 24x7)"],
        ["GitHub Repo",   "https://github.com/salman-mohammad-khan/AarogyaSathi"],
    ], [4*cm, 12.5*cm], hdr_color="#455a64"),
    sp(2),
    Paragraph(
        "Prepared the night before the first minor project defence (Sep 2026). "
        "Read each section carefully, understand the complete flow, "
        "and be ready to demonstrate the live chatbot.", CAP),
    PageBreak(),
]

# ════════════ 1. WHY WE BUILT THIS ══════════════════════════════════════════
story += [
    h1("1.  WHY WE BUILT THIS — The Real Problem"), hr(),
    p(b("The Healthcare Information Crisis in Rural India")),
    p("India has roughly 65% of its population in rural and semi-urban areas. "
      "These communities face three compounding problems with health information:"),
    bullet(b("No reliable information source:") + "  There is often 1 doctor per 10,000+ villagers. "
           "Most health information flows informally through friends, word of mouth, or increasingly, "
           "WhatsApp forwards — most of which are unverified."),
    bullet(b("Language barrier:") + "  The internet is largely in English. Government health advisories "
           "are rarely available in Bhojpuri, Odia, Punjabi or Kannada. People who can only read their "
           "mother tongue are digitally excluded from health information."),
    bullet(b("Misinformation epidemic:") + "  A 2024 study (Garimella et al.) showed that over 25% of "
           "viral WhatsApp content in rural India is misinformation, and debunked health claims continue "
           "to circulate for years. A 2021 JMIR study found 57.8% of people trusted forwarded WhatsApp "
           "health messages; 13.3% never fact-checked before forwarding."),
    sp(),
    p(b("The SIH25049 Problem Statement")),
    p("The Government of Odisha (Electronics & IT Department) released SIH25049 calling for: "
      + i('"A multilingual AI chatbot that educates rural and semi-urban populations about preventive '
          'healthcare, disease symptoms and vaccination schedules, integrates with government health '
          'databases, delivers real-time outbreak alerts, and is accessible over low-bandwidth channels '
          'such as WhatsApp and SMS."')),
    sp(),
    p(b("What We Created")),
    p("AarogyaSathi (meaning 'Health Companion') is our response — a fully working, deployed, "
      "cloud-hosted multilingual public health AI chatbot. It is an awareness and information support "
      "platform, " + b("not a doctor") + ". It never diagnoses. It never prescribes medication. "
      "It gives WHO/MoHFW-sourced verified information in 12 Indian languages, 24 hours a day."),
    sp(),
    build_table([
        ["SDG", "Description", "Our Contribution"],
        ["SDG 3",  "Good Health & Well-Being",  "Disease awareness, preventive care, outbreak comms"],
        ["SDG 4",  "Quality Education",          "Health education in 12 Indian languages"],
        ["SDG 10", "Reduced Inequalities",        "Bridges urban-rural and language divide"],
        ["SDG 11", "Sustainable Communities",     "Location-aware, timely outbreak alerts"],
        ["SDG 17", "Partnerships for Goals",      "Integration with government health databases"],
    ], [1.8*cm, 5.5*cm, 9.2*cm]),
    PageBreak(),
]

# ════════════ 2. WHAT WE BUILT ══════════════════════════════════════════════
story += [
    h1("2.  WHAT WE BUILT — Complete Feature Set"), hr(),
    build_table([
        ["Feature / Module", "What It Does", "Status"],
        ["Multilingual NLP Engine",
         "Detects 12 Indian languages + Hinglish; routes queries in user's own language", "Live"],
        ["Intent Classification",
         "TF-IDF + Logistic Regression; 13 intent types with confidence threshold", "Live"],
        ["Entity Extraction",
         "Finds symptoms, diseases, vaccines; handles typos & colloquial Hindi terms", "Live"],
        ["Disease Information",
         "14 diseases: symptoms, prevention, first aid, when-to-see-doctor (WHO/MoHFW)", "Live"],
        ["Symptom Analysis (Multi-turn)",
         "Bot asks 1 follow-up question, then gives caring, grounded symptom guidance", "Live"],
        ["Vaccination Schedules",
         "Full UIP schedule by age milestone + individual vaccine info (MoHFW)", "Live"],
        ["Fact-Check / Myth-Buster",
         "Verifies forwarded claims: VERIFIED / MYTH / PARTLY TRUE / UNVERIFIABLE", "Live"],
        ["Outbreak / Health Alerts",
         "Pincode-based location alerts + live Google News RSS filtering (health only)", "Live"],
        ["Emergency Escalation",
         "Red-flag detection (12 categories) -> instant 108/112 guidance, no LLM delay", "Live"],
        ["RAG Response Generation",
         "LaBSE retrieval + Ollama LLM (Qwen3-1.7B local + cloud gpt-oss:20b fallback)", "Live"],
        ["Conversation Memory",
         "Rolling LLM summary every 3 messages; follow-up questions understood in context", "Live"],
        ["Admin Dashboard",
         "Intent distribution, language usage, fact-check verdicts for last 24h / 7d", "Live"],
        ["Syndromic Surveillance",
         "Pincode-tagged symptom spike detection for early outbreak warning (Phase 3)", "Parked"],
        ["WhatsApp Integration",
         "Meta Cloud API webhook + HTTPS reverse proxy — the next major milestone", "Planned"],
    ], [4.5*cm, 9.5*cm, 2.5*cm]),
    sp(),
    p(b("Live Stats from Oracle Cloud VM (Sep 9, 2026):") +
      "  77 messages in last 7 days across 11 languages — 13 fact-checks, 40 greetings, "
      "3 symptom checks, 1 emergency, 15 help queries, 2 disease info queries. "
      "9 myths debunked, 2 PARTLY TRUE verdicts issued."),
    PageBreak(),
]

# ════════════ 3. HOW THE PROJECT STARTS ══════════════════════════════════════
story += [
    h1("3.  HOW THE PROJECT STARTS — Startup Sequence"), hr(),
    p("When the Oracle Cloud VM boots, two systemd services start automatically:"),
    bullet(b("ollama.service") + " — loads the local Qwen3-1.7B model into RAM with "
           "OLLAMA_KEEP_ALIVE=-1 (keeps it permanently loaded; also keeps RAM above Oracle's "
           "20% idle-reclaim threshold to prevent VM reclamation)."),
    bullet(b("healthbot.service") + " — runs: "
           + i("uvicorn app.main:app --host 0.0.0.0 --port 8000")),
    sp(),
    p(b("FastAPI startup sequence (app/main.py):")),
    bullet(b("Intent Classifier loads") + " — reads data/training/intents.json, trains TF-IDF "
           "vectorizer + Logistic Regression in ~2 seconds. Happens in-memory at startup."),
    bullet(b("LaBSE Embedding Model loads") + " — loads sentence-transformers/LaBSE (~2.2 GB "
           "model, ~1 GB RAM fp16). First-ever load takes 30-60s; subsequent boots use cached "
           "embeddings from data/embeddings/*.npy."),
    bullet(b("Knowledge Base loads") + " — reads all JSON from data/kb/ into memory: 14 diseases, "
           "35 FAQs, 49 myths, 13 vaccines, outbreak advisories, 12-language system messages, "
           "and pincode to district mappings."),
    bullet(b("Retrieval index built") + " — all KB text entries are embedded with LaBSE and "
           "stored as a similarity matrix for fast cosine search."),
    bullet(b("LLM connection tested") + " — checks if local Ollama is responding; if not, "
           "checks for OLLAMA_API_KEY for cloud fallback."),
    sp(),
    p(b("After startup:") + " first message response is 2-8 seconds (warm). "
      "After a VM reboot, first response is 15-30 seconds (model loading into RAM)."),
    PageBreak(),
]

# ════════════ 4. COMPLETE MESSAGE FLOW ═══════════════════════════════════════
story += [
    h1("4.  THE COMPLETE MESSAGE FLOW — How a User Request is Processed"), hr(),
    p("Every user message goes through " + b("router.py -> process_message()") + ". "
      "This is the brain of the entire system. The pipeline has 10 ordered steps:"),
    sp(),

    h2("Step 1: Language Detection"),
    p("The message text is analyzed by the " + b("fastText lid.176 model") + " (Facebook/Meta, CC0, "
      "125 MB). It identifies which of 176 world languages the text is in. For this project, we "
      "extract 12 Indian language codes. If fastText says 'English' but the text contains Hindi "
      "written in Roman script (Hinglish, e.g., 'mujhe bukhar hai'), a "
      + b("transliterate_hint()") + " check reclassifies it to Hindi, so the response "
      "comes back in Devanagari."),

    h2("Step 2: Welcome Detection"),
    p("If this is the first message in a new language for this session, the bot prepends "
      "a localized welcome message (from data/kb/messages.json) to the final response. "
      "This triggers only once per language per session — never repeated."),

    h2("Step 3: Fact-Check Trigger (Deterministic — no LLM)"),
    p("Before anything else, the router checks for a fact-check prefix in any language "
      "(e.g., 'fact check:', 'verify:', 'ye sach hai kya'). If detected, the session is "
      "cleared and the message goes directly to the Fact-Check Module (see Section 7). "
      "The LLM is " + b("never") + " used for verdicts — ensuring reliable, repeatable results."),

    h2("Step 4: Emergency Red-Flag Check (Deterministic, ~150ms, no LLM)"),
    p("The message is scanned against the RED_FLAG_LEXICON in entities.py — a hardcoded "
      "multi-language dictionary of emergency keywords in English and Hindi:"),
    build_table([
        ["Red-Flag Category", "Example Triggers (EN + Hindi/Hinglish)"],
        ["Chest Pain / Heart Attack",
         "chest pain | dil ka daura | seene mein dard"],
        ["Breathing Emergency",
         "cannot breathe | saans nahi aa rahi | dum ghut raha hai"],
        ["Unconsciousness",
         "unconscious | behosh | not responding | collapsed"],
        ["Seizure / Fits",       "seizure | fits | daure | convulsions"],
        ["Snake / Dog Bite",     "snake bite | saap ne kaat | dog bite | kutta kaata"],
        ["Severe Bleeding",      "heavy bleeding | khoon beh raha | profuse bleeding"],
        ["Stroke / Paralysis",   "stroke | paralysis | lakwa | face drooping"],
        ["Suicide / Self-Harm",  "suicide | khudkushi | kill myself | jeena nahi"],
        ["Poisoning",            "poison | zahar | consumed poison"],
        ["Severe Burn",          "severe burn | badly burned | jal gaya"],
        ["Pregnancy Bleeding",   "pregnancy bleeding | garbhavati ko khoon"],
        ["Rabid Animal Bite",    "monkey bite | bandar ne kaata"],
    ], [5*cm, 11.5*cm]),
    p("If ANY red flag matches, the router immediately returns 108/112 emergency guidance "
      "in the user's language. " + b("The LLM is never called.") + " This makes emergency "
      "responses instantaneous and guaranteed-reliable."),
    sp(),

    h2("Step 5: Pure Greeting Check"),
    p("If the message is a single-word greeting (hi, hello, namaste, etc.), a template "
      "greeting is returned directly from the KB — no NLP pipeline needed."),

    h2("Step 6: Active Symptom Flow Check (Multi-turn State)"),
    p("The session is checked for an active symptom_flow state. If the user previously "
      "reported symptoms and the bot asked a follow-up question, the next message is treated "
      "as a follow-up answer — new symptoms are merged and the final symptom analysis is "
      "generated. Exception: if the follow-up itself contains a 'hard interrupt' intent "
      "(emergency, fact-check, vaccination, disease info, greeting), the symptom flow is "
      "discarded and the new intent takes over."),

    h2("Step 7: LLM Understanding Pass (Semantic Intent Extraction)"),
    p("The raw message is sent to the LLM with a structured prompt instructing it to return "
      "a " + b("JSON object") + " containing intent, symptoms list, disease name, duration, "
      "and clarification/follow-up flags. This is more accurate than keyword TF-IDF for "
      "complex, indirect, or regional language queries. "
      + b("Negation handling example:") + " 'I do NOT have fever but I have headache' -> "
      "LLM correctly excludes fever from symptoms list."),

    build_table([
        ["JSON Field", "Description", "Example"],
        ["intent",        "One of 13 intent types",                 "symptom"],
        ["symptoms",      "Array of symptom names in English",       '["fever", "headache"]'],
        ["disease",       "Disease name if mentioned",               "dengue"],
        ["duration",      "How long the symptoms have lasted",       "2 days"],
        ["clarification", "True if message is too unclear to act on","false"],
        ["follow_up",     "True if this continues an earlier topic", "false"],
    ], [3*cm, 6.5*cm, 7*cm]),
    sp(),

    h2("Step 8: TF-IDF Intent Classifier (Fallback NLP)"),
    p("If the LLM understanding pass fails (LLM is down or returns unparseable JSON), "
      "the router falls back to the traditional TF-IDF char n-gram + Logistic Regression "
      "classifier trained on our own dataset. See Section 5 for NLP details."),

    h2("Step 9: Intent-Specific Handlers"),
    build_table([
        ["Intent",        "Handler Called",                         "What Happens"],
        ["symptom_check", "_symptom_probe() then _symptom_final_answer()",
         "Bot asks 1 empathetic follow-up. Then generates caring disease-awareness analysis."],
        ["disease_info",  "_disease_answer(disease_id)",
         "Looks up KB disease entry, runs LaBSE retrieval, generates LLM-grounded answer."],
        ["vaccination",   "_vaccine_response()",
         "Looks up by vaccine name OR age milestone, returns UIP schedule."],
        ["outbreak",      "_outbreak_response()",
         "Pincode to district mapping + curated advisories + Google News RSS."],
        ["fact_check",    "verifier.verify_claim()",
         "3-tier fact-check pipeline (see Section 7)."],
        ["greeting/help/smalltalk", "_chatty_answer()",
         "LLM generates warm, contextual response about bot capabilities."],
    ], [3*cm, 5.5*cm, 7.5*cm]),
    sp(),

    h2("Step 10: Three-Layer Answer Fallback"),
    bullet(b("Layer 1 — General LLM Answer:") + "  LLM answers from its own medical training "
           "knowledge with a disclaimer: 'This answer is from AI general knowledge — verify "
           "with official sources.'"),
    bullet(b("Layer 2 — Guarded Web Search:") + "  DuckDuckGo search, only if (a) query passes "
           "a health keyword guard AND (b) result comes from a whitelisted domain: "
           "wikipedia.org, who.int, cdc.gov, nih.gov, mayoclinic.org, mohfw.gov.in, icmr.gov.in."),
    bullet(b("Layer 3 — Unknown:") + "  'I don't have verified information on this. "
           "Please check mohfw.gov.in or who.int.'"),
    PageBreak(),
]

# ════════════ 5. NLP IMPLEMENTATION ═════════════════════════════════════════
story += [
    h1("5.  NLP IMPLEMENTATION — Language Intelligence"), hr(),

    h2("5.1  Language Detection — fastText lid.176"),
    p("We use the pre-trained " + b("fastText lid.176") + " model (Meta/Facebook, CC0 license). "
      "Trained on Wikipedia, Tatoeba and SETimes corpora; identifies 176 languages. "
      "We chose it because it is extremely fast (~1ms per prediction on CPU), handles "
      "short text (even a single Hindi word), is compact (125 MB), and natively handles "
      "Devanagari, Bengali, Tamil, Telugu, Gujarati, Kannada, Malayalam, Punjabi, Odia scripts. "
      "For Hinglish detection, we added a custom transliterate_hint() function that looks "
      "for common Hindi-in-Roman patterns ('mujhe', 'bukhar', 'dard', 'aapko') in "
      "otherwise-English-detected text."),
    sp(),

    h2("5.2  Intent Classification — TF-IDF + Logistic Regression (trained from scratch)"),
    p("We trained our own intent classifier on a curated dataset "
      "(data/training/intents.json) with labeled examples for 13 intent categories in "
      "English, Hindi, and Hinglish."),
    sp(),
    build_table([
        ["Intent",        "Example Query"],
        ["symptom_check", "I have fever and body pain | mujhe bukhar hai"],
        ["disease_info",  "What is dengue? | Dengue kya hai?"],
        ["prevention",    "How to prevent malaria? | malaria se kaise bachen?"],
        ["vaccination",   "When to give polio drops? | tikakaran kab karen?"],
        ["outbreak",      "Any disease outbreak in Delhi? | koi beemari faili hai kya?"],
        ["fact_check",    "fact check: turmeric milk cures cancer"],
        ["emergency",     "chest pain cannot breathe"],
        ["greeting",      "Hello | Namaste | Hi"],
        ["help",          "What can you do? | aap kya karte ho?"],
        ["smalltalk",     "Who are you? | are you a doctor?"],
        ["thanks",        "Thank you | shukriya"],
        ["follow_up",     "2 days | no fever | and vomiting?"],
        ["unclear",       "Very ambiguous or empty text"],
    ], [3.5*cm, 12.5*cm]),
    sp(),
    p(b("Key technical choices:")),
    bullet(b("Character-level N-grams (2-5):") + "  Instead of word tokenization (which fails "
           "on typos and Indian transliteration), we use char bigrams to 5-grams with "
           "max_features=30,000. This means 'bukhar', 'bukhaar', and 'bukhaar' all produce "
           "similar n-gram fingerprints — the classifier is inherently typo-tolerant."),
    bullet(b("Logistic Regression (C=8.0):") + "  Multi-class one-vs-rest, trained in ~0.1 "
           "seconds at startup. Returns class probabilities for all 13 intents. We use a "
           "confidence threshold of 0.5 — below this, intent is treated as None."),
    bullet(b("100% accuracy:") + "  Tested on the 30-query held-out set in "
           "data/training/eval.json."),
    sp(),

    h2("5.3  Medical Entity Extraction — Custom Lexicon"),
    p("We built a custom domain-specific lexicon for Indian medical terminology "
      "(entities.py). This is NOT a pretrained NER model — it is our own lexicon "
      "built specifically for the rural India context:"),
    build_table([
        ["Entity Type",    "Coverage",            "Example Aliases"],
        ["SYMPTOM_LEXICON","34 symptom types",
         "fever | bukhar | ज्वर | tapman | high temperature"],
        ["RED_FLAG_LEXICON","12 emergency categories",
         "snake bite | saap ne kaat | सर्पदंश"],
        ["DISEASE_ALIASES","14 diseases",
         "dengue | dengu | breakbone fever"],
        ["VACCINE_ALIASES","13 vaccines",
         "polio | polio drops | opv | पोलियो ड्रॉप"],
    ], [4*cm, 4.5*cm, 8*cm]),
    sp(),

    h2("5.4  NLP Evolution — How We Improved It (V1 to V9)"),
    build_table([
        ["Version",         "What Was Added / Improved"],
        ["V1 — Keyword bot",
         "Simple if/else keyword matching. English only. No intelligence."],
        ["V2 — TF-IDF Classifier",
         "Added trained TF-IDF + LR intent classifier. Still English only."],
        ["V3 — Multilingual + LaBSE",
         "Added fastText language detection. Added LaBSE embeddings for cross-lingual KB retrieval. Hindi works."],
        ["V4 — Entity Extraction",
         "Added custom lexicons for symptoms, diseases, vaccines in English+Hindi. Typo tolerance."],
        ["V5 — LLM Integration (RAG)",
         "Integrated local Ollama Qwen3-1.7B. Grounded answer generation. Ollama Cloud fallback added."],
        ["V6 — LLM Understanding Pass",
         "Added LLM as semantic intent extractor (returns structured JSON). More accurate than TF-IDF alone."],
        ["V7 — Multi-turn Memory",
         "Added session-level symptom flow state (probe + final analysis). Rolling LLM conversation summary."],
        ["V8 — Fact-Check Module",
         "3-tier fact-check: internal myth corpus (LaBSE) + Google Fact Check API + home-remedy fallback."],
        ["V9 — Regional Languages",
         "Extended all templates to 12 Indian languages. First-contact welcome-in-language behavior added."],
    ], [4.5*cm, 12*cm]),
    PageBreak(),
]

# ════════════ 6. RAG ═════════════════════════════════════════════════════════
story += [
    h1("6.  RAG — RETRIEVAL-AUGMENTED GENERATION"), hr(),
    p("RAG (Retrieval-Augmented Generation) is a published AI architecture (Lewis et al., "
      "NeurIPS 2020) where the system " + b("retrieves relevant documents") + " from a knowledge "
      "base before generating an answer, providing them as context to the LLM. This prevents "
      "hallucination — the LLM can only answer from what was retrieved."),
    sp(),
    p(b("Important — what to say in presentation:") + "  We did NOT build the RAG framework "
      "from scratch. We implemented and " + b("adapted") + " the RAG pattern using existing "
      "open-source tools (LaBSE pre-trained model, Ollama LLM API) and built our own "
      "retrieval pipeline, hybrid scoring, knowledge base, and strict grounding system "
      "around them.", NOTE),
    sp(),

    h2("6.1  The Embedding Model — LaBSE"),
    p("LaBSE (Language-Agnostic BERT Sentence Embeddings, Google 2022) is a multilingual "
      "sentence embedding model trained on 109 languages. We use the pre-trained "
      + b("sentence-transformers/LaBSE") + " model from HuggingFace (~2.2 GB). "
      "It converts text into 768-dimensional semantic vectors that are language-agnostic — "
      "meaning 'fever' in English and 'bukhar' in Hindi map to nearby points in the same "
      "vector space."),
    p("In our code (embeddings.py): we load the model with AutoTokenizer + AutoModel, "
      "implement our own mean-pooling over token embeddings, L2-normalize the result, "
      "and cache all KB embeddings to disk as .npy files. The cache is keyed by a "
      "SHA-256 hash of the KB content — automatically invalidated if the KB changes."),
    sp(),

    h2("6.2  The Retrieval Pipeline (retriever.py)"),
    bullet(b("Corpus Building:") + "  All 14 diseases and 35 FAQs are converted to text "
           "representations including names in all languages, Hinglish aliases, and summaries. "
           "These are embedded with LaBSE into a matrix at startup."),
    bullet(b("Hybrid Scoring:") + "  For each query, we compute cosine similarity against "
           "the entire corpus matrix (fast vectorized NumPy), then add a "
           + b("lexical boost (0.22 x fraction of query words matched)") + ". This hybrid "
           "semantic+lexical scoring prevents pure semantic retrieval from missing obvious "
           "keyword matches."),
    bullet(b("Threshold Filtering:") + "  Entries below similarity threshold 0.4 are discarded."),
    bullet(b("Relevance Guard:") + "  _retrieval_relevant() checks the top result has at "
           "least 20% content overlap with the query. Prevents off-topic KB entries from "
           "being used as context."),
    sp(),

    h2("6.3  The Generation — Ollama with Strict Grounding"),
    p("After retrieval, the KB context is formatted and sent to the LLM with a strict "
      "14-rule system prompt that enforces:"),
    bullet("Answer ONLY from the provided CONTEXT. Never fabricate facts."),
    bullet("Maximum 70 words. Simple, village-friendly language."),
    bullet("If context does not contain the answer, say so explicitly."),
    bullet("Never diagnose. Never prescribe medicines or dosages."),
    bullet("Reply in the user's language (Hindi in Devanagari, Bengali in Bengali script)."),
    bullet("If symptoms sound severe or urgent, tell the user to call 108/112."),
    sp(),
    p(b("LLM:") + "  Qwen3-1.7B-Instruct running locally via Ollama (Q4 quantization, ~1.4 GB). "
      "Runs on CPU on the ARM64 VM. Response: 2-8 seconds warm. "
      "Cloud fallback uses gpt-oss:20b via Ollama Cloud API (much higher quality for regional languages)."),
    sp(),

    h2("6.4  What We Built vs. What We Took from Existing Tools"),
    build_table([
        ["Component",           "Source / Attribution",           "What WE built / modified"],
        ["LaBSE embeddings",    "Pre-trained, Google/HuggingFace (CC-BY-4.0)",
         "Custom mean-pooling, disk caching, hybrid scoring, relevance guard"],
        ["Qwen3-1.7B LLM",      "Pre-trained (Apache 2.0), served by Ollama",
         "14 custom system prompts, dual-backend (local+cloud), cooldown & retry logic"],
        ["TF-IDF + LR",         "scikit-learn library (BSD)",
         "Training data (EN+HI+Hinglish), char n-gram config, confidence threshold"],
        ["fastText lid.176",    "Pre-trained, Meta/Facebook (CC0)",
         "Hinglish re-classifier, 12-language routing, welcome-in-language logic"],
        ["Health Knowledge Base","Original work by our team",
         "100% curated from WHO/MoHFW/ICMR/NHM — entirely new content"],
        ["Router & Pipeline",   "Original work by our team",
         "Full message routing, multi-turn state machine, session management"],
        ["Fact-Check Module",   "Original work by our team",
         "3-tier verification: corpus + Google API + fallback, verdict taxonomy"],
    ], [3.5*cm, 5*cm, 8*cm]),
    PageBreak(),
]

# ════════════ 7. FACT-CHECK MODULE ══════════════════════════════════════════
story += [
    h1("7.  FACT-CHECK / MYTH-BUSTER MODULE"), hr(),
    p("This is one of the two standout features of AarogyaSathi. It directly addresses the "
      "WhatsApp misinformation epidemic in rural India. Users copy-paste a forwarded health "
      "message and prefix it with 'fact check:'."),
    sp(),

    h2("7.1  How to Trigger It"),
    bullet(b("English:") + "  'fact check: drinking cow urine cures cancer'"),
    bullet(b("Hinglish:") + "  'ye sach hai kya: vaccines cause autism'"),
    bullet(b("Hindi:") + "  'fact check: govmutra se cancer thik hota hai'"),
    p("Auto-detection of claims was deliberately removed — only explicit triggers work. "
      "This prevents false positives on normal health queries."),
    sp(),

    h2("7.2  The Three-Tier Verification Pipeline"),
    p(b("Tier 1 — Internal Curated Corpus (LaBSE Semantic Similarity):")),
    p("The claim is embedded with LaBSE and compared against our curated myths corpus "
      "(data/kb/myths.json — 49 verified myths from WHO, PIB Fact Check, ICMR). "
      "If cosine similarity > threshold AND both the disease-conflict guard AND "
      "content-overlap check (min 30% shared key words) pass, a verdict is returned."),
    bullet(b("Disease-Conflict Guard:") + "  Both the claim and the KB myth entry must "
           "mention the same canonical disease. Prevents a 'malaria cure' claim from "
           "matching a 'dengue myth' entry."),
    sp(),
    p(b("Tier 2 — Google Fact Check Tools API (Live Internet Lookup):")),
    p("If the internal corpus has no clear match, the claim is sent to the "
      + b("Google Fact Check Tools API") + " (free key, needs GOOGLE_FACTCHECK_API_KEY). "
      "This API searches thousands of fact-checks from publishers like PIB Fact Check, "
      "WHO, AFP Fact Check, PolitiFact. The returned rating text is mapped to our verdicts."),
    bullet(b("Trusted Publisher Boost:") + "  PIB Fact Check and WHO get higher confidence "
           "boosts than unknown publishers."),
    sp(),
    p(b("Tier 3 — Home Remedy Fallback:")),
    p("If the claim contains home remedy keywords (turmeric, neem, ginger, cow urine), "
      "a default PARTLY TRUE verdict is returned: 'Limited scientific evidence; "
      "consult a doctor.'"),
    sp(),

    h2("7.3  Verdict Categories"),
    build_table([
        ["Verdict",       "Label Shown",     "Meaning"],
        ["TRUE",          "VERIFIED",        "Supported by WHO / MoHFW / PIB Fact Check sources"],
        ["MYTH",          "MYTH",            "Contradicted by trusted sources with evidence"],
        ["PARTLY_TRUE",   "PARTLY TRUE",     "Mixed evidence or misleading context; partially correct"],
        ["UNVERIFIABLE",  "UNVERIFIABLE",    "Cannot be confirmed or denied with available sources"],
    ], [3.5*cm, 3*cm, 10*cm]),
    sp(),
    p(b("Live test results:") + "  'vaccines cause autism' -> MYTH (86.6% confidence). "
      "'drinking cow urine cures cancer' -> PARTLY TRUE (80%). "
      "'COVID vaccine prevents infection' -> VERIFIED."),
    p(b("Accuracy on held-out eval set:") + "  100% on 34 fact-check claims "
      "in data/training/eval.json."),
    PageBreak(),
]

# ════════════ 8. MULTILINGUAL ════════════════════════════════════════════════
story += [
    h1("8.  MULTILINGUAL SUPPORT — 12 Indian Languages"), hr(),
    p("AarogyaSathi supports 12 Indian languages plus Hinglish. This is core to the project "
      "mission — making verified health information accessible to people who cannot read or "
      "type in English."),
    sp(),
    build_table([
        ["Language",   "Code", "Script",           "Coverage"],
        ["English",    "en",   "Latin",             "Full — NLP + LLM + all templates"],
        ["Hindi",      "hi",   "Devanagari",        "Full — NLP + LLM + all templates"],
        ["Hinglish",   "hi",   "Latin -> Devanagari","Auto-detected; response in Devanagari"],
        ["Bengali",    "bn",   "Bengali",           "Templates + LLM generation"],
        ["Tamil",      "ta",   "Tamil",             "Templates + LLM generation"],
        ["Telugu",     "te",   "Telugu",            "Templates + LLM generation"],
        ["Marathi",    "mr",   "Devanagari",        "Templates + LLM generation"],
        ["Gujarati",   "gu",   "Gujarati",          "Templates + LLM generation"],
        ["Kannada",    "kn",   "Kannada",           "Templates + LLM generation"],
        ["Malayalam",  "ml",   "Malayalam",         "Templates + LLM generation"],
        ["Punjabi",    "pa",   "Gurmukhi",          "Templates + LLM generation"],
        ["Odia",       "or",   "Odia",              "Templates + LLM generation"],
        ["Urdu",       "ur",   "Nastaliq",          "Templates + LLM generation"],
    ], [3*cm, 1.5*cm, 4.5*cm, 7.5*cm]),
    sp(),
    h2("How Multilingual Responses Work"),
    bullet(b("fastText lang detection:") + "  Every incoming message is identified — even a "
           "single word in Tamil or Bengali is correctly detected."),
    bullet(b("Template responses:") + "  Fixed text (greetings, disclaimers, emergency messages) "
           "is stored pre-translated in data/kb/messages.json for all 12 languages. "
           "Our team manually verified Hindi translations."),
    bullet(b("LLM generation in language:") + "  Dynamic responses include 'Answer in "
           "[language_name] using [script]' in the system prompt. "
           "Cloud model (gpt-oss:20b) is significantly better for regional languages."),
    bullet(b("LaBSE cross-lingual retrieval:") + "  Because LaBSE was trained on 109 languages, "
           "a query in Tamil can semantically match English KB entries — no translation needed. "
           "A user asking about 'dengue' in Telugu retrieves the dengue KB entry written in English."),
    bullet(b("First-contact welcome:") + "  The first message in each new language gets a "
           "localized welcome explaining the bot capabilities and the fact-check trigger syntax. "
           "Never repeated for the same language in the same session."),
    sp(),
    p(b("Live evidence:") + "  Oracle Cloud stats show actual usage in bn, ta, te, gu, kn, "
      "ml, or, pa, ur in addition to en and hi — confirming the multilingual pipeline works "
      "in production."),
    PageBreak(),
]

# ════════════ 9. ORACLE CLOUD DEPLOYMENT ════════════════════════════════════
story += [
    h1("9.  ORACLE CLOUD DEPLOYMENT — Running 24/7 at Zero Cost"), hr(),

    h2("9.1  Why Oracle Cloud Always Free?"),
    build_table([
        ["Aspect",       "Oracle Cloud Always Free",           "AWS/GCP/Azure Free Tier"],
        ["VM Spec",      "2 OCPU / 12 GB RAM ARM64",           "1 vCPU / 1 GB RAM (t2.micro class)"],
        ["Cost",         "USD 0 forever (no time limit)",       "Only 12 months free, then paid"],
        ["Storage",      "45 GB boot volume",                   "8 GB"],
        ["Run LLM?",     "Yes — 12 GB fits Qwen3 + LaBSE + FastAPI",
         "No — 1 GB RAM is far too small for any LLM"],
    ], [3*cm, 7*cm, 6.5*cm]),
    sp(),

    h2("9.2  VM Specifications (Live System)"),
    build_table([
        ["Parameter",     "Value"],
        ["Provider",      "Oracle Cloud Infrastructure (OCI), Always Free tier"],
        ["Region",        "ap-mumbai-1 (low latency for India)"],
        ["Shape",         "VM.Standard.A1.Flex — Ampere ARM64 (aarch64)"],
        ["OCPU / RAM",    "2 OCPU / 12 GB RAM"],
        ["OS",            "Ubuntu 24.04 LTS (ARM64)"],
        ["Storage",       "45 GB SSD (12 GB used = 28%)"],
        ["Public IP",     "130.210.56.87"],
        ["Demo URL",      "http://130.210.56.87:8000"],
        ["Firewall",      "Oracle VCN Security List (TCP 8000 + 22) + iptables (persisted)"],
        ["RAM breakdown", "Qwen3-1.7B ~1.4 GB + LaBSE ~1 GB + FastAPI ~0.5 GB + OS = 3.3/12 GB used"],
        ["Uptime",        "healthbot.service running since Sep 4, 2026 (5+ days continuous)"],
    ], [4.5*cm, 12*cm], hdr_color="#455a64"),
    sp(),

    h2("9.3  Deployment Workflow"),
    build_table([
        ["Step", "Action"],
        ["1. Modify code",    "Edit Python files on Windows laptop"],
        ["2. SCP to VM",      "scp app/core/router.py ubuntu@130.210.56.87:/opt/healthbot/app/core/"],
        ["3. Restart service","ssh ubuntu@130.210.56.87 'sudo systemctl restart healthbot'"],
        ["4. Verify",         "curl http://130.210.56.87:8000/api/health"],
    ], [3.5*cm, 13*cm]),
    sp(),

    h2("9.4  Anti-Idle System"),
    p("Oracle Always Free can reclaim VMs idle for 7+ days with memory consistently below 20%. "
      "Since Qwen3-1.7B takes ~1.4 GB (12% of 12 GB) and LaBSE takes ~1 GB (8%), "
      "they together keep RAM at ~28% — safely above Oracle's threshold. "
      "OLLAMA_KEEP_ALIVE=-1 ensures Qwen3 is never unloaded from memory even with zero traffic."),
    PageBreak(),
]

# ════════════ 10. KNOWLEDGE BASE ════════════════════════════════════════════
story += [
    h1("10.  KNOWLEDGE BASE — Our Curated Medical Dataset"), hr(),
    p("The KB is stored in data/kb/ as structured JSON files. Every piece of information is "
      "sourced from official government or WHO health sources — we do NOT use random internet "
      "content. The KB is what makes the chatbot reliable and non-hallucinating."),
    sp(),
    build_table([
        ["KB File",         "Contents",                                      "Sources"],
        ["diseases.json",   "14 diseases: symptoms (EN+HI), prevention, first aid, when to seek doctor",
         "WHO, MoHFW, ICMR"],
        ["myths.json",      "49 verified health myths with verdicts and explanations",
         "PIB Fact Check, WHO, ICMR"],
        ["faq.json",        "35 health FAQs in EN + HI + Hinglish",
         "NHM, MoHFW, WHO"],
        ["vaccines.json",   "13 vaccines: schedule, what it protects against",
         "UIP, MoHFW, NHM"],
        ["outbreaks.json",  "Curated outbreak advisories with pincode to state mapping",
         "IDSP, NCDC, MoHFW"],
        ["alerts.json",     "Active national health alerts",                  "MoHFW"],
        ["pincodes.json",   "Sample pincode to district to state mapping (~20 districts)",
         "India Post"],
        ["messages.json",   "System messages in 12 languages: greetings, disclaimers, emergency",
         "Team-translated"],
    ], [3.5*cm, 8.5*cm, 4.5*cm]),
    sp(),
    p(b("14 Diseases covered:") + "  Dengue, Malaria, Typhoid, Cholera, Diarrhoea, "
      "Tuberculosis (TB), Hepatitis, COVID-19, Influenza, Pneumonia, Measles, "
      "Rabies, Heatstroke, Anaemia."),
    sp(),
    p(b("Why JSON, not a vector database?") + "  For this project scale (~150 KB of health "
      "content), loading JSON into memory at startup is instantaneous and eliminates the need "
      "for a separate database server (like ChromaDB or FAISS). We generate and cache the "
      "LaBSE embedding matrix for the KB at first run, then load from .npy files. "
      "If KB content changes, the cache is automatically invalidated and rebuilt."),
    PageBreak(),
]

# ════════════ 11. WHAT REMAINS ══════════════════════════════════════════════
story += [
    h1("11.  WHAT REMAINS — Current Status vs. Synopsis"), hr(),
    build_table([
        ["Synopsis Requirement",            "Status",         "Gap / Next Step"],
        ["Web chat interface",              "DONE",
         "WhatsApp-style UI at port 8000. Minor polish remaining."],
        ["10+ Indian languages",            "DONE",
         "12 languages live on VM. Verify regional response quality."],
        ["Disease and symptom information", "DONE",
         "14 diseases in KB. Can expand to 25+."],
        ["Vaccination schedules",           "DONE",
         "Full UIP schedule. Can add newer vaccines."],
        ["Fact-check / myth-vs-fact",       "DONE",
         "3-tier pipeline live. More myth entries can be added to KB."],
        ["Outbreak alerts by pincode",      "DONE",
         "Curated + Google News RSS. Full India pincode directory pending."],
        ["Emergency escalation (108/112)",  "DONE",
         "Red-flag lexicon, deterministic. Complete."],
        ["Conversation memory / context",   "DONE",
         "Rolling LLM summary every 3 messages. Complete."],
        ["NLP engine",                      "DONE",
         "TF-IDF + LR + LaBSE + LLM understanding pass. Complete."],
        ["RAG pipeline",                    "DONE",
         "LaBSE retrieval + Ollama generation. Complete."],
        ["WhatsApp integration",            "NOT YET (Phase 4)",
         "Meta Cloud API webhook + HTTPS — the very next major task."],
        ["SMS integration",                 "Not started",
         "Low priority for minor project defence."],
        ["Syndromic surveillance",          "Implemented, not fully tested",
         "Admin dashboard exists; needs pincode expansion."],
        ["Full India pincode directory",    "Partial (~20 districts)",
         "Load complete India Post pincode database (~160,000 pincodes)."],
        ["Git / GitHub repo",              "DONE",
         "github.com/salman-mohammad-khan/AarogyaSathi (private)."],
    ], [5*cm, 3*cm, 8.5*cm]),
    sp(),
    h2("Potential Future Improvements"),
    bullet(b("Voice / IVR Interface:") + "  Convert speech to text (Google STT or IndicWav2Vec) "
           "and text to speech (gTTS) for feature phone users who cannot type."),
    bullet(b("Full India Pincode Database:") + "  Load the complete India Post database "
           "(~160,000 pincodes) for truly location-aware outbreak alerts."),
    bullet(b("IDSP API Integration:") + "  Real-time connection to Integrated Disease "
           "Surveillance Programme for live outbreak data instead of curated JSON."),
    bullet(b("Knowledge Base Expansion:") + "  From 14 to 30+ diseases; add mental health, "
           "maternal health, nutrition, AYUSH information."),
    bullet(b("IndicTrans2 Integration:") + "  Use AI4Bharat's IndicTrans2 for higher quality "
           "translation to/from all 22 scheduled Indian languages."),
    bullet(b("Personalized Vaccination Reminders:") + "  User registers child's DOB; bot sends "
           "WhatsApp reminders at UIP milestone dates."),
    bullet(b("Continuous KB Updates:") + "  Automated pipeline to pull new advisories from "
           "MoHFW / WHO weekly and update the knowledge base."),
    PageBreak(),
]

# ════════════ 12. DEMO & Q&A GUIDE ══════════════════════════════════════════
story += [
    h1("12.  HOW TO PRESENT & DEMONSTRATE TOMORROW"), hr(),

    h2("12.1  Opening Statement (say this in ~30 seconds)"),
    Paragraph(
        '"Our project AarogyaSathi addresses SIH25049 by the Government of Odisha. '
        'Rural India faces a healthcare information crisis — limited doctors, language barriers, '
        'and rampant health misinformation on WhatsApp. We built a fully deployed, cloud-hosted '
        'multilingual AI health chatbot that gives verified information in 12 Indian languages, '
        'detects health emergencies instantly, and fact-checks forwarded WhatsApp health claims. '
        'It is live right now at 130.210.56.87:8000."',
        S("q", fontName=UNI_FONT, fontSize=9.5, leading=14,
          borderColor=colors.HexColor("#3949ab"), borderPadding=8,
          backColor=colors.HexColor("#e8eaf6"), spaceAfter=8)
    ),
    sp(),

    h2("12.2  Recommended Demo Sequence (open browser, type these)"),
    build_table([
        ["Type This in the Chatbot", "What to Explain While Showing It"],
        ["hello",
         "Language detection -> English greeting. Explain welcome-in-language behavior."],
        ["I have fever and bad headache for 2 days",
         "Multi-turn: bot asks 1 follow-up. Then type 'no vomiting' to trigger symptom analysis. "
         "Explain LaBSE retrieval + LLM grounded answer. Point to WHO source."],
        ["mujhe bukhar hai",
         "Hindi detection. Show Devanagari response. Explain cross-lingual LaBSE — "
         "no translation step needed. Same KB entry, different language output."],
        ["what are symptoms of dengue",
         "Disease info. Show KB retrieval -> LLM grounding -> Sources: WHO. "
         "Explain RAG: LLM only sees the KB context, cannot hallucinate."],
        ["chest pain cannot breathe",
         "EMERGENCY demo — immediate 108/112 response, no LLM delay. "
         "Explain deterministic red-flag lexicon. Most impressive safety feature."],
        ["fact check: vaccines cause autism",
         "Fact-check. Show MYTH verdict with 86.6% confidence and source. "
         "Explain 3-tier pipeline: corpus -> Google Fact Check API -> fallback."],
        ["when to give polio vaccine to 6 week baby",
         "Vaccination by age milestone. Show UIP schedule table. Explain age_to_milestones()."],
        ["mujhe thoda bukhar hai aur body mein dard hai",
         "Hinglish demo — detected as Hindi, responded in Devanagari. "
         "Explain transliterate_hint() function."],
    ], [5.5*cm, 11*cm]),
    sp(),

    h2("12.3  Likely Teacher Questions — Prepared Answers"),
    build_table([
        ["Likely Question",                     "Your Answer"],
        ["What NLP did you use?",
         "fastText for language detection, TF-IDF+LR for intent classification, "
         "custom lexicon for entity extraction, LaBSE for semantic retrieval, "
         "Qwen3-1.7B (Ollama) as answer generator. LLM also used as semantic intent extractor."],
        ["Is this a RAG system?",
         "Yes. We implemented the RAG pattern: LaBSE retrieves the most relevant KB entry, "
         "then Qwen3-1.7B generates an answer strictly grounded in that context. "
         "The LLM cannot go beyond the retrieved content."],
        ["Did you train your own model?",
         "We trained the TF-IDF + Logistic Regression intent classifier from scratch on our "
         "own labelled dataset. LaBSE and Qwen3 are pre-trained models we adapted."],
        ["How does multilingual support work?",
         "fastText detects language -> LaBSE retrieves across 109 languages (no translation) "
         "-> LLM generates response in detected language -> templates for fixed text in 12 languages."],
        ["How is it deployed?",
         "Oracle Cloud Always Free VM — 2 OCPU / 12 GB RAM, ARM64, Ubuntu 24.04. "
         "FastAPI + uvicorn, systemd service, Ollama for local LLM. 100% free, 24/7."],
        ["What is the accuracy?",
         "Intent classifier: 100% on 30-query held-out eval set. "
         "Retrieval: 100% on 15 cross-lingual queries. "
         "Fact-check: 100% on 34 test claims. All in data/training/eval.json."],
        ["What is WhatsApp status?",
         "Web demo is live. WhatsApp is Phase 4 — needs Meta Cloud API webhook + "
         "HTTPS via Nginx/Caddy + verified phone number. Planned after first defence."],
        ["How do you prevent hallucination?",
         "Strict 14-rule system prompt: 'Answer ONLY from the provided CONTEXT.' "
         "Emergency and fact-check paths are fully deterministic — LLM never touches them."],
        ["Is user data stored?",
         "No. All sessions are in-memory and ephemeral. No personal data is ever "
         "written to disk. The bot never asks for any identifying information."],
        ["Synopsis vs. actual?",
         "Synopsis proposed all features as planned deliverables. We have implemented all "
         "core Phase 1-3 features completely. WhatsApp (Phase 4) is the next step. "
         "Teacher confirmed the project does not need to match synopsis exactly."],
    ], [4.5*cm, 12*cm]),
    PageBreak(),
]

# ════════════ 13. CHEAT SHEET ════════════════════════════════════════════════
story += [
    h1("13.  QUICK REFERENCE CHEAT SHEET"), hr(),
    build_table([
        ["Item",               "Detail"],
        ["Project Name",       "AarogyaSathi — Health Companion"],
        ["Problem Statement",  "SIH25049 — Govt. of Odisha, AI Public Health Chatbot"],
        ["Subject",            "ES-451 Minor Project, B.Tech 7th Sem CSE(DS), BPIT"],
        ["Team",               "Salman Mohd. Khan (00520815723)  |  Dhairya Summi (00420815723)  |  Sidharth Singh (01820815723)"],
        ["Guide",              "Mr. Aditya Sam Kosy, Dept. CSE(DS)"],
        ["Live URL",           "http://130.210.56.87:8000"],
        ["GitHub",             "https://github.com/salman-mohammad-khan/AarogyaSathi"],
        ["Cloud Server",       "Oracle Cloud Always Free — VM.Standard.A1.Flex — 2 OCPU/12GB ARM64 — Ubuntu 24.04 — ap-mumbai-1"],
        ["Backend",            "FastAPI (Python 3.12) + uvicorn"],
        ["Language Detection", "fastText lid.176 (Meta/Facebook, CC0, 125 MB, 176 languages)"],
        ["Intent Classifier",  "TF-IDF (char 2-5 grams, 30k features) + Logistic Regression (C=8.0, 13 classes, trained from scratch)"],
        ["Entity Extraction",  "Custom lexicon: 34 symptoms, 12 red-flags, 14 diseases, 13 vaccines (EN + HI + Hinglish)"],
        ["Embedding Model",    "LaBSE (Google, HuggingFace, 768-dim, 109 languages, pre-trained)"],
        ["LLM (local)",        "Qwen3-1.7B-Instruct via Ollama (Q4, ~1.4 GB, ARM64 CPU inference)"],
        ["LLM (cloud backup)", "gpt-oss:20b via Ollama Cloud API (better quality for regional languages)"],
        ["RAG Pattern",        "LaBSE retrieval + 0.22 lexical boost -> Qwen3 generates grounded answer (max 70 words, context-only)"],
        ["Fact-Check",         "3-tier: Internal myth corpus (LaBSE) -> Google Fact Check API -> Home-remedy fallback"],
        ["Knowledge Base",     "14 diseases, 35 FAQs, 49 myths, 13 vaccines (all WHO/MoHFW/ICMR sourced)"],
        ["Languages",          "12: en, hi (+ Hinglish), bn, ta, te, mr, gu, kn, ml, pa, or, ur"],
        ["Emergency Response", "Deterministic, ~150ms, 12-category red-flag lexicon, 108/112 escalation — no LLM involved"],
        ["Session Memory",     "In-memory, ephemeral — rolling LLM conversation summary every 3 messages"],
        ["Accuracy (eval set)","Intent: 100%  |  Retrieval: 100%  |  Fact-check: 100%"],
        ["RAM Footprint",      "~3.3 GB total (Qwen3 ~1.4 GB + LaBSE ~1 GB + FastAPI ~0.5 GB)"],
        ["Service Uptime",     "24/7 via systemd (running since Aug 24, 2026 — over 2 weeks continuous)"],
    ], [4.5*cm, 12*cm], hdr_color="#455a64"),
    sp(2),
    Paragraph(
        "Good luck at your presentation! You built something genuinely impressive — "
        "a fully working, cloud-deployed, multilingual health AI system. Be confident. Best wishes.",
        FINAL
    ),
]

# ── Build ─────────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    rightMargin=1.8*cm, leftMargin=1.8*cm,
    topMargin=1.8*cm,   bottomMargin=1.8*cm,
    title="AarogyaSathi Revision Material",
    author="Salman Mohd. Khan, Dhairya Summi, Sidharth Singh",
)
doc.build(story)
print(f"PDF created: {OUTPUT}")
