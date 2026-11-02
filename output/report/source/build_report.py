"""
AarogyaSathi Final Minor Project Report Master Builder
Department of Computer Science & Engineering - Data Science
Bhagwan Parshuram Institute of Technology (BPIT), Delhi
Affiliated to Guru Gobind Singh Indraprastha University (GGSIPU), Delhi

Builds:
1. Editable Native DOCX: output/report/AarogyaSathi_Minor_Project_Report_Final.docx
2. Matching Professional PDF: output/report/AarogyaSathi_Minor_Project_Report_Final.pdf
"""

import os
import sys
import subprocess
import pypdf
import docx
from docx.shared import Inches, Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION_START
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

# Import content generators
sys.path.insert(0, os.path.abspath(r"C:\Users\gamer\Desktop\minor project Health chatbot\output\report\source"))
import content_preliminary
import content_chapters_1_3
import content_chapters_4_5
import content_chapters_6_8

BASE_DIR = os.path.abspath(r"C:\Users\gamer\Desktop\minor project Health chatbot")
ASSETS_DIR = os.path.join(BASE_DIR, r"output\report\source\assets")
OUTPUT_DOCX = os.path.join(BASE_DIR, r"output\report\AarogyaSathi_Minor_Project_Report_Final.docx")
OUTPUT_PDF = os.path.join(BASE_DIR, r"output\report\AarogyaSathi_Minor_Project_Report_Final.pdf")
SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"

# XML Helpers
def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_table_borders(table, color="B0BEC5", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def remove_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:bottom w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="none"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_page_number_field(run):
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = 'PAGE'
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    r = run._r
    r.append(fldChar1)
    r.append(instrText)
    r.append(fldChar2)
    r.append(fldChar3)

# Typography Builders
def format_p(p, space_before=0, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.alignment = align
    return p

def add_body_p(doc, text):
    p = doc.add_paragraph()
    format_p(p, space_before=0, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    return p

def add_bullet_p(doc, bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    format_p(p, space_before=0, space_after=4, line_spacing=1.35, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    r_bold = p.add_run(bold_prefix + ": ")
    r_bold.font.name = 'Times New Roman'
    r_bold.font.size = Pt(12)
    r_bold.bold = True
    r_text = p.add_run(text)
    r_text.font.name = 'Times New Roman'
    r_text.font.size = Pt(12)
    return p

def add_chapter_title(doc, chapter_num, chapter_name):
    p = doc.add_paragraph()
    format_p(p, space_before=10, space_after=16, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(f"CHAPTER {chapter_num}\n{chapter_name.upper()}")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True
    return p

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    format_p(p, space_before=14, space_after=6, line_spacing=1.2, align=WD_ALIGN_PARAGRAPH.LEFT)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.bold = True
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    format_p(p, space_before=10, space_after=4, line_spacing=1.2, align=WD_ALIGN_PARAGRAPH.LEFT)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.italic = True
    r.bold = False
    return p

def add_figure(doc, img_name, fig_num, caption_text, width_inches=4.4):
    img_path = os.path.join(ASSETS_DIR, img_name)
    if not os.path.exists(img_path):
        print(f"Warning: Image {img_path} not found!")
        return
    p_img = doc.add_paragraph()
    format_p(p_img, space_before=6, space_after=2, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER)
    p_img.paragraph_format.keep_with_next = True
    r_img = p_img.add_run()
    r_img.add_picture(img_path, width=Inches(width_inches))
    p_cap = doc.add_paragraph()
    format_p(p_cap, space_before=2, space_after=6, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_cap = p_cap.add_run(f"Figure {fig_num}: {caption_text}")
    r_cap.font.name = 'Times New Roman'
    r_cap.font.size = Pt(10)
    r_cap.italic = True

def add_table(doc, headers, rows, tab_num, caption_text, col_widths=None, pad_v=60, font_sz=9.0):
    p_cap = doc.add_paragraph()
    format_p(p_cap, space_before=8, space_after=3, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
    p_cap.paragraph_format.keep_with_next = True
    r_cap = p_cap.add_run(f"Table {tab_num}: {caption_text}")
    r_cap.font.name = 'Times New Roman'
    r_cap.font.size = Pt(10)
    r_cap.bold = True
    
    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="B0BEC5", sz="4")
    
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "F1F5F9")
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=(30 if len(headers) > 8 else 100), right=(30 if len(headers) > 8 else 100))
        p = hdr_cells[i].paragraphs[0]
        format_p(p, space_before=0, space_after=0, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            r.bold = True
            
    for r_idx, row_data in enumerate(rows):
        row_cells = table.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            set_cell_margins(row_cells[c_idx], top=pad_v, bottom=pad_v, left=(30 if len(headers) > 8 else 100), right=(30 if len(headers) > 8 else 100))
            p = row_cells[c_idx].paragraphs[0]
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 or len(str(val)) < 15 else WD_ALIGN_PARAGRAPH.LEFT
            format_p(p, space_before=0, space_after=0, line_spacing=1.15, align=align)
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(font_sz)
                
    for ri, row in enumerate(table.rows):
        row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
        if (len(table.rows) <= 6 and ri < len(table.rows) - 1) or (len(table.rows) > 6 and ri < 2):
            for c in row.cells:
                for pp in c.paragraphs:
                    pp.paragraph_format.keep_with_next = True
    if col_widths:
        table.autofit = False
        for idx, width in enumerate(col_widths):
            table.columns[idx].width = Inches(width)
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)

def add_code_block(doc, code_str):
    p = doc.add_paragraph()
    format_p(p, space_before=4, space_after=8, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
    p.paragraph_format.left_indent = Inches(0.25)
    r = p.add_run(code_str)
    r.font.name = 'Consolas'
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(30, 41, 59)

def build_complete_report():
    print("Initializing document...")
    doc = docx.Document()
    for _sn in ('Normal', 'Footer', 'Header'):
        _st = doc.styles[_sn]
        _st.font.name = 'Times New Roman'
        _st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')

    # SECTION 1: COVER PAGE (copied from the official college format, page 2)
    print("Building Cover Page from the college template...")
    import template_cover
    template_cover.insert_cover(
        doc,
        title="AarogyaSathi: AI-Driven Public Health Chatbot for Disease Awareness",
        students=[("SALMAN MOHAMMAD KHAN", "00520815723"), ("DHAIRYA SUMMI", "00420815723"), ("SIDHARTH SINGH", "01820815723")],
        tight_students=60,
        supervisor="MR. ADITYA SAM KOSHY",
        designation="Assistant Professor, Department of CSE",
        month_year="NOVEMBER 2026")

    # SECTION 2: PRELIMINARY MATTER (the document's final sectPr now describes it)
    s2 = doc.sections[-1]
    s2.page_width = Mm(210)
    s2.page_height = Mm(297)
    s2.top_margin = Inches(1.0)
    s2.bottom_margin = Inches(1.0)
    s2.left_margin = Inches(1.5)
    s2.right_margin = Inches(1.0)

    # Configure Roman lower page numbers starting at ii (page 2)
    sectPr2 = s2._sectPr
    pgNumType2 = OxmlElement('w:pgNumType')
    pgNumType2.set(qn('w:fmt'), 'lowerRoman')
    pgNumType2.set(qn('w:start'), '2')
    sectPr2.append(pgNumType2)

    footer2 = s2.footer
    footer2.is_linked_to_previous = False
    tbl2 = footer2.add_table(1, 2, Inches(5.76))
    tbl2.alignment = WD_TABLE_ALIGNMENT.CENTER
    remove_table_borders(tbl2)
    c1, c2 = tbl2.rows[0].cells
    c1.width = Inches(4.8)
    c2.width = Inches(0.96)
    set_cell_margins(c1, top=0, bottom=0, left=0, right=0)
    set_cell_margins(c2, top=0, bottom=0, left=0, right=0)

    p_fl2 = c1.paragraphs[0]
    p_fl2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_fl2 = p_fl2.add_run("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING-DATA SCIENCE, BPIT")
    r_fl2.font.name = 'Times New Roman'
    r_fl2.font.size = Pt(9.5)

    p_fr2 = c2.paragraphs[0]
    p_fr2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_fr2 = p_fr2.add_run()
    r_fr2.font.name = 'Times New Roman'
    r_fr2.font.size = Pt(10)
    add_page_number_field(r_fr2)

    print("Building Preliminary Pages...")
    content_preliminary.add_institute_vision_mission(doc)
    doc.add_page_break()

    content_preliminary.add_pos_cos_sdgs(doc, add_table)
    doc.add_page_break()

    content_preliminary.add_department_vision_mission(doc)
    doc.add_page_break()

    content_preliminary.add_co_po_mapping(doc, add_table)
    doc.add_page_break()

    content_preliminary.add_project_to_sdg_mapping(doc, add_table)
    doc.add_page_break()

    content_preliminary.add_declaration(doc)
    doc.add_page_break()

    content_preliminary.add_certificate(doc)
    doc.add_page_break()

    content_preliminary.add_acknowledgement(doc)
    doc.add_page_break()

    content_preliminary.add_abstract_page(doc)
    doc.add_page_break()

    content_preliminary.add_table_of_contents(doc)
    doc.add_page_break()

    content_preliminary.add_list_of_figures(doc)
    doc.add_page_break()

    content_preliminary.add_list_of_tables(doc)

    # SECTION 3: CHAPTERS 1 - 8, BIBLIOGRAPHY, APPENDICES (Arabic Pages 1 - 45)
    s3 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    s3.page_width = Mm(210)
    s3.page_height = Mm(297)
    s3.top_margin = Inches(1.0)
    s3.bottom_margin = Inches(1.0)
    s3.left_margin = Inches(1.5)
    s3.right_margin = Inches(1.0)

    sectPr3 = s3._sectPr
    pgNumType3 = OxmlElement('w:pgNumType')
    pgNumType3.set(qn('w:fmt'), 'decimal')
    pgNumType3.set(qn('w:start'), '1')
    sectPr3.append(pgNumType3)

    footer3 = s3.footer
    footer3.is_linked_to_previous = False
    tbl3 = footer3.add_table(1, 2, Inches(5.76))
    tbl3.alignment = WD_TABLE_ALIGNMENT.CENTER
    remove_table_borders(tbl3)
    c31, c32 = tbl3.rows[0].cells
    c31.width = Inches(4.8)
    c32.width = Inches(0.96)
    set_cell_margins(c31, top=0, bottom=0, left=0, right=0)
    set_cell_margins(c32, top=0, bottom=0, left=0, right=0)

    p_fl3 = c31.paragraphs[0]
    p_fl3.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_fl3 = p_fl3.add_run("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING-DATA SCIENCE, BPIT")
    r_fl3.font.name = 'Times New Roman'
    r_fl3.font.size = Pt(9.5)

    p_fr3 = c32.paragraphs[0]
    p_fr3.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_fr3 = p_fr3.add_run()
    r_fr3.font.name = 'Times New Roman'
    r_fr3.font.size = Pt(10)
    add_page_number_field(r_fr3)

    print("Building Chapter 1: Introduction...")
    content_chapters_1_3.add_chapter_1(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_figure, add_table)
    doc.add_page_break()

    print("Building Chapter 2: Problem Statement...")
    content_chapters_1_3.add_chapter_2(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_table)
    doc.add_page_break()

    print("Building Chapter 3: Analysis...")
    content_chapters_1_3.add_chapter_3(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_figure, add_table)
    doc.add_page_break()

    print("Building Chapter 4: Design and Architecture...")
    content_chapters_4_5.add_chapter_4(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_figure, add_table, add_code_block)
    doc.add_page_break()

    print("Building Chapter 5: Implementation...")
    content_chapters_4_5.add_chapter_5(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_figure, add_code_block)
    doc.add_page_break()

    print("Building Chapter 6: Testing and Quality Assurance...")
    content_chapters_6_8.add_chapter_6(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_table, add_code_block)
    doc.add_page_break()

    print("Building Chapter 7: Summary and Conclusion...")
    content_chapters_6_8.add_chapter_7(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2)
    doc.add_page_break()

    print("Building Chapter 8: Limitations and Future Work...")
    content_chapters_6_8.add_chapter_8(doc, add_body_p, add_bullet_p, add_chapter_title, add_heading_1, add_heading_2, add_table)
    doc.add_page_break()

    print("Building Bibliography...")
    content_chapters_6_8.add_bibliography(doc, add_heading_1, add_body_p)
    doc.add_page_break()

    print("Building Appendices...")
    content_chapters_6_8.add_appendices(doc, add_heading_1, add_heading_2, add_body_p, add_table, add_code_block)

    print(f"Saving final DOCX to {OUTPUT_DOCX}...")
    os.makedirs(os.path.dirname(OUTPUT_DOCX), exist_ok=True)
    doc.save(OUTPUT_DOCX)
    print("DOCX saved successfully!")

    print(f"Converting DOCX to PDF using LibreOffice ({SOFFICE_PATH})...")
    cmd = [SOFFICE_PATH, "--headless", "--convert-to", "pdf", OUTPUT_DOCX, "--outdir", os.path.dirname(OUTPUT_PDF)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("LibreOffice conversion failed:", res.stderr)
        return False
    print("PDF generated successfully!")

    # Check page count
    reader = pypdf.PdfReader(OUTPUT_PDF)
    page_count = len(reader.pages)
    print(f"\n==========================================")
    print(f"TOTAL PDF PAGE COUNT: {page_count} PAGES")
    print(f"Target Range: 55 to 60 pages (Budget: 60)")
    print(f"==========================================\n")
    return page_count

import ast
import re


def _roman(n):
    out = ""
    for v, r in [(10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]:
        while n >= v:
            out += r
            n -= v
    return out


def _literal_lists():
    tree = ast.parse(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "content_preliminary.py"), encoding="utf8").read())
    found = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ("toc_items", "figures", "tables"):
            found[node.targets[0].id] = ast.literal_eval(node.value)
    return found


def compute_pagemap(pdf_path):
    """Find the printed page label of every contents / figure / table entry in the rendered PDF."""
    reader = pypdf.PdfReader(pdf_path)
    texts = [re.sub(r"\s+", " ", (p.extract_text() or "")).strip() for p in reader.pages]
    ch1 = next(i for i, t in enumerate(texts, 1) if t.startswith("CHAPTER 1 "))
    lab = lambda phys: _roman(phys) if phys < ch1 else str(phys - ch1 + 1)
    lists = _literal_lists()
    pm = {}
    prelim = {
        "Vision and Mission of the Institute": "VISION AND MISSION OF THE INSTITUTE",
        "Program Outcomes (POs), Course Outcomes (COs), and SDGs": "^PROGRAM OUTCOMES",
        "Department Vision, Mission, PEOs and PSOs": "DEPARTMENT VISION, MISSION, PEOs AND PSOs",
        "CO–PO and CO–PSO Mapping with Justifications": "MAPPING WITH JUSTIFICATIONS",
        "Project to SDG Mapping with Justifications": "PROJECT TO SUSTAINABLE DEVELOPMENT GOAL",
        "Declaration": "^DECLARATION", "Certificate": "^CERTIFICATE", "Acknowledgement": "^ACKNOWLEDGEMENT",
        "Abstract": "^ABSTRACT", "List of Figures": "^LIST OF FIGURES", "List of Tables": "^LIST OF TABLES",
    }
    for title, pat in prelim.items():
        pm[title] = lab(next(i for i, t in enumerate(texts[:ch1 - 1], 1) if i > 1 and re.search(pat, t)))
    missing = []
    for title, _, _ in lists["toc_items"]:
        key = title.strip()
        if key in pm:
            continue
        m = re.match(r"CHAPTER (\d+):", key)
        if m:
            pat = lambda t, n=m.group(1): t.startswith(f"CHAPTER {n} ")
        elif key.startswith(("BIBLIOGRAPHY", "APPENDIX")):
            pat = lambda t, k=key.split(":")[0]: (k + ":") in t if k.startswith("APPENDIX") else t.startswith(k)
        else:
            num, rest = key.split(" ", 1)
            probe = f"{num} {rest[:24]}"
            pat = lambda t, pr=probe: pr in t
        hit = next((i for i, t in enumerate(texts, 1) if i >= ch1 and pat(t)), None)
        if hit is None:
            missing.append(key)
        else:
            pm[key] = lab(hit)
    for kind, items in (("Figure", lists["figures"]), ("Table", lists["tables"])):
        for ident, _, _ in items:
            hit = next((i for i, t in enumerate(texts, 1) if i >= ch1 and f"{ident}: " in t), None)
            if hit is None:
                missing.append(ident)
            else:
                pm[ident] = lab(hit)
    return pm, missing, len(texts), ch1


if __name__ == "__main__":
    import content_preliminary
    count = None
    for attempt in range(4):
        count = build_complete_report()
        pm, missing, n, ch1 = compute_pagemap(OUTPUT_PDF)
        print("Unresolved entries:", missing)
        if pm == content_preliminary.PAGEMAP:
            print("Page map stable after", attempt + 1, "builds; chapter 1 starts on physical page", ch1)
            break
        content_preliminary.PAGEMAP.clear()
        content_preliminary.PAGEMAP.update(pm)
