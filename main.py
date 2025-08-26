import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CallbackContext, Job

TOKEN = "8376047382:AAEGZxhQuSuqLWIIC240pWgpWOL_Vm0IINs"
CHAT_ID = -1002960432716  # أي دي القناة أو الشخص

# جلب سعر الدولار بالدينار العراقي
def get_usd_price():
    url = "https://api.exchangerate.host/latest?base=USD&symbols=IQD"
    response = requests.get(url).json()
    return round(response["rates"]["IQD"], 2)

# جلب سعر الذهب بالغرام بالدينار العراقي
def get_gold_price():
    gold_usd_per_gram = 65  # تقديري
    usd_iqd = get_usd_price()
    return round(gold_usd_per_gram * usd_iqd, 0)

# دالة إرسال الأسعار
async def send_prices(context: ContextTypes.DEFAULT_TYPE):
    usd = get_usd_price()
    gold = get_gold_price()
    text = f"سعر الدولار: {usd} د.ع\nسعر الذهب (غرام واحد): {gold} د.ع"
    await context.bot.send_message(chat_id=CHAT_ID, text=text)

# التشغيل
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    # جدولة المهمة كل ساعة
    app.job_queue.run_repeating(send_prices, interval=3600, first=10)
    
    # تشغيل البوت
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())



