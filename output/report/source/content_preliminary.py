"""
Preliminary Pages Generator for AarogyaSathi Minor Project Report
Includes:
1. Cover Page (Unnumbered)
2. Institute Vision and Mission (Page ii)
3. POs, COs, SDGs (Page iii)
4. Department Vision, Mission, PEOs and PSOs (Page iv)
5. CO-PO and CO-PSO Mapping with Justifications (Pages v - vi)
6. Project to SDG Mapping with Justifications (Page vii)
7. Declaration (Page viii)
8. Certificate (Page ix)
9. Acknowledgement (Page x)
10. Abstract (Page xi) - Exactly 1 page
11. Table of Contents (Pages xii - xiii)
12. List of Figures (Page xiv)
13. List of Tables (Page xv)
"""

from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER

# Filled by build_report.py after a first render (title/ID -> page label)
PAGEMAP = {}
TEXT_WIDTH_IN = 5.77


def _leader_line(doc, left_runs, page, size, bold_page=False, indent=0.0, before=2, after=2):
    """One contents line with a right-aligned page number and a dotted leader."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = 1.15
    pf.left_indent = Inches(indent + 0.0)
    pf.first_line_indent = Inches(0)
    pf.tab_stops.add_tab_stop(Inches(TEXT_WIDTH_IN), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    for text, bold in left_runs:
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(size)
        r.bold = bold
    r = p.add_run("	" + page)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(size)
    r.bold = bold_page
    return p



def add_cover_page(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("BHAGWAN PARSHURAM INSTITUTE OF TECHNOLOGY\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.bold = True

    r2 = p.add_run("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING - DATA SCIENCE\n\n")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(13)
    r2.bold = True

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(14)
    p_title.paragraph_format.line_spacing = 1.2
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("AAROGYASATHI: AI-DRIVEN PUBLIC HEALTH CHATBOT FOR DISEASE AWARENESS\n")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(18)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(26, 54, 93)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(10)
    p_sub.paragraph_format.space_after = Pt(14)
    p_sub.paragraph_format.line_spacing = 1.2
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("A MINOR PROJECT DISSERTATION\n")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(14)
    r_sub.bold = True
    r_sub2 = p_sub.add_run("submitted in partial fulfillment of the requirement for the award of the degree of\n")
    r_sub2.font.name = 'Times New Roman'
    r_sub2.font.size = Pt(12)
    r_sub2.italic = True
    r_sub3 = p_sub.add_run("Bachelor of Technology\nin\nComputer Science & Engineering - Data Science\n\n")
    r_sub3.font.name = 'Times New Roman'
    r_sub3.font.size = Pt(13)
    r_sub3.bold = True

    p_team = doc.add_paragraph()
    p_team.paragraph_format.space_before = Pt(12)
    p_team.paragraph_format.space_after = Pt(12)
    p_team.paragraph_format.line_spacing = 1.15
    p_team.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    r_by = p_team.add_run("Submitted by:\n")
    r_by.font.name = 'Times New Roman'
    r_by.font.size = Pt(12)
    r_by.bold = True

    students = [
        ("SALMAN MOHAMMAD KHAN", "00520815723"),
        ("DHAIRYA SUMMI", "00420815723"),
        ("SIDHARTH SINGH", "01820815723")
    ]
    for name, roll in students:
        r_s = p_team.add_run(f"{name} (Enrollment No. {roll})\n")
        r_s.font.name = 'Times New Roman'
        r_s.font.size = Pt(11.5)

    p_sup = doc.add_paragraph()
    p_sup.paragraph_format.space_before = Pt(12)
    p_sup.paragraph_format.space_after = Pt(20)
    p_sup.paragraph_format.line_spacing = 1.15
    p_sup.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    r_sup_title = p_sup.add_run("Under the Supervision of:\n")
    r_sup_title.font.name = 'Times New Roman'
    r_sup_title.font.size = Pt(12)
    r_sup_title.bold = True

    r_sup = p_sup.add_run("Mr. Aditya Sam Koshy\nAssistant Professor\nDepartment of Computer Science and Engineering\n")
    r_sup.font.name = 'Times New Roman'
    r_sup.font.size = Pt(12)

    p_foot = doc.add_paragraph()
    p_foot.paragraph_format.space_before = Pt(14)
    p_foot.paragraph_format.space_after = Pt(0)
    p_foot.paragraph_format.line_spacing = 1.15
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_foot = p_foot.add_run(
        "Department of Computer Science & Engineering - Data Science\n"
        "Bhagwan Parshuram Institute of Technology\n"
        "Affiliated to Guru Gobind Singh Indraprastha University, Delhi\n"
        "PSP-4, Sector-17, Rohini, Delhi - 110089\n\n"
        "NOVEMBER 2026"
    )
    r_foot.font.name = 'Times New Roman'
    r_foot.font.size = Pt(11)
    r_foot.bold = True

def add_institute_vision_mission(doc):
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_before = Pt(12)
    p_h.paragraph_format.space_after = Pt(18)
    r = p_h.add_run("BHAGWAN PARSHURAM INSTITUTE OF TECHNOLOGY\nVISION AND MISSION OF THE INSTITUTE")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.bold = True

    p_v = doc.add_paragraph()
    p_v.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_v.paragraph_format.space_before = Pt(10)
    p_v.paragraph_format.space_after = Pt(6)
    r_v = p_v.add_run("VISION OF THE INSTITUTE")
    r_v.font.name = 'Times New Roman'
    r_v.font.size = Pt(12)
    r_v.bold = True

    v_points = [
        "To establish a leading Global Center of Excellence in multidisciplinary education, training and research in the area of Engineering, Technology and Management.",
        "To produce technologically competent, morally & emotionally strong and ethically sound professionals who excel in their chosen field, practice commitment to their profession and dedicate themselves to the service of mankind."
    ]
    for pt in v_points:
        p_pt = doc.add_paragraph(style='List Bullet')
        p_pt.paragraph_format.space_before = Pt(0)
        p_pt.paragraph_format.space_after = Pt(4)
        p_pt.paragraph_format.line_spacing = 1.35
        p_pt.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_pt = p_pt.add_run(pt)
        r_pt.font.name = 'Times New Roman'
        r_pt.font.size = Pt(12)

    p_m = doc.add_paragraph()
    p_m.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_m.paragraph_format.space_before = Pt(14)
    p_m.paragraph_format.space_after = Pt(6)
    r_m = p_m.add_run("MISSION OF THE INSTITUTE")
    r_m.font.name = 'Times New Roman'
    r_m.font.size = Pt(12)
    r_m.bold = True

    m_points = [
        "To develop world class Laboratories and other Infrastructure conducive in acquiring latest knowledge and expertise.",
        "To bridge the knowledge and competency gaps of institute’s fresh pass-outs vis-à-vis field requirements.",
        "To strengthen Industry-Institute Interaction and partnership for imbibing corporate culture amongst our faculty and students.",
        "To promote research culture among faculty and students enhancing their academic and professional confidence needed to face global challenges.",
        "To honor commitment towards social and moral values."
    ]
    for pt in m_points:
        p_pt = doc.add_paragraph(style='List Bullet')
        p_pt.paragraph_format.space_before = Pt(0)
        p_pt.paragraph_format.space_after = Pt(4)
        p_pt.paragraph_format.line_spacing = 1.35
        p_pt.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_pt = p_pt.add_run(pt)
        r_pt.font.name = 'Times New Roman'
        r_pt.font.size = Pt(12)

def add_pos_cos_sdgs(doc, add_table_fn):
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_before = Pt(10)
    p_h.paragraph_format.space_after = Pt(12)
    r = p_h.add_run("PROGRAM OUTCOMES (POs), COURSE OUTCOMES (COs),\nAND SUSTAINABLE DEVELOPMENT GOALS (SDGs)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True

    p_po = doc.add_paragraph()
    p_po.paragraph_format.space_before = Pt(6)
    p_po.paragraph_format.space_after = Pt(4)
    r_po = p_po.add_run("PROGRAM OUTCOMES (POs)")
    r_po.font.name = 'Times New Roman'
    r_po.font.size = Pt(12)
    r_po.bold = True

    pos = [
        ("PO 1. Engineering Knowledge", "Apply knowledge of mathematics, natural science, computing, and engineering fundamentals and an engineering specialization to solve complex engineering problems."),
        ("PO 2. Problem Analysis", "Identify, formulate, and analyze complex engineering problems, reaching substantiated conclusions considering holistic aspects."),
        ("PO 3. Design/development of Solutions", "Design creative solutions for complex engineering problems and design systems/components that meet identified needs with consideration for public health and safety, cultural, societal, and environmental factors."),
        ("PO 4. Conduct Investigations of Complex Problems", "Conduct investigations using research-based knowledge and methods, including design of experiments, data analysis, and synthesis to provide valid conclusions."),
        ("PO 5. Engineering Tool Usage", "Create, select, and apply appropriate techniques, modern engineering and IT tools, prediction, and modeling to solve complex problems, recognizing limitations."),
        ("PO 6. The Engineer and the World", "Analyze and evaluate societal and environmental aspects while solving complex problems, considering impacts on economy, health, safety, legal frameworks, and environment."),
        ("PO 7. Ethics", "Apply ethical principles and commit to professional ethics, human values, diversity, and inclusion; adhere to relevant laws."),
        ("PO 8. Individual and Collaborative Team Work", "Function effectively as an individual and as a member or leader in diverse and multidisciplinary teams."),
        ("PO 9. Communication", "Communicate effectively and inclusively with the engineering community and society, writing effective reports, documentation, and presentations."),
        ("PO 10. Project Management and Finance", "Apply engineering management principles and economic decision-making to manage multidisciplinary projects."),
        ("PO 11. Life-long Learning", "Recognize the need for, and have the ability for independent and lifelong learning in the broadest context of technological change.")
    ]
    for code, desc in pos:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_before = Pt(0)
        p_item.paragraph_format.space_after = Pt(2)
        p_item.paragraph_format.line_spacing = 1.0
        p_item.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_c = p_item.add_run(f"{code}: ")
        r_c.font.name = 'Times New Roman'
        r_c.font.size = Pt(12)
        r_c.bold = True
        r_d = p_item.add_run(desc)
        r_d.font.name = 'Times New Roman'
        r_d.font.size = Pt(12)

    p_co = doc.add_paragraph()
    p_co.paragraph_format.space_before = Pt(6)
    p_co.paragraph_format.space_after = Pt(4)
    r_co = p_co.add_run("COURSE OUTCOMES (COs) - MINOR PROJECT (ES-451)")
    r_co.font.name = 'Times New Roman'
    r_co.font.size = Pt(12)
    r_co.bold = True

    cos = [
        ("CO 1", "Apply engineering knowledge and design principles to identify, formulate, and solve a complex problem through a structured project."),
        ("CO 2", "Conduct systematic investigation and analysis using modern tools and techniques for designing and implementing the Project."),
        ("CO 3", "Demonstrate professional documentation, effective oral communication, and presentation skills through the dissertation."),
        ("CO 4", "Work ethically as an individual or in a team to manage the Project effectively, considering societal, environmental, and sustainability aspects.")
    ]
    for code, desc in cos:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_before = Pt(0)
        p_item.paragraph_format.space_after = Pt(2)
        p_item.paragraph_format.line_spacing = 1.0
        p_item.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_c = p_item.add_run(f"{code}: ")
        r_c.font.name = 'Times New Roman'
        r_c.font.size = Pt(12)
        r_c.bold = True
        r_d = p_item.add_run(desc)
        r_d.font.name = 'Times New Roman'
        r_d.font.size = Pt(12)

def add_department_vision_mission(doc):
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_before = Pt(10)
    p_h.paragraph_format.space_after = Pt(14)
    r = p_h.add_run("BHAGWAN PARSHURAM INSTITUTE OF TECHNOLOGY\nDEPARTMENT OF COMPUTER SCIENCE & ENGINEERING - DATA SCIENCE\nDEPARTMENT VISION, MISSION, PEOs AND PSOs")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True

    p_v = doc.add_paragraph()
    p_v.paragraph_format.space_before = Pt(6)
    p_v.paragraph_format.space_after = Pt(4)
    r_v = p_v.add_run("VISION OF THE DEPARTMENT")
    r_v.font.name = 'Times New Roman'
    r_v.font.size = Pt(12)
    r_v.bold = True

    p_vt = doc.add_paragraph()
    p_vt.paragraph_format.space_before = Pt(0)
    p_vt.paragraph_format.space_after = Pt(6)
    p_vt.paragraph_format.line_spacing = 1.0
    p_vt.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_vt = p_vt.add_run(
        "To be a leading centre of excellence in the field of Computer Science Engineering in the realms of Data Science education, "
        "research, and innovation, committed to empowering students to lead data-driven decision-making for the betterment of society."
    )
    r_vt.font.name = 'Times New Roman'
    r_vt.font.size = Pt(12)

    p_m = doc.add_paragraph()
    p_m.paragraph_format.space_before = Pt(8)
    p_m.paragraph_format.space_after = Pt(4)
    r_m = p_m.add_run("MISSION OF THE DEPARTMENT")
    r_m.font.name = 'Times New Roman'
    r_m.font.size = Pt(12)
    r_m.bold = True

    d_missions = [
        "To deliver comprehensive education in Data Science by integrating core principles of Computer Science with modern analytical and computational tools to build competent and industry-ready professionals.",
        "To cultivate self-driven learners capable of recognizing and responding to modern societal and technological needs through research, higher studies, or entrepreneurship.",
        "To empower students with critical thinking and problem-solving skills to lead and innovate in Data Science and related fields.",
        "To foster meaningful industry engagement for the enrichment of all stakeholders.",
        "To instil ethical data practices through the development of professional integrity, social responsibility, and a lifelong commitment to learning in students."
    ]
    for dm in d_missions:
        p_pt = doc.add_paragraph(style='List Bullet')
        p_pt.paragraph_format.space_before = Pt(0)
        p_pt.paragraph_format.space_after = Pt(3)
        p_pt.paragraph_format.line_spacing = 1.0
        p_pt.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_pt = p_pt.add_run(dm)
        r_pt.font.name = 'Times New Roman'
        r_pt.font.size = Pt(12)

    p_peo = doc.add_paragraph()
    p_peo.paragraph_format.space_before = Pt(8)
    p_peo.paragraph_format.space_after = Pt(4)
    r_peo = p_peo.add_run("PROGRAM EDUCATIONAL OBJECTIVES (PEOs)")
    r_peo.font.name = 'Times New Roman'
    r_peo.font.size = Pt(12)
    r_peo.bold = True

    peos = [
        ("PEO 1. Professional Excellence and Adaptability", "Graduates will establish themselves as successful professionals, researchers, or entrepreneurs in Data Science by applying analytical, computational, and domain-specific knowledge to solve real-world problems while adapting to emerging technologies."),
        ("PEO 2. Ethics, Social Responsibility, and Leadership", "Graduates will uphold ethical standards and social responsibility in data handling and decision-making while demonstrating leadership and teamwork in multidisciplinary environments."),
        ("PEO 3. Collaborative Engagement and Social Interaction", "Graduates will communicate effectively and collaborate with diverse teams, nurturing productive community engagement.")
    ]
    for code, desc in peos:
        p_pt = doc.add_paragraph()
        p_pt.paragraph_format.space_before = Pt(0)
        p_pt.paragraph_format.space_after = Pt(2)
        p_pt.paragraph_format.line_spacing = 1.0
        p_pt.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_c = p_pt.add_run(f"{code}: ")
        r_c.font.name = 'Times New Roman'
        r_c.font.size = Pt(12)
        r_c.bold = True
        r_d = p_pt.add_run(desc)
        r_d.font.name = 'Times New Roman'
        r_d.font.size = Pt(12)

    p_pso = doc.add_paragraph()
    p_pso.paragraph_format.space_before = Pt(8)
    p_pso.paragraph_format.space_after = Pt(4)
    r_pso = p_pso.add_run("PROGRAM SPECIFIC OUTCOMES (PSOs) (w.e.f 2021)")
    r_pso.font.name = 'Times New Roman'
    r_pso.font.size = Pt(12)
    r_pso.bold = True

    psos = [
        ("PSO 1", "Apply core concepts of Computer Science and Data Science to develop effective and scalable solutions by leveraging data collection, processing, visualization, statistical modeling, and machine learning for real-world problems."),
        ("PSO 2", "Design and develop sustainable data-driven intelligent systems using engineering principles and modern tools, while embracing lifelong learning to adapt to emerging technologies."),
        ("PSO 3", "Graduates will demonstrate ethical and legal awareness in data usage, along with strong communication skills, enabling them to succeed as professionals, entrepreneurs, or in higher studies.")
    ]
    for code, desc in psos:
        p_pt = doc.add_paragraph()
        p_pt.paragraph_format.space_before = Pt(0)
        p_pt.paragraph_format.space_after = Pt(2)
        p_pt.paragraph_format.line_spacing = 1.0
        p_pt.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_c = p_pt.add_run(f"{code}: ")
        r_c.font.name = 'Times New Roman'
        r_c.font.size = Pt(12)
        r_c.bold = True
        r_d = p_pt.add_run(desc)
        r_d.font.name = 'Times New Roman'
        r_d.font.size = Pt(12)

def add_co_po_mapping(doc, add_table_fn):
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_before = Pt(8)
    p_h.paragraph_format.space_after = Pt(10)
    r = p_h.add_run("CO–PO AND CO–PSO MAPPING WITH JUSTIFICATIONS")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True

    # CO-PO Table
    headers = ["CO", "PO1", "PO2", "PO3", "PO4", "PO5", "PO6", "PO7", "PO8", "PO9", "PO10", "PO11"]
    rows = [
        ["CO1", "3", "2", "2", "2", "1", "1", "1", "1", "1", "1", "1"],
        ["CO2", "2", "3", "3", "2", "3", "1", "1", "0", "1", "1", "2"],
        ["CO3", "1", "2", "1", "1", "2", "0", "0", "1", "2", "3", "1"],
        ["CO4", "0", "0", "0", "0", "0", "3", "3", "3", "2", "1", "1"]
    ]
    col_w = [0.55] + [0.47] * 11
    add_table_fn(doc, headers, rows, "1", "CO–PO Correlation Matrix for Minor Project", col_w)

    p_just = doc.add_paragraph()
    p_just.paragraph_format.space_before = Pt(4)
    p_just.paragraph_format.space_after = Pt(4)
    r_j = p_just.add_run("Project-Specific Justification for CO–PO Mapping:")
    r_j.font.name = 'Times New Roman'
    r_j.font.size = Pt(12)
    r_j.bold = True

    justifications = [
        ("CO1 (Apply knowledge and design principles)", 
         "Mapped strongly to PO1 (3) through the mathematical formulation of character n-gram TF-IDF representations, logistic regression intent extraction, and cosine similarity ranking with Language-agnostic BERT Sentence Embeddings (LaBSE). Substantial mapping to PO2-PO4 (2) through problem decomposition of rural infodemics and empirical evaluation across 49 clinical records, 13 vaccine milestones, and 64 Indian myth entries."),
        ("CO2 (Systematic investigation and implementation)", 
         "High correlation with PO2 (3), PO3 (3), and PO5 (3) through the design and deployment of the hybrid conversational pipeline, integration of scikit-learn 1.9.0, PyTorch 2.6.0, Transformers 5.15.1, Ollama local inference (Qwen3:1.7b), FastAPI ASGI architecture, and Meta WhatsApp Cloud API v25.0 webhook routing over Cloudflare secure tunnels on an Ubuntu ARM64 Oracle Cloud VM."),
        ("CO3 (Documentation and communication)", 
         "Strongly mapped to PO10 (3) and PO9 (2) through structured engineering documentation, architecture diagrams, sequence models, data flow models, and formal dissertation synthesis adhering strictly to college engineering formatting and APA reference standards."),
        ("CO4 (Ethics, teamwork, and sustainability)", 
         "Directly correlates with PO6 (3), PO7 (3), and PO8 (3) through adherence to WHO ethical guidelines for health AI, rigorous implementation of non-diagnostic clinical safety disclaimers, emergency triage escalation (108/112 hotlines), limited retention of personal data, collaborative peer pair programming, and git version-controlled task division.")
    ]
    for title, text in justifications:
        p_pt = doc.add_paragraph()
        p_pt.paragraph_format.space_before = Pt(0)
        p_pt.paragraph_format.space_after = Pt(2)
        p_pt.paragraph_format.line_spacing = 1.15
        p_pt.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_t = p_pt.add_run(f"• {title}: ")
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(12)
        r_t.bold = True
        r_d = p_pt.add_run(text)
        r_d.font.name = 'Times New Roman'
        r_d.font.size = Pt(12)

    doc.add_page_break()

    # CO-PSO Table
    p_h2 = doc.add_paragraph()
    p_h2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h2.paragraph_format.space_before = Pt(8)
    p_h2.paragraph_format.space_after = Pt(10)
    r2 = p_h2.add_run("CO–PSO MAPPING TABLE AND JUSTIFICATIONS")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(13)
    r2.bold = True

    pso_headers = ["Course Outcome", "PSO 1", "PSO 2", "PSO 3"]
    pso_rows = [
        ["CO1: Identify, formulate, and design data-driven solutions", "3", "2", "2"],
        ["CO2: Systematic investigation and modern tool implementation", "2", "3", "2"],
        ["CO3: Professional technical documentation and presentation", "1", "2", "3"],
        ["CO4: Ethical data handling, teamwork, and sustainability", "1", "2", "3"]
    ]
    pso_col_w = [2.76, 1.0, 1.0, 1.0]
    add_table_fn(doc, pso_headers, pso_rows, "2", "CO–PSO Correlation Matrix for Minor Project", pso_col_w)

    p_pso_just = doc.add_paragraph()
    p_pso_just.paragraph_format.space_before = Pt(6)
    p_pso_just.paragraph_format.space_after = Pt(4)
    r_pj = p_pso_just.add_run("Project-Specific Justification for CO–PSO Mapping:")
    r_pj.font.name = 'Times New Roman'
    r_pj.font.size = Pt(12)
    r_pj.bold = True

    pso_justifications = [
        ("CO1 to PSO1 (Level 3)", "CO1 directly applies core Computer Science and Data Science principles to engineer multilingual NLP pipelines, combining lexical term-frequency modeling and dense semantic embeddings to resolve public health inquiries."),
        ("CO2 to PSO2 (Level 3)", "CO2 involves end-to-end implementation and deployment of an intelligent conversational system using modern cloud platforms (Oracle Cloud Infrastructure ARM64, FastAPI, HuggingFace Transformers, Ollama, and Meta Graph API)."),
        ("CO3 to PSO3 (Level 3)", "CO3 emphasizes professional scientific writing, technical precision, and communication of complex AI architectural principles through structured engineering documentation."),
        ("CO4 to PSO3 (Level 3)", "CO4 instills ethical data practices, clinical disclaimer integration, user privacy safeguards (ephemeral session state without persistent PII storage), and social responsibility in public health communication.")
    ]
    for title, text in pso_justifications:
        p_pt = doc.add_paragraph()
        p_pt.paragraph_format.space_before = Pt(0)
        p_pt.paragraph_format.space_after = Pt(3)
        p_pt.paragraph_format.line_spacing = 1.15
        p_pt.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_t = p_pt.add_run(f"• {title}: ")
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(12)
        r_t.bold = True
        r_d = p_pt.add_run(text)
        r_d.font.name = 'Times New Roman'
        r_d.font.size = Pt(12)

def add_project_to_sdg_mapping(doc, add_table_fn):
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_before = Pt(10)
    p_h.paragraph_format.space_after = Pt(14)
    r = p_h.add_run("PROJECT TO SUSTAINABLE DEVELOPMENT GOAL (SDG) MAPPING")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True

    p_t = doc.add_paragraph()
    p_t.paragraph_format.space_before = Pt(4)
    p_t.paragraph_format.space_after = Pt(8)
    r_t = p_t.add_run("PROJECT TITLE: AarogyaSathi: AI-Driven Public Health Chatbot for Disease Awareness")
    r_t.font.name = 'Times New Roman'
    r_t.font.size = Pt(12)
    r_t.bold = True

    sdg_headers = ["Mapped Sustainable Development Goals", "Relevance Level"]
    sdg_rows = [
        ["SDG 3: Good Health and Well-Being", "Primary Direct Target (High)"],
        ["SDG 10: Reduced Inequalities", "Secondary Target (Substantial)"],
        ["SDG 9: Industry, Innovation, and Infrastructure", "Technological Target (Moderate)"]
    ]
    add_table_fn(doc, sdg_headers, sdg_rows, "3", "Alignment with United Nations Sustainable Development Goals", [4.0, 1.76])

    p_j = doc.add_paragraph()
    p_j.paragraph_format.space_before = Pt(6)
    p_j.paragraph_format.space_after = Pt(6)
    r_j = p_j.add_run("Justification for SDG Mapping:")
    r_j.font.name = 'Times New Roman'
    r_j.font.size = Pt(12)
    r_j.bold = True

    sdg_justifications = [
        ("SDG 3: Good Health and Well-Being (Target 3.3, 3.d)",
         "AarogyaSathi directly contributes to Target 3.3 (combating communicable diseases such as dengue, malaria, and tuberculosis) and Target 3.d (strengthening early warning, risk reduction, and management of national health risks). By disseminating verified WHO/MoHFW preventive guidance, validating viral misinformation, and routing potential emergencies directly to national emergency dispatch lines (108/112), the project promotes community well-being and health literacy."),
        ("SDG 10: Reduced Inequalities (Target 10.2, 10.3)",
         "In rural and semi-urban India, socio-economic and linguistic barriers severely limit access to qualified healthcare professionals. AarogyaSathi democratizes health information access by providing cross-lingual conversational assistance across 12 Indian languages, breaking literacy barriers through ubiquitous mobile channels like WhatsApp and lightweight browser interfaces, ensuring that vulnerable populations receive the same verified health facts as urban communities."),
        ("SDG 9: Industry, Innovation, and Infrastructure (Target 9.b)",
         "The project leverages open-source AI infrastructure (FastAPI, PyTorch, HuggingFace LaBSE, and Ollama) deployed on cloud computing infrastructure (Oracle Cloud ARM64), demonstrating how cost-effective, decentralized digital public infrastructure (DPI) can be developed and sustained in developing nations without commercial cloud dependency.")
    ]
    for title, text in sdg_justifications:
        p_pt = doc.add_paragraph()
        p_pt.paragraph_format.space_before = Pt(0)
        p_pt.paragraph_format.space_after = Pt(4)
        p_pt.paragraph_format.line_spacing = 1.2
        p_pt.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_t = p_pt.add_run(f"• {title}: ")
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(12)
        r_t.bold = True
        r_d = p_pt.add_run(text)
        r_d.font.name = 'Times New Roman'
        r_d.font.size = Pt(12)

def add_declaration(doc):
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_before = Pt(14)
    p_h.paragraph_format.space_after = Pt(24)
    r = p_h.add_run("DECLARATION")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.bold = True

    p_body = doc.add_paragraph()
    p_body.paragraph_format.space_before = Pt(10)
    p_body.paragraph_format.space_after = Pt(14)
    p_body.paragraph_format.line_spacing = 1.5
    p_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_body = p_body.add_run(
        "This is to certify that the material embodied in this Minor Project - Dissertation titled "
        "'AarogyaSathi: AI-Driven Public Health Chatbot for Disease Awareness' being submitted in partial fulfillment "
        "of the requirements for the award of the degree of Bachelor of Technology in Computer Science & Engineering - Data Science "
        "is based on our original work. It is further certified that this Minor Project - Dissertation work has not been submitted "
        "in full or in part to this or any other university for the award of any other degree or diploma. "
        "Our indebtedness to other works has been duly acknowledged at the relevant places."
    )
    r_body.font.name = 'Times New Roman'
    r_body.font.size = Pt(12)

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(50)
    p_space.paragraph_format.space_after = Pt(0)

    # Student Signatures
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(20)
    p_sig.paragraph_format.space_after = Pt(6)
    p_sig.paragraph_format.line_spacing = 1.3
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    students = [
        ("Salman Mohammad Khan", "00520815723"),
        ("Dhairya Summi", "00420815723"),
        ("Sidharth Singh", "01820815723")
    ]
    for name, roll in students:
        r_line = p_sig.add_run("_______________________________\n")
        r_line.font.name = 'Times New Roman'
        r_line.font.size = Pt(11)
        r_name = p_sig.add_run(f"({name})\nEnrollment No. {roll}\n\n")
        r_name.font.name = 'Times New Roman'
        r_name.font.size = Pt(11)
        r_name.bold = True

def add_certificate(doc):
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_before = Pt(14)
    p_h.paragraph_format.space_after = Pt(24)
    r = p_h.add_run("CERTIFICATE")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.bold = True

    p_body = doc.add_paragraph()
    p_body.paragraph_format.space_before = Pt(10)
    p_body.paragraph_format.space_after = Pt(14)
    p_body.paragraph_format.line_spacing = 1.5
    p_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_body = p_body.add_run(
        "This is to certify that the work embodied in this Minor Project - Dissertation titled "
        "'AarogyaSathi: AI-Driven Public Health Chatbot for Disease Awareness' being submitted in partial fulfillment "
        "of the requirements for the award of the degree of Bachelor of Technology in Computer Science & Engineering - Data Science, "
        "is original and has been carried out by Salman Mohammad Khan (Enrollment No. 00520815723), Dhairya Summi (Enrollment No. 00420815723), "
        "and Sidharth Singh (Enrollment No. 01820815723) under my supervision and guidance."
    )
    r_body.font.name = 'Times New Roman'
    r_body.font.size = Pt(12)

    p_body2 = doc.add_paragraph()
    p_body2.paragraph_format.space_before = Pt(10)
    p_body2.paragraph_format.space_after = Pt(14)
    p_body2.paragraph_format.line_spacing = 1.5
    p_body2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_body2 = p_body2.add_run(
        "It is further certified that this Minor Project - Dissertation work has not been submitted in full or in part to this "
        "university or any other university for the award of any other degree or diploma to the best of my knowledge and belief."
    )
    r_body2.font.name = 'Times New Roman'
    r_body2.font.size = Pt(12)

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(45)

    # Signatures Table (Supervisor on left, Incharge on right)
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1, c2 = table.rows[0].cells
    c1.width = Inches(3.2)
    c2.width = Inches(2.56)

    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r1 = p1.add_run(
        "_______________________________\n"
        "(Mr. Aditya Sam Koshy)\n"
        "Faculty Supervisor\n"
        "Assistant Professor\n"
        "Department of Computer Science & Engineering\n"
        "Bhagwan Parshuram Institute of Technology"
    )
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(10.5)

    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r2 = p2.add_run(
        "_______________________________\n"
        "(Dr. Monika Arora)\n"
        "Incharge - CSE-DS\n"
        "Department of CSE-DS\n"
        "Bhagwan Parshuram Institute\nof Technology"
    )
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(10.5)

def add_acknowledgement(doc):
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_before = Pt(14)
    p_h.paragraph_format.space_after = Pt(22)
    r = p_h.add_run("ACKNOWLEDGEMENT")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.bold = True

    p1 = doc.add_paragraph()
    p1.paragraph_format.space_before = Pt(8)
    p1.paragraph_format.space_after = Pt(10)
    p1.paragraph_format.line_spacing = 1.5
    p1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r1 = p1.add_run(
        "An endeavor is not complete and successful till the people who made it possible are given due credit for their guidance and support. "
        "We take this opportunity to express our profound gratitude to all those who have contributed to the successful completion of this Minor Project Dissertation."
    )
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(12)

    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(8)
    p2.paragraph_format.space_after = Pt(10)
    p2.paragraph_format.line_spacing = 1.5
    p2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r2 = p2.add_run(
        "At the very onset, we express our heartfelt gratitude to our faculty supervisor, Mr. Aditya Sam Koshy, Assistant Professor, "
        "Department of Computer Science and Engineering, for providing scholarly guidance, technical direction, and continuous encouragement "
        "throughout the formulation, implementation, and evaluation of AarogyaSathi. His profound insights into software architecture, "
        "machine learning methodologies, and rigorous verification standards kept our work grounded in engineering reality and steered us in the right direction."
    )
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)

    p3 = doc.add_paragraph()
    p3.paragraph_format.space_before = Pt(8)
    p3.paragraph_format.space_after = Pt(10)
    p3.paragraph_format.line_spacing = 1.5
    p3.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r3 = p3.add_run(
        "We extend our sincere thanks to Prof. Payal Pahwa, Principal, Bhagwan Parshuram Institute of Technology, and Dr. Monika Arora, "
        "Incharge, Department of Computer Science & Engineering - Data Science, for providing institutional infrastructure, state-of-the-art facilities, "
        "and continuous academic encouragement to undertake challenging multidisciplinary research."
    )
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(12)

    p4 = doc.add_paragraph()
    p4.paragraph_format.space_before = Pt(8)
    p4.paragraph_format.space_after = Pt(18)
    p4.paragraph_format.line_spacing = 1.5
    p4.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r4 = p4.add_run(
        "Last but not least, we convey our deepest gratitude to our parents, family members, and peers for their unconditional moral support, "
        "patience, and understanding throughout the course of our project work."
    )
    r4.font.name = 'Times New Roman'
    r4.font.size = Pt(12)

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(20)
    p_sig.paragraph_format.space_after = Pt(4)
    p_sig.paragraph_format.line_spacing = 1.3
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_s = p_sig.add_run(
        "Salman Mohammad Khan (00520815723)\n"
        "Dhairya Summi (00420815723)\n"
        "Sidharth Singh (01820815723)\n"
        "B.Tech (CSE-DS), 7th Semester"
    )
    r_s.font.name = 'Times New Roman'
    r_s.font.size = Pt(11)

def add_abstract_page(doc):
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_before = Pt(8)
    p_h.paragraph_format.space_after = Pt(12)
    r = p_h.add_run("ABSTRACT")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.bold = True

    p1 = doc.add_paragraph()
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(4)
    p1.paragraph_format.line_spacing = 1.25
    p1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r1 = p1.add_run(
        "AarogyaSathi (आरोग्यसाथी) is an AI-driven, multilingual public health conversational assistant engineered to provide verified "
        "preventive healthcare guidance, viral health-claim verification, national immunization schedule tracking, and localized syndromic "
        "surveillance. Developed in response to Smart India Hackathon problem statement SIH25049 under the Government of Odisha's healthcare technology theme, "
        "the system addresses the severe infodemic of health misinformation and the acute scarcity of qualified clinical guidance in rural and semi-urban India. "
        "AarogyaSathi implements a multi-tier hybrid architecture combining deterministic rule-based triage, rule-based fast-path intent extraction, "
        "Language-agnostic BERT Sentence Embeddings (LaBSE) for cross-lingual dense semantic retrieval, and retrieval-augmented generation (RAG) powered by a "
        "locally hosted Qwen3 (1.7B parameter) language model alongside Ollama runtime inference pathways. The entire pipeline is deployed on an Oracle Cloud "
        "Infrastructure virtual machine (2 OCPUs, 12 GiB RAM, Ubuntu 24.04 ARM64) serving a FastAPI application, reached through a Cloudflare HTTPS "
        "tunnel, and accessible via a lightweight responsive web portal and a Meta WhatsApp Cloud API test-number channel (outbound API v25.0)."
    )
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(12)

    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(2)
    p2.paragraph_format.space_after = Pt(6)
    p2.paragraph_format.line_spacing = 1.25
    p2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r2 = p2.add_run(
        "System reliability was evaluated through 37 automated unit and regression tests run on the deployment VM on 26 October 2026, covering routing, session caching, "
        "ML classifiers and surveillance anomaly detection—all passing; five WhatsApp webhook security tests added later also passed. Component benchmark evaluations demonstrated "
        "30/30 (100%) exact intent classification, 15/15 (100%) top-1 LaBSE retrieval accuracy, and 34/34 (100%) concordance on categorical health-claim verification "
        "(mean latency 387 ms). However, rigorous evaluation uncovered critical engineering constraints: 14 of 30 intent test inputs duplicated training examples; "
        "lexical red-flag matching caused a negated phrase ('no chest pain, only a mild headache') to falsely trigger emergency ambulance escalation; a month-to-year "
        "conversion defect mapped 2-month infants to the 9–12 month vaccination schedule; and regional Odia vernacular generation dropped into a safe fallback. "
        "A Meta WhatsApp test-number demonstration answered three test messages from an approved recipient with no sending errors recorded in the server logs. AarogyaSathi demonstrates the "
        "feasibility of a low-cost public health information service on free-tier cloud infrastructure while establishing transparent boundaries for clinical safety, negation handling, and verified data linkage."
    )
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(6)
    p_kw.paragraph_format.space_after = Pt(0)
    p_kw.paragraph_format.line_spacing = 1.2
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_kwh = p_kw.add_run("Keywords: ")
    r_kwh.font.name = 'Times New Roman'
    r_kwh.font.size = Pt(12)
    r_kwh.bold = True
    r_kwt = p_kw.add_run("Public Health Informatics, Multilingual Conversational Agents, Retrieval-Augmented Generation (RAG), LaBSE Dense Embeddings, Health Misinformation Verification, Meta WhatsApp Cloud API, Syndromic Surveillance.")
    r_kwt.font.name = 'Times New Roman'
    r_kwt.font.size = Pt(12)
    r_kwt.italic = True

def add_table_of_contents(doc):
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_before = Pt(12)
    p_h.paragraph_format.space_after = Pt(14)
    r = p_h.add_run("TABLE OF CONTENTS")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.bold = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("(Development Based Project)")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(11)
    r_sub.italic = True

    toc_items = [
        # Prelim
        ("Vision and Mission of the Institute", "ii", True),
        ("Program Outcomes (POs), Course Outcomes (COs), and SDGs", "iii", True),
        ("Department Vision, Mission, PEOs and PSOs", "iv", True),
        ("CO–PO and CO–PSO Mapping with Justifications", "v", True),
        ("Project to SDG Mapping with Justifications", "vii", True),
        ("Declaration", "viii", True),
        ("Certificate", "ix", True),
        ("Acknowledgement", "x", True),
        ("Abstract", "xi", True),
        ("List of Figures", "xiv", True),
        ("List of Tables", "xv", True),
        # Chapters
        ("CHAPTER 1: INTRODUCTION", "1", True),
        ("    1.1 Healthcare Information Landscape and the Infodemic", "1", False),
        ("    1.2 Target Audience and Socio-Economic Context in Rural India", "1", False),
        ("    1.3 Project Motivation and Clinical Scope Boundaries", "2", False),
        ("    1.4 Smart India Hackathon Brief (SIH25049) and Objectives", "2", False),
        ("    1.5 Overview of the AarogyaSathi Solution Architecture", "3", False),
        ("    1.6 Background and Literature Review", "4", False),
        ("    1.7 Organization of the Report", "5", False),
        ("CHAPTER 2: PROBLEM STATEMENT", "6", True),
        ("    2.1 Formal Problem Definition", "6", False),
        ("    2.2 Core Project Objectives", "6", False),
        ("    2.3 Key Stakeholders and User Personas", "7", False),
        ("    2.4 System Boundaries, Operating Assumptions, and Clinical Non-Claims", "8", False),
        ("    2.5 Acceptance Criteria and Success Metrics", "9", False),
        ("CHAPTER 3: ANALYSIS", "10", True),
        ("    3.1 Software Requirement Specifications (SRS Overview)", "10", False),
        ("    3.2 Functional Requirements (FR-1 through FR-8)", "10", False),
        ("    3.3 Non-Functional Requirements (NFR-1 through NFR-6)", "11", False),
        ("    3.4 Feasibility Study (Technical, Operational, Economic)", "12", False),
        ("    3.5 Tools, Technologies, and Hardware Platform", "12", False),
        ("    3.6 Use Case Modeling and Actor Interactions", "13", False),
        ("    3.7 Data Flow Modeling (Level 0 and Level 1 DFD)", "14", False),
        ("CHAPTER 4: DESIGN AND ARCHITECTURE", "16", True),
        ("    4.1 System Architecture and Work Breakdown Structure (WBS)", "16", False),
        ("    4.2 Detailed Module Responsibilities", "16", False),
        ("    4.3 Data Storage Architecture: SQLite vs. Curated JSON vs. Sessions", "17", False),
        ("    4.4 Knowledge Base Schema and Domain Taxonomy", "19", False),
        ("    4.5 Cross-Lingual Semantic Retrieval and Dense Vector Search", "19", False),
        ("    4.6 Fallback Intent Classification Taxonomy", "20", False),
        ("    4.7 Multi-Tier Triage, Fast-Path Heuristics, and Routing Flow", "21", False),
        ("    4.8 Health Misinformation Verification Engine", "22", False),
        ("    4.9 Syndromic Telemetry and Outbreak Surveillance Modeling", "23", False),
        ("    4.10 Meta WhatsApp Cloud API Channel Sequence Flow", "23", False),
        ("CHAPTER 5: IMPLEMENTATION", "25", True),
        ("    5.1 System Implementation Overview and Service Topology", "25", False),
        ("    5.2 Core Router and Fast-Path Heuristic Implementation", "25", False),
        ("    5.3 Knowledge Base Retrieval and Dense Vector Search Implementation", "26", False),
        ("    5.4 Misinformation Verification Engine Implementation", "26", False),
        ("    5.5 Meta WhatsApp Webhook Security and Handler Implementation", "27", False),
        ("    5.6 Web Conversational Interface Implementation", "27", False),
        ("    5.7 Conversational Walkthrough and Real-World Query Execution", "28", False),
        ("CHAPTER 6: TESTING AND QUALITY ASSURANCE", "32", True),
        ("    6.1 Comprehensive Verification and Testing Strategy", "32", False),
        ("    6.2 Unit and Regression Test Suite Execution", "32", False),
        ("    6.3 Component Benchmark Evaluation (Intent, Retrieval, Fact-Check)", "33", False),
        ("    6.4 Synthetic End-to-End Query Spot Checks and Clinical Defect Analysis", "34", False),
        ("    6.5 Code Inspection Findings: Vaccination Age Conversion Defect", "36", False),
        ("    6.6 Meta WhatsApp Cloud API Channel Live Verification", "36", False),
        ("    6.7 SIH25049 Challenge Compliance Matrix", "37", False),
        ("CHAPTER 7: SUMMARY AND CONCLUSION", "38", True),
        ("    7.1 Summary of Delivered Work and Technical Achievements", "38", False),
        ("    7.2 Significance for Public Health Information Dissemination", "39", False),
        ("    7.3 Concluding Remarks", "39", False),
        ("CHAPTER 8: LIMITATIONS AND FUTURE WORK", "40", True),
        ("    8.1 Identified Architectural and Clinical Safety Limitations", "40", False),
        ("    8.2 Geographic and Epidemiological Surveillance Modeling Constraints", "40", False),
        ("    8.3 Linguistic and Regional Knowledge Base Gaps", "41", False),
        ("    8.4 Deployment, Privacy, and Channel Constraints", "41", False),
        ("    8.5 Prioritized Strategic Roadmap for Future Enhancements", "41", False),
        ("BIBLIOGRAPHY", "42", True),
        ("APPENDIX A: PRODUCTION HARDWARE & ENVIRONMENT SPECIFICATIONS", "44", True),
        ("APPENDIX B: INTENT CLASSIFICATION TAXONOMY & API DIRECTORY", "45", True)
    ]

    for title, pg, is_major in toc_items:
        pg = PAGEMAP.get(title.strip(), pg)
        indented = title.startswith("    ")
        _leader_line(doc, [(title.strip(), is_major)], pg, 11 if is_major else 10.5, bold_page=is_major,
                     indent=0.3 if indented else 0.0, before=4 if is_major else 0, after=2 if is_major else 1)

def add_list_of_figures(doc):
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_before = Pt(12)
    p_h.paragraph_format.space_after = Pt(16)
    r = p_h.add_run("LIST OF FIGURES")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.bold = True

    figures = [
        ("Figure 1.1", "High-Level Solution Topology and Channel Architecture of AarogyaSathi", "3"),
        ("Figure 3.1", "Use Case Model for Citizen, Health Worker, and Administrative Actors", "13"),
        ("Figure 3.2", "Context-Level Data Flow Diagram (DFD Level 0) for Public Health Inquiries", "14"),
        ("Figure 3.3", "Detailed Functional Data Flow Diagram (DFD Level 1) of Core Engine", "15"),
        ("Figure 4.1", "Work Breakdown Structure (WBS) of AarogyaSathi Engineering Modules", "16"),
        ("Figure 4.2", "Data Storage Architecture: SQLite Telemetry vs. Curated JSON vs. RAM Sessions", "17"),
        ("Figure 4.3", "Activity and Decision Flowchart of Multi-Tier Triage and Fast-Path Routing", "21"),
        ("Figure 4.4", "Meta WhatsApp Cloud API Integration Sequence Flow and Webhook Ingress", "23"),
        ("Figure 5.1", "Web Chat Landing View and Disease-Information Answer (Dengue)", "28"),
        ("Figure 5.2", "Fact-Check Verdict (MYTH) and Hindi Answer for a Malaria Query", "29"),
        ("Figure 5.3", "Administrative Syndromic Surveillance Dashboard Populated with Demonstration Data", "30"),
        ("Figure 5.4", "WhatsApp Exchange on an Approved Test Recipient's Phone: Greeting, Dengue Symptoms and Fact-Check Verdict", "31")
    ]

    for f_id, f_title, f_pg in figures:
        f_pg = PAGEMAP.get(f_id, f_pg)
        _leader_line(doc, [(f_id + ": ", True), (f_title, False)], f_pg, 11, indent=0.0, before=3, after=3)

def add_list_of_tables(doc):
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_before = Pt(12)
    p_h.paragraph_format.space_after = Pt(16)
    r = p_h.add_run("LIST OF TABLES")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.bold = True

    tables = [
        ("Table 1.1", "Comparative Analysis of Conventional Chatbots vs. AarogyaSathi Hybrid Pipeline", "4"),
        ("Table 3.1", "Functional Requirements Specification (FR-1 through FR-8)", "10"),
        ("Table 3.2", "Non-Functional Requirements Specification (NFR-1 through NFR-6)", "11"),
        ("Table 3.3", "Minimum Hardware and Software Execution Environment Specifications", "12"),
        ("Table 4.1", "Curated Knowledge Base Inventory Across Public Health Domains", "19"),
        ("Table 4.2", "Intent Classification Taxonomy and Training Corpus Distribution", "20"),
        ("Table 6.1", "Automated Test Suite Coverage (37 Tests Run on 26 October 2026; 5 Channel Security Tests Added on 31 October 2026)", "32"),
        ("Table 6.2", "Component Benchmark Evaluation Results on Deployed Host", "33"),
        ("Table 6.3", "Selected Live Synthetic Query Spot Checks and Clinical Response Observations", "35"),
        ("Table 6.4", "Meta WhatsApp Cloud API Channel Live Verification Summary", "36"),
        ("Table 6.5", "SIH25049 Challenge Compliance Matrix: Brief Requirements vs. Prototype Status", "37"),
        ("Table 8.1", "Prioritized Strategic Roadmap and Clinical Validation Matrix for Future Work", "41"),
        ("Table A.1", "Oracle Cloud VM Production Hardware and Environment Topology", "44"),
        ("Table B.1", "AarogyaSathi Production REST API Endpoint Directory", "45")
    ]

    for t_id, t_title, t_pg in tables:
        t_pg = PAGEMAP.get(t_id, t_pg)
        _leader_line(doc, [(t_id + ": ", True), (t_title, False)], t_pg, 11, indent=0.0, before=3, after=3)

print("Preliminary content generator module defined successfully.")
