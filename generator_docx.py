import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from texts import DOC

def set_cell_margins(cell, top=60, bottom=60, left=80, right=80):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    borders = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    for edge, val in borders.items():
        if val is not None:
            tag = f'w:{edge}'
            el = OxmlElement(tag)
            el.set(qn('w:val'), val.get('val', 'single'))
            el.set(qn('w:sz'), str(val.get('sz', 4)))
            el.set(qn('w:space'), '0')
            el.set(qn('w:color'), val.get('color', '000000'))
            tcBorders.append(el)
        else:
            tag = f'w:{edge}'
            el = OxmlElement(tag)
            el.set(qn('w:val'), 'none')
            tcBorders.append(el)
    tcPr.append(tcBorders)

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
        f'  <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
        f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
        f'  <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

def set_cell_shading(cell, color_hex="F2F2F2"):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def generate_docx(data: dict, output_path: str):
    lang = data.get("lang", "lat")
    if lang not in DOC:
        lang = "lat"
    labels = DOC[lang]["labels"]
    none_text = DOC[lang]["none"]
    
    doc = Document()
    
    # Standart A4 va rasmiy davlat formati hoshiyalari
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.6)
    section.bottom_margin = Inches(0.6)
    section.left_margin = Inches(0.85)
    section.right_margin = Inches(0.6)
    
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    
    # 1. Markaziy Sarlavha: MA'LUMOTNOMA
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(12)
    t_run = title_p.add_run(DOC[lang]["title"])
    t_run.bold = True
    t_run.font.size = Pt(14)
    
    # 2. Yuqori qism: Chapda F.I.Sh va Lavozim, O'ngda 3x4 rasm
    top_table = doc.add_table(rows=1, cols=2)
    top_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    top_table.autofit = False
    
    cell_info = top_table.cell(0, 0)
    cell_photo = top_table.cell(0, 1)
    
    cell_info.width = Inches(5.1)
    cell_photo.width = Inches(1.7)
    
    set_cell_borders(cell_info)
    set_cell_borders(cell_photo)
    
    # F.I.Sh. (Katta, qalin harflar bilan)
    p_fio = cell_info.paragraphs[0]
    p_fio.paragraph_format.space_before = Pt(0)
    p_fio.paragraph_format.space_after = Pt(6)
    r_fio = p_fio.add_run(data.get("fio", "").strip())
    r_fio.bold = True
    r_fio.font.size = Pt(13)
    
    # Lavozim (faqat mavjud bo'lsa va "yo'q" bo'lmasa)
    pos_val = data.get("position", "").strip()
    if pos_val and pos_val.lower() not in ["yo'q", "йўқ", "нет", "none", "-"]:
        p_pos = cell_info.add_paragraph()
        p_pos.paragraph_format.space_before = Pt(0)
        p_pos.paragraph_format.space_after = Pt(4)
        p_pos.paragraph_format.line_spacing = 1.15
        r_pos = p_pos.add_run(pos_val)
        r_pos.font.size = Pt(10.5)
        
    # 3x4 Rasm
    photo_path = data.get("photo_path")
    p_photo = cell_photo.paragraphs[0]
    p_photo.paragraph_format.space_before = Pt(0)
    p_photo.paragraph_format.space_after = Pt(0)
    
    if photo_path and os.path.exists(photo_path):
        try:
            p_photo.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p_photo.add_run().add_picture(photo_path, width=Inches(1.25), height=Inches(1.65))
        except Exception:
            p_photo.add_run("3x4")
    else:
        # Bo'sh ramka
        p_photo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_borders(cell_photo,
                         top={"sz": 4, "val": "single", "color": "A0A0A0"},
                         bottom={"sz": 4, "val": "single", "color": "A0A0A0"},
                         left={"sz": 4, "val": "single", "color": "A0A0A0"},
                         right={"sz": 4, "val": "single", "color": "A0A0A0"})
        set_cell_margins(cell_photo, top=140, bottom=140, left=40, right=40)
        p_photo.add_run("\n3x4\n").font.color.rgb = RGBColor(160, 160, 160)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # 3. Savol-Javob Jadvali
    fields_to_show = [
        ("birth_date", labels["birth_date"]),
        ("birth_place", labels["birth_place"]),
        ("nationality", labels["nationality"]),
        ("party", labels["party"]),
        ("education", labels["education"]),
        ("graduated", labels["graduated"]),
        ("specialty", labels["specialty"]),
        ("degree", labels["degree"]),
        ("title", labels["title"]),
        ("languages", labels["languages"]),
        ("military", labels["military"]),
        ("awards", labels["awards"]),
        ("deputy", labels["deputy"]),
    ]
    
    info_table = doc.add_table(rows=0, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_table.autofit = False
    
    for key, lbl in fields_to_show:
        raw_val = data.get(key, "").strip()
        val = raw_val if raw_val else none_text
        
        row = info_table.add_row()
        c_lbl = row.cells[0]
        c_val = row.cells[1]
        
        c_lbl.width = Inches(2.7)
        c_val.width = Inches(4.1)
        
        set_cell_margins(c_lbl, top=25, bottom=25, left=40, right=40)
        set_cell_margins(c_val, top=25, bottom=25, left=40, right=40)
        set_cell_borders(c_lbl)
        set_cell_borders(c_val)
        
        p1 = c_lbl.paragraphs[0]
        p1.paragraph_format.space_before = Pt(1)
        p1.paragraph_format.space_after = Pt(1)
        p1.paragraph_format.line_spacing = 1.05
        r1 = p1.add_run(lbl)
        r1.font.size = Pt(10.5)
        
        p2 = c_val.paragraphs[0]
        p2.paragraph_format.space_before = Pt(1)
        p2.paragraph_format.space_after = Pt(1)
        p2.paragraph_format.line_spacing = 1.05
        r2 = p2.add_run(val)
        r2.font.size = Pt(10.5)
        if key in ["birth_date", "birth_place", "education"]:
            r2.bold = True

    # 4. Mehnat Faoliyati
    work_exp = data.get("work", "").strip()
    if work_exp and work_exp.lower() not in ["yo'q", "йўқ", "нет", "none", "-"]:
        p_wt = doc.add_paragraph()
        p_wt.paragraph_format.space_before = Pt(14)
        p_wt.paragraph_format.space_after = Pt(6)
        p_wt.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_wt = p_wt.add_run(DOC[lang]["work_title"])
        r_wt.bold = True
        r_wt.font.size = Pt(12)
        
        work_lines = [l.strip() for l in work_exp.split("\n") if l.strip()]
        work_table = doc.add_table(rows=0, cols=2)
        work_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        work_table.autofit = False
        
        for w_line in work_lines:
            parts = w_line.split(" - ", 1)
            row = work_table.add_row()
            c_years = row.cells[0]
            c_desc = row.cells[1]
            
            c_years.width = Inches(1.8)
            c_desc.width = Inches(5.0)
            
            set_cell_margins(c_years, top=30, bottom=30, left=40, right=40)
            set_cell_margins(c_desc, top=30, bottom=30, left=40, right=40)
            set_cell_borders(c_years)
            set_cell_borders(c_desc)
            
            if len(parts) == 2:
                y_text, d_text = parts[0].strip(), parts[1].strip()
            else:
                y_text, d_text = "", w_line
                
            p_y = c_years.paragraphs[0]
            p_y.paragraph_format.space_before = Pt(2)
            p_y.paragraph_format.space_after = Pt(2)
            r_y = p_y.add_run(y_text)
            r_y.font.size = Pt(10.5)
            
            p_d = c_desc.paragraphs[0]
            p_d.paragraph_format.space_before = Pt(2)
            p_d.paragraph_format.space_after = Pt(2)
            r_d = p_d.add_run(d_text)
            r_d.font.size = Pt(10.5)

    # 5. Qarindoshlar (2-sahifa)
    relatives = data.get("relatives", [])
    valid_relatives = [
        r for r in relatives 
        if r.get("fio") or r.get("job") or r.get("birth") or r.get("address")
    ]
    
    if valid_relatives:
        doc.add_page_break()
        
        p_rt = doc.add_paragraph()
        p_rt.paragraph_format.space_before = Pt(6)
        p_rt.paragraph_format.space_after = Pt(10)
        p_rt.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        title_rel = DOC[lang]["rel_title"].format(fio=data.get("fio", ""))
        r_rt = p_rt.add_run(title_rel)
        r_rt.bold = True
        r_rt.font.size = Pt(12)
        
        headers = DOC[lang]["rel_headers"]
        rtable = doc.add_table(rows=1, cols=5)
        rtable.alignment = WD_TABLE_ALIGNMENT.CENTER
        rtable.autofit = False
        set_table_borders(rtable)
        
        col_widths = [Inches(1.1), Inches(1.8), Inches(1.3), Inches(1.4), Inches(1.2)]
        
        # Sarlavha qatori
        hdr_cells = rtable.rows[0].cells
        for i, h_text in enumerate(headers):
            hdr_cells[i].width = col_widths[i]
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            r = p.add_run(h_text)
            r.bold = True
            r.font.size = Pt(9.5)
            set_cell_shading(hdr_cells[i], "EAEAEA")
            set_cell_margins(hdr_cells[i], top=50, bottom=50, left=50, right=50)
            
        # Ma'lumot qatorlari
        for rel in valid_relatives:
            row_cells = rtable.add_row().cells
            row_vals = [
                rel.get("kind", ""),
                rel.get("fio", ""),
                rel.get("birth", ""),
                rel.get("job", ""),
                rel.get("address", "")
            ]
            for i, val in enumerate(row_vals):
                row_cells[i].width = col_widths[i]
                p = row_cells[i].paragraphs[0]
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
                r = p.add_run(val)
                r.font.size = Pt(9.5)
                set_cell_margins(row_cells[i], top=50, bottom=50, left=50, right=50)

    doc.save(output_path)
    return output_path
