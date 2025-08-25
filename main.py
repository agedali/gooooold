import requests
from telegram import Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from PIL import Image, ImageDraw, ImageFont
import os

TOKEN = os.getenv("BOT_TOKEN", "ضع_التوكن_هنا")
CHAT_ID = os.getenv("CHAT_ID", "ضع_الـchat_id_او_اسم_القناة")
GOLD_API_KEY = os.getenv("GOLD_API_KEY", "ضع_المفتاح_هنا")

bot = Bot(token=TOKEN)

def get_gold_price():
    url = "https://www.goldapi.io/api/XAU/IQD"
    headers = {"x-access-token": GOLD_API_KEY, "Content-Type": "application/json"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        price = data.get("price", "N/A")
        return f"💰 سعر الذهب الآن: {price} دينار عراقي للغرام"
    else:
        return "⚠️ فشل في جلب سعر الذهب"

async def send_price(update, context: ContextTypes.DEFAULT_TYPE):
    msg = get_gold_price()
    await update.message.reply_text(msg)

async def auto_send(context: ContextTypes.DEFAULT_TYPE):
    msg = get_gold_price()
    await bot.send_message(chat_id=CHAT_ID, text=msg)

def main():
    app = Application.builder().token(TOKEN).build()

    # أوامر يدوية
    app.add_handler(CommandHandler("gold", send_price))

    # إرسال تلقائي كل 30 دقيقة
    app.job_queue.run_repeating(auto_send, interval=1800, first=10)

    app.run_polling()

if __name__ == "__main__":
    main()
