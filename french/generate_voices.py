# -*- coding: utf-8 -*-
# ============================================================
#  ساختِ فایل‌های صوتی برای اپِ یادگیری فرانسوی  (OpenAI TTS)
#  این را روی ویندوزِ خودتان اجرا کنید (فقط آن‌جا به OpenAI دسترسی هست).
# ------------------------------------------------------------
#   ۱) نصب (یک‌بار):      python -m pip install openai
#   ۲) کلید را بگذارید:   یا در API_KEY پایین، یا به‌صورت متغیر محیطی OPENAI_API_KEY
#   ۳) اجرا:              python generate_voices.py
#   ۴) خروجی در پوشه‌ی  audio/  ساخته می‌شود (audio/fr و audio/fa).
#
#   نکته: اسکریپت هوشمند است؛ فایلی که قبلاً ساخته شده را دوباره نمی‌سازد.
#   این فایل را هرگز با کلیدِ داخلش روی گیت‌هاب پوش نکنید.
# ============================================================
import os, sys, time
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("اول:  python -m pip install openai"); sys.exit(1)

# ---------- تنظیمات ----------
API_KEY = ""                 # کلید OpenAI (یا خالی بگذارید تا از OPENAI_API_KEY خوانده شود)
MODEL   = "gpt-4o-mini-tts"  # اگر نبود: "tts-1"
VOICE   = "alloy"            # گزینه‌ها: nova, shimmer, fable, onyx, echo ...
OUT     = Path("audio")
# -----------------------------

client = OpenAI(api_key=(API_KEY or os.environ.get("OPENAI_API_KEY", "")))

FR_INSTR = ("Speak clear, natural, calm French like a patient teacher for an "
            "absolute beginner. Pronounce each sound precisely.")
FA_INSTR = ("به فارسیِ روان، واضح و آرام صحبت کن، مثل یک معلمِ مهربان برای یک "
            "فرد مسن که تازه شروع کرده. شمرده و دوستانه.")

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
def tts(text, instr, path):
    global made, skipped, failed
    path = Path(path)
    if path.exists() and path.stat().st_size > 0:
        skipped += 1; return
    path.parent.mkdir(parents=True, exist_ok=True)
    for attempt in (1, 2):
        try:
            with client.audio.speech.with_streaming_response.create(
                model=MODEL, voice=VOICE, input=text,
                instructions=instr, response_format="mp3") as r:
                r.stream_to_file(path)
            made += 1; print("  OK", path); time.sleep(0.2); return
        except Exception as e:
            if attempt == 1:
                print("  retry", path, e); time.sleep(1.5)
            else:
                failed += 1; print("  FAIL", path, e)

def main():
    if not (API_KEY or os.environ.get("OPENAI_API_KEY")):
        print("کلید OpenAI را در API_KEY یا در متغیر محیطی OPENAI_API_KEY بگذارید."); sys.exit(1)
    print("» الفبا (فرانسوی)…")
    for L, say in LETTERS: tts(say, FR_INSTR, OUT/"fr"/f"{L}.mp3")
    print("» حروف ویژه (فرانسوی)…")
    for sid, w in SPECIALS: tts(w, FR_INSTR, OUT/"fr"/f"{sid}.mp3")
    print("» کلمات (فرانسوی)…")
    for wid, fr, _ in WORDS: tts(fr, FR_INSTR, OUT/"fr"/f"{wid}.mp3")
    print("» کلمات (فارسی — معنی)…")
    for wid, _, fa in WORDS: tts(fa, FA_INSTR, OUT/"fa"/f"{wid}.mp3")
    print(f"\nساخته: {made} | رد(قبلاً بود): {skipped} | ناموفق: {failed}")
    print(f"خروجی: {OUT.resolve()}")

if __name__ == "__main__":
    main()
