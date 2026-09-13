import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Wedge, Arrow
import numpy as np
from PIL import Image, ImageDraw, ImageFont

os.makedirs("docs/ppt_assets", exist_ok=True)

# Colors
C_NAVY = "#0F2043"
C_TEAL = "#16A085"
C_CYAN = "#00B4D8"
C_LIGHT_BLUE = "#EBF5FB"
C_RED = "#E74C3C"
C_GOLD = "#D4AC0D"
C_DARK = "#212F3D"
C_GRAY = "#7F8C8D"
C_WHITE = "#FFFFFF"

# -------------------------------------------------------------
# 1. HERO LOGO / EMBLEM (docs/ppt_assets/hero_emblem.png)
# -------------------------------------------------------------
def generate_hero_emblem():
    fig, ax = plt.subplots(figsize=(6, 6), dpi=220)
    ax.set_facecolor("none")
    fig.patch.set_alpha(0.0)

    # Outer glow rings
    circle_outer = Circle((0.5, 0.5), 0.46, color=C_NAVY, ec=C_TEAL, lw=4, zorder=1)
    ax.add_patch(circle_outer)
    circle_inner = Circle((0.5, 0.5), 0.40, color="#12264F", ec=C_CYAN, lw=2, linestyle='--', zorder=2)
    ax.add_patch(circle_inner)

    # Medical Cross in center
    rect_v = FancyBboxPatch((0.44, 0.28), 0.12, 0.44, boxstyle="round,pad=0.02,rounding_size=0.03", 
                            color=C_TEAL, zorder=3)
    rect_h = FancyBboxPatch((0.28, 0.44), 0.44, 0.12, boxstyle="round,pad=0.02,rounding_size=0.03", 
                            color=C_TEAL, zorder=3)
    ax.add_patch(rect_v)
    ax.add_patch(rect_h)

    # Heartbeat Pulse (ECG wave) through center
    pulse_x = [0.22, 0.35, 0.42, 0.46, 0.50, 0.54, 0.58, 0.65, 0.78]
    pulse_y = [0.50, 0.50, 0.44, 0.66, 0.32, 0.58, 0.50, 0.50, 0.50]
    ax.plot(pulse_x, pulse_y, color=C_WHITE, lw=3.5, zorder=5, solid_capstyle='round')

    # Neural AI nodes
    nodes = [(0.26, 0.68), (0.74, 0.68), (0.26, 0.32), (0.74, 0.32)]
    for nx, ny in nodes:
        ax.plot([0.5, nx], [0.5, ny], color=C_CYAN, lw=1.2, alpha=0.6, zorder=2)
        ax.add_patch(Circle((nx, ny), 0.032, color=C_CYAN, ec=C_WHITE, lw=1.5, zorder=4))

    # Center glowing core
    ax.add_patch(Circle((0.5, 0.5), 0.05, color=C_WHITE, ec=C_CYAN, lw=2, zorder=6))

    # Text Ribbon
    ax.text(0.5, 0.18, "AAROGYASATHI", color=C_WHITE, fontsize=13, fontweight='bold', 
            ha='center', va='center', zorder=6, family='sans-serif')
    ax.text(0.5, 0.12, "AI PUBLIC HEALTH INFORMATICS", color=C_CYAN, fontsize=8, fontweight='bold', 
            ha='center', va='center', zorder=6, family='sans-serif')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    out_path = "docs/ppt_assets/hero_emblem.png"
    plt.savefig(out_path, bbox_inches='tight', transparent=True)
    plt.close()
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# 2. MOTIVATION 3-IN-1 INFOGRAPHIC (docs/ppt_assets/motivation_infographic.png)
# -------------------------------------------------------------
def generate_motivation_infographic():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 5.2), dpi=220)
    fig.patch.set_facecolor("#F8F9FA")

    # PANEL 1: Doctor-to-Citizen Ratio
    ax1.set_facecolor(C_WHITE)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.spines['bottom'].set_color("#BDC3C7")

    bars = ax1.bar(["WHO Norm", "India Actual"], [1000, 1456], color=[C_TEAL, C_RED], width=0.55, zorder=3)
    ax1.grid(axis='y', linestyle='--', alpha=0.3, zorder=1)
    ax1.set_ylabel("Citizens per Single Doctor", fontsize=11, fontweight='bold', color=C_DARK)
    ax1.set_title("1. Healthcare Workforce Deficit", fontsize=13, fontweight='bold', color=C_NAVY, pad=12)
    
    # Value labels
    ax1.text(0, 1050, "1 : 1,000\n(Standard)", ha='center', va='bottom', fontsize=10.5, fontweight='bold', color=C_TEAL)
    ax1.text(1, 1500, "1 : 1,456\n(Severe Deficit)", ha='center', va='bottom', fontsize=10.5, fontweight='bold', color=C_RED)
    ax1.set_ylim(0, 1850)
    
    # Annotation box
    ax1.text(0.5, 400, "45.6% Deficit\nin Primary Care Delivery\nOver 70% Rural Gap", 
             ha='center', va='center', bbox=dict(boxstyle="round,pad=0.5", fc="#FDEDEC", ec=C_RED, lw=1.5),
             fontsize=9.5, color=C_DARK, fontweight='bold')

    # PANEL 2: Viral Misinformation Hoaxes
    ax2.set_facecolor(C_WHITE)
    ax2.axis('off')
    ax2.set_title("2. Deadly Social Media Infodemic", fontsize=13, fontweight='bold', color=C_NAVY, pad=12)

    # WhatsApp Chat bubble mockup
    box_chat = FancyBboxPatch((0.08, 0.52), 0.84, 0.40, boxstyle="round,pad=0.03,rounding_size=0.05",
                              color="#E1F5FE", ec="#81D4FA", lw=1.5)
    ax2.add_patch(box_chat)
    ax2.text(0.12, 0.84, "Forwarded WhatsApp Hoax:", fontsize=9.5, fontweight='bold', color="#0277BD")
    ax2.text(0.12, 0.68, "\"Drink boiled garlic juice daily to\ncure Diabetes in 7 days!\"\n\"Apply red chilli powder on dog bites!\"", 
             fontsize=9.5, color=C_DARK, fontstyle='italic')

    # Warning Stamp
    box_stamp = FancyBboxPatch((0.15, 0.14), 0.70, 0.28, boxstyle="round,pad=0.03,rounding_size=0.04",
                               color="#FDEDEC", ec=C_RED, lw=2)
    ax2.add_patch(box_stamp)
    ax2.text(0.5, 0.32, "CATASTROPHIC REAL-WORLD IMPACT", fontsize=9, fontweight='bold', color=C_RED, ha='center')
    ax2.text(0.5, 0.20, "• Delayed insulin -> Diabetic coma\n• Caustic chemical necrosis", 
             fontsize=8.5, color=C_DARK, ha='center', fontweight='bold')

    # PANEL 3: Surveillance Latency (Timeline)
    ax3.set_facecolor(C_WHITE)
    ax3.axis('off')
    ax3.set_title("3. Outbreak Detection Latency Gap", fontsize=13, fontweight='bold', color=C_NAVY, pad=12)

    # Traditional IDSP Bar
    box_idsp = FancyBboxPatch((0.08, 0.56), 0.84, 0.32, boxstyle="round,pad=0.03,rounding_size=0.04",
                              color="#FADBD8", ec=C_RED, lw=1.5)
    ax3.add_patch(box_idsp)
    ax3.text(0.12, 0.78, "Traditional IDSP System (Lab Registry)", fontsize=10, fontweight='bold', color=C_RED)
    ax3.text(0.12, 0.64, "Latency: 14 to 21 Days Delay\nOutbreak spreads before response", fontsize=9, color=C_DARK)

    # AarogyaSathi Bar
    box_ours = FancyBboxPatch((0.08, 0.12), 0.84, 0.32, boxstyle="round,pad=0.03,rounding_size=0.04",
                              color="#D5F5E3", ec=C_TEAL, lw=2)
    ax3.add_patch(box_ours)
    ax3.text(0.12, 0.34, "AarogyaSathi Syndromic Surveillance", fontsize=10, fontweight='bold', color=C_TEAL)
    ax3.text(0.12, 0.20, "Latency: REAL-TIME (<24 Hours)\n14-Day Proactive Prevention Lead", fontsize=9, color=C_DARK, fontweight='bold')

    out_path = "docs/ppt_assets/motivation_infographic.png"
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# 3. LaBSE BILINGUAL CONVERGENCE DIAGRAM (docs/ppt_assets/labse_concept.png)
# -------------------------------------------------------------
def generate_labse_concept():
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=220)
    fig.patch.set_facecolor(C_WHITE)
    ax.set_facecolor("#F8F9FA")
    ax.axis('off')

    ax.text(0.5, 0.94, "Cross-Lingual LaBSE Semantic Embedding Space (d = 768)", 
            ha='center', fontsize=14, fontweight='bold', color=C_NAVY)

    inputs = [
        ("English Query", "\"Does garlic cure diabetes?\"", "#EBF5FB", "#2980B9", 0.72),
        ("Hindi (Devanagari)", "\"क्या लहसुन से डायबिटीज ठीक होती है?\"", "#FEF9E7", "#D4AC0D", 0.48),
        ("Colloquial Hinglish", "\"kya lehsun khane se diabetes theek hogi?\"", "#FDEDEC", "#E74C3C", 0.24),
    ]

    for lang, text, bg, border, y in inputs:
        box = FancyBboxPatch((0.04, y - 0.08), 0.36, 0.16, boxstyle="round,pad=0.02,rounding_size=0.03",
                             color=bg, ec=border, lw=1.8)
        ax.add_patch(box)
        ax.text(0.06, y + 0.03, lang, fontsize=9.5, fontweight='bold', color=border)
        font_fam = 'Nirmala UI' if "Hindi" in lang else 'sans-serif'
        ax.text(0.06, y - 0.04, text, fontsize=9, color=C_DARK, 
                fontstyle='italic' if "Hindi" not in lang else 'normal', fontfamily=font_fam)
        
        ax.annotate('', xy=(0.49, 0.50), xytext=(0.41, y),
                    arrowprops=dict(arrowstyle="->", color=border, lw=2.2, mutation_scale=15))

    core_box = FancyBboxPatch((0.50, 0.22), 0.24, 0.56, boxstyle="round,pad=0.03,rounding_size=0.04",
                              color=C_NAVY, ec=C_CYAN, lw=2.5)
    ax.add_patch(core_box)
    ax.text(0.62, 0.66, "Google LaBSE", fontsize=12, fontweight='bold', color=C_WHITE, ha='center')
    ax.text(0.62, 0.57, "Dual-Encoder\nTransformer", fontsize=9.5, color=C_CYAN, ha='center')
    ax.text(0.62, 0.42, "Unified\n768-Dim Vector\nCosine Sim > 0.88", fontsize=9.5, color=C_WHITE, ha='center', fontweight='bold')
    ax.text(0.62, 0.27, "Zero Translation Loss", fontsize=8.5, color="#A2D9CE", ha='center')

    ax.annotate('', xy=(0.80, 0.50), xytext=(0.75, 0.50),
                arrowprops=dict(arrowstyle="->", color=C_TEAL, lw=3, mutation_scale=18))

    out_box = FancyBboxPatch((0.80, 0.28), 0.17, 0.44, boxstyle="round,pad=0.03,rounding_size=0.03",
                             color="#E8F8F5", ec=C_TEAL, lw=2)
    ax.add_patch(out_box)
    ax.text(0.885, 0.62, "Knowledge Base\nMatch", fontsize=10, fontweight='bold', color=C_TEAL, ha='center')
    ax.text(0.885, 0.46, "Claim ID: C-014\n\"Garlic & Glycemic\nControl Realities\"", fontsize=8.5, color=C_DARK, ha='center')
    ax.text(0.885, 0.33, "Latency < 0.12s", fontsize=9, fontweight='bold', color="#117864", ha='center')

    ax.set_xlim(0, 1)
    ax.set_ylim(0.1, 1.0)

    out_path = "docs/ppt_assets/labse_concept.png"
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# 4. AUTONOMOUS 4-TIER FACT-CHECKING FLOWCHART (docs/ppt_assets/factcheck_flowchart.png)
# -------------------------------------------------------------
def generate_factcheck_flowchart():
    fig, ax = plt.subplots(figsize=(11, 5.0), dpi=220)
    fig.patch.set_facecolor(C_WHITE)
    ax.set_facecolor("#F8F9FA")
    ax.axis('off')

    ax.text(0.5, 0.94, "Autonomous 4-Tier Health Fact-Checking Engine Pipeline ($0 Cost)", 
            ha='center', fontsize=13.5, fontweight='bold', color=C_NAVY)

    steps = [
        ("Tier 0: Fast Guard", "Lethal First-Aid Regex\n(Dog bites, Snakebites, Burns)\nLatency: <0.01s", "#FDEDEC", C_RED, 0.05),
        ("Tier 1: Hash Cache", "Exact MD5 / SHA-256 Cache\nInstant Memory Hits\nLatency: <0.02s", "#EBF5FB", "#2980B9", 0.29),
        ("Tier 2: Semantic FAISS", "LaBSE Vector Projection\nCosine Sim Threshold >= 0.82\nLatency: <0.15s", "#FEF9E7", C_GOLD, 0.53),
        ("Tier 3: Web Consensus", "DuckDuckGo / WHO / CDC\nMulti-Source Evidence Harvester\nLatency: 2 - 4s", "#E8F8F5", C_TEAL, 0.77),
    ]

    for title, desc, bg, border, x in steps:
        box = FancyBboxPatch((x, 0.40), 0.20, 0.46, boxstyle="round,pad=0.02,rounding_size=0.03",
                             color=bg, ec=border, lw=2)
        ax.add_patch(box)
        ax.text(x + 0.10, 0.78, title, fontsize=10.5, fontweight='bold', color=border, ha='center')
        ax.text(x + 0.10, 0.58, desc, fontsize=8.5, color=C_DARK, ha='center')

        if x < 0.70:
            ax.annotate('', xy=(x + 0.24, 0.63), xytext=(x + 0.20, 0.63),
                        arrowprops=dict(arrowstyle="->", color=C_NAVY, lw=2.2, mutation_scale=14))

    synth_box = FancyBboxPatch((0.05, 0.12), 0.92, 0.22, boxstyle="round,pad=0.02,rounding_size=0.03",
                               color=C_NAVY, ec=C_CYAN, lw=2)
    ax.add_patch(synth_box)
    ax.text(0.5, 0.26, "Tier 4: Local Small Language Model (Qwen3-1.7B) Synthesis & Verdict Badging", 
            fontsize=11, fontweight='bold', color=C_WHITE, ha='center')
    ax.text(0.5, 0.16, "Emits Structured Output: [FACT CHECK: FALSE / MISLEADING] with Calibrated Confidence % and Official WHO/MoHFW Citations", 
            fontsize=8.5, color=C_CYAN, ha='center')

    ax.set_xlim(0, 1.02)
    ax.set_ylim(0.08, 1.0)

    out_path = "docs/ppt_assets/factcheck_flowchart.png"
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# 5. SURVEILLANCE ANOMALY MATH & CURVE (docs/ppt_assets/surveillance_chart.png)
# -------------------------------------------------------------
def generate_surveillance_chart():
    fig, ax = plt.subplots(figsize=(7.5, 4.8), dpi=220)
    fig.patch.set_facecolor(C_WHITE)
    ax.set_facecolor("#FAFCFF")

    days = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    day_labels = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7", "Today (24h)"]
    baseline_cases = np.array([1, 0, 1, 1, 0, 2, 1, 1])
    spike_cases = np.array([1, 0, 1, 1, 0, 2, 1, 13])

    ax.plot(days[:-1], baseline_cases[:-1], color="#2980B9", marker='o', lw=2.2, label="7-Day Rolling Baseline (B = 0.86 cases/day)")
    ax.plot(days[-2:], [1, 13], color=C_RED, marker='s', markersize=8, lw=3, linestyle='--', label="Surge Vector")
    ax.scatter(8, 13, color=C_RED, s=160, zorder=5, edgecolors=C_NAVY, lw=2)

    ax.axhline(y=1.72, color=C_GOLD, linestyle=':', lw=2, label="Anomaly Threshold Trigger (2.0x Baseline)")
    ax.fill_between([1, 8], 1.72, 15, color="#FDEDEC", alpha=0.35)

    ax.annotate("OUTBREAK SPIKE ALERT!\nPINCODE 110001 (New Delhi)\nN=13 Cases in 24h\n15.1x Above Normal Baseline", 
                xy=(8, 13), xytext=(4.2, 9.5),
                arrowprops=dict(facecolor=C_RED, shrink=0.08, width=2, headwidth=8),
                bbox=dict(boxstyle="round,pad=0.5", fc="#FDEDEC", ec=C_RED, lw=2),
                fontsize=9.5, fontweight='bold', color=C_RED)

    ax.set_xticks(days)
    ax.set_xticklabels(day_labels, rotation=15, fontsize=9.5)
    ax.set_ylabel("Reported Symptom Inquiries", fontsize=11, fontweight='bold', color=C_DARK)
    ax.set_title("Geospatial Syndromic Anomaly Detection: 7-Day Baseline vs 24h Surge", 
                 fontsize=11.5, fontweight='bold', color=C_NAVY, pad=10)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_ylim(-0.5, 15)
    ax.legend(loc='upper left', fontsize=8.5, framealpha=0.9)

    out_path = "docs/ppt_assets/surveillance_chart.png"
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# 6. RESULTS SCORECARD & COMPARISON (docs/ppt_assets/results_scorecard.png)
# -------------------------------------------------------------
def generate_results_scorecard():
    fig, ax = plt.subplots(figsize=(10.5, 4.4), dpi=220)
    fig.patch.set_facecolor(C_WHITE)
    ax.set_facecolor("#F8F9FA")
    ax.axis('off')

    ax.text(0.5, 0.92, "Empirical Validation Summary Across 15 Health Claim Typologies", 
            ha='center', fontsize=13, fontweight='bold', color=C_NAVY)

    cards = [
        ("15 / 15", "100% Pass Rate", "100% Fact-Check Accuracy\nAcross Clinical, Food, Myth\nand Hinglish Categories", "#D5F5E3", C_TEAL, 0.04),
        ("$0.00", "Zero Cost", "100% Autonomous\nNo Google/OpenAI API Keys\nNo Credit Card Mandate", "#EBF5FB", "#2980B9", 0.28),
        ("< 0.15s", "Sub-Second", "Instant Local Retrieval\nVia Memory-Mapped LaBSE\nand SHA-256 Hashing", "#FEF9E7", C_GOLD, 0.52),
        ("14 Days", "Early Warning", "Proactive Community Lead\nOver Lagging Centralized\nHospital Registries", "#FADBD8", C_RED, 0.76),
    ]

    for stat, badge, desc, bg, border, x in cards:
        box = FancyBboxPatch((x, 0.16), 0.20, 0.68, boxstyle="round,pad=0.03,rounding_size=0.04",
                             color=bg, ec=border, lw=2.2)
        ax.add_patch(box)
        ax.text(x + 0.10, 0.72, stat, fontsize=20, fontweight='bold', color=border, ha='center')
        
        badge_box = FancyBboxPatch((x + 0.02, 0.56), 0.16, 0.10, boxstyle="round,pad=0.01,rounding_size=0.02",
                                   color=border)
        ax.add_patch(badge_box)
        ax.text(x + 0.10, 0.61, badge, fontsize=8.5, fontweight='bold', color=C_WHITE, ha='center')

        ax.text(x + 0.10, 0.36, desc, fontsize=8.5, color=C_DARK, ha='center')

    ax.set_xlim(0, 1.0)
    ax.set_ylim(0.08, 1.0)

    out_path = "docs/ppt_assets/results_scorecard.png"
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# 7. PHASE 4 ROADMAP TIMELINE (docs/ppt_assets/roadmap_visual.png)
# -------------------------------------------------------------
def generate_roadmap_visual():
    fig, ax = plt.subplots(figsize=(11, 4.4), dpi=220)
    fig.patch.set_facecolor(C_WHITE)
    ax.set_facecolor("#F8F9FA")
    ax.axis('off')

    ax.text(0.5, 0.92, "Phase 4 Execution Timeline & Strategic Milestones", 
            ha='center', fontsize=13.5, fontweight='bold', color=C_NAVY)

    phases = [
        ("Phase 4A", "WhatsApp & SMS Gateway", "Months 1 - 2", 
         "• Meta WhatsApp Cloud API\n• SMS / USSD fallback\n• Reaches 500M+ rural users\n  without downloading apps", 
         "#EBF5FB", "#2980B9", 0.05),
        ("Phase 4B", "Vernacular Speech AI", "Months 3 - 4", 
         "• IndicWav2Vec / Bhashini\n• Whisper Voice Activity Det.\n• Dual-way Voice UI\n• Eliminates literacy barrier", 
         "#FEF9E7", C_GOLD, 0.38),
        ("Phase 4C", "ASHA Pilot & Edge TPU", "Months 5 - 6", 
         "• Clinical pilot at rural PHCs\n• Direct IDSP API sync\n• 4-bit Edge-TPU APK\n• Offline district operation", 
         "#E8F8F5", C_TEAL, 0.71),
    ]

    for p_id, p_title, p_time, p_desc, bg, border, x in phases:
        box = FancyBboxPatch((x, 0.14), 0.24, 0.70, boxstyle="round,pad=0.03,rounding_size=0.04",
                             color=bg, ec=border, lw=2.2)
        ax.add_patch(box)
        ax.text(x + 0.12, 0.74, p_id, fontsize=12, fontweight='bold', color=border, ha='center')
        ax.text(x + 0.12, 0.65, p_title, fontsize=10, fontweight='bold', color=C_NAVY, ha='center')
        ax.text(x + 0.12, 0.57, f"[{p_time}]", fontsize=8.5, fontweight='bold', color=border, ha='center')
        ax.text(x + 0.12, 0.34, p_desc, fontsize=8.5, color=C_DARK, ha='center')

        if x < 0.65:
            ax.annotate('', xy=(x + 0.28, 0.50), xytext=(x + 0.25, 0.50),
                        arrowprops=dict(arrowstyle="->", color=border, lw=2.5, mutation_scale=15))

    ax.set_xlim(0, 1.0)
    ax.set_ylim(0.08, 1.0)

    out_path = "docs/ppt_assets/roadmap_visual.png"
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

if __name__ == "__main__":
    generate_hero_emblem()
    generate_motivation_infographic()
    generate_labse_concept()
    generate_factcheck_flowchart()
    generate_surveillance_chart()
    generate_results_scorecard()
    generate_roadmap_visual()
    print("All presentation visual assets generated successfully!")
