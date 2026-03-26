import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    BotCommand,
    WebAppInfo
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("TOKEN") or "8037476033:AAFWi8Kbv7x0nHLhufLRwNRyYicrOm9DsN8"

if not TOKEN:
    raise ValueError("❌ TOKEN belgilanmagan. Iltimos, TOKEN ni kiriting.")

# ================= BUTTONS DATA =================
BUTTONS = {
    "🎓 Maktabimiz qulayliklari": """
🟢 1-sinfdan 11-sinfgacha rus va uzbek ta'lim tillarida qabul qilamiz
🟢 Har bir o'quvchi bilan individual shug'illanamiz
🟢 Darslar 3xil tilda olib boriladi: Ingliz, Rus, Uzbek tillarida
🟢 Sinflarda o'quvchi soni 15tadan
🟢 4 mahal issiq ovqat
🟢 Yotoqxona (uzoqdan keluvchilarga)
🟢 Transport shahar buylab uydan uyga
🟢 Bepul repititorlar (Ingliz tili, Rus tili, Matematika, IT)
🟢 10ga yaqin sport turlarini taklif qilamiz
🟢 Dushanbadan Jumagacha
🟢 Maktab vaqti 08:00dan 17:00gacha
""",
    "🏨 Maktabimiz bir oylik ta'lim xizmati narxi": """
1 975 000 so’m

Bu to'lov uchun Farzandingiz
Dushanbadan-Jumagacha soat 8:00dan 18:00gacha maktabda bo’lish imkoniyatini, sifatli ta’lim tarbiya, Ingliz va Rus tillaridagi muhitni, 3 mahal issiq ovqat, 10 ga yaqin sport to'garaklari va Bepul repititorlar (Ingliz tili,Rus tili, Matematika, IT) ni oladi!!!

Doimiy doktor va psixolog ko'rigi o'tkaziladi.

Boshlang'ich sinf rahbari Matematika, o'qish, ona tili, tabiiy fanlardan ta'lim bersa, tarbiyachi o'qituvchi uyga vazifalarini tayyorlatadi.

5-sinfdan 11-sinfgacha maktabda o'qitilishi kerak bo'lgan barcha fanlar tajribaga ega uztozlar tomonida o'tiladi!

📢 Chegirmalar:

Bir oiladan 2ta farzand kelsa 2-farzand uchun har oylik 30%lik chegirma, 3 nafar kelsa 3-farzandga 40%, 4- farzandga 50% chegirma qilib beriladi 

Oylik toʻlovni har oyning 10-sanasigacha qilsangiz yana 100 000ming soʻm chegirma boʻladi 

Yarim yillik toʻlov bir martada toʻlov qilinsa 10% 

Yillik toʻlov bir martada qilinsa 20% chegirma
""",
    "🎓 Maktabga tayyorlov narxi": """
1 880 000 so'm

✅ Har bir o‘quvchi bilan individual shug‘ullanish
✅ Sinflarda 10–15 nafar o‘quvchi
✅ 3 mahal issiq ovqat
✅ Transport xizmati
✅ Shifokor ko‘rigi
✅ Logoped xizmati
✅ Psixolog xizmati

📚 Fan mashg‘ulotlari:

📖 Nutq va o‘qishni rivojlantirish
🔢 Matematika
✍️ Husnixat (yozuv)
🌍 Ingliz tili (o‘yinlar orqali, QR-kod)
🧠 Diqqat, xotira va ijodkorlikni rivojlantirish
🔬 Atrofimizdagi olam va rasm chizish
🧩 Mantiqiy fikrlash
🥗 Ovqatlanish madaniyati va gigiyena
⚽️ Sport mashg‘ulotlari
""",
    "🛏 Yotoqxona xizmati bir oylik narxi": """
600 000 so’m

Bu xizmatimiz uzoq masofadan maktabimizga kelib ta'lim oluvchilar uchun.
Xizmatdan foydalanuvchi o'quvchilarimiz yotoq joy, 4 mahal issiq ovqat bilan ta'minlanadi,
24/7 kamera kuzatuvi va tarbiyachi-nazoratchilar nazoratida bo'lishadi.
""",
    "🧳 Yozgi lager dasturi narxi": """
1 650 000 so'm

Dastur davomiyligi:
Haftasiga 6 kun | Soat 09:00 — 18:00

Dasturga kiritilganlar:
📘 Ingliz tili
📕 Rus tili
🧮 Matematika
💻 IT
⚽️ Suzish | Futbol | Taekwondo
‍♀️ Qizlar uchun: Xoreografiya | Gimnastika
♟ Shaxmat

🍽 Kuniga 4 mahal issiq ovqat
🚌 Shahar bo‘ylab transport xizmati
🛏 Yotoqxona
✈️ Sayohatlar
""",
    "🚗 Transport xizmati bir oylik narxi": """
300 000 so'm

Maktabimiz transporti shahar bo'ylab farzandingizni uydan dars mashg'ulotlariga olib ketadi va dars mashg'ulotlari tugaganidan keyin uygacha yetkazib qo'yadi.

🚌 Bir oiladan 2 ta o‘quvchi transportdan foydalansa, 2-o‘quvchi uchun transport BEPUL
""",
}

# ================= HANDLERS =================

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.set_my_commands([
        BotCommand("menu", "📋 Xizmatlar menyusi")
    ])
    await update.message.reply_text("Assalomu alaykum! Pastdagi menyudan foydalaning.")

# /menu komandasi
async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("phone_number"):
        contact_button = KeyboardButton("📱 Raqam yuborish", request_contact=True)
        contact_keyboard = ReplyKeyboardMarkup(
            [[contact_button]], resize_keyboard=True, one_time_keyboard=True
        )
        await update.message.reply_text("Iltimos, telefon raqamingizni yuboring:", reply_markup=contact_keyboard)
        return

    await send_main_menu(update, context)

# Asosiy menyuni yuborish
async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(k, callback_data=k)] for k in BUTTONS]

    # Qo‘shimcha tugmalar
    keyboard.append([
        InlineKeyboardButton("📄 Maktab shartnomasini yuklab olish", callback_data="download_contract")
    ])
    keyboard.append([
        InlineKeyboardButton(
            "🌐 Maktab saytiga o'tish",
            web_app=WebAppInfo(url="https://kelajakschoolqarshi.uz/")
        )
    ])

    # InlineKeyboardButton ro'yxatini to'g'ri shakllantirish
    reply_markup = InlineKeyboardMarkup(keyboard)

    # `update` turi Message yoki CallbackQuery ekanligini tekshiramiz
    if update.message:
        await update.message.reply_text("📋 Xizmatlar menyusi:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text("📋 Xizmatlar menyusi:", reply_markup=reply_markup)

# Tugma bosilganda
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "back_to_menu":
        await send_main_menu(update, context)
        return

    if query.data == "download_contract":
        file_path = "SHARTNOMA1.docx"
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                await context.bot.send_document(
                    chat_id=query.message.chat.id,
                    document=file,
                    filename="SHARTNOMA1.docx",
                    caption="📄 Maktab shartnomasi yuklab olish uchun:"
                )
        else:
            await context.bot.send_message(chat_id=query.message.chat.id,
                                           text="❌ Fayl topilmadi. Administrator bilan bog'laning.")
        return

    text = BUTTONS.get(query.data, "❌ Ma’lumot topilmadi.")
    back_button = InlineKeyboardButton("◀️ Orqaga", callback_data="back_to_menu")
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup([[back_button]]))

# Kontakt yuborilganda
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if contact:
        context.user_data["phone_number"] = contact.phone_number

        phone_number = contact.phone_number
        chat_id = -1002150211504  # Admin chat ID

        message = (
            "📥 Telegram botdan kelgan yangi ariza:\n\n"
            f"📞 Telefon raqami: {phone_number}"
        )
        await context.bot.send_message(chat_id=chat_id, text=message)

        await update.message.reply_text(
            "✅ Raqamingiz qabul qilindi. Endi menyudan foydalanishingiz mumkin.",
            reply_markup=ReplyKeyboardRemove()
        )

        await send_main_menu(update, context)

# ================= MAIN =================
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

    print("🤖 Bot ishga tushmoqda...")
    app.run_polling(drop_pending_updates=True)