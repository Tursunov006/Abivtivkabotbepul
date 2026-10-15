# Obyektivka Yaratuvchi Telegram Bot (Bepul Xizmat)

O'zbekiston davlat va xususiy sektorlarida rasmiy qabul qilingan davlat standarti (namuna) bo'yicha obyektivka (ma'lumotnoma) yaratib beruvchi Telegram bot.

## Imkoniyatlari:
1. **3 ta tilda ishlaydi:**
   - 🇺🇿 O'zbekcha (lotin)
   - 🇺🇿 Ўзбекча (кирилл)
   - 🇷🇺 Русский
2. **Rasmiy standart format:**
   - Asosiy ma'lumotlar (F.I.Sh., tug'ilgan joyi, yili, millati, partiyaviyligi, ma'lumoti, mutaxassisligi, ilmiy daraja/unvonlar, chet tillari, harbiy unvon, davlat mukofotlari, deputatlik).
   - 3x4 rasm joylashuvi.
   - Mehnat faoliyati (xronologik tartibda).
   - 2-sahifada: Yaqin qarindoshlari haqida to'liq jadval (qarindoshligi, FIO, tug'ilgan yili/joyi, ish joyi/lavozimi, manzili).
3. **Formatlar:**
   - **PDF** (Times New Roman shriftida, kirill va o'zbek harflari buzilmaydi).
   - **Word (DOCX)** (foydalanuvchi xohlasa o'zi tahrirlashi mumkin).
   - Ikkalasini birdaniga olish imkoniyati.
4. **Qulay interfeys:**
   - Ixtiyoriy savollarni bitta tugma bilan o'tkazib yuborish (Skip).
   - Qarindoshlarni ketma-ket istagancha qo'shish.
   - 100% bepul.

---

## Ishga tushirish yo'riqnomasi:

### 1. Bot tokenini olish:
Telegramda [@BotFather](https://t.me/BotFather) ga kiring va `/newbot` buyrug'i orqali yangi bot yarating. U bergan tokenni oling.

### 2. .env fayliga tokenni yozing:
`obyektivka_bot/.env` faylini oching va tokenni qo'ying:
```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ
```

### 3. Botni ishga tushiring:
Terminalda ushbu jildga kiring va botni yurgizing:
```powershell
cd C:\Users\acer\.gemini\antigravity\scratch\obyektivka_bot
python bot.py
```
