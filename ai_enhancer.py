import os
import json
import logging
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()

# OmniRoute yoki boshqa OpenAI-mos server sozlamalari
AI_BASE_URL = os.getenv("AI_BASE_URL", "http://localhost:20128/v1").rstrip("/")
AI_API_KEY = os.getenv("AI_API_KEY", "sk-254f317fc7fb7bd6-971712-75c500c7").strip()
AI_MODEL = os.getenv("AI_MODEL", "openrouter/minimax/minimax-m3.1-flash:free").strip()


def enhance_text_with_ai(text: str, category: str = "achievements", lang: str = "lat") -> str:
    """
    Foydalanuvchi yozgan yutuqlar yoki mehnat faoliyati matnini rasmiy idoraviy uslubda,
    imlo va uslubiy xatolarsiz chiroyli shaklga keltiradi.
    Agar AI xizmati ulanmagan bo'lsa yoki xatolik bersa, asl matn o'zgartirilmasdan qaytariladi.
    """
    if not text or len(text.strip()) < 5:
        return text

    lang_instructions = {
        "lat": "O'zbek adabiy tilida (lotin alifbosida)",
        "cyr": "Ўзбек адабий тилида (кирилл алифбосида)",
        "ru": "На официальном деловом русском языке"
    }.get(lang, "O'zbek tilida (lotin alifbosida)")

    target_type = "erishilgan yutuqlar (sertifikat, olimpiada, stipendiya, mukofotlar)" if category == "achievements" else "mehnat faoliyati (ish joylari, lavozimlar)"

    prompt = (
        f"Sen rasmiy davlat obyektivka (ma'lumotnoma) hujjati bo'yicha professional kotibsan. "
        f"Quyidagi foydalanuvchi tomonidan kiritilgan {target_type} matnini {lang_instructions} "
        f"rasmiy idoraviy uslubda, har bir bandni alohida yangi qatordan, aniq sanalari bilan chiroyli tartibga keltirib ber. "
        f"Hech qanday kirish so'zlari, tushuntirish yoki izoh yozma. Faqat va faqat rasmiy tahrirlangan tayyor matnni qaytar.\n\n"
        f"Asl matn:\n{text.strip()}"
    )

    req_data = json.dumps({
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": "Sen faqat rasmiy idoraviy hujjat uslubida yozuvchi yordamchisan. Hech qanday ortiqcha so'z yozmaysan."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{AI_BASE_URL}/chat/completions",
        data=req_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AI_API_KEY}"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            enhanced = data["choices"][0]["message"]["content"].strip()
            # Keltirilgan matndan ortiqcha tirnoqlarni tozalash
            if enhanced.startswith('"""') and enhanced.endswith('"""'):
                enhanced = enhanced[3:-3].strip()
            if enhanced.startswith('"') and enhanced.endswith('"'):
                enhanced = enhanced[1:-1].strip()
            return enhanced if enhanced else text
    except Exception as e:
        logging.warning(f"AI enhance failed, using original text: {e}")
        return text
