import re
import json
import random
import string
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# BOT_TOKEN = "YOUR_BOT_TOKEN"

# حفظ الأكواد المستخدمة حتى لا تتكرر
used_codes = set()


def generate_unique_code():
    while True:
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        numbers = ''.join(random.choices(string.digits, k=7))
        code = letters + numbers

        if code not in used_codes:
            used_codes.add(code)
            return code


def generate_second_code():
    first = random.choice("456789")
    last = ''.join(random.choices(string.digits, k=7))
    return f"{first}-{last}"


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    # استخراج JSON
    match = re.search(r'\{.*?\}', text, re.DOTALL)

    if not match:
        await update.message.reply_text("لم يتم العثور على البيانات.")
        return

    json_text = match.group(0).replace("”", '"').replace("“", '"')

    try:
        data = json.loads(json_text)
    except:
        await update.message.reply_text("صيغة JSON غير صحيحة.")
        return

    # حذف JSON من الرسالة
    remaining = text.replace(match.group(0), "").strip()

    lines = [x.strip() for x in remaining.splitlines() if x.strip()]

    if len(lines) < 3:
        await update.message.reply_text("البيانات ناقصة.")
        return

    name = lines[0]
    nationality = lines[1]
    company = lines[2]

    nationality_map = {
        "مصر": "مصري",
        "الهند": "هندي",
        "اليمن": "يمني",
        "سوريا": "سوري",
        "باكستان": "باكستان",
        "بنجلاديش": "بنجلاديش",
        "السودان": "سوداني",
        "الاردن": "اردني",
    }

    nationality = nationality_map.get(nationality, nationality)

    result = f"""{generate_unique_code()}

{name}

{data['occupation']}

{data['id_number']}
{nationality}


{company}

{generate_second_code()}"""

    await update.message.reply_text(result)


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()