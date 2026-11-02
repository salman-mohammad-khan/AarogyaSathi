"""Builds the AarogyaSathi second-defense deck (16:9) with python-pptx."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "report", "source", "assets")
PHONE = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "AarogyaSathi_Second_Defense_Presentation.pptx")

DARK, TEAL, MINT = "0E3B43", "1F8A70", "E3F3EE"
SAFFRON, INK, MUTED, BG, WHITE, RED, LINE = "F2A541", "1B2B2F", "5B6B70", "F7FBFA", "FFFFFF", "C2412D", "CFE3DC"
HEAD, BODY = "Cambria", "Calibri"


def rgb(h):
    return RGBColor.from_string(h)


prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
_count = [0]


def shape(slide, kind, x, y, w, h, fill=None, line=None, lw=1.0, name=None, radius=None):
    s = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = rgb(fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(lw)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    if radius is not None and kind == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    if name:
        s.name = name
    return s


def text(slide, x, y, w, h, runs, size=16, color=INK, bold=False, font=BODY, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, italic=False, name=None, spacing=None):
    """runs: str, or list of paragraphs; a paragraph is str or list of (text, {opts})."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    paras = runs if isinstance(runs, list) else [runs]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if spacing:
            p.space_after = Pt(spacing)
        parts = para if isinstance(para, list) else [(para, {})]
        for t, o in parts:
            r = p.add_run()
            r.text = t
            f = r.font
            f.name = o.get("font", font)
            f.size = Pt(o.get("size", size))
            f.bold = o.get("bold", bold)
            f.italic = o.get("italic", italic)
            f.color.rgb = rgb(o.get("color", color))
    if name:
        tb.name = name
    return tb


def card_text(slide, shp, runs, size=14, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE, pad=0.15, bold=False, font=BODY):
    tf = shp.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(pad)
    tf.margin_top = tf.margin_bottom = Inches(0.08)
    tf.vertical_anchor = anchor
    paras = runs if isinstance(runs, list) else [runs]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        parts = para if isinstance(para, list) else [(para, {})]
        for t, o in parts:
            r = p.add_run()
            r.text = t
            r.font.name = o.get("font", font)
            r.font.size = Pt(o.get("size", size))
            r.font.bold = o.get("bold", bold)
            r.font.italic = o.get("italic", False)
            r.font.color.rgb = rgb(o.get("color", color))


def new_slide(title=None, notes="", dark=False, kicker=None):
    s = prs.slides.add_slide(BLANK)
    _count[0] += 1
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = rgb(DARK if dark else BG)
    if title:
        if kicker:
            text(s, 0.6, 0.38, 10, 0.3, kicker.upper(), size=12, color=TEAL, bold=True, name="Kicker")
        text(s, 0.6, 0.62, 12.1, 0.8, title, size=34, bold=True, font=HEAD, color=WHITE if dark else INK, name="Title")
    if not dark:
        text(s, 0.6, 7.08, 8, 0.25, "AarogyaSathi  |  Minor Project ES-451  |  BPIT, CSE-DS", size=10, color=MUTED, name="Footer")
        text(s, 12.0, 7.08, 0.73, 0.25, str(_count[0]), size=10, color=MUTED, align=PP_ALIGN.RIGHT, name="SlideNo")
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def pic(slide, name, x, y, w=None, h=None, folder=None):
    path = os.path.join(folder or ASSETS, name)
    kw = {}
    if w:
        kw["width"] = Inches(w)
    if h:
        kw["height"] = Inches(h)
    return slide.shapes.add_picture(path, Inches(x), Inches(y), **kw)


def badge(slide, x, y, d, label, fill=TEAL, color=WHITE, size=20):
    c = shape(slide, MSO_SHAPE.OVAL, x, y, d, d, fill=fill)
    card_text(slide, c, label, size=size, color=color, align=PP_ALIGN.CENTER, bold=True, pad=0.02, font=HEAD)
    return c


def arrow(slide, x, y, w=0.4, h=0.3, fill=SAFFRON):
    return shape(slide, MSO_SHAPE.RIGHT_ARROW, x, y, w, h, fill=fill)


# ------------------------------------------------------------------ 1 title
s = new_slide(dark=True, notes=(
    "Good morning. We are presenting AarogyaSathi, an AI-driven public health chatbot for disease awareness, built for Smart India Hackathon "
    "problem statement SIH25049. It is deployed on Oracle Cloud and reachable on the web and on WhatsApp through a Meta test number. "
    "It is an awareness tool: it does not diagnose or prescribe."))
shape(s, MSO_SHAPE.OVAL, 9.4, -1.2, 6.2, 6.2, fill="124C56")
shape(s, MSO_SHAPE.OVAL, 10.6, 4.2, 3.6, 3.6, fill="0B3139")
text(s, 0.8, 0.9, 9, 0.4, "MINOR PROJECT (ES-451)  |  SECOND DEFENSE", size=14, color=SAFFRON, bold=True)
text(s, 0.8, 1.7, 9.6, 2.2, [[("AarogyaSathi", {"size": 60, "bold": True, "font": HEAD, "color": WHITE})],
                              [("AI-Driven Public Health Chatbot for Disease Awareness", {"size": 28, "color": "BFE3D8", "font": HEAD})]], name="Title")
text(s, 0.8, 4.35, 8.4, 1.6, [
    [("Salman Mohammad Khan", {"bold": True}), ("  (00520815723)", {"color": "9FC7BC"})],
    [("Dhairya Summi", {"bold": True}), ("  (00420815723)", {"color": "9FC7BC"})],
    [("Sidharth Singh", {"bold": True}), ("  (01820815723)", {"color": "9FC7BC"})]], size=18, color=WHITE, spacing=4)
text(s, 0.8, 6.0, 9, 0.9, [[("Under the supervision of ", {"color": "9FC7BC"}), ("Mr. Aditya Sam Koshy", {"bold": True}), (", Assistant Professor, CSE", {"color": "9FC7BC"})],
                           [("Bhagwan Parshuram Institute of Technology, Delhi  |  November 2026", {"color": "9FC7BC"})]], size=14, color=WHITE, spacing=3)

# ------------------------------------------------------------------ 2 problem
s = new_slide("Why this problem matters", kicker="Problem", notes=(
    "Health information reaches people mainly through forwarded messages. Good guidance exists from WHO and MoHFW, but it is often in formal English, "
    "and people cannot easily check whether a claim is true or whether a symptom is urgent. SIH25049 from the Government of Odisha asks for an AI chatbot "
    "for disease awareness; that is the brief we answered."))
items = [("1", "Myths spread fast", "Home remedies and myths spread in forwarded messages, with no quick way to check them."),
         ("2", "Language and access gaps", "Official health guidance is mostly in formal English or Hindi, hard to use in regional languages."),
         ("3", "Unclear urgency", "People struggle to tell routine symptoms from emergencies, and care is delayed or skipped.")]
for i, (n, t, d) in enumerate(items):
    x = 0.6 + i * 4.1
    c = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 1.75, 3.85, 3.3, fill=WHITE, line=LINE, radius=0.06)
    badge(s, x + 0.3, 2.05, 0.7, n, fill=TEAL, size=22)
    text(s, x + 0.3, 3.0, 3.3, 0.5, t, size=20, bold=True, font=HEAD)
    text(s, x + 0.3, 3.6, 3.3, 1.4, d, size=15, color=MUTED)
b = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.6, 5.45, 12.1, 1.2, fill=MINT, radius=0.1)
card_text(s, b, [[("The brief: ", {"bold": True, "color": DARK}),
                  ("Smart India Hackathon SIH25049 (Government of Odisha) asks for an AI-driven chatbot that gives verified preventive-health information, "
                   "symptom awareness, vaccination schedules, outbreak alerts and health-claim verification over WhatsApp and SMS.", {})]], size=16, pad=0.3)

# ------------------------------------------------------------------ 3 objectives
s = new_slide("Objectives and scope", kicker="What we set out to do", notes=(
    "We set five objectives. The important boundary is on the right: AarogyaSathi gives awareness information with sources and disclaimers. "
    "It does not diagnose, prescribe, or replace a doctor, and we state that on every answer."))
objs = ["Answer disease, prevention and vaccination questions from a curated knowledge base",
        "Understand queries across languages, with English and Hindi strongest",
        "Check forwarded health claims and return a verdict with an explanation",
        "Escalate emergency phrases to 108 / 112 without waiting for a model",
        "Reach people on the web and on WhatsApp, with simple outbreak signals by pincode"]
for i, o in enumerate(objs):
    y = 1.7 + i * 1.0
    badge(s, 0.6, y, 0.6, str(i + 1), size=18)
    text(s, 1.45, y + 0.02, 6.6, 0.8, o, size=17, anchor=MSO_ANCHOR.MIDDLE)
box = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 8.5, 1.7, 4.2, 4.85, fill=DARK, radius=0.05)
text(s, 8.85, 1.95, 3.5, 0.4, "Scope boundaries", size=20, bold=True, font=HEAD, color=SAFFRON)
text(s, 8.85, 2.6, 3.5, 3.8, [
    [("Awareness only. ", {"bold": True}), ("No diagnosis, no dosage or prescriptions.", {})],
    [("Grounded answers. ", {"bold": True}), ("Sources and a disclaimer on every reply.", {})],
    [("Prototype. ", {"bold": True}), ("Demonstrated on the web and a WhatsApp test number, not a public service.", {})]],
     size=16, color=WHITE, spacing=14)

# ------------------------------------------------------------------ 4 features
s = new_slide("What AarogyaSathi does", kicker="Features", notes=(
    "Eight capabilities. The numbers in the circles are real counts from our knowledge base: 14 disease profiles, 13 vaccine entries, 64 myth records, "
    "and 12 language codes detected. We are careful here: language detection covers twelve codes, but answer quality is strongest in English and Hindi."))
feats = [("14", "Disease profiles", "Symptoms, prevention, when to see a doctor, with sources"),
         ("13", "Vaccine entries", "Immunisation schedule lookups by age and pregnancy"),
         ("64", "Myth records", "Fact-check verdicts: Verified, Myth, Partly true, Unverifiable"),
         ("12", "Language codes", "Detected and welcomed; English and Hindi strongest"),
         ("1", "Symptom flow", "Asks one clarifying question before suggesting conditions"),
         ("108", "Emergency path", "Red-flag phrases go straight to 108 / 112 advice"),
         ("7d", "Outbreak signals", "Pincode symptom counts vs a 7-day baseline"),
         ("2", "Channels", "Web chat and WhatsApp (approved test number)")]
for i, (n, t, d) in enumerate(feats):
    col, row = i % 4, i // 4
    x, y = 0.6 + col * 3.07, 1.7 + row * 2.65
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, 2.88, 2.45, fill=WHITE, line=LINE, radius=0.06)
    badge(s, x + 0.2, y + 0.2, 0.72, n, fill=TEAL if row == 0 else DARK, size=18 if len(n) < 3 else 15)
    text(s, x + 0.2, y + 1.05, 2.5, 0.4, t, size=17, bold=True, font=HEAD)
    text(s, x + 0.2, y + 1.5, 2.5, 0.9, d, size=14, color=MUTED)

# ------------------------------------------------------------------ 5 pipeline
s = new_slide("How one message is handled", kicker="Architecture", notes=(
    "Every message passes the same ordered pipeline. First three gates are deterministic: an emergency check, a fact-check trigger, and fast-path rules "
    "that combine a TF-IDF intent classifier with entity matching. If none resolves it, LaBSE multilingual embeddings retrieve the right records from the "
    "knowledge base, and the local Qwen3 1.7B model writes a short answer using only that context. If the model is unavailable we fall back to templates. "
    "The emergency and fact-check results are never rewritten by the model."))
steps = [("Incoming message", "Web or WhatsApp", DARK),
         ("1  Emergency check", "Red-flag phrases to 108 / 112", RED),
         ("2  Fact-check trigger", "'fact check:' prefix or myth match", "B7791F"),
         ("3  Fast-path rules", "TF-IDF intent + entity matching", TEAL),
         ("4  Semantic retrieval", "LaBSE embeddings + lexical overlap", "3D5A80"),
         ("5  Answer generation", "Qwen3-1.7B via Ollama, or template", "3D5A80"),
         ("6  Reply", "Sources and disclaimer attached", TEAL)]
xs = [0.6, 3.72, 6.84, 9.96]
for k, (t, d, f) in enumerate(steps):
    px, py = (xs[k], 1.75) if k < 4 else (xs[k - 4], 4.35)
    b = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, px, py, 2.75, 1.65, fill=f, radius=0.08)
    card_text(s, b, [[(t, {"size": 18, "bold": True, "font": HEAD})], [(d, {"size": 14})]], color=WHITE, pad=0.2)
for k in (0, 1, 2):
    arrow(s, xs[k] + 2.78, 2.45, 0.32, 0.28)
for k in (0, 1):
    arrow(s, xs[k] + 2.78, 5.05, 0.32, 0.28)
shape(s, MSO_SHAPE.RECTANGLE, 11.3, 3.4, 0.06, 0.45, fill=SAFFRON)
shape(s, MSO_SHAPE.RECTANGLE, 1.95, 3.82, 9.41, 0.06, fill=SAFFRON)
shape(s, MSO_SHAPE.DOWN_ARROW, 1.78, 3.82, 0.4, 0.5, fill=SAFFRON)
nb = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 9.96, 4.35, 2.75, 1.65, fill=MINT, radius=0.08)
card_text(s, nb, [[("Steps 1 to 3 are deterministic", {"bold": True, "color": DARK, "size": 15})], [("The language model never rewrites the emergency or fact-check results.", {"size": 13, "color": MUTED})]], pad=0.2)
text(s, 0.6, 6.3, 12.1, 0.5, "Each message is checked for safety first; the language model is used only when the rules cannot answer.", size=15, color=MUTED, italic=True)

# ------------------------------------------------------------------ 6 stack and deployment
s = new_slide("Technology and deployment", kicker="Implementation", notes=(
    "The whole system runs on one Oracle Cloud Arm virtual machine with 2 OCPUs and 12 GiB RAM. FastAPI serves the web UI and the API. LaBSE and Qwen3 1.7B "
    "run locally, and SQLite stores only anonymous counts. A Cloudflare tunnel gives Meta an HTTPS address for the WhatsApp webhook. "
    "We verified that the deployed files match our local code by comparing hashes."))
rows = [("Backend", "Python 3.12, FastAPI, Uvicorn"), ("NLP and ML", "scikit-learn (TF-IDF + logistic regression), PyTorch, Transformers"),
        ("Retrieval", "LaBSE multilingual sentence embeddings"), ("Answer model", "Qwen3-1.7B served locally by Ollama"),
        ("Storage", "SQLite for counts, JSON knowledge base, in-memory sessions"), ("Channels", "Web chat UI, Meta WhatsApp Cloud API")]
for i, (k, v) in enumerate(rows):
    y = 1.7 + i * 0.82
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.6, y, 6.3, 0.7, fill=WHITE, line=LINE, radius=0.12)
    text(s, 0.8, y, 1.7, 0.7, k, size=14, bold=True, color=TEAL, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 2.5, y, 4.3, 0.7, v, size=14, anchor=MSO_ANCHOR.MIDDLE)
vm = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 7.5, 1.7, 5.2, 3.3, fill=DARK, radius=0.05)
text(s, 7.8, 1.85, 4.6, 0.4, "Oracle Cloud VM (Arm, 2 OCPU, 12 GiB)", size=16, bold=True, font=HEAD, color=SAFFRON)
for j, lab in enumerate(["FastAPI app + router", "LaBSE + intent model", "Ollama: Qwen3-1.7B", "SQLite + JSON knowledge base"]):
    b = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 7.8 + (j % 2) * 2.3, 2.55 + (j // 2) * 1.2, 2.15, 1.0, fill="1A5560", radius=0.1)
    card_text(s, b, lab, size=14, color=WHITE, align=PP_ALIGN.CENTER)
b = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 7.5, 5.3, 2.45, 0.9, fill=TEAL, radius=0.1)
card_text(s, b, "Cloudflare HTTPS tunnel", size=14, color=WHITE, align=PP_ALIGN.CENTER, bold=True)
b = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 10.25, 5.3, 2.45, 0.9, fill="3D5A80", radius=0.1)
card_text(s, b, "Meta WhatsApp Cloud API", size=14, color=WHITE, align=PP_ALIGN.CENTER, bold=True)
arrow(s, 9.98, 5.58, 0.25, 0.3, fill=SAFFRON)
shape(s, MSO_SHAPE.UP_ARROW, 8.55, 5.0, 0.3, 0.3, fill=SAFFRON)
text(s, 0.6, 6.7, 6.3, 0.3, "Deployed files verified identical to the local project by hash comparison.", size=12, color=MUTED, italic=True)

# ------------------------------------------------------------------ 7 web demo
s = new_slide("Live on the web: three real responses", kicker="Demo", notes=(
    "These are captures from the web interface running on our Oracle server. Left: a disease question about dengue returns symptoms, sources and the "
    "disclaimer. Middle: a forwarded claim, 'garlic cures dengue', is checked and returns a MYTH verdict with an explanation; the percentage shown is a heuristic score, "
    "not a calibrated probability. Right: a Hindi malaria question is answered in Hindi. If time allows, we will run one of these live."))
shots = [("02_dengue_response.png", "Disease information", "Symptoms, sources and a disclaimer"),
         ("03_factcheck_myth.png", "Claim check", "MYTH verdict with explanation"),
         ("04_hindi_malaria.png", "Hindi answer", "Language detected as Hindi")]
for i, (f, cap, sub) in enumerate(shots):
    x = 0.6 + i * 2.95
    pic(s, f, x, 1.6, h=4.55)
    text(s, x, 6.25, 2.7, 0.3, cap, size=14, bold=True)
    text(s, x, 6.55, 2.7, 0.3, sub, size=12, color=MUTED)
shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 9.65, 1.6, 3.05, 4.55, fill=MINT, radius=0.06)
text(s, 9.9, 1.8, 2.6, 0.4, "What to notice", size=18, bold=True, font=HEAD, color=DARK)
text(s, 9.9, 2.4, 2.6, 3.6, ["Every answer names its sources", "A disclaimer says it is not a doctor", "Verdict labels: Verified, Myth, Partly true, Unverifiable",
                             "Confidence is a heuristic score, not a probability"], size=14, spacing=10)

# ------------------------------------------------------------------ 8 whatsapp
s = new_slide("WhatsApp channel", kicker="Integration", notes=(
    "The WhatsApp channel uses Meta's Cloud API on a test number. Meta sends each message to our webhook; we check the HMAC signature, acknowledge with 200 straight away, "
    "and process in the background. On 31 October three test messages from an approved phone were answered, and the server logs showed no sending errors. "
    "Be clear: this is a restricted test number, so only registered recipients can use it; it is not a public production bot."))
flow = [("Phone", "Approved test recipient", "1F8A70"), ("Meta Cloud API", "Delivers the webhook", "3D5A80"),
        ("Cloudflare tunnel", "HTTPS to the VM", "B7791F"), ("AarogyaSathi", "Verify, ack, process, reply", DARK)]
for i, (t, d, f) in enumerate(flow):
    x = 0.6 + i * 3.1
    b = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 1.7, 2.6, 1.4, fill=f, radius=0.08)
    card_text(s, b, [[(t, {"size": 17, "bold": True, "font": HEAD})], [(d, {"size": 12})]], color=WHITE, align=PP_ALIGN.CENTER)
    if i < 3:
        arrow(s, x + 2.65, 2.25, 0.4, 0.3)
pts = [("Signed webhooks", "HMAC-SHA256 check; unsigned requests get HTTP 403"), ("Fast acknowledgement", "200 returned first; reply sent from a background task"),
       ("Evidence", "3 messages from an approved phone answered; 0 sending errors in the logs"), ("Scope", "Runs on a Meta test number, available to approved test recipients")]
for i, (t, d) in enumerate(pts):
    y = 3.55 + i * 0.85
    badge(s, 0.6, y + 0.05, 0.5, str(i + 1), size=14, fill=TEAL if i < 3 else SAFFRON, color=WHITE if i < 3 else DARK)
    text(s, 1.3, y, 5.0, 0.8, [[(t + "  ", {"bold": True, "color": DARK}), (d, {"color": MUTED})]], size=14, anchor=MSO_ANCHOR.MIDDLE)
phone = [("wa_hi.jpeg", "1. hi"), ("wa_dengue.jpeg", "2. What are dengue symptoms?"), ("wa_factcheck.jpeg", "3. Fact check: garlic cures dengue")]
px = 6.75
for fn, cap in phone:
    p = pic(s, fn, px, 3.4, h=2.95, folder=PHONE)
    w_in = p.width / 914400
    text(s, px, 6.45, max(w_in, 1.7), 0.5, cap, size=11, color=MUTED)
    px += w_in + 0.12

# ------------------------------------------------------------------ 9 surveillance
s = new_slide("Early-warning signals by pincode", kicker="Surveillance", notes=(
    "Users can optionally add a pincode. The system counts symptom reports per pincode and compares the last 24 hours with a seven-day baseline. "
    "An alert is raised when the count is at least six and at least three times the baseline. The figure on screen is the admin dashboard with demonstration data. "
    "Important: these are chatbot counts, not confirmed disease cases, and we do not have a live government data feed."))
pic(s, "05_admin_dashboard.png", 0.6, 1.65, w=6.6)
text(s, 0.6, 6.4, 6.6, 0.3, "Admin dashboard (/admin), populated with demonstration data", size=12, color=MUTED, italic=True)
b = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 7.6, 1.65, 5.1, 2.35, fill=DARK, radius=0.05)
text(s, 7.9, 1.85, 4.5, 0.4, "Alert rule", size=18, bold=True, font=HEAD, color=SAFFRON)
text(s, 7.9, 2.4, 4.5, 1.5, [[("count in last 24 h  >=  6", {"font": "Consolas", "size": 14})],
                             [("and  >=  3 x the 7-day baseline", {"font": "Consolas", "size": 14})],
                             [("(or baseline below 1)", {"font": "Consolas", "size": 14})]], size=14, color=WHITE, spacing=4)
text(s, 7.6, 4.3, 5.1, 2.4, [[("How the dashboard works", {"bold": True, "color": DARK, "size": 16, "font": HEAD})],
                             "Symptom reports are counted per 6-digit pincode and symptom.",
                             "Each count is compared with a rolling 7-day baseline.",
                             "Spikes appear on the admin dashboard next to curated health advisories."], size=14, color=MUTED, spacing=6)

# ------------------------------------------------------------------ 10 testing
s = new_slide("Testing and results", kicker="Evaluation", notes=(
    "37 automated tests passed on 26 October, and five WhatsApp security tests added later also passed, so 42 now. On our supplied evaluation sets we got 30 of 30 for intent, "
    "15 of 15 for retrieval and 34 of 34 for claim verdicts. We want to be upfront: these are our own development sets, 14 of the 30 intent questions also appear in the "
    "training data, and the benchmark thresholds differ from production. So we treat them as evidence the components work, not as real-world accuracy."))
stats = [("42", "automated tests passed", "37 on 26 Oct + 5 channel security tests"), ("30/30", "intent labels", "TF-IDF + logistic regression"),
         ("15/15", "retrieval top-1", "LaBSE + lexical overlap"), ("34/34", "claim verdicts", "mean 387 ms per claim")]
for i, (n, t, d) in enumerate(stats):
    x = 0.6 + i * 3.07
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 1.7, 2.88, 2.7, fill=WHITE, line=LINE, radius=0.06)
    text(s, x + 0.2, 1.9, 2.5, 0.9, n, size=44, bold=True, font=HEAD, color=TEAL)
    text(s, x + 0.2, 2.9, 2.5, 0.4, t, size=16, bold=True)
    text(s, x + 0.2, 3.4, 2.5, 0.8, d, size=14, color=MUTED)
b = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.6, 4.75, 12.1, 1.95, fill=MINT, radius=0.06)
text(s, 0.95, 4.95, 11.4, 0.4, "How to read these numbers", size=18, bold=True, font=HEAD, color=DARK)
text(s, 0.95, 5.45, 11.4, 1.2, ["Evaluation sets were written by the team: 14 of 30 intent questions also appear in the training data.",
                                "Benchmark thresholds differ from production (intent 0.45 vs 0.55; retrieval top-3 / 0.35 vs top-5 / 0.52).",
                                "Claim set is imbalanced: 24 MYTH, 4 TRUE, 5 PARTLY TRUE, 1 UNVERIFIABLE."], size=14, spacing=4)

# ------------------------------------------------------------------ 11 findings
s = new_slide("What whole-conversation testing found", kicker="Quality assurance", notes=(
    "Live spot checks found three real problems that the benchmarks missed. One: 'I have no chest pain, only a mild headache' triggered an emergency reply, "
    "because the red-flag matcher does not understand negation, and that reply also included unrelated snakebite advice. Two: a code defect maps a 2-month-old to the "
    "9 to 12 month vaccine bucket. Three: an Odia question fell back to a generic apology."))
fnd = [("Negation in emergency phrases", "'No chest pain, only a mild headache' triggered an emergency reply, with unrelated snakebite advice."),
       ("Vaccine age mapping", "Code maps ages in months to the 9 to 12 month bucket and 1 year to the 5 to 6 year bucket."),
       ("Regional-language gap", "An Odia prevention question fell back to a generic answer after 11.4 s.")]
for i, (t, d) in enumerate(fnd):
    x = 0.6 + i * 4.1
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 1.7, 3.85, 3.2, fill=WHITE, line=LINE, radius=0.05)
    badge(s, x + 0.25, 1.95, 0.6, str(i + 1), fill=RED, size=18)
    text(s, x + 0.25, 2.8, 3.4, 0.7, t, size=18, bold=True, font=HEAD)
    text(s, x + 0.25, 3.55, 3.4, 1.9, d, size=16, color=MUTED)
b = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.6, 5.2, 12.1, 0.75, fill=MINT, radius=0.15)
card_text(s, b, [[("Why this matters: ", {"bold": True, "color": DARK}), ("passing benchmarks did not show these faults. Only whole-conversation testing did.", {})]], size=15, pad=0.3)

# ------------------------------------------------------------------ 12 privacy, security, limits
s = new_slide("Privacy, security and deployment limits", kicker="Responsible engineering", notes=(
    "On privacy: the database stores only pincode, symptom, intent, language and verdict, not message text, names or phone numbers; conversation state lives in memory and expires after 30 minutes. "
    "On security: WhatsApp webhooks are verified with HMAC-SHA256. On limits: the tunnel address is temporary, there is no durable retry queue, and we have not run load tests. "
    "These are the gaps between a prototype and a public service."))
left = [("Built in", TEAL, ["Webhook signatures verified with HMAC-SHA256", "No message text, names or phone numbers in the database", "Sessions held in memory and expire after 30 minutes",
                            "Disclaimer and sources on every answer"]),
        ("Deployment scope", SAFFRON, ["Demonstration tunnel address", "WhatsApp through an approved test number", "Not load-tested; no uptime study",
                                  "Answers not clinically reviewed"])]
for i, (h, col, lines) in enumerate(left):
    x = 0.6 + i * 6.15
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 1.7, 5.95, 4.6, fill=WHITE, line=LINE, radius=0.04)
    badge(s, x + 0.3, 1.95, 0.55, "+" if i == 0 else "i", fill=col, size=20, color=WHITE if i == 0 else DARK)
    text(s, x + 1.05, 2.0, 4.5, 0.5, h, size=22, bold=True, font=HEAD)
    text(s, x + 0.35, 2.85, 5.3, 3.4, lines, size=18, spacing=14)

# ------------------------------------------------------------------ 14 conclusion
s = new_slide(dark=True, notes=(
    "To conclude: we built and deployed a working multilingual public-health awareness chatbot with a safety-first routing design, a claim checker, and a WhatsApp channel, "
    "and we tested it honestly, including the failures. We are happy to run a live demo and take questions."))
shape(s, MSO_SHAPE.OVAL, 9.6, -1.4, 6.0, 6.0, fill="124C56")
text(s, 0.8, 0.8, 9, 0.4, "CONCLUSION", size=14, color=SAFFRON, bold=True)
text(s, 0.8, 1.3, 9.5, 1.2, "A working, honestly evaluated health-awareness chatbot", size=38, bold=True, font=HEAD, color=WHITE, name="Title")
pts = [("Built and deployed", "FastAPI + LaBSE + Qwen3 on Oracle Cloud, reachable on the web and a WhatsApp test number"),
       ("Safety-first design", "Deterministic emergency and fact-check paths, sources and disclaimers on every answer"),
       ("Tested honestly", "Component benchmarks plus whole-conversation spot checks, reported openly")]
for i, (t, d) in enumerate(pts):
    y = 3.05 + i * 1.1
    badge(s, 0.8, y, 0.6, str(i + 1), fill=SAFFRON, color=DARK, size=18)
    text(s, 1.65, y - 0.02, 8.3, 0.9, [[(t + "  ", {"bold": True, "color": WHITE, "size": 19, "font": HEAD})], [(d, {"color": "BFE3D8", "size": 15})]], anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.8, 6.45, 9, 0.4, "Thank you. Questions?", size=26, bold=True, font=HEAD, color=SAFFRON)
text(s, 0.8, 7.0, 11, 0.3, "Research paper (6 pages) and final project report (59 pages) available on request", size=12, color="9FC7BC")

prs.core_properties.title = "AarogyaSathi - Second Defense Presentation"
prs.core_properties.author = "Salman Mohammad Khan, Dhairya Summi, Sidharth Singh"
prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides))
