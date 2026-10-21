import os
import sys
import time
import asyncio
import logging
import urllib.request
from pathlib import Path
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
    InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile,
    WebAppInfo, MenuButtonWebApp
)

from texts import T, LANGS, REL_KINDS, CHOOSE_LANG, LANG_BUTTONS
from generator_docx import generate_docx
from generator_pdf import generate_pdf
from ai_enhancer import enhance_text_with_ai

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://abivtivkabotbepul.onrender.com").strip()

BASE_DIR = Path(__file__).parent
DOWNLOADS_DIR = BASE_DIR / "temp_files"
DOWNLOADS_DIR.mkdir(exist_ok=True)


def cleanup_temp_files(max_age_seconds: int = 1800):
    """30 daqiqadan eski vaqtinchalik fayllarni tozalaydi (stats.json saqlanadi)."""
    try:
        now = time.time()
        for f in DOWNLOADS_DIR.glob("*"):
            if f.is_file() and f.name != "stats.json":
                if now - f.stat().st_mtime > max_age_seconds:
                    try:
                        f.unlink()
                    except Exception:
                        pass
    except Exception:
        pass

class ObyektivkaStates(StatesGroup):
    lang = State()
    fio = State()
    position = State()
    birth_date = State()
    birth_place = State()
    nationality = State()
    specialty = State()
    graduated = State()
    contact = State()
    languages = State()
    awards = State()
    photo = State()
    rel_kind = State()
    rel_fio = State()
    rel_birth = State()
    rel_address = State()
    rel_job = State()
    rel_ask_more = State()
    achievements = State()
    finished = State()

dp = Dispatcher(storage=MemoryStorage())

def get_main_menu_kb(lang: str = "lat"):
    buttons = []
    
    # 1. Mini Web App tugmasi (Asosiy tavsiya)
    if WEBAPP_URL:
        btn_webapp_text = {
            "lat": "🚀 Mini Ilovada 1 daqiqada tayyorlash",
            "cyr": "🚀 Мини Иловада 1 дақиқада тайёрлаш",
            "ru": "🚀 Создать за 1 минуту в Мини-Приложении"
        }.get(lang, "🚀 Mini Ilovada tayyorlash")
        buttons.append([InlineKeyboardButton(text=btn_webapp_text, web_app=WebAppInfo(url=WEBAPP_URL))])

    # 2. Bot ichida qadamma-qadam to'ldirish
    btn_chat_text = {
        "lat": "💬 Savol-javob orqali to'ldirish",
        "cyr": "💬 Савол-жавоб орқали тўлдириш",
        "ru": "💬 Заполнить пошагово в чате"
    }.get(lang, "💬 Savol-javob orqali to'ldirish")
    buttons.append([InlineKeyboardButton(text=btn_chat_text, callback_data="start_chat_flow")])

    # 3. Tilni o'zgartirish
    btn_lang_text = {
        "lat": "🌐 Tilni o'zgartirish",
        "cyr": "🌐 Тилни ўзгартириш",
        "ru": "🌐 Изменить язык"
    }.get(lang, "🌐 Tilni o'zgartirish")
    buttons.append([InlineKeyboardButton(text=btn_lang_text, callback_data="change_lang")])
    
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

def get_format_kb(lang: str, current_tpl: str = "student"):
    alt_script_text = "🔄 Kirillda olish (Авто-ўгириш)" if lang == "lat" else "🔄 Lotinda olish (Avto-o‘girish)"
    tpl_switch_text = (
        "🏛 Klassik shaklga o‘tish (Ish uchun)"
        if current_tpl == "student" else
        "🎓 Talaba shakliga o‘tish"
    )
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=T[lang]["btn_pdf"], callback_data="get_pdf"),
            InlineKeyboardButton(text=T[lang]["btn_docx"], callback_data="get_docx"),
        ],
        [
            InlineKeyboardButton(text=T[lang]["btn_both"], callback_data="get_both"),
        ],
        [
            InlineKeyboardButton(text=alt_script_text, callback_data="toggle_doc_script"),
        ],
        [
            InlineKeyboardButton(text=tpl_switch_text, callback_data="toggle_doc_tpl"),
        ],
        [
            InlineKeyboardButton(text=T[lang]["btn_restart"], callback_data="restart"),
        ]
    ])

def get_welcome_card(lang: str, first_name: str = ""):
    cards = {
        "lat": (
            f"📋 <b>Assalomu alaykum{', ' + first_name if first_name else ''}!</b>\n\n"
            "<b>Abivtivkabot</b> — barcha uchun (talabalar, o‘qituvchilar, shifokorlar va davlat xizmatchilari) "
            "rasmiy <b>Obyektivka (Ma’lumotnoma)</b> tayyorlab beruvchi universal platforma.\n\n"
            "✨ <b>Yangi imkoniyatlar:</b>\n"
            "• 🏛 <b>2 xil shablon</b> — Talaba namunasi hamda Klassik 3.5-shakl (Mehnat faoliyati bilan)\n"
            "• 🔄 <b>Lotin ↔ Kirill</b> — 1 marta yozib, xohlagan alifboda yuklab olish\n"
            "• 📸 <b>Aqlli 3x4 rasm</b> — istalgan rasmni avtomatik 3x4 formatga keltirish\n"
            "• 📄 <b>Word va PDF</b> — 100% bepul va tayyor formatlar\n\n"
            "👇 <i>Quyidagi o‘zingizga qulay usulni tanlang:</i>"
        ),
        "cyr": (
            f"📋 <b>Ассалому алайкум{', ' + first_name if first_name else ''}!</b>\n\n"
            "<b>Abivtivkabot</b> — барча учун (талабалар, ўқитувчилар, шифокорлар ва давлат хизматчилари) "
            "расмий <b>Объективка (Маълумотнома)</b> тайёрлаб берувчи универсал платформа.\n\n"
            "✨ <b>Янги имкониятлар:</b>\n"
            "• 🏛 <b>2 хил шаблон</b> — Талаба намунаси ҳамда Классик 3.5-шакл (Меҳнат фаолияти билан)\n"
            "• 🔄 <b>Лотин ↔ Кирилл</b> — 1 марта ёзиб, хоҳлаган алифбода юклаб олиш\n"
            "• 📸 <b>Ақлли 3x4 расм</b> — исталган расмни автоматик 3x4 форматга келтириш\n"
            "• 📄 <b>Word ва PDF</b> — 100% бепул ва тайёр форматлар\n\n"
            "👇 <i>Қуйидаги ўзингизга қулай усулни танланг:</i>"
        ),
        "ru": (
            f"📋 <b>Здравствуйте{', ' + first_name if first_name else ''}!</b>\n\n"
            "<b>Abivtivkabot</b> — универсальная платформа для бесплатного создания официальной "
            "<b>Объективки (Справки)</b> для студентов, учителей и госслужащих.\n\n"
            "✨ <b>Возможности:</b>\n"
            "• 🏛 <b>2 шаблона</b> — Студенческий и Классический (госслужба / работа)\n"
            "• 🔄 <b>Латиница ↔ Кириллица</b> — автоперевод в 1 клик\n"
            "• 📸 <b>Умное фото 3x4</b> — автообрезка из галереи\n"
            "• 📄 <b>Word и PDF</b> — 100% бесплатно\n\n"
            "👇 <i>Выберите удобный способ заполнения:</i>"
        )
    }
    return cards.get(lang, cards["lat"])

# ----------------- Buyruqlar -----------------
@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "lat")
    await state.clear()
    await state.update_data(lang=lang, template_type="student", relatives=[])
    
    first_name = message.from_user.first_name or ""
    await message.answer(
        get_welcome_card(lang, first_name),
        reply_markup=get_main_menu_kb(lang)
    )

@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    import json
    stats_file = DOWNLOADS_DIR / "stats.json"
    stats = {"total": 0, "pdf": 0, "docx": 0, "student": 0, "classic": 0}
    if stats_file.exists():
        try:
            stats.update(json.loads(stats_file.read_text(encoding="utf-8")))
        except Exception:
            pass
    await message.answer(
        f"📊 <b>Bot statistikasi (Abivtivkabot):</b>\n\n"
        f"📄 Jami tayyorlangan hujjatlar: <b>{stats.get('total', 0)}</b> ta\n"
        f"• PDF formatda: <b>{stats.get('pdf', 0)}</b> ta\n"
        f"• Word (.docx) formatda: <b>{stats.get('docx', 0)}</b> ta\n"
        f"• 🎓 Talaba namunasi: <b>{stats.get('student', 0)}</b> ta\n"
        f"• 🏛 Klassik (Ish/Xodim) namunasi: <b>{stats.get('classic', 0)}</b> ta"
    )

@dp.message(Command("lang"))
async def cmd_lang(message: types.Message, state: FSMContext):
    await message.answer(CHOOSE_LANG, reply_markup=get_lang_kb())

@dp.callback_query(F.data == "change_lang")
async def cb_change_lang(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(CHOOSE_LANG, reply_markup=get_lang_kb())
    await call.answer()

@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "lat")
    await state.clear()
    await message.answer(T[lang]["cancelled"], reply_markup=ReplyKeyboardRemove())
    await message.answer(get_welcome_card(lang), reply_markup=get_main_menu_kb(lang))

# Til tanlash
@dp.callback_query(F.data.startswith("setlang_"))
async def cb_set_lang(call: types.CallbackQuery, state: FSMContext):
    lang = call.data.split("_")[1]
    if lang not in LANGS:
        lang = "lat"
    await state.update_data(lang=lang, relatives=[])
    first_name = call.from_user.first_name or ""
    await call.message.edit_text(
        get_welcome_card(lang, first_name),
        reply_markup=get_main_menu_kb(lang)
    )
    await call.answer()

# Bot ichida savol-javob orqali davom etish — oldin shablon turini so'raymiz
@dp.callback_query(F.data == "start_chat_flow")
async def cb_start_chat(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "lat")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎓 Talabalar uchun (OTM / Yutuqlar)", callback_data="chat_tpl_student")],
        [InlineKeyboardButton(text="🏛 Barcha / Ish uchun (Klassik 3.5-shakl)", callback_data="chat_tpl_classic")],
    ])
    prompt_text = {
        "lat": "👇 <b>Qaysi shakl (shablon) bo‘yicha tayyorlaymiz?</b>",
        "cyr": "👇 <b>Қайси шакл (шаблон) бўйича тайёрлаймиз?</b>",
        "ru": "👇 <b>Выберите тип шаблона:</b>"
    }.get(lang, "👇 <b>Qaysi shakl bo‘yicha tayyorlaymiz?</b>")
    await call.message.edit_text(prompt_text, reply_markup=kb)
    await call.answer()

@dp.callback_query(F.data.in_(["chat_tpl_student", "chat_tpl_classic"]))
async def cb_choose_chat_tpl(call: types.CallbackQuery, state: FSMContext):
    tpl = "classic" if call.data == "chat_tpl_classic" else "student"
    await state.update_data(template_type=tpl)
    data = await state.get_data()
    lang = data.get("lang", "lat")
    await call.message.delete()
    await state.set_state(ObyektivkaStates.fio)
    await call.message.answer(T[lang]["fio"], reply_markup=ReplyKeyboardRemove())
    await call.answer()

import re

LETTER_RE = re.compile(r"[A-Za-zА-Яа-яЁёЎўҚқҒғҲҳ]")

def is_valid_fio(text: str) -> bool:
    t = text.strip()
    if any(ch.isdigit() for ch in t):
        return False
    if re.search(r"[@#$%^&*+=<>?/|~\\!;:\[\]{}]", t):
        return False
    words = [w for w in t.split() if len(LETTER_RE.findall(w)) >= 2]
    return len(words) >= 2 and len(LETTER_RE.findall(t)) >= 5

def is_valid_birth(text: str) -> bool:
    t = text.strip()
    years = re.findall(r"\b(19[2-9]\d|20[0-2]\d)\b", t)
    return len(years) >= 1

def is_valid_text_min(text: str, min_letters: int = 3) -> bool:
    return len(LETTER_RE.findall(text)) >= min_letters

def is_valid_nationality(text: str) -> bool:
    t = text.strip()
    if any(ch.isdigit() for ch in t):
        return False
    return 3 <= len(LETTER_RE.findall(t)) <= 25

def is_valid_phone(text: str) -> bool:
    digits = re.findall(r"\d", text)
    letters = LETTER_RE.findall(text)
    return 7 <= len(digits) <= 15 and len(letters) == 0

ERR_MSG = {
    "lat": {
        "fio": "⚠️ <b>Xato kiritildi!</b>\nIsm-sharifda raqamlar (masalan: <code>444</code>) bo‘lishi mumkin emas va kamida <b>Familiya hamda Ism</b> (2 ta so‘z) yozilishi shart.\n\n<i>Masalan: O‘rinov Rustamjon Akmaljon o‘g‘li</i>",
        "birth": "⚠️ <b>Sana yoki yil xato kiritildi!</b>\nIltimos, tug‘ilgan sanangizni to‘g‘ri yozing (1920–2022 oralig‘idagi yil bo‘lishi shart).\n\n<i>Masalan: 14.07.2003 y</i>",
        "place": "⚠️ <b>Manzil xato kiritildi!</b>\nFaqat raqam yozish mumkin emas. Viloyat va tuman/shaharni harflar bilan yozing.\n\n<i>Masalan: Farg‘ona viloyati Uchko‘prik tumani</i>",
        "nat": "⚠️ <b>Millat xato kiritildi!</b>\nRaqamlarsiz, harflar bilan yozing (masalan: <i>O‘zbek, Qoraqalpoq, Tojik, Rus</i>).",
        "phone": "⚠️ <b>Telefon raqami xato!</b>\nIltimos, haqiqiy telefon raqamingizni yozing yoki «O'tkazib yuborish» tugmasini bosing.\n\n<i>Masalan: +998943987505</i>",
        "text": "⚠️ <b>Ma’lumot noto‘g‘ri kiritildi!</b>\nFaqat raqamlar (masalan: <code>444</code>) yozish mumkin emas, so‘z bilan to‘liqroq yozing yoki «O'tkazib yuborish» ni bosing.",
    },
    "cyr": {
        "fio": "⚠️ <b>Хато киритилди!</b>\nИсм-шарифда рақамлар бўлиши мумкин эмас ва камида <b>Фамилия ҳамда Исм</b> (2 та сўз) ёзилиши шарт.\n\n<i>Масалан: Ўринов Рустамжон Акмалжон ўғли</i>",
        "birth": "⚠️ <b>Сана ёки йил хато киритилди!</b>\nТуғилган санани тўғри ёзинг.\n\n<i>Масалан: 14.07.2003 й</i>",
        "place": "⚠️ <b>Манзил хато киритилди!</b>\nВилоят ва туман/шаҳарни ҳарфлар билан ёзинг.",
        "nat": "⚠️ <b>Миллат хато киритилди!</b>\nРақамларсиз, ҳарфлар билан ёзинг (масалан: <i>Ўзбек</i>).",
        "phone": "⚠️ <b>Телефон рақами хато!</b>\nТўғри телефон рақам ёзинг (масалан: <i>+998943987505</i>).",
        "text": "⚠️ <b>Маълумот нотўғри киритилди!</b>\nФақат рақам ёзиш мумкин эмас, сўз билан ёзинг.",
    },
    "ru": {
        "fio": "⚠️ <b>Ошибка!</b>\nФ.И.О. не может содержать цифры и должно состоять минимум из 2 слов (Фамилия и Имя).\n\n<i>Например: Уринов Рустамжон Акмалжон угли</i>",
        "birth": "⚠️ <b>Неверная дата рождения!</b>\nУкажите реальный год рождения (например: <i>14.07.2003 г.</i>).",
        "place": "⚠️ <b>Неверный адрес!</b>\nВведите область и район буквами.",
        "nat": "⚠️ <b>Неверная национальность!</b>\nВведите буквами без цифр (например: <i>Узбек</i>).",
        "phone": "⚠️ <b>Неверный номер телефона!</b>\nВведите корректный номер (например: <i>+998943987505</i>).",
        "text": "⚠️ <b>Некорректный ввод!</b>\nНельзя вводить только цифры, напишите текстом.",
    }
}

# 1. FIO
@dp.message(ObyektivkaStates.fio)
async def process_fio(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "lat")
    if not message.text or not is_valid_fio(message.text):
        await message.answer(ERR_MSG[lang]["fio"])
        return
    await state.update_data(fio=message.text.strip())
    await state.set_state(ObyektivkaStates.position)
    await message.answer(T[lang]["position"], reply_markup=get_skip_kb(lang))

# 2. Position (OTM, fakultet, yo'nalish, guruh va kurs)
@dp.message(ObyektivkaStates.position)
async def process_position(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if not message.text:
        return
    if message.text != T[lang]["btn_skip"] and not is_valid_text_min(message.text, 4):
        await message.answer(ERR_MSG[lang]["text"], reply_markup=get_skip_kb(lang))
        return
    val = "" if message.text == T[lang]["btn_skip"] else message.text
    await state.update_data(position=val.strip())
    
    await state.set_state(ObyektivkaStates.birth_date)
    await message.answer(T[lang]["birth_date"], reply_markup=ReplyKeyboardRemove())

# 3. Birth date
@dp.message(ObyektivkaStates.birth_date)
async def process_birth_date(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if not message.text or not is_valid_birth(message.text):
        await message.answer(ERR_MSG[lang]["birth"])
        return
    await state.update_data(birth_date=message.text.strip())
    
    await state.set_state(ObyektivkaStates.birth_place)
    await message.answer(T[lang]["birth_place"], reply_markup=ReplyKeyboardRemove())

# 4. Birth place
@dp.message(ObyektivkaStates.birth_place)
async def process_birth_place(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if not message.text or not is_valid_text_min(message.text, 4):
        await message.answer(ERR_MSG[lang]["place"])
        return
    await state.update_data(birth_place=message.text.strip())
    
    await state.set_state(ObyektivkaStates.nationality)
    nat_Preset = {
        "lat": ["O‘zbek", "Qoraqalpoq", "Tojik", "Qozoq", "Rus"],
        "cyr": ["Ўзбек", "Қорақалпоқ", "Тожик", "Қозоқ", "Рус"],
        "ru": ["Узбек", "Каракалпак", "Таджик", "Казах", "Русский"]
    }.get(lang, ["O‘zbek"])
    kb = [[KeyboardButton(text=nat_Preset[0]), KeyboardButton(text=nat_Preset[1])],
          [KeyboardButton(text=nat_Preset[2]), KeyboardButton(text=nat_Preset[3]), KeyboardButton(text=nat_Preset[4])]]
    await message.answer(
        T[lang]["nationality"],
        reply_markup=ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    )

# 5. Nationality
@dp.message(ObyektivkaStates.nationality)
async def process_nationality(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if not message.text or not is_valid_nationality(message.text):
        await message.answer(ERR_MSG[lang]["nat"])
        return
    await state.update_data(nationality=message.text.strip())
    
    await state.set_state(ObyektivkaStates.specialty)
    await message.answer(T[lang]["specialty"], reply_markup=get_skip_kb(lang))

# 6. Specialty (Ta'lim yo'nalishi)
@dp.message(ObyektivkaStates.specialty)
async def process_specialty(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if not message.text:
        return
    if message.text != T[lang]["btn_skip"] and not is_valid_text_min(message.text, 3):
        await message.answer(ERR_MSG[lang]["text"], reply_markup=get_skip_kb(lang))
        return
    val = "" if message.text == T[lang]["btn_skip"] else message.text
    await state.update_data(specialty=val.strip())
    
    await state.set_state(ObyektivkaStates.graduated)
    await message.answer(T[lang]["graduated"], reply_markup=get_skip_kb(lang))

# 7. Graduated (Tamomlagan maktab/litseyi)
@dp.message(ObyektivkaStates.graduated)
async def process_graduated(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if not message.text:
        return
    if message.text != T[lang]["btn_skip"] and not is_valid_text_min(message.text, 3):
        await message.answer(ERR_MSG[lang]["text"], reply_markup=get_skip_kb(lang))
        return
    val = "" if message.text == T[lang]["btn_skip"] else message.text
    await state.update_data(graduated=val.strip())
    
    await state.set_state(ObyektivkaStates.contact)
    await message.answer(T[lang]["contact"], reply_markup=get_skip_kb(lang))

# 8. Contact (Telefon nomeri)
@dp.message(ObyektivkaStates.contact)
async def process_contact(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if not message.text:
        return
    if message.text != T[lang]["btn_skip"] and not is_valid_phone(message.text):
        await message.answer(ERR_MSG[lang]["phone"], reply_markup=get_skip_kb(lang))
        return
    val = "" if message.text == T[lang]["btn_skip"] else message.text
    await state.update_data(contact=val.strip())
    
    await state.set_state(ObyektivkaStates.languages)
    await message.answer(T[lang]["languages"], reply_markup=get_skip_kb(lang))

# 9. Languages (Chet tillari)
@dp.message(ObyektivkaStates.languages)
async def process_languages(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if not message.text:
        return
    if message.text != T[lang]["btn_skip"] and not is_valid_text_min(message.text, 3):
        await message.answer(ERR_MSG[lang]["text"], reply_markup=get_skip_kb(lang))
        return
    val = "" if message.text == T[lang]["btn_skip"] else message.text
    await state.update_data(languages=val.strip())
    
    await state.set_state(ObyektivkaStates.awards)
    await message.answer(T[lang]["awards"], reply_markup=get_skip_kb(lang))

# 10. Awards (Davlat mukofotlari)
@dp.message(ObyektivkaStates.awards)
async def process_awards(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if not message.text:
        return
    if message.text != T[lang]["btn_skip"] and not is_valid_text_min(message.text, 2):
        await message.answer(ERR_MSG[lang]["text"], reply_markup=get_skip_kb(lang))
        return
    val = "" if message.text == T[lang]["btn_skip"] else message.text
    await state.update_data(awards=val.strip())
    
    await state.set_state(ObyektivkaStates.photo)
    await message.answer(T[lang]["photo"], reply_markup=get_skip_kb(lang))

# 11. Photo
@dp.message(ObyektivkaStates.photo, F.photo)
async def process_photo(message: types.Message, state: FSMContext, bot: Bot):
    photo = message.photo[-1]
    photo_file = await bot.get_file(photo.file_id)
    save_path = DOWNLOADS_DIR / f"photo_{message.from_user.id}.jpg"
    await bot.download_file(photo_file.file_path, destination=save_path)
    
    await state.update_data(photo_path=str(save_path))
    data = await state.get_data()
    lang = data["lang"]
    
    await message.answer(T[lang]["rel_intro"])
    await state.set_state(ObyektivkaStates.rel_kind)
    await message.answer(T[lang]["rel_kind"], reply_markup=get_skip_kb(lang, extra_buttons=REL_KINDS[lang]))

@dp.message(ObyektivkaStates.photo)
async def process_photo_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if message.text == T[lang]["btn_skip"]:
        await state.update_data(photo_path=None)
        await message.answer(T[lang]["rel_intro"])
        await state.set_state(ObyektivkaStates.rel_kind)
        await message.answer(T[lang]["rel_kind"], reply_markup=get_skip_kb(lang, extra_buttons=REL_KINDS[lang]))
    else:
        await message.answer(T[lang]["photo_need"], reply_markup=get_skip_kb(lang))

# 12. Relatives (SHAXSIY MA'LUMOTLARI)
@dp.message(ObyektivkaStates.rel_kind)
async def process_rel_kind(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if not message.text:
        return
    if message.text == T[lang]["btn_skip"]:
        await state.set_state(ObyektivkaStates.achievements)
        return await message.answer(T[lang]["achievements"], reply_markup=get_skip_kb(lang))
    if not is_valid_text_min(message.text, 2) or any(ch.isdigit() for ch in message.text):
        await message.answer(ERR_MSG[lang]["text"], reply_markup=get_skip_kb(lang, extra_buttons=REL_KINDS[lang]))
        return
        
    await state.update_data(cur_rel={"kind": message.text.strip()})
    await state.set_state(ObyektivkaStates.rel_fio)
    await message.answer(T[lang]["rel_fio"], reply_markup=ReplyKeyboardRemove())

@dp.message(ObyektivkaStates.rel_fio)
async def process_rel_fio(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if not message.text or not is_valid_fio(message.text):
        await message.answer(ERR_MSG[lang]["fio"])
        return
    cur = data.get("cur_rel", {})
    cur["fio"] = message.text.strip()
    await state.update_data(cur_rel=cur)
    
    await state.set_state(ObyektivkaStates.rel_birth)
    await message.answer(T[lang]["rel_birth"], reply_markup=ReplyKeyboardRemove())

@dp.message(ObyektivkaStates.rel_birth)
async def process_rel_birth(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if not message.text or not is_valid_birth(message.text):
        await message.answer(ERR_MSG[lang]["birth"])
        return
    cur = data.get("cur_rel", {})
    cur["birth"] = message.text.strip()
    await state.update_data(cur_rel=cur)
    
    await state.set_state(ObyektivkaStates.rel_address)
    await message.answer(T[lang]["rel_address"], reply_markup=ReplyKeyboardRemove())

@dp.message(ObyektivkaStates.rel_address)
async def process_rel_address(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if not message.text or not is_valid_text_min(message.text, 4):
        await message.answer(ERR_MSG[lang]["place"])
        return
    cur = data.get("cur_rel", {})
    cur["address"] = message.text.strip()
    await state.update_data(cur_rel=cur)
    
    await state.set_state(ObyektivkaStates.rel_job)
    await message.answer(T[lang]["rel_job"], reply_markup=ReplyKeyboardRemove())

@dp.message(ObyektivkaStates.rel_job)
async def process_rel_job(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if not message.text or not is_valid_text_min(message.text, 3):
        await message.answer(ERR_MSG[lang]["text"])
        return
    cur = data.get("cur_rel", {})
    cur["job"] = message.text.strip()
    
    relatives = data.get("relatives", [])
    relatives.append(cur)
    await state.update_data(relatives=relatives, cur_rel=None)
    
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
        await state.set_state(ObyektivkaStates.achievements)
        await message.answer(T[lang]["achievements"], reply_markup=get_skip_kb(lang))
    else:
        await message.answer(T[lang]["press_button"], reply_markup=get_rel_more_kb(lang))

# 13. Achievements (ERISHGAN YUTUQLARI)
@dp.message(ObyektivkaStates.achievements)
async def process_achievements(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if not message.text:
        return
    if message.text != T[lang]["btn_skip"] and not is_valid_text_min(message.text, 4):
        await message.answer(ERR_MSG[lang]["text"], reply_markup=get_skip_kb(lang))
        return
    val = "" if message.text == T[lang]["btn_skip"] else message.text.strip()
    if val:
        # Sun'iy intellekt orqali rasmiy uslubda chiroyli tahrirlash (OmniRoute / AI)
        try:
            val = await asyncio.to_thread(enhance_text_with_ai, val, "achievements", lang)
        except Exception:
            pass
    await state.update_data(achievements=val)
    await show_finish_menu(message, state)

# Istalgan boshqa matn yozilganda asosiy menyuni chiqarish
@dp.message()
async def fallback_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "lat")
    first_name = message.from_user.first_name or ""
    await message.answer(
        get_welcome_card(lang, first_name),
        reply_markup=get_main_menu_kb(lang)
    )

async def show_finish_menu(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    tpl = data.get("template_type", "student")
    await state.set_state(ObyektivkaStates.finished)
    
    has_photo = T[lang]["photo_yes"] if data.get("photo_path") else T[lang]["photo_no"]
    n_rel = len(data.get("relatives", []))
    tpl_name = "🎓 Talaba namunasi" if tpl == "student" else "🏛 Klassik (Ish/Xodim) namunasi"
    
    summary = (
        f"{T[lang]['preview']}\n\n"
        f"📑 Shablon: <b>{tpl_name}</b>\n"
        f"👤 <b>{data.get('fio', '')}</b>\n"
        f"📅 {data.get('birth_date', '')}\n"
        f"📍 {data.get('birth_place', '')}\n"
        f"📘 {data.get('specialty', '')}\n"
        f"📞 {data.get('contact', '')}\n"
        f"{has_photo}\n"
        f"👨‍👩‍👧 Oila a'zolari: {n_rel} ta\n\n"
        f"{T[lang]['choose_format']}"
    )
    
    await message.answer(summary, reply_markup=ReplyKeyboardRemove())
    await message.answer("👇", reply_markup=get_format_kb(lang, tpl))

@dp.callback_query(F.data.in_(["get_pdf", "get_docx", "get_both", "toggle_doc_script", "toggle_doc_tpl", "restart"]))
async def cb_download(call: types.CallbackQuery, state: FSMContext):
    action = call.data
    data = await state.get_data()
    lang = data.get("lang", "lat")
    tpl = data.get("template_type", "student")
    user_id = call.from_user.id
    
    if action == "restart":
        await state.clear()
        await state.update_data(lang=lang, template_type="student", relatives=[])
        first_name = call.from_user.first_name or ""
        await call.message.answer(get_welcome_card(lang, first_name), reply_markup=get_main_menu_kb(lang))
        await call.answer()
        return

    if action == "toggle_doc_script":
        new_lang = "cyr" if lang == "lat" else "lat"
        await state.update_data(lang=new_lang)
        await call.message.edit_reply_markup(reply_markup=get_format_kb(new_lang, tpl))
        await call.answer("✅ Alifbo o‘zgartirildi! Endi PDF yoki Word tugmasini bosing.")
        return

    if action == "toggle_doc_tpl":
        new_tpl = "classic" if tpl == "student" else "student"
        await state.update_data(template_type=new_tpl)
        await call.message.edit_reply_markup(reply_markup=get_format_kb(lang, new_tpl))
        await call.answer("✅ Shablon turi o‘zgartirildi! Endi PDF yoki Word tugmasini bosing.")
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
        await call.message.answer(T[lang]["ready"], reply_markup=get_format_kb(lang, tpl))
    except Exception as e:
        logging.error(f"Generate error: {e}", exc_info=True)
        await msg_wait.edit_text(T[lang]["error"])

async def keep_alive_ping():
    """Render Free serveri uxlab qolmasligi uchun har 4 daqiqada o'zini uyg'otib turadi va eski fayllarni tozalaydi."""
    target_url = (os.getenv("RENDER_EXTERNAL_URL") or WEBAPP_URL or "https://abivtivkabotbepul.onrender.com").rstrip("/")
    while True:
        await asyncio.sleep(240)  # Har 4 daqiqada
        try:
            cleanup_temp_files(max_age_seconds=1800)  # 30 daqiqadan eski vaqtinchalik fayllarni tozalash
        except Exception:
            pass

        if target_url:
            for path in ("/health", "/"):
                try:
                    req = urllib.request.Request(
                        f"{target_url}{path}",
                        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) KeepAlive/1.0"}
                    )
                    await asyncio.to_thread(urllib.request.urlopen, req, None, 10)
                    break
                except Exception:
                    pass

async def start_bot():
    if not BOT_TOKEN:
        print("XATOLIK: BOT_TOKEN topilmadi!")
        return
        
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Webhook bo'lsa tozalab yuboramiz va Menu tugmasini o'rnatamiz
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        if WEBAPP_URL:
            await bot.set_chat_menu_button(
                menu_button=MenuButtonWebApp(text="📋 Obyektivka", web_app=WebAppInfo(url=WEBAPP_URL))
            )
    except Exception as e:
        print(f"Init setup warning: {e}")

    # Keep-alive vazifasini fonda ishga tushiramiz
    asyncio.create_task(keep_alive_ping())

    print("Telegram Bot polling boshlandi (24/7 rejim)...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())
