"""O'zbek lotin <-> kirill aqlli transliteratsiya moduli."""
import re

LAT_TO_CYR_MULTI = [
    ("O‘", "Ў"), ("o‘", "ў"), ("O'", "Ў"), ("o'", "ў"), ("O’", "Ў"), ("o’", "ў"), ("O`", "Ў"), ("o`", "ў"),
    ("G‘", "Ғ"), ("g‘", "ғ"), ("G'", "Ғ"), ("g'", "ғ"), ("G’", "Ғ"), ("g’", "ғ"), ("G`", "Ғ"), ("g`", "ғ"),
    ("SH", "Ш"), ("Sh", "Ш"), ("sh", "ш"),
    ("CH", "Ч"), ("Ch", "Ч"), ("ch", "ч"),
    ("YO", "Ё"), ("Yo", "Ё"), ("yo", "ё"),
    ("YU", "Ю"), ("Yu", "Ю"), ("yu", "ю"),
    ("YA", "Я"), ("Ya", "Я"), ("ya", "я"),
    ("YE", "Е"), ("Ye", "Е"), ("ye", "е"),
    ("TS", "Ц"), ("Ts", "Ц"), ("ts", "ц"),
    ("’", "ъ"), ("'", "ъ"), ("`", "ъ"), ("‘", "ъ"),
]

LAT_TO_CYR_SINGLE = {
    'A': 'А', 'a': 'а',
    'B': 'Б', 'b': 'б',
    'D': 'Д', 'd': 'д',
    'E': 'Э', 'e': 'е',
    'F': 'Ф', 'f': 'ф',
    'G': 'Г', 'g': 'г',
    'H': 'Ҳ', 'h': 'ҳ',
    'I': 'И', 'i': 'и',
    'J': 'Ж', 'j': 'ж',
    'K': 'К', 'k': 'к',
    'L': 'Л', 'l': 'л',
    'M': 'М', 'm': 'м',
    'N': 'Н', 'n': 'н',
    'O': 'О', 'o': 'о',
    'P': 'П', 'p': 'п',
    'Q': 'Қ', 'q': 'қ',
    'R': 'Р', 'r': 'р',
    'S': 'С', 's': 'с',
    'T': 'Т', 't': 'т',
    'U': 'У', 'u': 'у',
    'V': 'В', 'v': 'в',
    'X': 'Х', 'x': 'х',
    'Y': 'Й', 'y': 'й',
    'Z': 'З', 'z': 'з',
}

CYR_TO_LAT_MAP = {
    'А': 'A', 'а': 'a',
    'Б': 'B', 'б': 'b',
    'В': 'V', 'в': 'v',
    'Г': 'G', 'г': 'g',
    'Д': 'D', 'д': 'd',
    'Е': 'Ye', 'е': 'e',
    'Ё': 'Yo', 'ё': 'yo',
    'Ж': 'J', 'ж': 'j',
    'З': 'Z', 'з': 'z',
    'И': 'I', 'и': 'i',
    'Й': 'Y', 'й': 'y',
    'К': 'K', 'к': 'k',
    'Л': 'L', 'л': 'l',
    'М': 'M', 'м': 'm',
    'Н': 'N', 'н': 'n',
    'О': 'O', 'о': 'o',
    'П': 'P', 'п': 'p',
    'Р': 'R', 'р': 'r',
    'С': 'S', 'с': 's',
    'Т': 'T', 'т': 't',
    'У': 'U', 'у': 'u',
    'Ф': 'F', 'ф': 'f',
    'Х': 'X', 'х': 'x',
    'Ц': 'Ts', 'ц': 'ts',
    'Ч': 'Ch', 'ч': 'ch',
    'Ш': 'Sh', 'ш': 'sh',
    'Ъ': '’', 'ъ': '’',
    'Ь': '', 'ь': '',
    'Э': 'E', 'э': 'e',
    'Ю': 'Yu', 'ю': 'yu',
    'Я': 'Ya', 'я': 'ya',
    'Ў': 'O‘', 'ў': 'o‘',
    'Қ': 'Q', 'қ': 'q',
    'Ғ': 'G‘', 'ғ': 'g‘',
    'Ҳ': 'H', 'ҳ': 'h',
}


def to_cyrillic(text: str) -> str:
    if not text:
        return ""
    # So'z boshidagi E/e -> Э/э
    res = re.sub(r'(^|[\s(\["\'-])e', r'\1э', text)
    res = re.sub(r'(^|[\s(\["\'-])E', r'\1Э', res)
    for k, v in LAT_TO_CYR_MULTI:
        res = res.replace(k, v)
    out = []
    for ch in res:
        out.append(LAT_TO_CYR_SINGLE.get(ch, ch))
    return "".join(out)


def to_latin(text: str) -> str:
    if not text:
        return ""
    out = []
    for i, ch in enumerate(text):
        if ch in ('Е', 'е'):
            prev = text[i - 1] if i > 0 else ' '
            if i == 0 or prev in ' \n\t(["\'-аоуэияёюеўАОУЭИЯЁЮЕЎ':
                out.append('Ye' if ch == 'Е' else 'ye')
            else:
                out.append('E' if ch == 'Е' else 'e')
        else:
            out.append(CYR_TO_LAT_MAP.get(ch, ch))
    return "".join(out)


def normalize_data_script(data: dict) -> dict:
    """Agar tanlangan til 'cyr' bo'lsa lotin matnlarni kirillga, 'lat' bo'lsa kirillni lotinga o'giradi."""
    lang = data.get("lang", "lat")
    if lang not in ("lat", "cyr"):
        return data

    conv = to_cyrillic if lang == "cyr" else to_latin
    str_keys = [
        "fio", "position", "birth_date", "birth_place", "nationality",
        "party", "education", "graduated", "specialty", "degree",
        "title", "languages", "military", "awards", "deputy",
        "marital_status", "contact", "address", "work", "achievements"
    ]
    out = dict(data)
    for k in str_keys:
        if out.get(k) and isinstance(out[k], str):
            out[k] = conv(out[k])

    if "relatives" in out and isinstance(out["relatives"], list):
        new_rels = []
        for r in out["relatives"]:
            nr = dict(r)
            for rk in ("kind", "fio", "birth", "job", "address"):
                if nr.get(rk) and isinstance(nr[rk], str):
                    nr[rk] = conv(nr[rk])
            new_rels.append(nr)
        out["relatives"] = new_rels

    return out
