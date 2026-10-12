# -*- coding: utf-8 -*-
# ============================================================
#  ساختِ فایل‌های صوتی برای اپِ یادگیری فرانسوی
#  با صدای نورالِ رایگانِ مایکروسافت (edge-tts) — بدون کلید، بدون هزینه.
# ------------------------------------------------------------
#   ۱) نصب (یک‌بار):   python -m pip install edge-tts
#   ۲) اجرا:           python generate_voices.py
#   ۳) خروجی در پوشه‌ی  audio/  ساخته می‌شود (audio/fr و audio/fa).
#
#   نیازی به اینترنتِ خاص یا کلید نیست — فقط اتصالِ معمولیِ اینترنت.
#   اسکریپت هوشمند است؛ فایلی که قبلاً ساخته شده را دوباره نمی‌سازد،
#   پس اگر وسطش قطع شد، دوباره اجرا کن تا بقیه را بسازد.
# ============================================================
import asyncio, sys
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print("اول این را اجرا کن:   python -m pip install edge-tts"); sys.exit(1)

# ---------- صداها (می‌توانی عوض کنی) ----------
FR_VOICE = "fr-FR-DeniseNeural"   # فرانسویِ زنانه و واضح. مردانه: fr-FR-HenriNeural
FA_VOICE = "fa-IR-DilaraNeural"   # فارسیِ زنانه و واضح.   مردانه: fa-IR-FaridNeural
OUT      = Path("audio")
# ---------------------------------------------

LETTERS = [
    ("A","a"),("B","bé"),("C","cé"),("D","dé"),("E","euh"),("F","èf"),
    ("G","jé"),("H","ache"),("I","i"),("J","ji"),("K","ka"),("L","èl"),
    ("M","èm"),("N","èn"),("O","o"),("P","pé"),("Q","ku"),("R","èr"),
    ("S","ès"),("T","té"),("U","u"),("V","vé"),("W","double vé"),
    ("X","iks"),("Y","i grec"),("Z","zèd"),
]
SPECIALS = [
    ("s01","été"),("s02","très"),("s03","être"),("s04","Noël"),("s05","voilà"),
    ("s06","âge"),("s07","île"),("s08","maïs"),("s09","hôtel"),("s10","où"),
    ("s11","sûr"),("s12","aigüe"),("s13","ça"),("s14","cœur"),("s15","et cætera"),
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
    print(f"\nساخته: {made} | رد(قبلاً بود): {skipped} | ناموفق: {failed}")
    print(f"خروجی: {OUT.resolve()}")

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        try: asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except Exception: pass
    asyncio.run(main())
