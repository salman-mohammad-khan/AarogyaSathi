"""Inserts the college cover page (copied from the official format document) into a python-docx document.

The cover XML, border, BPIT logo and the heading styles it relies on come from assets/cover_template.docx,
which is page 2 of 'Minor Proj report format(CSE-DS).docx' with all other content removed.
"""
import copy
import io
import os

from docx import Document
from docx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
COVER = os.path.join(HERE, "assets", "cover_template.docx")
STYLE_IDS = ["Heading1", "Heading2", "Heading3", "Heading4", "BodyText"]


def _direct_text_runs(p):
    """Runs that are direct children of the paragraph and carry text (drawings are left alone)."""
    return [r for r in p.findall(qn("w:r")) if r.find(qn("w:t")) is not None]


def set_text(p, text):
    runs = _direct_text_runs(p)
    first = runs[0]
    for t in first.findall(qn("w:t")):
        first.remove(t)
    t = first.makeelement(qn("w:t"), {})
    t.text = text
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    first.append(t)
    for r in runs[1:]:
        p.remove(r)


def set_space_before(p, twips):
    sp = p.find(qn("w:pPr")).find(qn("w:spacing"))
    sp.set(qn("w:before"), str(twips))


def insert_cover(doc, title, students, supervisor, designation, month_year, tight_students=60):
    tpl = Document(COVER)
    dst_styles = doc.styles.element
    for sid in STYLE_IDS:
        src = tpl.styles.element.xpath(f'w:style[@w:styleId="{sid}"]')
        if not src:
            continue
        for old in dst_styles.xpath(f'w:style[@w:styleId="{sid}"]'):
            dst_styles.remove(old)
        dst_styles.append(copy.deepcopy(src[0]))

    elems = [copy.deepcopy(e) for e in tpl.element.body if e.tag != qn("w:sectPr")]
    # remap image relationships (border group, BPIT logo)
    rid_map = {}
    for e in elems:
        for node in e.iter():
            for attr in (qn("r:embed"), qn("r:id"), qn("r:link")):
                rid = node.get(attr)
                if rid:
                    if rid not in rid_map:
                        blob = tpl.part.related_parts[rid].blob
                        rid_map[rid] = doc.part.get_or_add_image(io.BytesIO(blob))[0]
                    node.set(attr, rid_map[rid])

    # indexes follow the template body: 0=p39 ... 1=p40 title, 11=p50 name, 12=p51 enrollment, 16=p55 supervisor, 17=p56 designation
    title_p, name_p, enr_p, sup_p, des_p = elems[1], elems[11], elems[12], elems[16], elems[17]
    set_text(title_p, title)
    set_text(sup_p, supervisor)
    set_text(des_p, designation)

    name_tpl = copy.deepcopy(name_p)
    enr_run = copy.deepcopy(_direct_text_runs(enr_p)[0])
    blocks = []
    for i, (name, enr) in enumerate(students):
        n = copy.deepcopy(name_tpl)
        set_text(n, name)
        r = copy.deepcopy(enr_run)
        for t in r.findall(qn("w:t")):
            r.remove(t)
        t = r.makeelement(qn("w:t"), {})
        t.text = "  (" + enr + ")"
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        r.append(t)
        n.append(r)
        set_space_before(n, 367 if i == 0 else tight_students)
        blocks.append(n)
    # compress blank spacer paragraphs so the longer title and three students fit the same page frame
    set_space_before(elems[2], 20)
    set_space_before(elems[9], 180)
    set_space_before(elems[15], 330)
    final = elems[:11] + blocks + elems[15:]
    final = [e for k, e in enumerate(final) if e not in ()]

    for p in final:
        if p.tag != qn("w:p"):
            continue
        ppr = p.find(qn("w:pPr"))
        if ppr is None:
            ppr = p.makeelement(qn("w:pPr"), {})
            p.insert(0, ppr)
        sp = ppr.find(qn("w:spacing"))
        if sp is None:
            sp = ppr.makeelement(qn("w:spacing"), {})
            # spacing must precede ind/jc/rPr/sectPr in pPr
            idx = 0
            for k, child in enumerate(ppr):
                if child.tag in (qn("w:pStyle"), qn("w:keepNext"), qn("w:keepLines"), qn("w:pageBreakBefore"), qn("w:widowControl"), qn("w:numPr")):
                    idx = k + 1
            ppr.insert(idx, sp)
        if sp.get(qn("w:after")) is None:
            sp.set(qn("w:after"), "0")
        if sp.get(qn("w:line")) is None:
            sp.set(qn("w:line"), "240")
            sp.set(qn("w:lineRule"), "auto")

    body = doc.element.body
    sentinel = body.find(qn("w:sectPr"))
    for e in final:
        sentinel.addprevious(e)
    return final
