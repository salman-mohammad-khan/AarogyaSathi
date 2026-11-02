"""Redraws the report's engineering diagrams (1 data unit = 1 inch, fonts 6.5-8 pt)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Circle, Polygon, Rectangle

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
NAVY, BLUE, GREEN, ORANGE, RED, GOLD, SLATE = "#1F3A5F", "#2B6CB0", "#2F855A", "#C05621", "#C53030", "#B7791F", "#4A5568"
INK, LIGHT, LINE = "#1A202C", "#EBF4FF", "#4A5568"
plt.rcParams["font.family"] = "DejaVu Sans"


def canvas(w, h):
    fig = plt.figure(figsize=(w, h), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=300, facecolor="white")
    plt.close(fig)


def box(ax, cx, cy, w, h, text, fc=BLUE, tc="white", ec=None, fs=7.2, bold=True, sub=None, subfs=6.2, z=3):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.06",
                                fc=fc, ec=ec or fc, lw=1.0, zorder=z))
    if sub:
        ax.text(cx, cy + h * 0.17, text, ha="center", va="center", color=tc, fontsize=fs,
                fontweight="bold" if bold else "normal", zorder=z + 1)
        ax.text(cx, cy - h * 0.22, sub, ha="center", va="center", color=tc, fontsize=subfs, zorder=z + 1)
    else:
        ax.text(cx, cy, text, ha="center", va="center", color=tc, fontsize=fs,
                fontweight="bold" if bold else "normal", zorder=z + 1, linespacing=1.25)


def arrow(ax, p1, p2, color=LINE, lw=1.0, both=False, z=2, ms=7):
    ax.annotate("", xy=p2, xytext=p1, zorder=z,
                arrowprops=dict(arrowstyle="<|-|>" if both else "-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


def path(ax, pts, color=LINE, lw=1.0, z=2, ms=7):
    for a, b in zip(pts[:-2], pts[1:-1]):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw, zorder=z, solid_capstyle="butt")
    arrow(ax, pts[-2], pts[-1], color=color, lw=lw, z=z, ms=ms)


def label(ax, x, y, text, fs=6.2, color=INK, ha="center", bg=True, bold=False):
    ax.text(x, y, text, ha=ha, va="center", fontsize=fs, color=color, zorder=6, linespacing=1.2,
            fontweight="bold" if bold else "normal",
            bbox=dict(fc="white", ec="none", pad=0.8) if bg else None)


def stick(ax, x, y, name):
    ax.add_patch(Circle((x, y + 0.42), 0.11, fc="white", ec=INK, lw=1.1, zorder=4))
    ax.plot([x, x], [y + 0.31, y - 0.05], color=INK, lw=1.1, zorder=4)
    ax.plot([x - 0.17, x + 0.17], [y + 0.22, y + 0.22], color=INK, lw=1.1, zorder=4)
    ax.plot([x, x - 0.14], [y - 0.05, y - 0.30], color=INK, lw=1.1, zorder=4)
    ax.plot([x, x + 0.14], [y - 0.05, y - 0.30], color=INK, lw=1.1, zorder=4)
    ax.text(x, y - 0.52, name, ha="center", va="top", fontsize=6.8, fontweight="bold", color=INK, linespacing=1.2)


def store(ax, cx, cy, w, h, ident, text, fs=6.4):
    ax.plot([cx - w / 2, cx + w / 2], [cy + h / 2, cy + h / 2], color=SLATE, lw=1.2, zorder=3)
    ax.plot([cx - w / 2, cx + w / 2], [cy - h / 2, cy - h / 2], color=SLATE, lw=1.2, zorder=3)
    ax.plot([cx - w / 2 + 0.34, cx - w / 2 + 0.34], [cy - h / 2, cy + h / 2], color=SLATE, lw=1.2, zorder=3)
    ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h, fc="#F7FAFC", ec="none", zorder=2))
    ax.text(cx - w / 2 + 0.17, cy, ident, ha="center", va="center", fontsize=6.6, fontweight="bold", color=SLATE, zorder=4)
    ax.text(cx - w / 2 + 0.42, cy, text, ha="left", va="center", fontsize=fs, color=INK, zorder=4, linespacing=1.15)


def proc(ax, cx, cy, w, h, num, text, fs=6.3):
    ax.add_patch(Ellipse((cx, cy), w, h, fc=LIGHT, ec=BLUE, lw=1.3, zorder=3))
    ax.text(cx, cy + h * 0.2, num, ha="center", va="center", fontsize=7.2, fontweight="bold", color=NAVY, zorder=4)
    ax.text(cx, cy - h * 0.12, text, ha="center", va="center", fontsize=fs, color=INK, zorder=4, linespacing=1.15)


# ---------------------------------------------------------------- Figure 3.1 use case
def fig_usecase():
    W, H = 6.3, 4.9
    fig, ax = canvas(W, H)
    ax.add_patch(Rectangle((1.55, 0.2), 3.25, 4.5, fc="#F7FAFC", ec="#718096", lw=1.1, ls="--", zorder=1))
    ax.text(3.175, 4.5, "AarogyaSathi System Boundary", ha="center", va="center", fontsize=7.6, fontweight="bold", color=NAVY)
    ucs = ["UC-1: Inquire Disease & Symptoms", "UC-2: Verify Forwarded Health Claim", "UC-3: Query Vaccination Milestones",
           "UC-4: Emergency Red-Flag Triage", "UC-5: Report Symptoms with Pincode", "UC-6: Interact via WhatsApp Test Channel",
           "UC-7: Monitor Syndromic Cluster Alerts"]
    ys = [4.0 - i * 0.57 for i in range(7)]
    for t, y in zip(ucs, ys):
        ax.add_patch(Ellipse((3.175, y), 2.85, 0.43, fc="#E2E8F0", ec=SLATE, lw=1.0, zorder=3))
        ax.text(3.175, y, t, ha="center", va="center", fontsize=6.5, fontweight="bold", color=INK, zorder=4)
    left_x, right_x = 1.78, 4.57

    def link(ax_x, ay, idx, side):
        px = left_x if side == "L" else right_x
        ax.plot([ax_x, px], [ay, ys[idx]], color="#718096", lw=0.9, zorder=2)

    cit, hw, adm = (0.7, 3.4), (0.7, 1.55), (5.65, 2.45)
    for i in (0, 1, 2, 3, 5):
        link(cit[0] + 0.12, cit[1] + 0.2, i, "L")
    for i in (0, 1, 2, 3, 4):
        link(hw[0] + 0.12, hw[1] + 0.2, i, "L")
    for i in (4, 6):
        link(adm[0] - 0.12, adm[1] + 0.2, i, "R")
    stick(ax, *cit, "Citizen /\nMobile User")
    stick(ax, *hw, "Health Worker /\nASHA")
    stick(ax, *adm, "Public Health Admin /\nSurveillance Officer")
    save(fig, "fig_usecase.png")


# ---------------------------------------------------------------- Figure 3.2 DFD level 0
def fig_dfd0():
    W, H = 6.4, 3.7
    fig, ax = canvas(W, H)
    cx, cy, a, b = 3.2, 1.85, 0.9, 1.55
    ax.add_patch(Ellipse((cx, cy), 2 * a, 2 * b, fc=LIGHT, ec=BLUE, lw=1.6, zorder=3))
    ax.text(cx, cy + 0.38, "0.0", ha="center", fontsize=9, fontweight="bold", color=NAVY, zorder=4)
    ax.text(cx, cy - 0.02, "AarogyaSathi", ha="center", fontsize=8.4, fontweight="bold", color=NAVY, zorder=4)
    ax.text(cx, cy - 0.4, "Public Health\nAI Chatbot", ha="center", va="center", fontsize=6.8, color=BLUE, zorder=4, linespacing=1.2)

    def edge_x(y, side):
        dx = a * (1 - ((y - cy) / b) ** 2) ** 0.5
        return cx - dx if side == "L" else cx + dx

    ents = [("Rural / Semi-Urban\nCitizen (Web Browser)", 0.05, 2.75, "L", NAVY, ("Health query /\nsymptoms", "Verified health\nguidance")),
            ("WhatsApp Mobile\nUser (Test Recipient)", 0.05, 0.95, "L", GREEN, ("WhatsApp message /\nclaim", "Interactive\nbot reply")),
            ("Public Health Authority\n(IDSP / Advisories)", 4.75, 2.75, "R", ORANGE, ("Local advisory\nbulletins", "Syndromic alert\nevent")),
            ("Meta WhatsApp Cloud\n& Cloudflare Tunnel", 4.75, 0.95, "R", SLATE, ("Signed webhook\ncallback", "Outbound\nmessage"))]
    for name, x0, yc, side, col, (l1, l2) in ents:
        box(ax, x0 + 0.8, yc, 1.6, 0.75, name, fc=col, fs=6.6)
        xb = x0 + 1.6 if side == "L" else x0
        y_up, y_dn = yc + 0.16, yc - 0.16
        if side == "L":
            xe1, xe2 = edge_x(y_up, "L"), edge_x(y_dn, "L")
            arrow(ax, (xb, y_up), (xe1, y_up))
            arrow(ax, (xe2, y_dn), (xb, y_dn))
            mid = (xb + min(xe1, xe2)) / 2
        else:
            xe1, xe2 = edge_x(y_up, "R"), edge_x(y_dn, "R")
            arrow(ax, (xe1, y_up), (xb, y_up))
            arrow(ax, (xb, y_dn), (xe2, y_dn))
            mid = (xb + max(xe1, xe2)) / 2
        # labels sit above (upper arrow) and below (lower arrow) the pair
        up_text = l1 if side == "L" else l2
        dn_text = l2 if side == "L" else l1
        ax.text(mid, y_up + 0.21, up_text, ha="center", va="center", fontsize=5.9, color=INK, linespacing=1.1)
        ax.text(mid, y_dn - 0.21, dn_text, ha="center", va="center", fontsize=5.9, color=INK, linespacing=1.1)
    save(fig, "fig_dfd_lvl0.png")


# ---------------------------------------------------------------- Figure 3.3 DFD level 1
def fig_dfd1():
    W, H = 6.5, 5.75
    fig, ax = canvas(W, H)
    box(ax, 0.55, 2.35, 0.95, 3.9, "Citizen /\nWhatsApp\nUser", fc=NAVY, fs=6.8)
    p1, p2, p3 = (2.2, 3.95), (3.95, 3.95), (5.7, 3.95)
    p4, p5, p6 = (3.95, 2.45), (3.95, 1.0), (5.7, 1.0)
    for (x, y), n, t in [(p1, "1.0", "Emergency\nFilter"), (p2, "2.0", "Fast-Path\nRouter"), (p3, "3.0", "Fact-Check\nEngine"),
                         (p4, "4.0", "LaBSE\nRetriever"), (p5, "5.0", "RAG / Template\nGenerator"), (p6, "6.0", "Syndromic\nSurveillance")]:
        proc(ax, x, y, 1.15, 0.82, n, t)
    # external <-> 1.0
    arrow(ax, (1.025, 4.15), (1.63, 4.15))
    label(ax, 1.33, 4.34, "User query", fs=5.9, bg=False)
    arrow(ax, (1.7, 3.75), (1.025, 3.75))
    label(ax, 1.33, 3.56, "108/112 alert", fs=5.9, bg=False)
    # flows between processes
    arrow(ax, (2.78, 3.95), (3.37, 3.95))
    label(ax, 3.07, 4.18, "Non-urgent\nquery", fs=5.7, bg=False)
    arrow(ax, (4.53, 3.95), (5.12, 3.95))
    label(ax, 4.82, 4.18, "Claim\nquery", fs=5.7, bg=False)
    arrow(ax, (3.95, 3.54), (3.95, 2.86))
    label(ax, 4.42, 3.2, "Unresolved\nquery", fs=5.7, bg=False)
    arrow(ax, (3.95, 2.04), (3.95, 1.41))
    label(ax, 4.42, 1.72, "Ranked\nrecords", fs=5.7, bg=False)
    arrow(ax, (4.53, 1.0), (5.12, 1.0))
    label(ax, 4.82, 1.25, "Symptom event\n+ pincode", fs=5.5, bg=False)
    # stores
    store(ax, 5.7, 2.45, 1.4, 0.42, "D2", "Myth Store (64)")
    arrow(ax, (5.7, 3.54), (5.7, 2.66), both=True)
    label(ax, 6.15, 3.1, "Match /\nverdict", fs=5.5, bg=False)
    store(ax, 2.15, 2.45, 1.45, 0.42, "D3", "Knowledge Base\n(49 indexed)", fs=6.0)
    arrow(ax, (2.88, 2.45), (3.37, 2.45))
    store(ax, 3.95, 5.12, 1.5, 0.42, "D1", "Session (RAM, 30 min)", fs=5.9)
    arrow(ax, (3.95, 4.91), (3.95, 4.36), both=True)
    label(ax, 4.4, 4.64, "Context", fs=5.5, bg=False)
    store(ax, 5.7, 0.2, 1.4, 0.34, "D4", "Telemetry (SQLite)", fs=5.9)
    arrow(ax, (5.7, 0.59), (5.7, 0.37))
    # replies back to the user
    path(ax, [(3.37, 1.0), (1.025, 1.0)], lw=1.0)
    label(ax, 2.2, 1.0, "Grounded reply", fs=5.9)
    path(ax, [(5.7, 4.36), (5.7, 5.55), (0.55, 5.55), (0.55, 4.3)], lw=1.0)
    label(ax, 2.0, 5.55, "Claim verdict + explanation", fs=5.9)
    save(fig, "fig_dfd_lvl1.png")


# ---------------------------------------------------------------- Figure 4.1 WBS
def fig_wbs():
    W, H = 6.4, 3.5
    fig, ax = canvas(W, H)
    box(ax, 3.2, 3.15, 3.0, 0.42, "AarogyaSathi System (SIH25049)", fc=NAVY, fs=8)
    cols = [("1. Core NLP & Routing", "Intent, entities, fast path", ["1.1 TF-IDF classifier", "1.2 Entity & red-flag rules", "1.3 Session context"]),
            ("2. Retrieval & Knowledge", "LaBSE, diseases, FAQs", ["2.1 LaBSE embeddings", "2.2 Cosine + lexical rerank", "2.3 RAG answer generation"]),
            ("3. Fact-Check & Safety", "Myth engine, red flags", ["3.1 64-myth verifier", "3.2 Emergency escalation", "3.3 Clinical disclaimers"]),
            ("4. Channels & Deployment", "Web, WhatsApp, Oracle VM", ["4.1 FastAPI service & web UI", "4.2 WhatsApp Cloud API", "4.3 Cloudflare tunnel & VM"])]
    xs = [0.8, 2.4, 4.0, 5.6]
    path(ax, [(3.2, 2.94), (3.2, 2.62)], lw=1.2, ms=1) if False else None
    ax.plot([3.2, 3.2], [2.94, 2.65], color=LINE, lw=1.2)
    ax.plot([xs[0], xs[-1]], [2.65, 2.65], color=LINE, lw=1.2)
    for x, (t, s, kids) in zip(xs, cols):
        ax.plot([x, x], [2.65, 2.42], color=LINE, lw=1.2)
        box(ax, x, 2.1, 1.5, 0.62, t, fc=BLUE, fs=6.6, sub=s, subfs=5.6)
        ax.plot([x - 0.66, x - 0.66], [1.79, 0.38], color="#A0AEC0", lw=1.0)
        for i, k in enumerate(kids):
            y = 1.45 - i * 0.5
            ax.plot([x - 0.66, x - 0.58], [y, y], color="#A0AEC0", lw=1.0)
            box(ax, x + 0.04, y, 1.2, 0.36, k, fc="#EDF2F7", tc=INK, fs=5.8, bold=False)
    save(fig, "fig_wbs.png")


# ---------------------------------------------------------------- Figure 4.2 storage
def card(ax, x0, y0, w, h, title, sub, lines, col):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0,rounding_size=0.06", fc="#F7FAFC", ec=col, lw=1.3, zorder=2))
    ax.add_patch(FancyBboxPatch((x0, y0 + h - 0.62), w, 0.62, boxstyle="round,pad=0,rounding_size=0.06", fc=col, ec=col, zorder=3))
    ax.text(x0 + w / 2, y0 + h - 0.22, title, ha="center", va="center", color="white", fontsize=7.4, fontweight="bold", zorder=4)
    ax.text(x0 + w / 2, y0 + h - 0.45, sub, ha="center", va="center", color="white", fontsize=6.0, zorder=4)
    for i, ln in enumerate(lines):
        ax.text(x0 + 0.1, y0 + h - 0.85 - i * 0.215, ln, ha="left", va="center", color=INK, fontsize=5.9, zorder=4,
                family="DejaVu Sans Mono" if ln.startswith(("events", "messages", "alerts", "id", "state", "updated")) else "DejaVu Sans")


def fig_storage():
    W, H = 6.4, 4.3
    fig, ax = canvas(W, H)
    card(ax, 0.1, 1.75, 2.0, 2.45, "SQLite database", "data/surveillance.db (persistent)",
         ["events(id, pincode, symptom,", "        lang, ts)", "messages(id, pincode, intent,", "        lang, verdict, ts)",
          "alerts(id, pincode, symptom,", "        current_count, baseline,", "        severity, ts)"], BLUE)
    card(ax, 2.25, 1.75, 1.95, 2.45, "In-memory sessions", "Session class (volatile, 30-min TTL)",
         ["id        session / sender key", "state{}    active flow, recent", "           turns, summary", "updated   last-activity time",
          "Lost on server restart"], ORANGE)
    card(ax, 4.35, 1.75, 1.95, 2.45, "Curated JSON store", "data/kb/ (read at startup)",
         ["diseases.json    14 profiles", "faq.json          35 FAQs", "vaccines.json   13 entries", "myths.json        64 myths",
          "outbreaks.json  8 advisories", "pincodes.json, messages.json"], GREEN)
    box(ax, 3.2, 0.62, 5.3, 0.9, "FastAPI application core (app/main.py, app/core/router.py)", fc=NAVY, fs=7.4,
        sub="Routes each request, reads the knowledge base, keeps session state, and records anonymous telemetry", subfs=6.1)
    for x, txt in [(1.1, "writes events,\nmessages, alerts"), (3.225, "reads / updates\nconversation state"), (5.325, "indexes records")]:
        both = x != 5.325
        arrow(ax, (x, 1.07), (x, 1.75), both=both, lw=1.2)
        label(ax, x, 1.41, txt, fs=5.8)
    save(fig, "fig_er_class.png")


# ---------------------------------------------------------------- Figure 4.3 flowchart
def diamond(ax, cx, cy, w, h, text, col, fs=6.8):
    ax.add_patch(Polygon([(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)], closed=True,
                         fc="white", ec=col, lw=1.4, zorder=3))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, fontweight="bold", color=col, zorder=4, linespacing=1.2)


def fig_flow():
    W, H = 6.3, 7.1
    fig, ax = canvas(W, H)
    X = 2.25
    ax.add_patch(Ellipse((X, 6.88), 0.8, 0.3, fc=GREEN, ec=GREEN, zorder=3))
    ax.text(X, 6.88, "Start", ha="center", va="center", color="white", fontsize=7, fontweight="bold", zorder=4)
    arrow(ax, (X, 6.73), (X, 6.5))
    box(ax, X, 6.28, 3.2, 0.44, "Inbound query received", fc=BLUE, fs=7.2, sub="Web HTTP POST or Meta WhatsApp webhook", subfs=5.8)
    arrow(ax, (X, 6.06), (X, 5.82))
    rows = [(5.42, "Emergency red flag?", "(chest pain, breathing ...)", RED, "Immediate escalation", "108 / 112 helpline advice", RED),
            (4.34, "Fact-check trigger?", "('fact check:' prefix)", GOLD, "Claim verification engine", "Curated 64-myth match", GOLD),
            (3.26, "Fast-path rule match?", "(greeting, disease, vaccine)", BLUE, "Fast-path extraction", "Curated template / milestones", BLUE)]
    for i, (y, t1, t2, col, bt, bs, bc) in enumerate(rows):
        diamond(ax, X, y, 3.3, 0.95, t1 + "\n" + t2, col, fs=6.5)
        arrow(ax, (X + 1.65, y), (4.4, y))
        label(ax, X + 2.0, y + 0.13, "Yes", fs=6.3, bg=False, bold=True)
        box(ax, 5.25, y, 1.65, 0.62, bt, fc=bc, fs=6.4, sub=bs, subfs=5.3)
        nxt = rows[i + 1][0] + 0.48 if i < 2 else 2.72
        arrow(ax, (X, y - 0.48), (X, nxt))
        label(ax, X + 0.22, y - 0.62 if i < 2 else 2.95, "No", fs=6.3, bg=False, bold=True)
    box(ax, X, 2.5, 3.2, 0.44, "Dense semantic retrieval", fc=SLATE, fs=7.2, sub="LaBSE embeddings + lexical overlap", subfs=5.8)
    arrow(ax, (X, 2.28), (X, 2.02))
    box(ax, X, 1.8, 3.2, 0.44, "Answer generation", fc=SLATE, fs=7.2, sub="Local Qwen3-1.7B (Ollama) or template fallback", subfs=5.8)
    arrow(ax, (X, 1.58), (X, 1.22))
    box(ax, X, 1.0, 3.2, 0.44, "Format reply and attach sources / disclaimer", fc=GREEN, fs=6.9, sub="Deterministic safety text is never rewritten by the LLM", subfs=5.5)
    # right-hand bus: all fast branches merge into the reply formatter
    bus = 6.25
    for y, c in [(5.42, RED), (4.34, GOLD), (3.26, BLUE)]:
        ax.plot([6.075, bus], [y, y], color=LINE, lw=1.0, zorder=2)
    ax.plot([bus, bus], [5.42, 1.0], color=LINE, lw=1.0, zorder=2)
    arrow(ax, (bus, 1.0), (X + 1.6, 1.0))
    arrow(ax, (X, 0.78), (X, 0.45))
    box(ax, X, 0.28, 3.2, 0.3, "Send reply (web JSON or WhatsApp message)", fc="#EDF2F7", tc=INK, fs=6.6)
    save(fig, "fig_flowchart.png")


# ---------------------------------------------------------------- Figure 4.4 sequence
def fig_seq():
    W, H = 6.4, 4.5
    fig, ax = canvas(W, H)
    xs = [0.8, 2.35, 3.95, 5.55]
    names = ["User phone\n(approved test recipient)", "Meta WhatsApp\nCloud API", "Cloudflare\nHTTPS tunnel", "Oracle VM\nFastAPI service"]
    cols = [GREEN, BLUE, SLATE, NAVY]
    for x, n, c in zip(xs, names, cols):
        box(ax, x, 4.1, 1.35, 0.6, n, fc=c, fs=6.2)
        ax.plot([x, x], [3.8, 0.15], color="#CBD5E0", lw=1.0, ls=(0, (4, 3)), zorder=1)
    def msg(i, y, a, b, text, col=BLUE):
        arrow(ax, (xs[a], y), (xs[b], y), color=col, lw=1.2)
        ax.text((xs[a] + xs[b]) / 2, y + 0.13, f"{i}. {text}", ha="center", va="bottom", fontsize=6.0, color=INK, zorder=5)
    msg(1, 3.45, 0, 1, "User sends a message")
    msg(2, 2.85, 1, 2, "Webhook POST + X-Hub-Signature-256")
    msg(3, 2.25, 2, 3, "Forward HTTPS to /webhook/whatsapp")
    ax.add_patch(FancyBboxPatch((4.3, 1.4), 1.95, 0.62, boxstyle="round,pad=0,rounding_size=0.05", fc="#EBF8FF", ec=BLUE, lw=1.0, zorder=4))
    ax.text(5.275, 1.71, "4. Verify HMAC-SHA256, reject if invalid,\nreturn 200, drop duplicate message IDs", ha="center", va="center", fontsize=5.9, color=INK, zorder=5)
    ax.add_patch(FancyBboxPatch((4.3, 0.62), 1.95, 0.62, boxstyle="round,pad=0,rounding_size=0.05", fc="#EBF8FF", ec=BLUE, lw=1.0, zorder=4))
    ax.text(5.275, 0.93, "5. Background worker: session lookup,\nrouter, answer generation", ha="center", va="center", fontsize=5.9, color=INK, zorder=5)
    msg(6, 0.35, 3, 1, "POST /{phone-number-id}/messages (reply)")
    arrow(ax, (xs[1], 0.12), (xs[0], 0.12), color=BLUE, lw=1.2)
    ax.text((xs[0] + xs[1]) / 2, 0.2, "7. Reply delivered", ha="center", va="bottom", fontsize=6.0, color=INK, zorder=5)
    save(fig, "fig_whatsapp_seq.png")


if __name__ == "__main__":
    for f in (fig_usecase, fig_dfd0, fig_dfd1, fig_wbs, fig_storage, fig_flow, fig_seq):
        f()
        print("ok", f.__name__)
