import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from texts import DOC

FONT_REGULAR = "Times-Roman"
FONT_BOLD = "Times-Bold"

try:
    local_times = os.path.join(os.path.dirname(__file__), "fonts", "times.ttf")
    local_times_bd = os.path.join(os.path.dirname(__file__), "fonts", "timesbd.ttf")
    win_times = "C:\\Windows\\Fonts\\times.ttf"
    win_times_bd = "C:\\Windows\\Fonts\\timesbd.ttf"
    
    t_path = local_times if os.path.exists(local_times) else (win_times if os.path.exists(win_times) else None)
    t_bd_path = local_times_bd if os.path.exists(local_times_bd) else (win_times_bd if os.path.exists(win_times_bd) else None)

    if t_path and t_bd_path:
        pdfmetrics.registerFont(TTFont("CustomTimes", t_path))
        pdfmetrics.registerFont(TTFont("CustomTimesBd", t_bd_path))
        FONT_REGULAR = "CustomTimes"
        FONT_BOLD = "CustomTimesBd"
except Exception as e:
    print(f"Font loading error: {e}")

def generate_pdf(data: dict, output_path: str):
    lang = data.get("lang", "lat")
    if lang not in DOC:
        lang = "lat"
    labels = DOC[lang]["labels"]
    none_text = DOC[lang]["none"]
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm
    )
    
    content_width = 496 # 595 - 35mm
    
    styles = getSampleStyleSheet()
    
    # Katta markaziy sarlavha: MA'LUMOTNOMA
    title_style = ParagraphStyle(
        'DocTitle',
        fontName=FONT_BOLD,
        fontSize=14,
        leading=17,
        alignment=1, # Center
        spaceAfter=12
    )
    
    # F.I.Sh. (chap tomonda)
    fio_style = ParagraphStyle(
        'DocFio',
        fontName=FONT_BOLD,
        fontSize=12.5,
        leading=16,
        spaceAfter=4
    )
    
    # Lavozim
    pos_style = ParagraphStyle(
        'DocPos',
        fontName=FONT_REGULAR,
        fontSize=10,
        leading=13,
        spaceAfter=3
    )
    
    lbl_style = ParagraphStyle(
        'DocLbl',
        fontName=FONT_REGULAR,
        fontSize=9.5,
        leading=12
    )
    
    val_style = ParagraphStyle(
        'DocVal',
        fontName=FONT_REGULAR,
        fontSize=9.5,
        leading=12
    )
    
    val_bold_style = ParagraphStyle(
        'DocValBold',
        fontName=FONT_BOLD,
        fontSize=9.5,
        leading=12
    )
    
    section_title = ParagraphStyle(
        'SecTitle',
        fontName=FONT_BOLD,
        fontSize=11.5,
        leading=14,
        alignment=1,
        spaceBefore=12,
        spaceAfter=6
    )
    
    rel_header_style = ParagraphStyle(
        'RelHdr',
        fontName=FONT_BOLD,
        fontSize=8.5,
        leading=11,
        alignment=1
    )
    
    rel_cell_style = ParagraphStyle(
        'RelCell',
        fontName=FONT_REGULAR,
        fontSize=8.5,
        leading=11
    )

    story = []
    
    # 1. Asosiy Markaziy Sarlavha: MA'LUMOTNOMA
    story.append(Paragraph(DOC[lang]["title"], title_style))
    
    # 2. Yuqori qism: Chapda F.I.Sh + Lavozim, O'ngda 3x4 rasm
    fio_text = data.get("fio", "").strip()
    pos_text = data.get("position", "").strip()
    
    info_flowables = [Paragraph(fio_text, fio_style)]
    # Agar lavozim bo'sh yoki "yo'q" bo'lmasa ko'rsatiladi
    if pos_text and pos_text.lower() not in ["yo'q", "йўқ", "нет", "none", "-"]:
        info_flowables.append(Paragraph(pos_text, pos_style))
        
    photo_path = data.get("photo_path")
    if photo_path and os.path.exists(photo_path):
        try:
            img = RLImage(photo_path, width=32 * mm, height=42 * mm)
            photo_flowable = img
        except Exception:
            photo_flowable = Paragraph("3x4", lbl_style)
    else:
        empty_box = Table([["3x4"]], colWidths=[32 * mm], rowHeights=[42 * mm])
        empty_box.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#999999')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#999999')),
            ('FONTNAME', (0,0), (-1,-1), FONT_REGULAR),
            ('FONTSIZE', (0,0), (-1,-1), 10),
        ]))
        photo_flowable = empty_box
        
    top_table = Table([[info_flowables, photo_flowable]], colWidths=[content_width - 100, 100])
    top_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(top_table)
    story.append(Spacer(1, 6))
    
    # 3. Savol-Javob jadvali
    fields = [
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
    
    t_data = []
    for key, lbl in fields:
        raw_val = data.get(key, "").strip()
        val = raw_val if raw_val else none_text
        use_style = val_bold_style if key in ["birth_date", "birth_place", "education"] else val_style
        t_data.append([
            Paragraph(lbl, lbl_style),
            Paragraph(val, use_style)
        ])
        
    main_table = Table(t_data, colWidths=[180, content_width - 180])
    main_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 1.8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.8),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(main_table)
    
    # 4. Mehnat faoliyati
    work_exp = data.get("work", "").strip()
    if work_exp and work_exp.lower() not in ["yo'q", "йўқ", "нет", "none", "-"]:
        story.append(Paragraph(DOC[lang]["work_title"], section_title))
        work_lines = [l.strip() for l in work_exp.split("\n") if l.strip()]
        w_data = []
        for line in work_lines:
            parts = line.split(" - ", 1)
            if len(parts) == 2:
                y_text, d_text = parts[0].strip(), parts[1].strip()
            else:
                y_text, d_text = "", line
            w_data.append([
                Paragraph(y_text, lbl_style),
                Paragraph(d_text, val_style)
            ])
            
        w_table = Table(w_data, colWidths=[120, content_width - 120])
        w_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(w_table)
        
    # 5. Qarindoshlar (2-sahifa)
    relatives = data.get("relatives", [])
    valid_relatives = [
        r for r in relatives 
        if r.get("fio") or r.get("job") or r.get("birth") or r.get("address")
    ]
    
    if valid_relatives:
        story.append(PageBreak())
        title_rel = DOC[lang]["rel_title"].format(fio=fio_text).replace("\n", "<br/>")
        story.append(Paragraph(title_rel, title_style))
        
        headers = DOC[lang]["rel_headers"]
        r_cols = [75, 125, 95, 110, 91] # total 496
        
        r_data = [[Paragraph(h, rel_header_style) for h in headers]]
        for rel in valid_relatives:
            r_data.append([
                Paragraph(rel.get("kind", ""), rel_cell_style),
                Paragraph(rel.get("fio", ""), rel_cell_style),
                Paragraph(rel.get("birth", ""), rel_cell_style),
                Paragraph(rel.get("job", ""), rel_cell_style),
                Paragraph(rel.get("address", ""), rel_cell_style),
            ])
            
        rel_table = Table(r_data, colWidths=r_cols)
        rel_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F2F2F2')),
            ('TOPPADDING', (0, 0), (-1, -1), 3.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(rel_table)
        
    doc.build(story)
    return output_path
