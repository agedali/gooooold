import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# بياناتك
TOKEN = "8376047382:AAEGZxhQuSuqLWIIC240pWgpWOL_Vm0IINs"
CHAT_ID = "@iq_gold_price"   # لازم تخلي @ قبل اسم القناة
GOLD_API_KEY = "goldapi-durssmemxt19z-io"

# دالة لجلب السعر من API
def get_gold_price():
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": GOLD_API_KEY, "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        price_usd = data.get("price", "N/A")
        return price_usd
    else:
        return None

# أمر /price
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price_usd = get_gold_price()
    if price_usd:
        msg = f"💰 سعر الذهب الآن: {price_usd} دولار للأونصة"
    else:
        msg = "❌ تعذر جلب السعر حالياً"
    await update.message.reply_text(msg)

# إرسال تلقائي للقناة
async def send_auto_price(context: ContextTypes.DEFAULT_TYPE):
    price_usd = get_gold_price()
    if price_usd:
        msg = f"🔔 تحديث تلقائي:\n💰 سعر الذهب الآن: {price_usd} دولار للأونصة"
    else:
        msg = "❌ تعذر جلب السعر التلقائي"
    await context.bot.send_message(chat_id=CHAT_ID, text=msg)

# تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # أمر يدوي
    app.add_handler(CommandHandler("price", price))

    # إرسال تلقائي كل 30 دقيقة
    app.job_queue.run_repeating(send_auto_price, interval=1800, first=10)

    print("✅ Bot started...")
    app.run_polling()

