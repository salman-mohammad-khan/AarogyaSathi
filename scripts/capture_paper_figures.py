import time
import requests
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from playwright.sync_api import sync_playwright

BASE_URL = "http://130.210.56.87:8000"

print("--- 1. Generating Architecture Diagram (Fig 1) ---")
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
ax.axis("off")

# Styles
box_kw = dict(boxstyle="round,pad=0.5", facecolor="#EBF5FB", edgecolor="#2980B9", linewidth=1.5)
safety_kw = dict(boxstyle="round,pad=0.5", facecolor="#FDEDEC", edgecolor="#C0392B", linewidth=1.5)
retrieval_kw = dict(boxstyle="round,pad=0.5", facecolor="#E8F8F5", edgecolor="#16A085", linewidth=1.5)
rag_kw = dict(boxstyle="round,pad=0.5", facecolor="#FEF9E7", edgecolor="#F39C12", linewidth=1.5)
surv_kw = dict(boxstyle="round,pad=0.5", facecolor="#F4ECF7", edgecolor="#8E44AD", linewidth=1.5)

# Boxes
ax.text(0.5, 0.93, "User Query (Web Chat / WhatsApp / SMS)\n[Multilingual: EN / Hindi / Hinglish / Regional]", 
        ha="center", va="center", bbox=box_kw, fontsize=10, weight="bold", color="#1B4F72")

ax.text(0.18, 0.77, "Tier 0: Red-Flag & Dangerous\nFirst-Aid Guard (0.01s)\n[Deterministic Escalation 108/112]", 
        ha="center", va="center", bbox=safety_kw, fontsize=8.5, weight="bold", color="#78281F")

ax.text(0.5, 0.77, "Multilingual Language ID (fastText)\n& Intent Classifier (TF-IDF + LR)\n[13 Canonical Health Intents]", 
        ha="center", va="center", bbox=box_kw, fontsize=8.5, weight="bold", color="#1B4F72")

ax.text(0.82, 0.77, "Syndromic Surveillance Engine\n[SQLite Events + Pincode Anomaly]\n[Rolling 7-day Baseline vs 24h Count]", 
        ha="center", va="center", bbox=surv_kw, fontsize=8.5, weight="bold", color="#512E5F")

ax.text(0.28, 0.55, "Tier 1: Semantic KB Match\n[Google LaBSE 768-dim Embeddings]\n[Dual Token Coverage: min(Dice, Cov) >= 0.35]\n128 Curated Myths / 14 Disease Profiles", 
        ha="center", va="center", bbox=retrieval_kw, fontsize=8.5, weight="bold", color="#0E6251")

ax.text(0.72, 0.55, "Tier 2: Live Multi-Strategy Web Search\n[ddgs News + Wikipedia REST API]\n[Tier-1 Domain Filtering: WHO, MoHFW, CDC]\nAutonomous Web Evidence Aggregator", 
        ha="center", va="center", bbox=retrieval_kw, fontsize=8.5, weight="bold", color="#0E6251")

ax.text(0.5, 0.33, "Tier 3: Retrieval-Augmented Generation (RAG)\n[Local SLM: Qwen3-1.7B-Instruct / Cloud Fallback]\nStrict Grounding: Evidence-Only, Negative Constraints (<70 words)", 
        ha="center", va="center", bbox=rag_kw, fontsize=9, weight="bold", color="#7D6608")

ax.text(0.5, 0.12, "Final Structured Response Assembly\n• Fact-Check: Verdict (VERIFIED / MYTH / PARTLY TRUE) + Confidence % + Source Links\n• Disease & Symptoms: Empathetic Guidance + Mandatory Medical Disclaimer\n• Outbreaks: Localized Advisories + Live Breaking News Feed", 
        ha="center", va="center", bbox=box_kw, fontsize=9, weight="bold", color="#154360")

# Connecting Arrows
arrow_kw = dict(arrowstyle="->", lw=1.5, color="#34495E")
ax.annotate("", xy=(0.18, 0.83), xytext=(0.42, 0.90), arrowprops=arrow_kw)
ax.annotate("", xy=(0.5, 0.83), xytext=(0.5, 0.88), arrowprops=arrow_kw)
ax.annotate("", xy=(0.82, 0.83), xytext=(0.58, 0.90), arrowprops=arrow_kw)

ax.annotate("", xy=(0.28, 0.63), xytext=(0.45, 0.72), arrowprops=arrow_kw)
ax.annotate("", xy=(0.72, 0.63), xytext=(0.55, 0.72), arrowprops=arrow_kw)

ax.annotate("", xy=(0.42, 0.40), xytext=(0.32, 0.48), arrowprops=arrow_kw)
ax.annotate("", xy=(0.58, 0.40), xytext=(0.68, 0.48), arrowprops=arrow_kw)

ax.annotate("", xy=(0.5, 0.19), xytext=(0.5, 0.27), arrowprops=arrow_kw)

plt.tight_layout()
fig.savefig("docs/fig1_architecture.png", dpi=300, bbox_inches="tight")
plt.close()
print("Fig 1 generated successfully.")

print("--- 2. Generating Evaluation Benchmark Chart (Fig 4) ---")
fig, ax = plt.subplots(figsize=(8.5, 4.5), dpi=300)

categories = [
    "Vaccine Myth", "Deadly First-Aid", "WhatsApp Hoax", 
    "Food/Pregnancy", "Cancer Fake Cure", "5G Conspiracy", 
    "Home Remedy", "Medical Fact", "Immunization", 
    "Hindi Viral", "Hinglish Cancer", "Snakebite", 
    "Animal Bite", "Absurd Claim", "Dehydration"
]
latencies = [0.08, 0.01, 0.07, 0.10, 0.11, 0.11, 0.11, 0.14, 0.11, 0.14, 7.31, 0.01, 0.01, 7.66, 0.11]
colors = ["#27AE60" if l < 1.0 else "#E67E22" for l in latencies]

bars = ax.barh(categories[::-1], latencies[::-1], color=colors[::-1], edgecolor="#2C3E50", height=0.65)
ax.set_xlabel("Inference & Retrieval Latency (seconds)", fontsize=10, weight="bold")
ax.set_title("Empirical Verification Latency Across 15 Representative Indian Health Claims", fontsize=11, weight="bold")
ax.grid(axis="x", linestyle="--", alpha=0.6)

for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.15, bar.get_y() + bar.get_height()/2, f"{w:.2f}s", va="center", fontsize=8, weight="bold")

ax.set_xlim(0, 9.5)
plt.tight_layout()
fig.savefig("docs/fig4_benchmark_latency.png", dpi=300, bbox_inches="tight")
plt.close()
print("Fig 4 generated successfully.")

print("--- 3. Capturing Live Screenshots with Playwright ---")
try:
    # Seed surveillance DB
    requests.post(f"{BASE_URL}/api/surveillance/seed", timeout=5)
    print("Surveillance DB seeded.")
except Exception as e:
    print("Seed warning:", e)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    
    # 3A. Surveillance Dashboard
    page_admin = browser.new_page(viewport={"width": 1280, "height": 850})
    page_admin.goto(f"{BASE_URL}/admin", wait_until="networkidle")
    time.sleep(1.5)
    page_admin.screenshot(path="docs/fig3_surveillance_dashboard.png")
    print("Fig 3 (Surveillance Dashboard) captured.")

    # 3B. Web Chat Interface with rich conversation
    page_chat = browser.new_page(viewport={"width": 1200, "height": 850})
    page_chat.goto(BASE_URL, wait_until="networkidle")
    time.sleep(2)
    
    # Send fact check query
    page_chat.fill("#userInput", "fact check: drinking cow urine cures cancer")
    page_chat.click("#sendBtn")
    time.sleep(4)
    
    # Send second query with pincode
    page_chat.fill("#pincodeInput", "110001")
    page_chat.fill("#userInput", "Any dengue alert near me?")
    page_chat.click("#sendBtn")
    time.sleep(4)
    
    page_chat.screenshot(path="docs/fig2_chat_interface.png")
    print("Fig 2 (Chat Interface) captured.")
    
    browser.close()

print("All figures ready in docs/ folder!")
