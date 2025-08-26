import requests
import asyncio
from telegram import Bot
from telegram.ext import ApplicationBuilder, JobQueue

TOKEN = "8376047382:AAEGZxhQuSuqLWIIC240pWgpWOL_Vm0IINs"
CHAT_ID = -1002960432716  # ضع هنا أي دي القناة أو الشخص

bot = Bot(TOKEN)

# جلب سعر الدولار بالدينار العراقي
def get_usd_price():
    url = "https://api.exchangerate.host/convert?from=USD&to=IQD"
    response = requests.get(url).json()
    return round(response["result"], 2)

# جلب سعر الذهب بالدولار وتحويله إلى الدينار العراقي
def get_gold_price():
    gold_usd_per_gram = 65  # يمكنك تحديث السعر حسب السوق
    usd_iqd = get_usd_price()
    return round(gold_usd_per_gram * usd_iqd, 0)

# دالة الإرسال
async def send_prices(context):
    usd = get_usd_price()
    gold = get_gold_price()
    text = f"سعر الدولار: {usd} د.ع\nسعر الذهب (غرام واحد): {gold} د.ع"
    await bot.send_message(chat_id=CHAT_ID, text=text)

# تشغيل البوت
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    job_queue = app.job_queue
    # إرسال كل ساعة
    job_queue.run_repeating(send_prices, interval=3600, first=10)
    await app.start()
    await app.updater.start_polling()
    await app.wait_until_closed()

if __name__ == "__main__":
    asyncio.run(main())



