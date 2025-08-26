import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    JobQueue,
)

TOKEN = "8376047382:AAEGZxhQuSuqLWIIC240pWgpWOL_Vm0IINs"

# --- مثال دالة لتشغيل مهمة متكررة ---
async def send_auto_price(context: ContextTypes.DEFAULT_TYPE):
    chat_id = "-1002960432716"
    # مثال: إرسال رسالة ثابتة
    await context.bot.send_message(chat_id=chat_id, text="سعر الذهب الآن: 1000 USD") 

# --- مثال دالة أمر /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! البوت يعمل بنجاح ✅")

# --- Main function ---
async def main():
    # بناء التطبيق
    app = ApplicationBuilder().token(TOKEN).build()

    # إضافة Handlers
    app.add_handler(CommandHandler("start", start))

    # إعداد JobQueue لتشغيل مهمة كل 30 دقيقة
    job_queue: JobQueue = app.job_queue
    job_queue.run_repeating(send_auto_price, interval=1800, first=10)

    # تشغيل البوت
    await app.run_polling()

# --- تشغيل البرنامج ---
if __name__ == "__main__":
    asyncio.run(main())
