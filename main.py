import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, JobQueue

# ضع التوكن هنا
TOKEN = "8376047382:AAEGZxhQuSuqLWIIC240pWgpWOL_Vm0IINs"

# اي دي القروب
CHAT_ID = -1002960432716

# دالة لإرسال الرسائل تلقائيًا
async def send_auto_price(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=CHAT_ID, text="تحديث تلقائي للأسعار!")

# دالة تستجيب لأوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! البوت يعمل الآن ✅")

async def main():
    # انشاء التطبيق
    app = ApplicationBuilder().token(TOKEN).build()

    # اضافة Handlers للأوامر
    app.add_handler(CommandHandler("start", start))

    # جدولة الرسائل كل 30 دقيقة
    app.job_queue.run_repeating(send_auto_price, interval=1800, first=10)

    # بدء البوت
    await app.run_polling()

# نقطة البداية
if __name__ == "__main__":
    asyncio.run(main())

