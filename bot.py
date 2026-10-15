import os
import sys
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
    InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile,
    WebAppInfo
)

from texts import T, LANGS, EDU, REL_KINDS, CHOOSE_LANG, LANG_BUTTONS
from generator_docx import generate_docx
from generator_pdf import generate_pdf

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://abivtivkabotbepul.onrender.com").strip()

BASE_DIR = Path(__file__).parent
DOWNLOADS_DIR = BASE_DIR / "temp_files"
DOWNLOADS_DIR.mkdir(exist_ok=True)

class ObyektivkaStates(StatesGroup):
    lang = State()
    fio = State()
    position = State()
    birth_date = State()
    birth_place = State()
    nationality = State()
    party = State()
    education = State()
    graduated = State()
    specialty = State()
    degree = State()
    title = State()
    languages = State()
    military = State()
    awards = State()
    deputy = State()
    photo = State()
    work = State()
    rel_kind = State()
    rel_fio = State()
    rel_birth = State()
    rel_job = State()
    rel_address = State()
    rel_ask_more = State()
    finished = State()

dp = Dispatcher(storage=MemoryStorage())

def get_main_menu_kb(lang: str = "lat"):
    buttons = []
    
    # 1. Mini Web App tugmasi
    if WEBAPP_URL:
        btn_webapp_text = {
            "lat": "📱 Mini Ilovada to'ldirish (Tez va qulay)",
            "cyr": "📱 Мини Иловада тўлдириш (Тез ва қулай)",
            "ru": "📱 Заполнить в Мини-Приложении"
        }.get(lang, "📱 Mini Ilovada to'ldirish")
        buttons.append([InlineKeyboardButton(text=btn_webapp_text, web_app=WebAppInfo(url=WEBAPP_URL))])

    # 2. Bot ichida qadamma-qadam to'ldirish
    btn_chat_text = {
        "lat": "💬 Bot ichida savol-javob orqali",
        "cyr": "💬 Бот ичида савол-жавоб орқали",
        "ru": "💬 Внутри бота пошагово"
    }.get(lang, "💬 Bot ichida savol-javob orqali")
    buttons.append([InlineKeyboardButton(text=btn_chat_text, callback_data="start_chat_flow")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_lang_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn_text, callback_data=f"setlang_{code}")]
        for code, btn_text in LANG_BUTTONS
    ])

def get_skip_kb(lang: str, extra_buttons: list = None):
    kb = []
    if extra_buttons:
        row = []
        for b in extra_buttons:
            row.append(KeyboardButton(text=b))
            if len(row) == 2:
                kb.append(row)
                row = []
        if row:
            kb.append(row)
            
    kb.append([KeyboardButton(text=T[lang]["btn_skip"])])
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)

def get_rel_more_kb(lang: str):
    return ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=T[lang]["btn_add_more"]),
            KeyboardButton(text=T[lang]["btn_done"])
        ]
    ], resize_keyboard=True, one_time_keyboard=True)

def get_format_kb(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=T[lang]["btn_pdf"], callback_data="get_pdf"),
            InlineKeyboardButton(text=T[lang]["btn_docx"], callback_data="get_docx"),
        ],
        [
            InlineKeyboardButton(text=T[lang]["btn_both"], callback_data="get_both"),
        ],
        [
            InlineKeyboardButton(text=T[lang]["btn_restart"], callback_data="restart"),
        ]
    ])

# ----------------- Buyruqlar -----------------
@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(ObyektivkaStates.lang)
    await message.answer(CHOOSE_LANG, reply_markup=get_lang_kb())

@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "lat")
    await state.clear()
    await message.answer(T[lang]["cancelled"], reply_markup=ReplyKeyboardRemove())

# Til tanlash
@dp.callback_query(F.data.startswith("setlang_"))
async def cb_set_lang(call: types.CallbackQuery, state: FSMContext):
    lang = call.data.split("_")[1]
    if lang not in LANGS:
        lang = "lat"
    await state.update_data(lang=lang, relatives=[])
    await call.message.delete()
    
    welcome_text = {
        "lat": "Obyektivkani qanday to'ldirishni xohlaysiz?",
        "cyr": "Объективкани қандай тўлдиришни хоҳлайсиз?",
        "ru": "Как вы хотите заполнить объективку?"
    }.get(lang, "Obyektivkani qanday to'ldirishni xohlaysiz?")

    await call.message.answer(f"{T[lang]['welcome']}\n\n<b>{welcome_text}</b>", reply_markup=get_main_menu_kb(lang))

# Bot ichida savol-javob orqali davom etish
@dp.callback_query(F.data == "start_chat_flow")
async def cb_start_chat(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "lat")
    await call.message.delete()
    await state.set_state(ObyektivkaStates.fio)
    await call.message.answer(T[lang]["fio"], reply_markup=ReplyKeyboardRemove())

# 1. FIO
@dp.message(ObyektivkaStates.fio)
async def process_fio(message: types.Message, state: FSMContext):
    if not message.text:
        return
    await state.update_data(fio=message.text.strip())
    data = await state.get_data()
    lang = data["lang"]
    await state.set_state(ObyektivkaStates.position)
    await message.answer(T[lang]["position"], reply_markup=get_skip_kb(lang))

# 2. Position
@dp.message(ObyektivkaStates.position)
async def process_position(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    val = "" if message.text == T[lang]["btn_skip"] else (message.text or "")
    await state.update_data(position=val.strip())
    
    await state.set_state(ObyektivkaStates.birth_date)
    await message.answer(T[lang]["birth_date"], reply_markup=ReplyKeyboardRemove())

# 3. Birth date
@dp.message(ObyektivkaStates.birth_date)
async def process_birth_date(message: types.Message, state: FSMContext):
    if not message.text:
        return
    data = await state.get_data()
    lang = data["lang"]
    await state.update_data(birth_date=message.text.strip())
    
    await state.set_state(ObyektivkaStates.birth_place)
    await message.answer(T[lang]["birth_place"], reply_markup=ReplyKeyboardRemove())

# 4. Birth place
@dp.message(ObyektivkaStates.birth_place)
async def process_birth_place(message: types.Message, state: FSMContext):
    if not message.text:
        return
    data = await state.get_data()
    lang = data["lang"]
    await state.update_data(birth_place=message.text.strip())
    
    await state.set_state(ObyektivkaStates.nationality)
    await message.answer(T[lang]["nationality"], reply_markup=ReplyKeyboardRemove())

# 5. Nationality
@dp.message(ObyektivkaStates.nationality)
async def process_nationality(message: types.Message, state: FSMContext):
    if not message.text:
        return
    data = await state.get_data()
    lang = data["lang"]
    await state.update_data(nationality=message.text.strip())
    
    await state.set_state(ObyektivkaStates.party)
    await message.answer(T[lang]["party"], reply_markup=get_skip_kb(lang))

# 6. Party
@dp.message(ObyektivkaStates.party)
async def process_party(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    val = "" if message.text == T[lang]["btn_skip"] else (message.text or "")
    await state.update_data(party=val.strip())
    
    await state.set_state(ObyektivkaStates.education)
    await message.answer(T[lang]["education"], reply_markup=get_skip_kb(lang, extra_buttons=EDU[lang]))

# 7. Education
@dp.message(ObyektivkaStates.education)
async def process_education(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    val = "" if message.text == T[lang]["btn_skip"] else (message.text or "")
    await state.update_data(education=val.strip())
    
    await state.set_state(ObyektivkaStates.graduated)
    await message.answer(T[lang]["graduated"], reply_markup=get_skip_kb(lang))

# 8. Graduated
@dp.message(ObyektivkaStates.graduated)
async def process_graduated(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    val = "" if message.text == T[lang]["btn_skip"] else (message.text or "")
    await state.update_data(graduated=val.strip())
    
    await state.set_state(ObyektivkaStates.specialty)
    await message.answer(T[lang]["specialty"], reply_markup=get_skip_kb(lang))

# 9. Specialty
@dp.message(ObyektivkaStates.specialty)
async def process_specialty(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    val = "" if message.text == T[lang]["btn_skip"] else (message.text or "")
    await state.update_data(specialty=val.strip())
    
    await state.set_state(ObyektivkaStates.degree)
    await message.answer(T[lang]["degree"], reply_markup=get_skip_kb(lang))

# 10. Degree
@dp.message(ObyektivkaStates.degree)
async def process_degree(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    val = "" if message.text == T[lang]["btn_skip"] else (message.text or "")
    await state.update_data(degree=val.strip())
    
    await state.set_state(ObyektivkaStates.title)
    await message.answer(T[lang]["title"], reply_markup=get_skip_kb(lang))

# 11. Title
@dp.message(ObyektivkaStates.title)
async def process_title(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    val = "" if message.text == T[lang]["btn_skip"] else (message.text or "")
    await state.update_data(title=val.strip())
    
    await state.set_state(ObyektivkaStates.languages)
    await message.answer(T[lang]["languages"], reply_markup=get_skip_kb(lang))

# 12. Languages
@dp.message(ObyektivkaStates.languages)
async def process_languages(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    val = "" if message.text == T[lang]["btn_skip"] else (message.text or "")
    await state.update_data(languages=val.strip())
    
    await state.set_state(ObyektivkaStates.military)
    await message.answer(T[lang]["military"], reply_markup=get_skip_kb(lang))

# 13. Military
@dp.message(ObyektivkaStates.military)
async def process_military(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    val = "" if message.text == T[lang]["btn_skip"] else (message.text or "")
    await state.update_data(military=val.strip())
    
    await state.set_state(ObyektivkaStates.awards)
    await message.answer(T[lang]["awards"], reply_markup=get_skip_kb(lang))

# 14. Awards
@dp.message(ObyektivkaStates.awards)
async def process_awards(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    val = "" if message.text == T[lang]["btn_skip"] else (message.text or "")
    await state.update_data(awards=val.strip())
    
    await state.set_state(ObyektivkaStates.deputy)
    await message.answer(T[lang]["deputy"], reply_markup=get_skip_kb(lang))

# 15. Deputy
@dp.message(ObyektivkaStates.deputy)
async def process_deputy(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    val = "" if message.text == T[lang]["btn_skip"] else (message.text or "")
    await state.update_data(deputy=val.strip())
    
    await state.set_state(ObyektivkaStates.photo)
    await message.answer(T[lang]["photo"], reply_markup=get_skip_kb(lang))

# 16. Photo
@dp.message(ObyektivkaStates.photo, F.photo)
async def process_photo(message: types.Message, state: FSMContext, bot: Bot):
    photo = message.photo[-1]
    photo_file = await bot.get_file(photo.file_id)
    save_path = DOWNLOADS_DIR / f"photo_{message.from_user.id}.jpg"
    await bot.download_file(photo_file.file_path, destination=save_path)
    
    await state.update_data(photo_path=str(save_path))
    data = await state.get_data()
    lang = data["lang"]
    
    await state.set_state(ObyektivkaStates.work)
    await message.answer(T[lang]["work"], reply_markup=get_skip_kb(lang))

@dp.message(ObyektivkaStates.photo)
async def process_photo_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if message.text == T[lang]["btn_skip"]:
        await state.update_data(photo_path=None)
        await state.set_state(ObyektivkaStates.work)
        await message.answer(T[lang]["work"], reply_markup=get_skip_kb(lang))
    else:
        await message.answer(T[lang]["photo_need"], reply_markup=get_skip_kb(lang))

# 17. Work
@dp.message(ObyektivkaStates.work)
async def process_work(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    val = "" if message.text == T[lang]["btn_skip"] else (message.text or "")
    await state.update_data(work=val.strip())
    
    await message.answer(T[lang]["rel_intro"])
    await state.set_state(ObyektivkaStates.rel_kind)
    await message.answer(T[lang]["rel_kind"], reply_markup=get_skip_kb(lang, extra_buttons=REL_KINDS[lang]))

# 18. Relatives
@dp.message(ObyektivkaStates.rel_kind)
async def process_rel_kind(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if message.text == T[lang]["btn_skip"]:
        return await show_finish_menu(message, state)
        
    await state.update_data(cur_rel={"kind": message.text.strip()})
    await state.set_state(ObyektivkaStates.rel_fio)
    await message.answer(T[lang]["rel_fio"], reply_markup=ReplyKeyboardRemove())

@dp.message(ObyektivkaStates.rel_fio)
async def process_rel_fio(message: types.Message, state: FSMContext):
    if not message.text:
        return
    data = await state.get_data()
    cur = data.get("cur_rel", {})
    cur["fio"] = message.text.strip()
    await state.update_data(cur_rel=cur)
    
    lang = data["lang"]
    await state.set_state(ObyektivkaStates.rel_birth)
    await message.answer(T[lang]["rel_birth"], reply_markup=ReplyKeyboardRemove())

@dp.message(ObyektivkaStates.rel_birth)
async def process_rel_birth(message: types.Message, state: FSMContext):
    if not message.text:
        return
    data = await state.get_data()
    cur = data.get("cur_rel", {})
    cur["birth"] = message.text.strip()
    await state.update_data(cur_rel=cur)
    
    lang = data["lang"]
    await state.set_state(ObyektivkaStates.rel_job)
    await message.answer(T[lang]["rel_job"], reply_markup=ReplyKeyboardRemove())

@dp.message(ObyektivkaStates.rel_job)
async def process_rel_job(message: types.Message, state: FSMContext):
    if not message.text:
        return
    data = await state.get_data()
    cur = data.get("cur_rel", {})
    cur["job"] = message.text.strip()
    await state.update_data(cur_rel=cur)
    
    lang = data["lang"]
    await state.set_state(ObyektivkaStates.rel_address)
    await message.answer(T[lang]["rel_address"], reply_markup=ReplyKeyboardRemove())

@dp.message(ObyektivkaStates.rel_address)
async def process_rel_address(message: types.Message, state: FSMContext):
    if not message.text:
        return
    data = await state.get_data()
    cur = data.get("cur_rel", {})
    cur["address"] = message.text.strip()
    
    relatives = data.get("relatives", [])
    relatives.append(cur)
    await state.update_data(relatives=relatives, cur_rel=None)
    
    lang = data["lang"]
    msg_added = T[lang]["rel_added"].format(kind=cur["kind"], fio=cur["fio"], n=len(relatives))
    await state.set_state(ObyektivkaStates.rel_ask_more)
    await message.answer(msg_added, reply_markup=get_rel_more_kb(lang))

@dp.message(ObyektivkaStates.rel_ask_more)
async def process_rel_ask_more(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    
    if message.text == T[lang]["btn_add_more"]:
        await state.set_state(ObyektivkaStates.rel_kind)
        await message.answer(T[lang]["rel_kind"], reply_markup=get_skip_kb(lang, extra_buttons=REL_KINDS[lang]))
    elif message.text == T[lang]["btn_done"]:
        await show_finish_menu(message, state)
    else:
        await message.answer(T[lang]["press_button"], reply_markup=get_rel_more_kb(lang))

async def show_finish_menu(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    await state.set_state(ObyektivkaStates.finished)
    
    has_photo = T[lang]["photo_yes"] if data.get("photo_path") else T[lang]["photo_no"]
    n_rel = len(data.get("relatives", []))
    
    summary = (
        f"{T[lang]['preview']}\n\n"
        f"👤 <b>{data.get('fio', '')}</b>\n"
        f"📅 {data.get('birth_date', '')}\n"
        f"📍 {data.get('birth_place', '')}\n"
        f"🎓 {data.get('education', '')}\n"
        f"{has_photo}\n"
        f"👨‍👩‍👧 Qarindoshlar soni: {n_rel}\n\n"
        f"{T[lang]['choose_format']}"
    )
    
    await message.answer(summary, reply_markup=ReplyKeyboardRemove())
    await message.answer("👇", reply_markup=get_format_kb(lang))

@dp.callback_query(F.data.in_(["get_pdf", "get_docx", "get_both", "restart"]))
async def cb_download(call: types.CallbackQuery, state: FSMContext):
    action = call.data
    data = await state.get_data()
    lang = data.get("lang", "lat")
    user_id = call.from_user.id
    
    if action == "restart":
        await state.clear()
        await state.set_state(ObyektivkaStates.lang)
        await call.message.answer(CHOOSE_LANG, reply_markup=get_lang_kb())
        await call.answer()
        return
        
    await call.answer(T[lang]["generating"])
    msg_wait = await call.message.answer(T[lang]["generating"])
    
    docx_file = DOWNLOADS_DIR / f"obyektivka_{user_id}.docx"
    pdf_file = DOWNLOADS_DIR / f"obyektivka_{user_id}.pdf"
    
    try:
        if action in ["get_docx", "get_both"]:
            generate_docx(data, str(docx_file))
            await call.message.answer_document(
                FSInputFile(str(docx_file), filename=f"Obyektivka_{data.get('fio', 'doc')}.docx")
            )
            
        if action in ["get_pdf", "get_both"]:
            generate_pdf(data, str(pdf_file))
            await call.message.answer_document(
                FSInputFile(str(pdf_file), filename=f"Obyektivka_{data.get('fio', 'doc')}.pdf")
            )
            
        await msg_wait.delete()
        await call.message.answer(T[lang]["ready"], reply_markup=get_format_kb(lang))
    except Exception as e:
        logging.error(f"Generate error: {e}", exc_info=True)
        await msg_wait.edit_text(T[lang]["error"])

async def start_bot():
    if not BOT_TOKEN:
        print("XATOLIK: BOT_TOKEN topilmadi!")
        return
    bot = Bot(token=BOT_TOKEN)
    print("Telegram Bot polling boshlandi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())
