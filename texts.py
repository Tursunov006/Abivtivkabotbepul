"""Bot xabarlari va hujjat matnlari: lotin (lat), kirill (cyr), rus (ru)."""

LANGS = ("lat", "cyr", "ru")

# (maydon kaliti, majburiymi)
FIELDS = [
    ("fio", True),
    ("position", False),
    ("birth_date", True),
    ("birth_place", True),
    ("nationality", True),
    ("party", False),
    ("education", True),
    ("graduated", False),
    ("specialty", False),
    ("degree", False),
    ("title", False),
    ("languages", False),
    ("military", False),
    ("awards", False),
    ("deputy", False),
]

REL_KEYS = ["kind", "fio", "birth", "job", "address"]

EDU = {
    "lat": ["Oliy", "Tugallanmagan oliy", "O'rta maxsus", "O'rta"],
    "cyr": ["Олий", "Тугалланмаган олий", "Ўрта махсус", "Ўрта"],
    "ru": ["Высшее", "Неоконченное высшее", "Среднее специальное", "Среднее"],
}

REL_KINDS = {
    "lat": ["Otasi", "Onasi", "Akasi", "Ukasi", "Opasi", "Singlisi",
            "Turmush o'rtog'i", "O'g'li", "Qizi"],
    "cyr": ["Отаси", "Онаси", "Акаси", "Укаси", "Опаси", "Синглиси",
            "Турмуш ўртоғи", "Ўғли", "Қизи"],
    "ru": ["Отец", "Мать", "Брат", "Сестра", "Супруг(а)", "Сын", "Дочь"],
}

CHOOSE_LANG = "Tilni tanlang / Тилни танланг / Выберите язык:"
LANG_BUTTONS = [
    ("lat", "🇺🇿 O'zbekcha (lotin)"),
    ("cyr", "🇺🇿 Ўзбекча (кирилл)"),
    ("ru", "🇷🇺 Русский"),
]

T = {
    # ------------------------------------------------------------------ LOTIN
    "lat": {
        "welcome": (
            "Assalomu alaykum! 👋\n\n"
            "Bu bot sizga <b>bepul</b> obyektivka (ma'lumotnoma) tayyorlab beradi. "
            "Savollarga javob bering — oxirida tayyor <b>PDF</b> yoki <b>Word</b> faylni olasiz.\n\n"
            "/start — qaytadan boshlash\n/cancel — bekor qilish"
        ),
        "fio": "👤 <b>Familiya, ism va otangizning ismini</b> kiriting.\n\n<i>Masalan: Aliyev Vali Karimovich</i>",
        "position": "💼 <b>Hozirgi lavozimingiz va ish joyingiz</b>ni kiriting (qachondan ishlayotganingiz bilan).\n\n<i>Masalan: 2021-yil 1-sentabrdan: «Ipak Yo'li» banki Toshkent filiali bosh mutaxassisi</i>",
        "birth_date": "📅 <b>Tug'ilgan sanangiz</b>:\n\n<i>Masalan: 15.03.1995</i>",
        "birth_place": "📍 <b>Tug'ilgan joyingiz</b>:\n\n<i>Masalan: Toshkent viloyati, Chirchiq shahri</i>",
        "nationality": "🏳️ <b>Millatingiz</b>:\n\n<i>Masalan: o'zbek</i>",
        "party": "🏛 <b>Partiyaviyligingiz</b> (a'zo bo'lmasangiz o'tkazib yuboring):",
        "education": "🎓 <b>Ma'lumotingiz</b>ni tanlang yoki yozing:",
        "graduated": "🏫 <b>Qayerni, qachon tamomlagansiz?</b>\n\n<i>Masalan: 2017-yil, Toshkent davlat iqtisodiyot universiteti (kunduzgi)</i>",
        "specialty": "📘 <b>Ma'lumotingiz bo'yicha mutaxassisligingiz</b>:\n\n<i>Masalan: Buxgalteriya hisobi va audit</i>",
        "degree": "🔬 <b>Ilmiy darajangiz</b> (bo'lmasa o'tkazib yuboring):",
        "title": "🎖 <b>Ilmiy unvoningiz</b> (bo'lmasa o'tkazib yuboring):",
        "languages": "🌐 <b>Qaysi chet tillarini bilasiz?</b>\n\n<i>Masalan: rus, ingliz</i>",
        "military": "🪖 <b>Harbiy (maxsus) unvoningiz</b> (bo'lmasa o'tkazib yuboring):",
        "awards": "🏅 <b>Davlat mukofotlari</b> bilan taqdirlanganmisiz? Qanaqa? (bo'lmasa o'tkazib yuboring)",
        "deputy": "🗳 <b>Deputat yoki saylanadigan organ a'zosimisiz?</b> (bo'lmasa o'tkazib yuboring)",
        "photo": "📸 <b>3x4 rasmingizni</b> yuboring. Rasmsiz kerak bo'lsa — o'tkazib yuboring.",
        "photo_need": "Iltimos, rasm yuboring yoki «O'tkazib yuborish» tugmasini bosing.",
        "work": (
            "🧾 <b>Mehnat faoliyatingiz</b>ni yozing. Har bir ish joyini <b>yangi qatordan</b>, "
            "«yillar - joy va lavozim» ko'rinishida yozing:\n\n"
            "<i>2013-2017 yy. - Toshkent davlat iqtisodiyot universiteti talabasi\n"
            "2017-2021 yy. - «Asaka» banki iqtisodchisi\n"
            "2021 y. - h.v. - «Ipak Yo'li» banki bosh mutaxassisi</i>"
        ),
        "rel_intro": "👨‍👩‍👧 Endi <b>yaqin qarindoshlaringiz</b> haqida ma'lumot kiritamiz (ota-ona, aka-uka, opa-singil, turmush o'rtog'i, farzandlar).",
        "rel_kind": "Qarindoshligini tanlang yoki yozing (qarindosh kiritmaslik uchun — o'tkazib yuboring):",
        "rel_fio": "Uning <b>familiyasi, ismi va otasining ismi</b>:",
        "rel_birth": "<b>Tug'ilgan yili va joyi</b>:\n\n<i>Masalan: 1965-yil, Samarqand viloyati, Urgut tumani</i>",
        "rel_job": "<b>Ish joyi va lavozimi</b>:\n\n<i>Masalan: 45-maktab o'qituvchisi\nNafaqada bo'lsa: Nafaqada\nVafot etgan bo'lsa: Vafot etgan (2018-yil)</i>",
        "rel_address": "<b>Turar joyi</b>:\n\n<i>Masalan: Toshkent shahri, Chilonzor tumani</i>",
        "rel_added": "✅ Qo'shildi: <b>{kind}</b> — {fio}\nJami: {n} ta. Yana qarindosh qo'shasizmi?",
        "btn_add_more": "➕ Yana qo'shish",
        "btn_done": "✅ Tugatish",
        "press_button": "Iltimos, yuqoridagi tugmalardan birini bosing.",
        "btn_skip": "⏭ O'tkazib yuborish",
        "btn_back": "⬅️ Orqaga",
        "need_text": "Iltimos, matn ko'rinishida yozing.",
        "required": "Bu maydon majburiy, o'tkazib bo'lmaydi.",
        "preview": "📋 <b>Ma'lumotlaringizni tekshiring:</b>",
        "photo_yes": "📸 Rasm: bor",
        "photo_no": "📸 Rasm: yo'q",
        "choose_format": "Qaysi formatda yuklab olasiz?",
        "btn_pdf": "📄 PDF",
        "btn_docx": "📝 Word",
        "btn_both": "📦 Ikkalasi",
        "btn_restart": "🔄 Qaytadan to'ldirish",
        "generating": "⏳ Tayyorlanmoqda...",
        "ready": "✅ Obyektivkangiz tayyor! Boshqa formatda ham yuklab olishingiz mumkin. Yangi obyektivka uchun — /start",
        "error": "⚠️ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.",
        "cancelled": "❌ Bekor qilindi. Qaytadan boshlash uchun /start bosing.",
    },
    # ------------------------------------------------------------------ KIRILL
    "cyr": {
        "welcome": (
            "Ассалому алайкум! 👋\n\n"
            "Бу бот сизга <b>бепул</b> объективка (маълумотнома) тайёрлаб беради. "
            "Саволларга жавоб беринг — охирида тайёр <b>PDF</b> ёки <b>Word</b> файлни оласиз.\n\n"
            "/start — қайтадан бошлаш\n/cancel — бекор қилиш"
        ),
        "fio": "👤 <b>Фамилия, исм ва отангизнинг исмини</b> киритинг.\n\n<i>Масалан: Алиев Вали Каримович</i>",
        "position": "💼 <b>Ҳозирги лавозимингиз ва иш жойингиз</b>ни киритинг (қачондан ишлаётганингиз билан).\n\n<i>Масалан: 2021 йил 1 сентябрдан: «Ипак Йўли» банки Тошкент филиали бош мутахассиси</i>",
        "birth_date": "📅 <b>Туғилган санангиз</b>:\n\n<i>Масалан: 15.03.1995</i>",
        "birth_place": "📍 <b>Туғилган жойингиз</b>:\n\n<i>Масалан: Тошкент вилояти, Чирчиқ шаҳри</i>",
        "nationality": "🏳️ <b>Миллатингиз</b>:\n\n<i>Масалан: ўзбек</i>",
        "party": "🏛 <b>Партиявийлигингиз</b> (аъзо бўлмасангиз ўтказиб юборинг):",
        "education": "🎓 <b>Маълумотингиз</b>ни танланг ёки ёзинг:",
        "graduated": "🏫 <b>Қаерни, қачон тамомлагансиз?</b>\n\n<i>Масалан: 2017 йил, Тошкент давлат иқтисодиёт университети (кундузги)</i>",
        "specialty": "📘 <b>Маълумотингиз бўйича мутахассислигингиз</b>:\n\n<i>Масалан: Бухгалтерия ҳисоби ва аудит</i>",
        "degree": "🔬 <b>Илмий даражангиз</b> (бўлмаса ўтказиб юборинг):",
        "title": "🎖 <b>Илмий унвонингиз</b> (бўлмаса ўтказиб юборинг):",
        "languages": "🌐 <b>Қайси чет тилларини биласиз?</b>\n\n<i>Масалан: рус, инглиз</i>",
        "military": "🪖 <b>Ҳарбий (махсус) унвонингиз</b> (бўлмаса ўтказиб юборинг):",
        "awards": "🏅 <b>Давлат мукофотлари</b> билан тақдирланганмисиз? Қанақа? (бўлмаса ўтказиб юборинг)",
        "deputy": "🗳 <b>Депутат ёки сайланадиган орган аъзосимисиз?</b> (бўлмаса ўтказиб юборинг)",
        "photo": "📸 <b>3x4 расмингизни</b> юборинг. Расмсиз керак бўлса — ўтказиб юборинг.",
        "photo_need": "Илтимос, расм юборинг ёки «Ўтказиб юбориш» тугмасини босинг.",
        "work": (
            "🧾 <b>Меҳнат фаолиятингиз</b>ни ёзинг. Ҳар бир иш жойини <b>янги қатордан</b>, "
            "«йиллар - жой ва лавозим» кўринишида ёзинг:\n\n"
            "<i>2013-2017 йй. - Тошкент давлат иқтисодиёт университети талабаси\n"
            "2017-2021 йй. - «Асака» банки иқтисодчиси\n"
            "2021 й. - ҳ.в. - «Ипак Йўли» банки бош мутахассиси</i>"
        ),
        "rel_intro": "👨‍👩‍👧 Энди <b>яқин қариндошларингиз</b> ҳақида маълумот киритамиз (ота-она, ака-ука, опа-сингил, турмуш ўртоғи, фарзандлар).",
        "rel_kind": "Қариндошлигини танланг ёки ёзинг (қариндош киритмаслик учун — ўтказиб юборинг):",
        "rel_fio": "Унинг <b>фамилияси, исми ва отасининг исми</b>:",
        "rel_birth": "<b>Туғилган йили ва жойи</b>:\n\n<i>Масалан: 1965 йил, Самарқанд вилояти, Ургут тумани</i>",
        "rel_job": "<b>Иш жойи ва лавозими</b>:\n\n<i>Масалан: 45-мактаб ўқитувчиси\nНафақада бўлса: Нафақада\nВафот этган бўлса: Вафот этган (2018 йил)</i>",
        "rel_address": "<b>Турар жойи</b>:\n\n<i>Масалан: Тошкент шаҳри, Чилонзор тумани</i>",
        "rel_added": "✅ Қўшилди: <b>{kind}</b> — {fio}\nЖами: {n} та. Яна қариндош қўшасизми?",
        "btn_add_more": "➕ Яна қўшиш",
        "btn_done": "✅ Тугатиш",
        "press_button": "Илтимос, юқоридаги тугмалардан бирини босинг.",
        "btn_skip": "⏭ Ўтказиб юбориш",
        "btn_back": "⬅️ Орқага",
        "need_text": "Илтимос, матн кўринишида ёзинг.",
        "required": "Бу майдон мажбурий, ўтказиб бўлмайди.",
        "preview": "📋 <b>Маълумотларингизни текширинг:</b>",
        "photo_yes": "📸 Расм: бор",
        "photo_no": "📸 Расм: йўқ",
        "choose_format": "Қайси форматда юклаб оласиз?",
        "btn_pdf": "📄 PDF",
        "btn_docx": "📝 Word",
        "btn_both": "📦 Иккаласи",
        "btn_restart": "🔄 Қайтадан тўлдириш",
        "generating": "⏳ Тайёрланмоқда...",
        "ready": "✅ Объективкангиз тайёр! Бошқа форматда ҳам юклаб олишингиз мумкин. Янги объективка учун — /start",
        "error": "⚠️ Хатолик юз берди. Илтимос, қайтадан уриниб кўринг.",
        "cancelled": "❌ Бекор қилинди. Қайтадан бошлаш учун /start босинг.",
    },
    # ------------------------------------------------------------------ RUS
    "ru": {
        "welcome": (
            "Здравствуйте! 👋\n\n"
            "Этот бот <b>бесплатно</b> подготовит вам объективку (справку). "
            "Ответьте на вопросы — в конце получите готовый файл <b>PDF</b> или <b>Word</b>.\n\n"
            "/start — начать заново\n/cancel — отменить"
        ),
        "fio": "👤 Введите <b>фамилию, имя и отчество</b>.\n\n<i>Например: Алиев Вали Каримович</i>",
        "position": "💼 Введите <b>текущую должность и место работы</b> (с какого времени).\n\n<i>Например: С 1 сентября 2021 г.: главный специалист Ташкентского филиала банка «Ипак Йули»</i>",
        "birth_date": "📅 <b>Дата рождения</b>:\n\n<i>Например: 15.03.1995</i>",
        "birth_place": "📍 <b>Место рождения</b>:\n\n<i>Например: Ташкентская область, г. Чирчик</i>",
        "nationality": "🏳️ <b>Национальность</b>:\n\n<i>Например: узбек</i>",
        "party": "🏛 <b>Партийность</b> (если не состоите — пропустите):",
        "education": "🎓 Выберите или напишите <b>образование</b>:",
        "graduated": "🏫 <b>Что и когда окончили?</b>\n\n<i>Например: 2017 г., Ташкентский государственный экономический университет (дневное)</i>",
        "specialty": "📘 <b>Специальность по образованию</b>:\n\n<i>Например: Бухгалтерский учёт и аудит</i>",
        "degree": "🔬 <b>Учёная степень</b> (если нет — пропустите):",
        "title": "🎖 <b>Учёное звание</b> (если нет — пропустите):",
        "languages": "🌐 <b>Какими иностранными языками владеете?</b>\n\n<i>Например: русский, английский</i>",
        "military": "🪖 <b>Воинское (специальное) звание</b> (если нет — пропустите):",
        "awards": "🏅 Награждены ли <b>государственными наградами</b>? Какими? (если нет — пропустите)",
        "deputy": "🗳 <b>Являетесь ли депутатом или членом выборных органов?</b> (если нет — пропустите)",
        "photo": "📸 Отправьте <b>фото 3x4</b>. Если без фото — пропустите.",
        "photo_need": "Пожалуйста, отправьте фото или нажмите «Пропустить».",
        "work": (
            "🧾 Опишите <b>трудовую деятельность</b>. Каждое место работы — <b>с новой строки</b>, "
            "в виде «годы - место и должность»:\n\n"
            "<i>2013-2017 гг. - студент Ташкентского государственного экономического университета\n"
            "2017-2021 гг. - экономист банка «Асака»\n"
            "2021 г. - н.в. - главный специалист банка «Ипак Йули»</i>"
        ),
        "rel_intro": "👨‍👩‍👧 Теперь введём сведения о <b>близких родственниках</b> (родители, братья, сёстры, супруг(а), дети).",
        "rel_kind": "Выберите или напишите степень родства (чтобы не указывать родственников — пропустите):",
        "rel_fio": "Его/её <b>фамилия, имя и отчество</b>:",
        "rel_birth": "<b>Год и место рождения</b>:\n\n<i>Например: 1965 г., Самаркандская область, Ургутский район</i>",
        "rel_job": "<b>Место работы и должность</b>:\n\n<i>Например: учитель школы №45\nЕсли на пенсии: Пенсионер(ка)\nЕсли умер(ла): Умер(ла) в 2018 г.</i>",
        "rel_address": "<b>Место жительства</b>:\n\n<i>Например: г. Ташкент, Чиланзарский район</i>",
        "rel_added": "✅ Добавлено: <b>{kind}</b> — {fio}\nВсего: {n}. Добавить ещё родственника?",
        "btn_add_more": "➕ Добавить ещё",
        "btn_done": "✅ Завершить",
        "press_button": "Пожалуйста, нажмите одну из кнопок выше.",
        "btn_skip": "⏭ Пропустить",
        "btn_back": "⬅️ Назад",
        "need_text": "Пожалуйста, отправьте текст.",
        "required": "Это поле обязательное, его нельзя пропустить.",
        "preview": "📋 <b>Проверьте ваши данные:</b>",
        "photo_yes": "📸 Фото: есть",
        "photo_no": "📸 Фото: нет",
        "choose_format": "В каком формате скачать?",
        "btn_pdf": "📄 PDF",
        "btn_docx": "📝 Word",
        "btn_both": "📦 Оба",
        "btn_restart": "🔄 Заполнить заново",
        "generating": "⏳ Готовится...",
        "ready": "✅ Ваша объективка готова! Можно скачать и в другом формате. Для новой объективки — /start",
        "error": "⚠️ Произошла ошибка. Пожалуйста, попробуйте снова.",
        "cancelled": "❌ Отменено. Чтобы начать заново, нажмите /start.",
    },
}

# Hujjat ichidagi matnlar
DOC = {
    "lat": {
        "title": "MA'LUMOTNOMA",
        "none": "yo'q",
        "labels": {
            "fio": "F.I.Sh.:",
            "position": "Hozirgi lavozimi va ish joyi:",
            "birth_date": "Tug'ilgan yili:",
            "birth_place": "Tug'ilgan joyi:",
            "nationality": "Millati:",
            "party": "Partiyaviyligi:",
            "education": "Ma'lumoti:",
            "graduated": "Tamomlagan:",
            "specialty": "Ma'lumoti bo'yicha mutaxassisligi:",
            "degree": "Ilmiy darajasi:",
            "title": "Ilmiy unvoni:",
            "languages": "Qaysi chet tillarini biladi:",
            "military": "Harbiy (maxsus) unvoni:",
            "awards": "Davlat mukofotlari bilan taqdirlanganmi (qanaqa):",
            "deputy": "Xalq deputatlari, respublika, viloyat, shahar va tuman Kengashi deputatimi "
                      "yoki boshqa saylanadigan organlarning a'zosimi (to'liq ko'rsatilishi lozim):",
        },
        "work_title": "MEHNAT FAOLIYATI",
        "rel_title": "{fio}ning yaqin qarindoshlari haqida\nMA'LUMOT",
        "rel_headers": ["Qarindoshligi", "Familiyasi, ismi va otasining ismi",
                        "Tug'ilgan yili va joyi", "Ish joyi va lavozimi", "Turar joyi"],
    },
    "cyr": {
        "title": "МАЪЛУМОТНОМА",
        "none": "йўқ",
        "labels": {
            "fio": "Ф.И.Ш.:",
            "position": "Ҳозирги лавозими ва иш жойи:",
            "birth_date": "Туғилган йили:",
            "birth_place": "Туғилган жойи:",
            "nationality": "Миллати:",
            "party": "Партиявийлиги:",
            "education": "Маълумоти:",
            "graduated": "Тамомлаган:",
            "specialty": "Маълумоти бўйича мутахассислиги:",
            "degree": "Илмий даражаси:",
            "title": "Илмий унвони:",
            "languages": "Қайси чет тилларини билади:",
            "military": "Ҳарбий (махсус) унвони:",
            "awards": "Давлат мукофотлари билан тақдирланганми (қанақа):",
            "deputy": "Халқ депутатлари, республика, вилоят, шаҳар ва туман Кенгаши депутатими "
                      "ёки бошқа сайланадиган органларнинг аъзосими (тўлиқ кўрсатилиши лозим):",
        },
        "work_title": "МЕҲНАТ ФАОЛИЯТИ",
        "rel_title": "{fio}нинг яқин қариндошлари ҳақида\nМАЪЛУМОТ",
        "rel_headers": ["Қариндошлиги", "Фамилияси, исми ва отасининг исми",
                        "Туғилган йили ва жойи", "Иш жойи ва лавозими", "Турар жойи"],
    },
    "ru": {
        "title": "СПРАВКА",
        "none": "нет",
        "labels": {
            "fio": "Ф.И.О.:",
            "position": "Текущая должность и место работы:",
            "birth_date": "Год рождения:",
            "birth_place": "Место рождения:",
            "nationality": "Национальность:",
            "party": "Партийность:",
            "education": "Образование:",
            "graduated": "Окончил(а):",
            "specialty": "Специальность по образованию:",
            "degree": "Учёная степень:",
            "title": "Учёное звание:",
            "languages": "Какими иностранными языками владеет:",
            "military": "Воинское (специальное) звание:",
            "awards": "Награждён(а) ли государственными наградами (какими):",
            "deputy": "Является ли народным депутатом, депутатом республиканского, областного, "
                      "городского и районного Кенгаша или членом других выборных органов (указать полностью):",
        },
        "work_title": "ТРУДОВАЯ ДЕЯТЕЛЬНОСТЬ",
        "rel_title": "СВЕДЕНИЯ\nо близких родственниках: {fio}",
        "rel_headers": ["Степень родства", "Фамилия, имя, отчество",
                        "Год и место рождения", "Место работы и должность", "Место жительства"],
    },
}
