# -*- coding: utf-8 -*-
# ============================================================
#  ساختِ فایل‌های صوتی برای اپِ یادگیری فرانسوی  (edge-tts، رایگان)
#  نسخهٔ سوئیسی + احساسات.  برای مادرِ سوئیسیِ کاربر.
# ------------------------------------------------------------
#   ۱) نصب (یک‌بار):   python -m pip install edge-tts
#   ۲) اجرا:           python generate_voices.py
#   ۳) خروجی در پوشه‌ی  audio/  (audio/fr و audio/fa).
#
#   توجه: صدای فرانسوی حالا سوئیسی است (fr-CH). اگر می‌خواهی کلِ
#   فرانسوی دوباره با لهجهٔ سوئیسی ساخته شود، اول فایل‌های قدیمی
#   را پاک کن:  Remove-Item audio\fr\*.mp3   سپس این اسکریپت را اجرا کن.
#   (فایل‌های فارسی audio/fa دست‌نخورده می‌مانند؛ فقط احساساتِ فارسی اضافه می‌شود.)
# ============================================================
import asyncio, sys
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print("اول این را اجرا کن:   python -m pip install edge-tts"); sys.exit(1)

# ---------- صداها ----------
FR_VOICE = "fr-CH-ArianeNeural"   # فرانسویِ سوئیسیِ زنانه. مردانه: fr-CH-FabriceNeural | فرانسهٔ فرانسه: fr-FR-DeniseNeural
FA_VOICE = "fa-IR-DilaraNeural"   # فارسیِ زنانه.          مردانه: fa-IR-FaridNeural
OUT      = Path("audio")

# عددِ ۸۰ در سوئیس بسته به کانتون فرق دارد — فردا بر اساس کانتونِ مادر نهایی شود:
#   "huitante"      → وو، والیس، فریبور (۸۱ = huitante et un)
#   "quatre-vingts" → ژنو، نوشاتل، ژورا (۸۱ = quatre-vingt-un)
EIGHTY = "huitante"
# ---------------------------

LETTERS = [
    ("A","a"),("B","bé"),("C","cé"),("D","dé"),("E","euh"),("F","èf"),
    ("G","jé"),("H","ache"),("I","i"),("J","ji"),("K","ka"),("L","èl"),
    ("M","èm"),("N","èn"),("O","o"),("P","pé"),("Q","ku"),("R","èr"),
    ("S","ès"),("T","té"),("U","u"),("V","vé"),("W","double vé"),
    ("X","iks"),("Y","i grec"),("Z","zèd"),
]
SPECIALS = [
    ("s01","é"),("s02","è"),("s03","ê"),("s04","ë"),("s05","à"),
    ("s06","â"),("s07","î"),("s08","ï"),("s09","ô"),("s10","ù"),
    ("s11","û"),("s12","ü"),("s13","ç"),("s14","œ"),("s15","æ"),
]
WORDS = [
    ("w01","Bonjour",         "بونژور یعنی سلام، روزِ خوش"),
    ("w02","Salut",           "سالو یعنی سلام، خودمانی"),
    ("w03","Bonsoir",         "بونسوار یعنی عصر بخیر"),
    ("w04","Bonne nuit",      "بون نویی یعنی شب بخیر، موقعِ خواب"),
    ("w05","Au revoir",       "اوروُوار یعنی خداحافظ"),
    ("w06","À bientôt",       "آ بیان‌تو یعنی به‌زودی می‌بینمت"),
    ("w07","Merci",           "مرسی یعنی تشکر"),
    ("w08","Merci beaucoup",  "مرسی بوکو یعنی خیلی ممنون"),
    ("w09","De rien",         "دو ریَن یعنی خواهش می‌کنم"),
    ("w10","S'il vous plaît", "سیل وو پله یعنی لطفاً، رسمی"),
    ("w11","Oui",             "وی یعنی بله"),
    ("w12","Non",             "نُن یعنی نه"),
    ("w13","Excusez-moi",     "اکسکوزه موا یعنی ببخشید"),
    ("w14","Pardon",          "پاردُن یعنی ببخشید، عذر می‌خواهم"),
    ("w15","Comment ça va",   "کومان سا وا یعنی حالت چطور است"),
    ("w16","Ça va bien",      "سا وا بیَن یعنی خوبم"),
    ("w17","Je m'appelle",    "ژو مَپل یعنی اسمِ من ... است"),
    ("w18","Enchanté",        "آنشانته یعنی از آشنایی خوشوقتم"),
    ("w19","S'il te plaît",   "سیل تو پله یعنی لطفاً، خودمانی"),
    ("w20","À demain",        "آ دومَن یعنی تا فردا"),
]

# احساسات — (شناسه، مذکر، مؤنث یا None اگر یکسان، معنی فارسی)
EMOTIONS = [
    ("e01","Je suis content","Je suis contente","یعنی خوشحالم"),
    ("e02","Je suis heureux","Je suis heureuse","یعنی خوشحال و خوشبختم"),
    ("e03","Je suis amoureux","Je suis amoureuse","یعنی عاشقم"),
    ("e04","Je suis malade",None,"یعنی مریضم و حالم خوب نیست"),
    ("e05","Je suis fatigué","Je suis fatiguée","یعنی خسته‌ام"),
    ("e06","Je suis rigolo","Je suis rigolote","یعنی بامزه و شوخم"),
    ("e07","Je suis triste",None,"یعنی ناراحت و غمگینم"),
    ("e08","Je suis inquiet","Je suis inquiète","یعنی نگرانم"),
    ("e09","Je suis fâché","Je suis fâchée","یعنی عصبانی‌ام"),
    ("e10","J'ai peur",None,"یعنی می‌ترسم"),
]

UNITS = {1:"un",2:"deux",3:"trois",4:"quatre",5:"cinq",6:"six",7:"sept",8:"huit",9:"neuf"}

def swiss_number(i):
    """متنِ عددِ سوئیسی برای خواندن. ۱ تا ۶۹ و ۱۰۰ را عدد خام می‌دهیم (یکسان است)."""
    if i <= 69 or i == 100:
        return str(i)
    if 70 <= i <= 79:
        rem = i - 70
        return "septante" if rem == 0 else ("septante et un" if rem == 1 else f"septante-{UNITS[rem]}")
    if 90 <= i <= 99:
        rem = i - 90
        return "nonante" if rem == 0 else ("nonante et un" if rem == 1 else f"nonante-{UNITS[rem]}")
    # 80..89
    rem = i - 80
    if EIGHTY == "huitante":
        return "huitante" if rem == 0 else ("huitante et un" if rem == 1 else f"huitante-{UNITS[rem]}")
    else:  # quatre-vingts
        return "quatre-vingts" if rem == 0 else f"quatre-vingt-{UNITS[rem]}"

made = skipped = failed = 0

async def tts(text, voice, path):
    global made, skipped, failed
    path = Path(path)
    if path.exists() and path.stat().st_size > 0:
        skipped += 1; return
    path.parent.mkdir(parents=True, exist_ok=True)
    for attempt in (1, 2):
        try:
            await edge_tts.Communicate(text, voice).save(str(path))
            if path.exists() and path.stat().st_size > 0:
                made += 1; print("  OK", path); return
            raise RuntimeError("empty file")
        except Exception as e:
            if attempt == 1:
                print("  retry", path, e); await asyncio.sleep(2)
            else:
                failed += 1; print("  FAIL", path, e)

async def main():
    print("» الفبا (فرانسوی)…")
    for L, say in LETTERS: await tts(say, FR_VOICE, OUT/"fr"/f"{L}.mp3")
    print("» حروف ویژه (فرانسوی)…")
    for sid, w in SPECIALS: await tts(w, FR_VOICE, OUT/"fr"/f"{sid}.mp3")
    print("» کلمات (فرانسوی)…")
    for wid, fr, _ in WORDS: await tts(fr, FR_VOICE, OUT/"fr"/f"{wid}.mp3")
    print("» کلمات (فارسی — معنی)…")
    for wid, _, fa in WORDS: await tts(fa, FA_VOICE, OUT/"fa"/f"{wid}.mp3")
    print("» احساسات (فرانسوی مذکر/مؤنث + معنی فارسی)…")
    for eid, m, f, fa in EMOTIONS:
        if f is None:
            await tts(m, FR_VOICE, OUT/"fr"/f"{eid}.mp3")
        else:
            await tts(m, FR_VOICE, OUT/"fr"/f"{eid}m.mp3")
            await tts(f, FR_VOICE, OUT/"fr"/f"{eid}f.mp3")
        await tts(fa, FA_VOICE, OUT/"fa"/f"{eid}.mp3")
    print(f"» اعداد ۱ تا ۱۰۰ (سوئیسی، ۸۰ = {EIGHTY})…")
    for i in range(1, 101): await tts(swiss_number(i), FR_VOICE, OUT/"fr"/f"n{i:03d}.mp3")
    print(f"\nساخته: {made} | رد(قبلاً بود): {skipped} | ناموفق: {failed}")
    print(f"خروجی: {OUT.resolve()}")

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        try: asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except Exception: pass
    asyncio.run(main())
