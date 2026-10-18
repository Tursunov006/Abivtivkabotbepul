"""Talabalar uchun maxsus Obyektivka (Ma'lumotnoma) matnlari: lotin (lat), kirill (cyr), rus (ru)."""

LANGS = ("lat", "cyr", "ru")

REL_KINDS = {
    "lat": ["OTASI", "ONASI", "AKASI", "UKASI", "OPASI", "SINGLISI", "TURMUSH O‘RTOG‘I"],
    "cyr": ["ОТАСИ", "ОНАСИ", "АКАСИ", "УКАСИ", "ОПАСИ", "СИНГЛИСИ", "ТУРМУШ ЎРТОҒИ"],
    "ru": ["ОТЕЦ", "МАТЬ", "БРАТ", "СЕСТРА", "СУПРУГ(А)"],
}

CHOOSE_LANG = "Tilni tanlang / Тилни танланг / Выберите язык:"
LANG_BUTTONS = [
    ("lat", "🇺🇿 O'zbekcha (lotin)"),
    ("cyr", "🇺🇿 Ўзбекча (кирилл)"),
    ("ru", "🇷🇺 Русский"),
]

T = {
    "lat": {
        "welcome": (
            "Assalomu alaykum! 👋\n\n"
            "Bu bot talabalar uchun <b>bepul</b> rasmiy obyektivka (ma'lumotnoma) tayyorlab beradi. "
            "Savollarga javob bering — oxirida tayyor <b>PDF</b> yoki <b>Word</b> faylni olasiz.\n\n"
            "/start — qaytadan boshlash\n/cancel — bekor qilish"
        ),
        "fio": "👤 <b>Familiya, ism va otangizning ismini</b> kiriting:\n\n<i>Masalan: O‘rinov Rustamjon Akmaljon o‘g‘li</i>",
        "position": "🎓 <b>Universitet, fakultet, yo‘nalish, guruh va kursingizni</b> kiriting:\n\n<i>Masalan: Axborot texnologiyalari va menejment universiteti,\nIjtimoiy fanlar fakulteti Filologiya va tillarni o‘qitish (arab tili) ta’lim yo‘nalishi Ar-125-24-guruh, 1-kurs talabasi</i>",
        "birth_date": "📅 <b>Tug‘ilgan yili va sanangiz</b>:\n\n<i>Masalan: 14.07.2003 y</i>",
        "birth_place": "📍 <b>Tug‘ilgan joyingiz</b>:\n\n<i>Masalan: Farg‘ona viloyati Uchko‘prik tumani</i>",
        "nationality": "🏳️ <b>Millatingiz</b>:\n\n<i>Masalan: O‘zbek</i>",
        "specialty": "📘 <b>Ta’lim yo‘nalishingiz</b>:\n\n<i>Masalan: Filologiya va tillarni o‘qitish (arab tili)</i>",
        "graduated": "🏫 <b>Qachon va qaysi maktab/litseyni tamomlagansiz?</b>\n\n<i>Masalan: 2021-yil Uchko‘prik t. 5-umumiy o‘rta ta’lim maktabi</i>",
        "contact": "📞 <b>Telefon nomeringiz</b>:\n\n<i>Masalan: +998943987505</i>",
        "languages": "🌐 <b>Qaysi chet tillarini bilasiz (sertifikat bo'lsa yozing)?</b>\n\n<i>Masalan: Arab tili (sertifikat At Tanal B1)</i>",
        "awards": "🏅 <b>Davlat mukofotlari bilan taqdirlanganmisiz (qanaqa)?</b>\n(Bo'lmasa «O'tkazib yuborish» ni bosing — avtomatik «yo‘q» yoziladi)",
        "photo": "📸 <b>3x4 rasmingizni</b> yuboring (Rasmsiz bo'lsa — o'tkazib yuboring):",
        "photo_need": "Iltimos, rasm yuboring yoki «O'tkazib yuborish» tugmasini bosing.",
        "rel_intro": "👨‍👩‍👧 <b>SHAXSIY MA’LUMOTLARI (Oila a'zolari)</b>:\nOta-ona, aka-uka, opa-singillaringizni kiritamiz.",
        "rel_kind": "Qarindoshligini tanlang (tugatish uchun — «O'tkazib yuborish»):",
        "rel_fio": "<b>Familiyasi, ismi va otasining ismi</b>:\n\n<i>Masalan: Madatov Akmaljon O‘rinovich</i>",
        "rel_birth": "<b>Tug‘ilgan sanasi (yoki yili)</b>:\n\n<i>Masalan: 1969.05.14</i>",
        "rel_address": "<b>Yashash manzili</b>:\n\n<i>Masalan: Farg‘ona viloyati Uchko‘prik tumani Qummozor qishlog‘i 4-uy</i>",
        "rel_job": "<b>Kasbi yoki ish joyi va lavozimi</b>:\n\n<i>Masalan: Fermer / Uy bekasi / Tadbirkor / O‘qituvchi</i>",
        "rel_added": "✅ Qo‘shildi: <b>{kind}</b> — {fio}\nJami: {n} ta. Yana oila a'zosini qo‘shasizmi?",
        "achievements": (
            "🏆 <b>ERISHGAN YUTUQLARI</b>\n"
            "Har bir yutuqni (tashakkurnoma, sertifikat, olimpiada, tanlov) <b>yangi qatordan</b> yozing:\n\n"
            "<i>Masalan:\n"
            "25 noyabr 2024 yilda Universitetda bo‘lib o‘tgan “Ma’rifat Ulashib” loyihasi doirasida zakovat musobaqasida 2-o‘rinni qo‘lga kiritgani uchun Tashakkurnoma bilan taqdirlangan.\n"
            "10 fevral 2025 yilda Matematika fanidan onlayn olimpiadada sertifikat bilan taqdirlangan.</i>\n\n"
            "(Bo'lmasa «O'tkazib yuborish» tugmasini bosing)"
        ),
        "btn_add_more": "➕ Yana qo'shish",
        "btn_done": "✅ Keyingi qadam (Yutuqlar)",
        "press_button": "Iltimos, yuqoridagi tugmalardan birini bosing.",
        "btn_skip": "⏭ O'tkazib yuborish",
        "btn_back": "⬅️ Orqaga",
        "need_text": "Iltimos, matn ko'rinishida yozing.",
        "required": "Bu maydon majburiy, o'tkazib bo'lmaydi.",
        "preview": "📋 <b>Ma'lumotlaringiz tayyor! Tekshiring:</b>",
        "photo_yes": "📸 Rasm: bor",
        "photo_no": "📸 Rasm: yo'q",
        "choose_format": "Qaysi formatda yuklab olasiz?",
        "btn_pdf": "📄 PDF",
        "btn_docx": "📝 Word",
        "btn_both": "📦 Ikkalasi",
        "btn_restart": "🔄 Qaytadan to'ldirish",
        "generating": "⏳ Tayyorlanmoqda...",
        "ready": "✅ Obyektivkangiz tayyor! Yangi obyektivka uchun — /start",
        "error": "⚠️ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.",
        "cancelled": "❌ Bekor qilindi. Qaytadan boshlash uchun /start bosing.",
    },
    "cyr": {
        "welcome": (
            "Ассалому алайкум! 👋\n\n"
            "Бу бот талабалар учун <b>бепул</b> расмий объективка (маълумотнома) тайёрлаб беради. "
            "Саволларга жавоб беринг — охирида тайёр <b>PDF</b> ёки <b>Word</b> файлни оласиз.\n\n"
            "/start — қайтадан бошлаш\n/cancel — бекор қилиш"
        ),
        "fio": "👤 <b>Фамилия, исм ва отангизнинг исмини</b> киритинг:\n\n<i>Масалан: Ўринов Рустамжон Акмалжон ўғли</i>",
        "position": "🎓 <b>Университет, факультет, йўналиш, гуруҳ ва курсингизни</b> киритинг:\n\n<i>Масалан: Ахборот технологиялари ва менежмент университети,\nИжтимоий фанлар факультети Филология ва тилларни ўқитиш (араб тили) таълим йўналиши Ar-125-24-гуруҳ, 1-курс талабаси</i>",
        "birth_date": "📅 <b>Туғилган йили ва санангиз</b>:\n\n<i>Масалан: 14.07.2003 й</i>",
        "birth_place": "📍 <b>Туғилган жойингиз</b>:\n\n<i>Масалан: Фарғона вилояти Учкўприк тумани</i>",
        "nationality": "🏳️ <b>Миллатингиз</b>:\n\n<i>Масалан: Ўзбек</i>",
        "specialty": "📘 <b>Таълим йўналишингиз</b>:\n\n<i>Масалан: Филология ва тилларни ўқитиш (араб тили)</i>",
        "graduated": "🏫 <b>Қачон ва қайси мактаб/лицейни тамомлагансиз?</b>\n\n<i>Масалан: 2021-йил Учкўприк т. 5-умумий ўрта таълим мактаби</i>",
        "contact": "📞 <b>Телефон номерингиз</b>:\n\n<i>Масалан: +998943987505</i>",
        "languages": "🌐 <b>Қайси чет тилларини биласиз (сертификат бўлса ёзинг)?</b>\n\n<i>Масалан: Араб тили (сертификат At Tanal B1)</i>",
        "awards": "🏅 <b>Давлат мукофотлари билан тақдирланганмисиз (қанақа)?</b>",
        "photo": "📸 <b>3x4 расмингизни</b> юборинг:",
        "photo_need": "Илтимос, расм юборинг ёки «Ўтказиб юбориш» тугмасини босинг.",
        "rel_intro": "👨‍👩‍👧 <b>ШАХСИЙ МАЪЛУМОТЛАРИ (Оила аъзолари)</b>:",
        "rel_kind": "Қариндошлигини танланг:",
        "rel_fio": "<b>Фамилияси, исми ва отасининг исми</b>:",
        "rel_birth": "<b>Туғилган санаси (ёки йили)</b>:\n\n<i>Масалан: 1969.05.14</i>",
        "rel_address": "<b>Яшаш манзили</b>:\n\n<i>Масалан: Фарғона вилояти Учкўприк тумани Қуммозор қишлоғи 4-уй</i>",
        "rel_job": "<b>Касби ёки иш жойи ва лавозими</b>:\n\n<i>Масалан: Фермер / Уй бекаси / Тадбиркор</i>",
        "rel_added": "✅ Қўшилди: <b>{kind}</b> — {fio}\nЖами: {n} та. Яна қўшасизми?",
        "achievements": "🏆 <b>ЭРИШГАН ЮТУҚЛАРИ</b>\nҲар бир ютуқни янги қатордан ёзинг:",
        "btn_add_more": "➕ Яна қўшиш",
        "btn_done": "✅ Кейинги қадам (Ютуқлар)",
        "press_button": "Илтимос, тугмалардан бирини босинг.",
        "btn_skip": "⏭ Ўтказиб юбориш",
        "btn_back": "⬅️ Орқага",
        "need_text": "Илтимос, матн кўринишида ёзинг.",
        "required": "Бу майдон мажбурий.",
        "preview": "📋 <b>Маълумотларингиз тайёр! Текширинг:</b>",
        "photo_yes": "📸 Расм: бор",
        "photo_no": "📸 Расм: йўқ",
        "choose_format": "Қайси форматда юклаб оласиз?",
        "btn_pdf": "📄 PDF",
        "btn_docx": "📝 Word",
        "btn_both": "📦 Иккаласи",
        "btn_restart": "🔄 Қайтадан тўлдириш",
        "generating": "⏳ Тайёрланмоқда...",
        "ready": "✅ Объективкангиз тайёр! Янги объективка учун — /start",
        "error": "⚠️ Хатолик юз берди.",
        "cancelled": "❌ Бекор қилинди. /start босинг.",
    },
    "ru": {
        "welcome": (
            "Здравствуйте! 👋\n\n"
            "Этот бот <b>бесплатно</b> подготовит официальную студенческую объективку (справку).\n\n"
            "/start — начать заново\n/cancel — отменить"
        ),
        "fio": "👤 Введите <b>Фамилию, имя и отчество</b>:\n\n<i>Например: Уринов Рустамжон Акмалжон угли</i>",
        "position": "🎓 <b>Университет, факультет, направление, группа и курс</b>:",
        "birth_date": "📅 <b>Дата рождения</b>:\n\n<i>Например: 14.07.2003 г.</i>",
        "birth_place": "📍 <b>Место рождения</b>:\n\n<i>Например: Ферганская область, Учкуприкский район</i>",
        "nationality": "🏳️ <b>Национальность</b>:\n\n<i>Например: Узбек</i>",
        "specialty": "📘 <b>Направление обучения</b>:",
        "graduated": "🏫 <b>Когда и какую школу/лицей окончили?</b>",
        "contact": "📞 <b>Номер телефона</b>:\n\n<i>Например: +998943987505</i>",
        "languages": "🌐 <b>Какими иностранными языками владеете?</b>",
        "awards": "🏅 <b>Награждены ли государственными наградами (какими)?</b>",
        "photo": "📸 Отправьте <b>фото 3x4</b>:",
        "photo_need": "Отправьте фото или нажмите «Пропустить».",
        "rel_intro": "👨‍👩‍👧 <b>ЛИЧНЫЕ СВЕДЕНИЯ (Члены семьи)</b>:",
        "rel_kind": "Выберите степень родства:",
        "rel_fio": "<b>Фамилия, имя, отчество</b>:",
        "rel_birth": "<b>Дата рождения</b>:\n\n<i>Например: 1969.05.14</i>",
        "rel_address": "<b>Адрес проживания</b>:",
        "rel_job": "<b>Род занятий или место работы и должность</b>:",
        "rel_added": "✅ Добавлено: <b>{kind}</b> — {fio}\nВсего: {n}. Добавить ещё?",
        "achievements": "🏆 <b>ДОСТИЖЕНИЯ</b>\nКаждое достижение укажите с новой строки:",
        "btn_add_more": "➕ Добавить ещё",
        "btn_done": "✅ Далее (Достижения)",
        "press_button": "Пожалуйста, выберите кнопку.",
        "btn_skip": "⏭ Пропустить",
        "btn_back": "⬅️ Назад",
        "need_text": "Отправьте текст.",
        "required": "Обязательное поле.",
        "preview": "📋 <b>Проверьте ваши данные:</b>",
        "photo_yes": "📸 Фото: есть",
        "photo_no": "📸 Фото: нет",
        "choose_format": "В каком формате скачать?",
        "btn_pdf": "📄 PDF",
        "btn_docx": "📝 Word",
        "btn_both": "📦 Оба",
        "btn_restart": "🔄 Заполнить заново",
        "generating": "⏳ Готовится...",
        "ready": "✅ Ваша объективка готова! Для новой — /start",
        "error": "⚠️ Ошибка.",
        "cancelled": "❌ Отменено. Нажмите /start.",
    },
}

# Hujjat ichidagi matnlar (Ham Talaba namunasi, ham Barcha uchun Klassik 3.5-shakl)
DOC = {
    "lat": {
        "title": "MA’LUMOTNOMA",
        "none": "yo‘q",
        "labels": {
            "birth_date": "Tug‘ilgan yili:",
            "birth_place": "Tug‘ilgan joyi:",
            "nationality": "Millati:",
            "party": "Partiyaviyligi:",
            "education": "Ma’lumoti:",
            "specialty": "Ta’lim yo‘nalishi",
            "classic_specialty": "Ma’lumoti bo‘yicha mutaxassisligi:",
            "graduated": "Tamomlagan:",
            "degree": "Ilmiy darajasi:",
            "title": "Ilmiy unvoni:",
            "contact": "Telefon nomeri",
            "languages": "Qaysi chet tillarini biladi:",
            "military": "Harbiy (maxsus) unvoni:",
            "awards": "Davlat mukofotlari bilan taqdirlanganmi (qanaqa):",
            "deputy": "Xalq deputatlari respublika, viloyat, shahar va tuman Kengashi deputatimi yoki boshqa saylanadigan organlarning a’zosimi (to‘liq ko‘rsatilishi lozim):",
        },
        "rel_title": "SHAXSIY MA’LUMOTLARI",
        "ach_title": "ERISHGAN YUTUQLARI",
        "work_title": "MEHNAT FAOLIYATI",
        "classic_rel_title": "{fio}ning yaqin qarindoshlari haqida\nMA’LUMOT",
        "classic_rel_headers": [
            "Qarindoshligi",
            "Familiyasi, ismi va otasining ismi",
            "Tug‘ilgan yili va joyi",
            "Ish joyi va lavozimi",
            "Turar joyi"
        ],
    },
    "cyr": {
        "title": "МАЪЛУМОТНОМА",
        "none": "йўқ",
        "labels": {
            "birth_date": "Туғилган йили:",
            "birth_place": "Туғилган жойи:",
            "nationality": "Миллати:",
            "party": "Партиявийлиги:",
            "education": "Маълумоти:",
            "specialty": "Таълим йўналиши",
            "classic_specialty": "Маълумоти бўйича мутахассислиги:",
            "graduated": "Тамомлаган:",
            "degree": "Илмий даражаси:",
            "title": "Илмий унвони:",
            "contact": "Телефон номери",
            "languages": "Қайси чет тилларини билади:",
            "military": "Ҳарбий (махсус) унвони:",
            "awards": "Давлат мукофотлари билан тақдирланганми (қанақа):",
            "deputy": "Халқ депутатлари республика, вилоят, шаҳар ва туман Кенгаши депутатими ёки бошқа сайланадиган органларнинг аъзосими (тўлиқ кўрсатилиши лозим):",
        },
        "rel_title": "ШАХСИЙ МАЪЛУМОТЛАРИ",
        "ach_title": "ЭРИШГАН ЮТУҚЛАРИ",
        "work_title": "МЕҲНАТ ФАОЛИЯТИ",
        "classic_rel_title": "{fio}нинг яқин қариндошлари ҳақида\nМАЪЛУМОТ",
        "classic_rel_headers": [
            "Қариндошлиги",
            "Фамилияси, исми ва отасининг исми",
            "Туғилган йили ва жойи",
            "Иш жойи ва лавозими",
            "Турар жойи"
        ],
    },
    "ru": {
        "title": "СПРАВКА-ОБЪЕКТИВКА",
        "none": "нет",
        "labels": {
            "birth_date": "Дата рождения:",
            "birth_place": "Место рождения:",
            "nationality": "Национальность:",
            "party": "Партийность:",
            "education": "Образование:",
            "specialty": "Направление обучения",
            "classic_specialty": "Специальность по образованию:",
            "graduated": "Окончил(а):",
            "degree": "Учёная степень:",
            "title": "Учёное звание:",
            "contact": "Номер телефона",
            "languages": "Какими иностранными языками владеет:",
            "military": "Воинское (специальное) звание:",
            "awards": "Награждён(а) ли государственными наградами (какими):",
            "deputy": "Является ли депутатом республиканского, областного, городского и районного Кенгаша народных депутатов или членом других выборных органов (указать полностью):",
        },
        "rel_title": "ЛИЧНЫЕ СВЕДЕНИЯ",
        "ach_title": "ДОСТИЖЕНИЯ",
        "work_title": "ТРУДОВАЯ ДЕЯТЕЛЬНОСТЬ",
        "classic_rel_title": "СВЕДЕНИЯ\nо близких родственниках ({fio})",
        "classic_rel_headers": [
            "Степень родства",
            "Фамилия, имя и отчество",
            "Год и место рождения",
            "Место работы и должность",
            "Место жительства"
        ],
    },
}
