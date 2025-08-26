import asyncio
import requests
from telegram import Bot
from telegram.ext import ApplicationBuilder, ContextTypes, JobQueue

# إعدادات البوت
TOKEN = "8376047382:AAEGZxhQuSuqLWIIC240pWgpWOL_Vm0IINs"
CHAT_ID = -1002960432716  # أي دي القناة أو الشخص

bot = Bot(TOKEN)

# دالة لجلب سعر الدولار بالدينار العراقي من مصدر مجاني
def get_usd_price():
    url = "https://api.exchangerate.host/latest?base=USD&symbols=IQD"
    response = requests.get(url).json()
    return round(response["rates"]["IQD"], 2)

# دالة لجلب سعر الذهب بالغرام بالدينار العراقي من مصدر مجاني
def get_gold_price():
    # سعر الذهب بالدولار للغرام (مباشر من موقع مجاني)
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": "goldapi-demo", "Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers).json()
        gold_usd_per_gram = response["price"]  # السعر بالدولار للغرام
    except:
        gold_usd_per_gram = 65  # سعر تقديري إذا فشل المصدر
    usd_iqd = get_usd_price()
    return round(gold_usd_per_gram * usd_iqd, 0)

# دالة إرسال الأسعار
async def send_prices(context: ContextTypes.DEFAULT_TYPE):
    usd = get_usd_price()
    gold = get_gold_price()
    text = f"سعر الدولار: {usd} د.ع\nسعر الذهب (غرام واحد): {gold} د.ع"
    await bot.send_message(chat_id=CHAT_ID, text=text)

# دالة التشغيل
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    job_queue: JobQueue = app.job_queue
    job_queue.run_repeating(send_prices, interval=3600, first=10)  # كل ساعة
    await app.start()
    await app.updater.start_polling()
    await app.wait_until_closed()

if __name__ == "__main__":
    asyncio.run(main())


