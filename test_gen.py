import os
from generator_docx import generate_docx
from generator_pdf import generate_pdf

test_data = {
    "lang": "lat",
    "fio": "Aliyev Vali Karimovich",
    "position": "2021-yil 1-sentabrdan: O'zbekiston Respublikasi Raqamli texnologiyalar vazirligi bosh mutaxassisi",
    "birth_date": "15.03.1995",
    "birth_place": "Toshkent shahri, Yunusobod tumani",
    "nationality": "o'zbek",
    "party": "yo'q",
    "education": "Oliy",
    "graduated": "2017-yil, Toshkent axborot texnologiyalari universiteti (kunduzgi)",
    "specialty": "Dasturiy injiniring",
    "degree": "yo'q",
    "title": "yo'q",
    "languages": "rus, ingliz",
    "military": "oddiy askar",
    "awards": "yo'q",
    "deputy": "yo'q",
    "work": "2013-2017 yy. - Toshkent axborot texnologiyalari universiteti talabasi\n2017-2021 yy. - «Aloqabank» ATB axborot texnologiyalari markazi yetakchi mutaxassisi\n2021 y. - h.v. - O'zbekiston Respublikasi Raqamli texnologiyalar vazirligi bosh mutaxassisi",
    "relatives": [
        {
            "kind": "Otasi",
            "fio": "Aliyev Karim Valiyevich",
            "birth": "1968-yil, Toshkent shahri",
            "job": "«O'zbektelekom» AK muhandisi",
            "address": "Toshkent shahri, Yunusobod tumani, 4-mavze, 12-uy"
        },
        {
            "kind": "Onasi",
            "fio": "Aliyeva Nozima Rustamovna",
            "birth": "1972-yil, Toshkent viloyati",
            "job": "72-maktab matematika fani o'qituvchisi",
            "address": "Toshkent shahri, Yunusobod tumani, 4-mavze, 12-uy"
        }
    ]
}

docx_out = "test_obyektivka.docx"
pdf_out = "test_obyektivka.pdf"

generate_docx(test_data, docx_out)
print(f"DOCX created: {os.path.exists(docx_out)}, size: {os.path.getsize(docx_out)} bytes")

generate_pdf(test_data, pdf_out)
print(f"PDF created: {os.path.exists(pdf_out)}, size: {os.path.getsize(pdf_out)} bytes")
