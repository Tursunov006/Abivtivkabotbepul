import os
import sys
import base64
import uuid
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from aiogram import Bot
from aiogram.types import FSInputFile
from dotenv import load_dotenv

from generator_docx import generate_docx
from generator_pdf import generate_pdf

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

app = FastAPI(title="Obyektivka Web App API")

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
TEMP_DIR = BASE_DIR / "temp_files"
TEMP_DIR.mkdir(exist_ok=True)

class RelativeItem(BaseModel):
    kind: str = ""
    fio: str = ""
    birth: str = ""
    job: str = ""
    address: str = ""

class GenerateRequest(BaseModel):
    lang: str = "lat"
    format: str = "docx" # "docx" yoki "pdf"
    fio: str
    position: Optional[str] = ""
    birth_date: Optional[str] = ""
    birth_place: Optional[str] = ""
    nationality: Optional[str] = ""
    party: Optional[str] = ""
    education: Optional[str] = ""
    graduated: Optional[str] = ""
    specialty: Optional[str] = ""
    degree: Optional[str] = ""
    title: Optional[str] = ""
    languages: Optional[str] = ""
    military: Optional[str] = ""
    awards: Optional[str] = ""
    deputy: Optional[str] = ""
    work: Optional[str] = ""
    photo_base64: Optional[str] = None
    relatives: List[RelativeItem] = []
    user_id: Optional[int] = None
    init_data: Optional[str] = ""

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = STATIC_DIR / "index.html"
    return HTMLResponse(content=index_file.read_text(encoding="utf-8"))

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Abivtivkabot 24/7"}

@app.post("/api/generate")
async def generate_document(req: GenerateRequest):
    req_id = str(uuid.uuid4())[:8]
    
    # 3x4 Rasmni saqlash (agar bo'lsa)
    photo_path = None
    if req.photo_base64 and "," in req.photo_base64:
        try:
            header, encoded = req.photo_base64.split(",", 1)
            img_data = base64.b64decode(encoded)
            photo_path = str(TEMP_DIR / f"photo_{req_id}.jpg")
            with open(photo_path, "wb") as f:
                f.write(img_data)
        except Exception as e:
            print(f"Photo save error: {e}")
            photo_path = None

    data = {
        "lang": req.lang,
        "fio": req.fio,
        "position": req.position or "",
        "birth_date": req.birth_date or "",
        "birth_place": req.birth_place or "",
        "nationality": req.nationality or "",
        "party": req.party or "",
        "education": req.education or "",
        "graduated": req.graduated or "",
        "specialty": req.specialty or "",
        "degree": req.degree or "",
        "title": req.title or "",
        "languages": req.languages or "",
        "military": req.military or "",
        "awards": req.awards or "",
        "deputy": req.deputy or "",
        "work": req.work or "",
        "photo_path": photo_path,
        "relatives": [r.dict() for r in req.relatives]
    }

    try:
        if req.format == "pdf":
            out_file = TEMP_DIR / f"obyektivka_{req_id}.pdf"
            generate_pdf(data, str(out_file))
            media_type = "application/pdf"
            filename = f"Obyektivka_{req.fio}.pdf"
        else:
            out_file = TEMP_DIR / f"obyektivka_{req_id}.docx"
            generate_docx(data, str(out_file))
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            filename = f"Obyektivka_{req.fio}.docx"

        # Agar foydalanuvchi Telegram ID si bo'lsa, to'g'ridan-to'g'ri uning lichkasiga ham yuboramiz!
        if req.user_id and BOT_TOKEN:
            try:
                bot = Bot(token=BOT_TOKEN)
                caption = "✅ Obyektivkangiz tayyor!" if req.lang == "lat" else ("✅ Объективкангиз тайёр!" if req.lang == "cyr" else "✅ Ваша объективка готова!")
                await bot.send_document(
                    chat_id=req.user_id,
                    document=FSInputFile(str(out_file), filename=filename),
                    caption=caption
                )
                await bot.session.close()
            except Exception as tg_err:
                print(f"Telegram send doc error: {tg_err}")

        return FileResponse(
            path=str(out_file),
            filename=filename,
            media_type=media_type
        )
    except Exception as e:
        print(f"Error generating document: {e}")
        raise HTTPException(status_code=500, detail=str(e))
