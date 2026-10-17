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


def generate_pdf(data: dict, output_path: str):
    lang = data.get("lang", "lat")
    if lang not in DOC:
        lang = "lat"
    labels = DOC[lang]["labels"]
    none_text = DOC[lang]["none"]

    # A4: 210mm x 297mm
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=15 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm
    )

    content_width = 175 * mm  # 210 - 35 = 175mm

    # Stillar (O'rinov Rustamjon namunasi asosida)
    title_style = ParagraphStyle(
        'DocTitle',
        fontName=FONT_BOLD,
        fontSize=12.5,
        leading=16,
        alignment=1,  # Center
        spaceAfter=8
    )

    fio_style = ParagraphStyle(
        'DocFio',
        fontName=FONT_BOLD,
        fontSize=12.5,
        leading=16,
        alignment=1,  # Center
        spaceAfter=10
    )

    pos_style = ParagraphStyle(
        'DocPos',
        fontName=FONT_REGULAR,
        fontSize=10.5,
        leading=13.5,
        alignment=0,  # Left
        spaceAfter=8
    )

    lbl_bold_style = ParagraphStyle(
        'DocLblBold',
        fontName=FONT_BOLD,
        fontSize=10.2,
        leading=13,
        alignment=0
    )

    val_style = ParagraphStyle(
        'DocVal',
        fontName=FONT_REGULAR,
        fontSize=10.2,
        leading=13,
        alignment=0
    )

    sec_title_style = ParagraphStyle(
        'SecTitle',
        fontName=FONT_BOLD,
        fontSize=11,
        leading=14,
        alignment=1,  # Center
        spaceBefore=10,
        spaceAfter=8
    )

    rel_kind_style = ParagraphStyle(
        'RelKind',
        fontName=FONT_BOLD,
        fontSize=9.8,
        leading=12.5,
        alignment=0  # Left bold uppercase
    )

    rel_cell_center = ParagraphStyle(
        'RelCellCenter',
        fontName=FONT_REGULAR,
        fontSize=9.8,
        leading=12.5,
        alignment=1  # Center
    )

    ach_item_style = ParagraphStyle(
        'AchItem',
        fontName=FONT_REGULAR,
        fontSize=10,
        leading=13,
        alignment=0
    )

    story = []

    # 1. Yuqori blok: Chapda (MA'LUMOTNOMA, F.I.Sh., Universitet/fakultet/kurs), O'ngda 3x4 rasm
    fio_text = data.get("fio", "").strip()
    pos_text = data.get("position", "").strip().replace("\n", "<br/>")

    left_header = [
        Paragraph(DOC[lang]["title"], title_style),
        Paragraph(fio_text, fio_style),
    ]
    if pos_text:
        left_header.append(Paragraph(pos_text, pos_style))

    # 2x2 qatorlar (Tug'ilgan yili va Tug'ilgan joyi rasmning chap tomonidan boshlanadi)
    b_date = data.get("birth_date", "").strip() or none_text
    b_place = data.get("birth_place", "").strip() or none_text
    nat_val = data.get("nationality", "").strip() or none_text
    spec_val = data.get("specialty", "").strip() or none_text
    grad_val = data.get("graduated", "").strip() or none_text
    phone_val = data.get("contact", "").strip() or none_text
    lang_val = data.get("languages", "").strip() or none_text
    awards_val = data.get("awards", "").strip() or none_text

    # Chap ustun ichidagi dastlabki 2 qator (rasm bilan yonma-yon chiqishi uchun)
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

    # 3x4 Rasm ramkasi (ko'k-kulrang chiziqli ramka)
    photo_path = data.get("photo_path")
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
        except Exception:
            photo_box = Table([["3x4"]], colWidths=[33 * mm], rowHeights=[43 * mm])
    else:
        photo_box = Table([["3x4"]], colWidths=[33 * mm], rowHeights=[43 * mm])
        photo_box.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#4A6984')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#888888')),
            ('FONTNAME', (0, 0), (-1, -1), FONT_REGULAR),
        ]))

    top_table = Table(
        [[left_header, photo_box]],
        colWidths=[138 * mm, 37 * mm]
    )
    top_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(top_table)

    # Qolgan asosiy qatorlar: Millati, Ta'lim yo'nalishi, Tamomlagan, Telefon nomeri, Chet tillari
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
        # Tamomlagan va Telefon nomeri orasida biroz kengroq masofa (namunadagidek)
        ('BOTTOMPADDING', (0, 2), (-1, 2), 7),
    ]))
    story.append(rest_table)

    # Davlat mukofotlari bilan taqdirlanganmi (qanaqa):   yo'q
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

    # 2. SHAXSIY MA'LUMOTLARI (Sarlavha qatorisiz 5 ustunli oila a'zolari jadvali!)
    relatives = data.get("relatives", [])
    valid_relatives = [
        r for r in relatives
        if r.get("fio") or r.get("job") or r.get("birth") or r.get("address")
    ]

    if valid_relatives:
        story.append(Paragraph(DOC[lang]["rel_title"], sec_title_style))

        # 5 ustun kengliklari: 1) Qarindoshligi (22mm), 2) FIO (41mm), 3) Tug'ilgan sana (26mm), 4) Manzil (50mm), 5) Kasbi/ish joyi (36mm) = 175mm
        r_cols = [22 * mm, 41 * mm, 26 * mm, 50 * mm, 36 * mm]
        r_data = []

        for rel in valid_relatives:
            kind_str = (rel.get("kind", "") or "").strip().upper()
            fio_str = (rel.get("fio", "") or "").strip()
            birth_str = (rel.get("birth", "") or "").strip()
            addr_str = (rel.get("address", "") or "").strip()
            job_str = (rel.get("job", "") or "").strip()

            r_data.append([
                Paragraph(kind_str, rel_kind_style),
                Paragraph(fio_str, rel_cell_center),
                Paragraph(birth_str, rel_cell_center),
                Paragraph(addr_str, rel_cell_center),
                Paragraph(job_str, rel_cell_center),
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

    # 3. ERISHGAN YUTUQLARI (Raqamlangan ro'yxat: 1., 2., 3.)
    ach_raw = (data.get("achievements", "") or data.get("work", "")).strip()
    if ach_raw and ach_raw.lower() not in ["yo'q", "yo‘q", "йўқ", "нет", "-"]:
        story.append(Spacer(1, 4))
        story.append(Paragraph(DOC[lang]["ach_title"], sec_title_style))

        ach_lines = [l.strip() for l in ach_raw.split("\n") if l.strip()]
        ach_rows = []
        for idx, line in enumerate(ach_lines, start=1):
            # Agar foydalanuvchi o'zi "1. " deb yozgan bo'lsa tozalaymiz
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
