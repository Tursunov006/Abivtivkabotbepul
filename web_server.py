import os
import sys
import time
import json
import base64
import uuid
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from aiogram import Bot
from aiogram.types import FSInputFile
from dotenv import load_dotenv

from generator_docx import generate_docx
from generator_pdf import generate_pdf
from ai_enhancer import enhance_text_with_ai

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

app = FastAPI(title="Obyektivka PRO Web App API")

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
TEMP_DIR = BASE_DIR / "temp_files"
TEMP_DIR.mkdir(exist_ok=True)
STATS_FILE = TEMP_DIR / "stats.json"


def cleanup_old_temp_files(max_age_seconds: int = 1800):
    """30 daqiqadan eski vaqtinchalik fayllarni tozalaydi (stats.json qoladi)."""
    try:
        now = time.time()
        for f in TEMP_DIR.glob("*"):
            if f.is_file() and f.name != "stats.json":
                if now - f.stat().st_mtime > max_age_seconds:
                    try:
                        f.unlink()
                    except Exception:
                        pass
    except Exception:
        pass


def increment_stat(fmt: str, template_type: str):
    try:
        stats = {"total": 0, "pdf": 0, "docx": 0, "student": 0, "classic": 0}
        if STATS_FILE.exists():
            stats.update(json.loads(STATS_FILE.read_text(encoding="utf-8")))
        stats["total"] = stats.get("total", 0) + 1
        stats[fmt] = stats.get(fmt, 0) + 1
        stats[template_type] = stats.get(template_type, 0) + 1
        STATS_FILE.write_text(json.dumps(stats), encoding="utf-8")
    except Exception:
        pass


class RelativeItem(BaseModel):
    kind: str = ""
    fio: str = ""
    birth: str = ""
    job: str = ""
    address: str = ""


class EnhanceRequest(BaseModel):
    text: str
    category: Optional[str] = "achievements"  # "achievements" yoki "work"
    lang: Optional[str] = "lat"


class GenerateRequest(BaseModel):
    lang: str = "lat"
    format: str = "pdf"  # "pdf" asosiy rasmiy format
    template_type: Optional[str] = "student"  # "student" yoki "classic"
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
    marital_status: Optional[str] = ""
    contact: Optional[str] = ""
    address: Optional[str] = ""
    work: Optional[str] = ""
    achievements: Optional[str] = ""
    photo_base64: Optional[str] = None
    relatives: List[RelativeItem] = []
    user_id: Optional[int] = None
    init_data: Optional[str] = ""


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = STATIC_DIR / "index.html"
    return HTMLResponse(
        content=index_file.read_text(encoding="utf-8"),
        headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
    )


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Obyektivka PRO Universal 24/7"}


@app.get("/api/stats")
async def get_stats():
    if STATS_FILE.exists():
        try:
            return json.loads(STATS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"total": 0, "pdf": 0, "docx": 0, "student": 0, "classic": 0}


@app.post("/api/ai_enhance")
async def api_ai_enhance(req: EnhanceRequest):
    """OmniRoute sun'iy intellekti orqali matnni rasmiy tahrirlab berish."""
    enhanced = enhance_text_with_ai(
        text=req.text,
        category=req.category or "achievements",
        lang=req.lang or "lat"
    )
    return {"original": req.text, "enhanced": enhanced}


@app.post("/api/generate")
async def generate_document(req: GenerateRequest, background_tasks: BackgroundTasks):
    # Fon vazifasida eski fayllarni tozalash
    background_tasks.add_task(cleanup_old_temp_files)
    req_id = str(uuid.uuid4())[:8]

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

    tpl = req.template_type if req.template_type in ("student", "classic") else "student"

    data = {
        "lang": req.lang,
        "template_type": tpl,
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
        "marital_status": req.marital_status or "",
        "contact": req.contact or "",
        "address": req.address or "",
        "work": req.work or "",
        "achievements": req.achievements or "",
        "photo_path": photo_path,
        "relatives": [r.model_dump() if hasattr(r, "model_dump") else r.dict() for r in req.relatives]
    }

    try:
        if req.format == "pdf":
            out_file = TEMP_DIR / f"obyektivka_{req_id}.pdf"
            generate_pdf(data, str(out_file))
            media_type = "application/pdf"
            filename = f"Obyektivka_{req.fio}.pdf"
            increment_stat("pdf", tpl)
        else:
            out_file = TEMP_DIR / f"obyektivka_{req_id}.docx"
            generate_docx(data, str(out_file))
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            filename = f"Obyektivka_{req.fio}.docx"
            increment_stat("docx", tpl)

        if req.user_id and BOT_TOKEN:
            try:
                bot = Bot(token=BOT_TOKEN)
                caption = (
                    "✅ Rasmiy Obyektivkangiz tayyor! (PDF)"
                    if req.lang == "lat" else (
                        "✅ Расмий Объективкангиз тайёр! (PDF)"
                        if req.lang == "cyr" else "✅ Ваша официальная справка-объективка готова! (PDF)"
                    )
                )
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
