import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from texts import DOC
from translit import normalize_data_script

FONT_REGULAR = "Times-Roman"
FONT_BOLD = "Times-Bold"

try:
    base_dir = os.path.dirname(__file__)
    local_times = os.path.join(base_dir, "fonts", "times.ttf")
    local_times_bd = os.path.join(base_dir, "fonts", "timesbd.ttf")

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


def _build_photo_box(photo_path):
    if photo_path and os.path.exists(photo_path):
        try:
            img = RLImage(photo_path, width=32 * mm, height=42 * mm)
            photo_box = Table([[img]], colWidths=[33 * mm], rowHeights=[43 * mm])
            photo_box.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#4A6984')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ]))
            return photo_box
        except Exception:
            pass
    photo_box = Table([["3x4"]], colWidths=[33 * mm], rowHeights=[43 * mm])
    photo_box.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#4A6984')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#888888')),
        ('FONTNAME', (0, 0), (-1, -1), FONT_REGULAR),
    ]))
    return photo_box


def generate_pdf(raw_data: dict, output_path: str):
    data = normalize_data_script(raw_data)
    lang = data.get("lang", "lat")
    if lang not in DOC:
        lang = "lat"
    template_type = data.get("template_type", "student")
    labels = DOC[lang]["labels"]
    none_text = DOC[lang]["none"]

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=15 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm
    )

    title_style = ParagraphStyle('DocTitle', fontName=FONT_BOLD, fontSize=12.5, leading=16, alignment=1, spaceAfter=8)
    fio_style = ParagraphStyle('DocFio', fontName=FONT_BOLD, fontSize=12.5, leading=16, alignment=1, spaceAfter=10)
    pos_style = ParagraphStyle('DocPos', fontName=FONT_REGULAR, fontSize=10.5, leading=13.5, alignment=0, spaceAfter=8)
    lbl_bold_style = ParagraphStyle('DocLblBold', fontName=FONT_BOLD, fontSize=10.2, leading=13, alignment=0)
    val_style = ParagraphStyle('DocVal', fontName=FONT_REGULAR, fontSize=10.2, leading=13, alignment=0)
    sec_title_style = ParagraphStyle('SecTitle', fontName=FONT_BOLD, fontSize=11, leading=14, alignment=1, spaceBefore=10, spaceAfter=8)
    rel_kind_style = ParagraphStyle('RelKind', fontName=FONT_BOLD, fontSize=9.5, leading=12, alignment=0)
    rel_header_style = ParagraphStyle('RelHeader', fontName=FONT_BOLD, fontSize=9.5, leading=12, alignment=1)
    rel_cell_center = ParagraphStyle('RelCellCenter', fontName=FONT_REGULAR, fontSize=9.5, leading=12, alignment=1)
    rel_cell_left = ParagraphStyle('RelCellLeft', fontName=FONT_REGULAR, fontSize=9.5, leading=12, alignment=0)
    ach_item_style = ParagraphStyle('AchItem', fontName=FONT_REGULAR, fontSize=10, leading=13, alignment=0)

    story = []
    fio_text = data.get("fio", "").strip()
    pos_text = data.get("position", "").strip().replace("\n", "<br/>")
    photo_box = _build_photo_box(data.get("photo_path"))

    b_date = data.get("birth_date", "").strip() or none_text
    b_place = data.get("birth_place", "").strip() or none_text
    nat_val = data.get("nationality", "").strip() or none_text
    spec_val = data.get("specialty", "").strip() or none_text
    grad_val = data.get("graduated", "").strip() or none_text
    phone_val = data.get("contact", "").strip() or none_text
    lang_val = data.get("languages", "").strip() or none_text
    awards_val = data.get("awards", "").strip() or none_text

    if template_type == "classic":
        # ==================== KLASSIK (BARCHA XODIMLAR / DAVLAT XIZMATI) SHABLONI ====================
        party_val = data.get("party", "").strip() or none_text
        edu_val = data.get("education", "").strip() or none_text
        deg_val = data.get("degree", "").strip() or none_text
        title_val = data.get("title", "").strip() or none_text
        mil_val = data.get("military", "").strip() or none_text
        dep_val = data.get("deputy", "").strip() or none_text

        left_header = [
            Paragraph(DOC[lang]["title"], title_style),
            Paragraph(fio_text, fio_style),
        ]
        if pos_text:
            left_header.append(Paragraph(pos_text, pos_style))

        top_table = Table([[left_header, photo_box]], colWidths=[138 * mm, 37 * mm])
        top_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(top_table)

        # 2 ustunli davlat standarti setkasi
        def pair_cell(lbl, val):
            return [Paragraph(f"<b>{lbl}</b>", val_style), Paragraph(val, val_style)]

        grid_rows = [
            [pair_cell(labels["birth_date"], b_date), pair_cell(labels["birth_place"], b_place)],
            [pair_cell(labels["nationality"], nat_val), pair_cell(labels["party"], party_val)],
            [pair_cell(labels["education"], edu_val), pair_cell(labels["graduated"], grad_val)],
            [pair_cell(labels["classic_specialty"], spec_val), pair_cell(labels["degree"], deg_val)],
            [pair_cell(labels["title"], title_val), pair_cell(labels["languages"], lang_val)],
            [pair_cell(labels["military"], mil_val), pair_cell(labels["awards"], awards_val)],
        ]
        grid_tbl = Table(grid_rows, colWidths=[85 * mm, 90 * mm])
        grid_tbl.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(grid_tbl)

        # Deputatligi + Telefon (agar kiritilgan bo'lsa)
        dep_p = Paragraph(f"<b>{labels['deputy']}</b><br/>{dep_val}", val_style)
        story.append(Spacer(1, 3))
        story.append(dep_p)
        if phone_val and phone_val != none_text:
            story.append(Spacer(1, 3))
            story.append(Paragraph(f"<b>{labels['contact']}:</b> {phone_val}", val_style))

        # MEHNAT FAOLIYATI
        work_raw = (data.get("work", "") or "").strip()
        if work_raw:
            story.append(Paragraph(DOC[lang]["work_title"], sec_title_style))
            for wline in [l.strip() for l in work_raw.split("\n") if l.strip()]:
                story.append(Paragraph(wline, ach_item_style))
                story.append(Spacer(1, 3))

        # Yutuqlar ham kiritilgan bo'lsa
        ach_raw = (data.get("achievements", "") or "").strip()
        if ach_raw and ach_raw != work_raw and ach_raw.lower() not in ["yo'q", "yo‘q", "йўқ", "нет", "-"]:
            story.append(Paragraph(DOC[lang]["ach_title"], sec_title_style))
            for idx, line in enumerate([l.strip() for l in ach_raw.split("\n") if l.strip()], 1):
                clean = line.lstrip("0123456789.) ").strip() or line
                story.append(Paragraph(f"{idx}. {clean}", ach_item_style))
                story.append(Spacer(1, 2.5))

        # YAQIN QARINDOSHLARI HAQIDA MA'LUMOT (Sarlavhali 5 ustunli rasmiy jadval)
        relatives = [r for r in data.get("relatives", []) if r.get("fio") or r.get("job") or r.get("birth") or r.get("address")]
        if relatives:
            rel_title_text = DOC[lang]["classic_rel_title"].format(fio=fio_text).replace("\n", "<br/>")
            story.append(Paragraph(rel_title_text, sec_title_style))
            headers = DOC[lang]["classic_rel_headers"]
            r_cols = [24 * mm, 41 * mm, 32 * mm, 44 * mm, 34 * mm]
            r_data = [[Paragraph(h, rel_header_style) for h in headers]]
            for rel in relatives:
                r_data.append([
                    Paragraph((rel.get("kind", "") or "").strip(), rel_kind_style),
                    Paragraph((rel.get("fio", "") or "").strip(), rel_cell_left),
                    Paragraph((rel.get("birth", "") or "").strip(), rel_cell_center),
                    Paragraph((rel.get("job", "") or "").strip(), rel_cell_center),
                    Paragraph((rel.get("address", "") or "").strip(), rel_cell_center),
                ])
            rel_table = Table(r_data, colWidths=r_cols, repeatRows=1)
            rel_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.6, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F8FAFC')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 3.5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 3.5),
            ]))
            story.append(rel_table)

        doc.build(story)
        return output_path

    # ==================== TALABA NAMUNASI (O'RINOV RUSTAMJON SHAKLI) ====================
    left_header = [
        Paragraph(DOC[lang]["title"], title_style),
        Paragraph(fio_text, fio_style),
    ]
    if pos_text:
        left_header.append(Paragraph(pos_text, pos_style))

    sub_info_rows = [
        [Paragraph(labels["birth_date"], lbl_bold_style), Paragraph(b_date, val_style)],
        [Paragraph(labels["birth_place"], lbl_bold_style), Paragraph(b_place, val_style)],
    ]
    sub_info_tbl = Table(sub_info_rows, colWidths=[68 * mm, 70 * mm])
    sub_info_tbl.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    left_header.append(sub_info_tbl)

    top_table = Table([[left_header, photo_box]], colWidths=[138 * mm, 37 * mm])
    top_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(top_table)

    rest_rows = [
        [Paragraph(labels["nationality"], lbl_bold_style), Paragraph(nat_val, val_style)],
        [Paragraph(labels["specialty"], lbl_bold_style), Paragraph(spec_val, val_style)],
        [Paragraph(labels["graduated"], lbl_bold_style), Paragraph(grad_val, val_style)],
        [Paragraph(labels["contact"], lbl_bold_style), Paragraph(phone_val, val_style)],
        [Paragraph(labels["languages"], lbl_bold_style), Paragraph(lang_val, val_style)],
    ]
    rest_table = Table(rest_rows, colWidths=[68 * mm, 107 * mm])
    rest_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 2), (-1, 2), 7),
    ]))
    story.append(rest_table)

    awards_p = Paragraph(
        f"<b>{labels['awards']}</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{awards_val}",
        val_style
    )
    awards_tbl = Table([[awards_p]], colWidths=[175 * mm])
    awards_tbl.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(awards_tbl)

    # SHAXSIY MA'LUMOTLARI (Sarlavha qatorisiz 5 ustunli oila a'zolari jadvali)
    valid_relatives = [
        r for r in data.get("relatives", [])
        if r.get("fio") or r.get("job") or r.get("birth") or r.get("address")
    ]

    if valid_relatives:
        story.append(Paragraph(DOC[lang]["rel_title"], sec_title_style))
        r_cols = [22 * mm, 41 * mm, 26 * mm, 50 * mm, 36 * mm]
        r_data = []
        for rel in valid_relatives:
            r_data.append([
                Paragraph((rel.get("kind", "") or "").strip().upper(), rel_kind_style),
                Paragraph((rel.get("fio", "") or "").strip(), rel_cell_center),
                Paragraph((rel.get("birth", "") or "").strip(), rel_cell_center),
                Paragraph((rel.get("address", "") or "").strip(), rel_cell_center),
                Paragraph((rel.get("job", "") or "").strip(), rel_cell_center),
            ])
        rel_table = Table(r_data, colWidths=r_cols)
        rel_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.6, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 2.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 3.5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3.5),
        ]))
        story.append(rel_table)

    # ERISHGAN YUTUQLARI
    ach_raw = (data.get("achievements", "") or data.get("work", "")).strip()
    if ach_raw and ach_raw.lower() not in ["yo'q", "yo‘q", "йўқ", "нет", "-"]:
        story.append(Spacer(1, 4))
        story.append(Paragraph(DOC[lang]["ach_title"], sec_title_style))
        ach_lines = [l.strip() for l in ach_raw.split("\n") if l.strip()]
        ach_rows = []
        for idx, line in enumerate(ach_lines, start=1):
            clean_line = line
            if len(clean_line) > 2 and clean_line[0].isdigit() and clean_line[1] in ['.', ')']:
                clean_line = clean_line[2:].strip()
            elif len(clean_line) > 3 and clean_line[:2].isdigit() and clean_line[2] in ['.', ')']:
                clean_line = clean_line[3:].strip()
            ach_rows.append([
                Paragraph(f"{idx}.", ach_item_style),
                Paragraph(clean_line, ach_item_style)
            ])
        ach_table = Table(ach_rows, colWidths=[7 * mm, 160 * mm])
        ach_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(ach_table)

    doc.build(story)
    return output_path
